#!/usr/bin/env python3
import rclpy
import numpy as np
import random
from rclpy.node import Node

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

from std_msgs.msg import Float64MultiArray
from my_robot_interfaces.msg import PathPlannerPoints

class RegulatorListener(Node):
    def __init__(self):
        super().__init__("compare_listener")
        self.viconSubscriber_ = self.create_subscription(Float64MultiArray, "/pid_regulator_vicon", self.onViconMsg, 10)
        self.pathPlannerSubscriber_ = self.create_subscription(PathPlannerPoints, "/pid_regulator_pathplanner", self.onPathPlannerMsg, 10)
        self.regulatorPublisher_ = self.create_publisher(Float64MultiArray, "/motioncontroller_regulator", 10)

        self.get_logger().info("Regulator node initialized.")

        self.viconPoint = []
        self.pathPlannerPoints = [] 
        self.velocityVector = []
        self.nextPoint = []
        self.error = 0
        self.start_time = self.get_clock().now().nanoseconds
        self.current_time = self.get_clock().now().nanoseconds

        self.create_timer(0.5, self.comparePoints)
    
    def onViconMsg(self, msg):
        self.viconPoint = msg.data
        self.get_logger().info("Received position from VICON: " + str(self.viconPoint))

        # only start sending velocity commands to the crazyflie once the pathplanner has sent points
        if self.pathPlannerPoints != []:
            # establishes the first point for the drone to fly to
            if self.nextPoint == []:
                self.start_time = self.get_clock().now().nanoseconds
                self.nextPoint = self.pathPlannerPoints[1]
                self.velocityVector = [abs(self.viconPoint[0] - self.nextPoint[0]) / self.nextPoint[3], abs(self.viconPoint[1] - self.nextPoint[1]) / self.nextPoint[3], abs(self.viconPoint[2] - self.nextPoint[2]) / self.nextPoint[3]]
            else:
                # change to read from where the pathplanner believes it should currently be
                # use polynomials for X, Y, and Z to to the current time to get the current position in the pathplanner
                # compare this to the vicon position to create an error and velocity vector
                self.error = [abs(self.viconPoint[0] - self.nextPoint[0]), abs(self.viconPoint[1] - self.nextPoint[1]), abs(self.viconPoint[2] - self.nextPoint[2])]
                self.velocityVector = [abs(self.viconPoint[0] - self.nextPoint[0]) / self.nextPoint[3], abs(self.viconPoint[1] - self.nextPoint[1]) / self.nextPoint[3], abs(self.viconPoint[2] - self.nextPoint[2]) / self.nextPoint[3]]
                # if error is below a certain threshold, start moving to the next point
                if self.error[0] < 1.5 and self.error[1] < 1.5 and self.error[2] < 1.5:
                    nextPointIndex = np.where(np.all(self.pathPlannerPoints == self.nextPoint, axis=1))[0][0]
                    self.nextPoint = self.pathPlannerPoints[nextPointIndex + 1]
                    self.velocityVector = [abs(self.viconPoint[0] - self.nextPoint[0]) / self.nextPoint[3], abs(self.viconPoint[1] - self.nextPoint[1]) / self.nextPoint[3], abs(self.viconPoint[2] - self.nextPoint[2]) / self.nextPoint[3]]
                    self.get_logger().info("Moving to next point: " + str(self.nextPoint))

            self.current_time = self.get_clock().now().nanoseconds - self.start_time
            self.get_logger().info("Current time: " + str(self.current_time / 1e+9))
            self.get_logger().info("Error: " + str(self.error))
            self.get_logger().info("Next point :" + str(self.nextPoint))
            self.get_logger().info("Velocity vector: " + str(self.velocityVector))
            # send velocity information to crazyflie motion controller

    def onPathPlannerMsg(self, msg):
        self.pathPlannerPoints = np.array(msg.data)
        self.pathPlannerPoints = self.pathPlannerPoints.reshape(msg.row, msg.col)
        self.get_logger().info("Received points from PathPlanner: " + str(self.pathPlannerPoints))      
    
    def comparePoints(self):
        msg = Float64MultiArray()
        msg.data = [random.uniform(0, 5.0), random.uniform(0, 5.0), 0.0]
        self.regulatorPublisher_.publish(msg)
        self.get_logger().info("Message sent to motion commander!")
#!/usr/bin/env python3
import rclpy
import numpy as np
import math
import random
import json
from sympy import symbols, parse_expr
from rclpy.node import Node

from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
from my_robot_interfaces.msg import PathPlannerMessage
from my_robot_interfaces.msg import RegulatedVelocity

class RegulatorListener(Node):
    def __init__(self):
        super().__init__("compare_listener")
        self.viconSubscriber_ = self.create_subscription(Float64MultiArray, "/pid_regulator_vicon", self.onViconMsg, 10)
        self.pathPlannerSubscriber_ = self.create_subscription(PathPlannerMessage, "/pid_regulator_pathplanner", self.onPathPlannerMsg, 10)
        self.regulatorPublisher_ = self.create_publisher(RegulatedVelocity, "/motioncontroller_regulator", 10)
        self.timeSubscriber_ = self.create_subscription(Float64, "/motioncontroller_time", self.onTimeMsg, 10)

        self.get_logger().info("Regulator node initialized.")

        self.viconPoint = []
        self.pathPlannerPoints = []
        self.pathPlannerPolynomials = [] 
        self.velocityVector = []
        self.nextPoint = []
        self.nextPointIndex = 1
        self.error = 0
        self.yawDegrees = 0
        self.angularVelocity = 0.0
        self.flightStatus = True
        self.start_time = None
        self.current_time = self.get_clock().now().nanoseconds / 1e+9

        #self.create_timer(0.5, self.comparePoints)
    
    def onViconMsg(self, msg):
        self.viconPoint = msg.data
        self.get_logger().info("Received position from VICON: " + str(self.viconPoint))

        # only start sending velocity commands to the crazyflie once the pathplanner has sent points
        if self.pathPlannerPoints != [] and self.start_time != None:
            # sets the current time to be the time since the start time (duration)
            self.current_time = (self.get_clock().now().nanoseconds / 1e+9) - self.start_time
            # adds 10 to the current time to make the time fit with the pathplanner
            jumpedTime = self.current_time + 10.0
            #timeToReachPoint = self.pathPlannerPolynomials[self.nextPointIndex][5] - jumpedTime
            # establishes the first point for the drone to fly to
            if self.nextPoint == []:
                # calculates the error between the vicon point and the first point
                self.nextPoint = self.pathPlannerPoints[1]
                self.nextPointIndex = 1
                self.error = [abs(self.viconPoint[0] - self.nextPoint[0]), abs(self.viconPoint[1] - self.nextPoint[1]), abs(self.viconPoint[2] - self.nextPoint[2])]
                # sets the velocity vector to be 0.1 m/s for x as the drone is just flying straight
                self.velocityVector = [0.1, 0, 0]
                # adjusts the yaw of the drone to be facing the point it is flyhing towards
                self.yawDegrees = math.degrees(math.atan2(self.error[1], self.error[0]))
                self.angularVelocity = (self.viconPoint[3] - self.yawDegrees) / 0.2
            else:
                # gets the next point to fly to and calculates the error between the vicon point and the next point
                self.nextPointIndex = np.where(np.all(self.pathPlannerPoints == self.nextPoint, axis=1))[0][0]
                # calculate where the drone should be according to the path planner
                self.pathPlannerPos = [self.pathPlannerPolynomials[self.nextPointIndex][0].subs('t', jumpedTime), self.pathPlannerPolynomials[self.nextPointIndex][1].subs('t', jumpedTime), np.polyval(self.pathPlannerPolynomials[self.nextPointIndex][2], jumpedTime)]
                # calculate the error between the path planner position and the vicon point (will be used for PID controller)
                self.pathError = [abs(self.viconPoint[0] - self.pathPlannerPos[0]), abs(self.viconPoint[1] - self.pathPlannerPos[1]), abs(self.viconPoint[2] - self.pathPlannerPos[2])]
                self.get_logger().info("PathPlanner position: " + str(self.pathPlannerPos) + " " + str(jumpedTime))
                self.get_logger().info("Pos error from path: " + str(self.pathError))
                # calculate the error between the vicon point and the next point (will be used to check whether the drone has reached the point)
                self.error = [abs(self.viconPoint[0] - self.nextPoint[0]), abs(self.viconPoint[1] - self.nextPoint[1]), abs(self.viconPoint[2] - self.nextPoint[2])]
                # ensures the drone is facing the point it is flying towards
                self.yawDegrees = math.degrees(math.atan2(self.error[1], self.error[0]))
                self.angularVelocity = (self.viconPoint[3] - self.yawDegrees) / 0.2
                self.get_logger().info("Yaw: " + str(self.yawDegrees))
                # if error is below a certain threshold, start moving to the next point
                if self.error[0] < 0.5 and self.error[1] < 0.5 and self.error[2] < 0.5:
                    self.nextPointIndex += 1
                    self.nextPoint = self.pathPlannerPoints[self.nextPointIndex]
                    self.get_logger().info("Moving to next point: " + str(self.nextPoint))
                    # if the drone has r eached the last point set flight status to false
                    # this will make the drone automatically land in the motion controller
                    if self.nextPointIndex == len(self.pathPlannerPoints) - 1:
                        self.flightStatus = False
                #self.velocityVector = [abs(self.viconPoint[0] - self.nextPoint[0]) / timeToReachPoint, abs(self.viconPoint[1] - self.nextPoint[1]) / timeToReachPoint, abs(self.viconPoint[2] - self.nextPoint[2]) / timeToReachPoint]
                # edit the velocity vector to be regulated based on the error 
                self.velocityVector = [0.1, 0, 0]
            
            self.get_logger().info("Current time: " + str(self.current_time))
            self.get_logger().info("Current time (jumped); " + str(self.current_time + 10.0))
            self.get_logger().info("Error: " + str(self.error))
            self.get_logger().info("Next point: " + str(self.nextPoint))
            self.get_logger().info("Polynomials for next point: " + str(self.pathPlannerPolynomials[self.nextPointIndex]))
            self.get_logger().info("Velocity vector: " + str(self.velocityVector))
            self.get_logger().info("Angular velocity: " + str(self.angularVelocity))
            # publish velocity vector, angular velcoity and flight status to motion controller
            msg = RegulatedVelocity()
            msg.data = [self.velocityVector[0], self.velocityVector[1], self.velocityVector[2], self.angularVelocity]
            msg.status = self.flightStatus
            self.regulatorPublisher_.publish(msg)
            self.get_logger().info("Velocity message sent to motion controller!")
        elif self.pathPlannerPoints != [] and self.start_time == None:
            # publish one message to motion controller to initiate start timer 
            msg = RegulatedVelocity()
            msg.data = [0.0, 0.0, 0.0]
            msg.status = True
            self.regulatorPublisher_.publish(msg)
            self.get_logger().info("Message sent to motion commander!")

    def onPathPlannerMsg(self, msg):
        if self.pathPlannerPoints == []:
            self.pathPlannerPoints = np.delete(np.array(msg.points).reshape(msg.point_row, msg.point_col), 0, 0)
            self.pathPlannerPolynomials = self.deserializeData(msg.polynomials)
            self.get_logger().info("Received polynomials from PathPlanner: " + str(self.pathPlannerPolynomials))    
            self.get_logger().info("Received points from PathPlanner: " + str(self.pathPlannerPoints))
    
    def onTimeMsg(self, msg):
        self.get_logger().info("Received time from MotionController: " + str(msg.data))
        self.start_time = msg.data
    
    def comparePoints(self):
        msg = RegulatedVelocity()
        msg.data = [random.uniform(0, 5.0), random.uniform(0, 5.0), 0.0]
        msg.status = True if random.uniform(0, 1.0) < 0.9 else False
        self.regulatorPublisher_.publish(msg)
        self.get_logger().info("Message sent to motion commander!")
    
    def deserializeData(self, stringData):
        polyArray = []
        for i in stringData:
            i = json.loads(i)
            poly = [parse_expr(i['poly_x']), parse_expr(i['poly_y']), np.poly1d(i['poly_z']), i['t_inter'], i['t_start'], i['t_end']]
            polyArray.append(poly)

        return polyArray
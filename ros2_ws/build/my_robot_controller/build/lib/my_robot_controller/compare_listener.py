#!/usr/bin/env python3
import rclpy
import numpy as np
from rclpy.node import Node

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

from std_msgs.msg import Float64MultiArray
from my_robot_interfaces.msg import PathPlannerPoints
from my_robot_interfaces.srv import StopPublishPath

class CompareListener(Node):
    def __init__(self):
        super().__init__("compare_listener")
        self.subscriber_ = self.create_subscription(Float64MultiArray, "/pid_comparison_vicon", self.onViconMsg, 10)
        self.subscriber2_ = self.create_subscription(PathPlannerPoints, "/pid_comparison_pathplanner", self.onPathPlannerMsg, 10)
        self.get_logger().info("Regulator node initialized.")

        self.viconPoint = []
        self.pathPlannerPoints = [] 
        self.velocityVector = []
        self.nextPoint = []
        self.start_time = self.get_clock().now().nanoseconds
        self.current_time = self.get_clock().now().nanoseconds

        #self.create_timer(1/2, self.comparePoints)
    
    def onViconMsg(self, msg):
        self.viconPoint = msg.data

        self.get_logger().info("Received position from VICON: " + str(self.viconPoint))
        self.current_time = self.get_clock().now().nanoseconds - self.start_time
        self.get_logger().info("Current time: " + str(self.current_time / 1e+9))

        if self.pathPlannerPoints != []:
            error = self.viconPoint - self.pathPlannerPoints[0]
            self.velocityVector = [abs(self.pathPlannerPoints[0][0] - self.pathPlannerPoints[1][0]) / self.pathPlannerPoints[1][3], abs(self.pathPlannerPoints[0][1] - self.pathPlannerPoints[1][1]) / self.pathPlannerPoints[1][3], abs(self.pathPlannerPoints[0][2] - self.pathPlannerPoints[1][2]) / self.pathPlannerPoints[1][3]]
            self.get_logger().info("Velocity vector: " + str(self.velocityVector))
            self.get_logger().info("Error: " + str(error))
            if self.nextPoint == []:
                self.nextPoint = self.pathPlannerPoints[1]
                self.velocityVector = [abs(self.viconPoint[0] - self.nextPoint[0]) / self.nextPoint[3], abs(self.viconPoint[1] - self.nextPoint[1]) / self.nextPoint[3], abs(self.viconPoint[2] - self.nextPoint[2]) / self.nextPoint[3],]

    def onPathPlannerMsg(self, msg):
        self.get_logger().info("HEYYY")
        self.pathPlannerPoints = np.array(msg.data)
        self.pathPlannerPoints = self.pathPlannerPoints.reshape(msg.row, msg.col)
        self.start_time = self.get_clock().now().nanoseconds
        self.get_logger().info("Received points from PathPlanner: " + str(self.pathPlannerPoints))      
    
    def comparePoints(self):
        self.get_logger().info("Velocity vector: " + str(self.velocityVector))


def main(args=None):
    rclpy.init()
    cflib.crtp.init_drivers()
    node = CompareListener()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

# output velocities? for crazyflie MotionCommander function/class
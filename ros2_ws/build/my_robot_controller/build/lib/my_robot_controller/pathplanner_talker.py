#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
from my_robot_interfaces.msg import PathPlannerPoints

TEMP_INPUT = [(0, 0, 0, 100), (0, 0, 100, 113), (62, 94, 100, 206), (269, 94, 100, 22), (279, 114, 100, 200), (0, 0, 100, 140), (0, 0, 0, 100)]

class PathPlannerTalker(Node):
    def __init__(self):
        super().__init__("pathplanner_talker")
        self.cmd_publisher_ = self.create_publisher(PathPlannerPoints, "/pid_comparison_pathplanner", 10)
        self.get_logger().info("My PathPlanner talker has been initialized.")

        self.timer_ = self.create_timer(1, self.broadcast)
        #self.broadcast()

    def broadcast(self):
        msg = PathPlannerPoints()
        input1D = [float(item) for sublist in TEMP_INPUT for item in sublist]
        msg.data = input1D
        msg.row = len(TEMP_INPUT)
        msg.col = 4
        self.cmd_publisher_.publish(msg)
        self.get_logger().info("Sent PathPlanner points to Regulator node.")
        if self.cmd_publisher_.get_subscription_count() >= 1:
            self.timer_.cancel()

def main(args=None):
    rclpy.init()
    node = PathPlannerTalker()
    rclpy.spin(node)
    rclpy.shutdown()
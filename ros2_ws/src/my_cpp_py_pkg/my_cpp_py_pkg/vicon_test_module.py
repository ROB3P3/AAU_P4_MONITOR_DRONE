#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
import random

TEMP_INPUT = [10, 10, 100, 30]

class ViconTalker(Node):
    def __init__(self):
        super().__init__("vicon_talker")
        self.cmd_publisher_ = self.create_publisher(Float64MultiArray, "/pid_regulator_vicon", 10)
        self.get_logger().info("My VICON talker has been initialized.")

        self.create_timer(1/3, self.broadcast) 

    def broadcast(self):
        msg = Float64MultiArray()
        TEMP_INPUT = [random.uniform(0.0, 2.0), random.uniform(0.0, 2.0), random.uniform(98.0, 102.0), random.uniform(0.0, 90.0)]
        msg.data = [float(i) for i in TEMP_INPUT]
        self.cmd_publisher_.publish(msg)
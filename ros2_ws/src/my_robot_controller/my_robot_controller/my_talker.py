#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyTalker(Node):
    def __init__(self):
        super().__init__("my_talker")
        self.cmd_publisher_ = self.create_publisher(String , "/we_are_talking" ,10)
        self.get_logger().info("My talker has been initialized")

        self.create_timer(1, self.broadcast)

    def broadcast(self):
        msg = String()
        msg.data = "HELLOW THERE"
        self.cmd_publisher_.publish(msg)

def main(args=None):
    rclpy.init()

    node = MyTalker()

    rclpy.spin(node)

    rclpy.shutdown()
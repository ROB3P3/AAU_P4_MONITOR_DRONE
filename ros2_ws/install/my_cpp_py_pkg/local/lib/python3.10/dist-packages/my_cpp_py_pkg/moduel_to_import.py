#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyNode(Node):

    def __init__(self):
        super().__init__("my_py_node")
        self.get_logger().info("Test Python Sucsess nr1")

class MyListener(Node):
    
    def __init__(self):
        super().__init__("python_listener")
        self.get_logger().info("Starting python listener")
        self.subscriber = self.create_subscription(String, "we_are_talking", self.on_msg, 10)

    def on_msg(self, msg):
        self.get_logger().info("PyListener heard:" + str(msg.data))


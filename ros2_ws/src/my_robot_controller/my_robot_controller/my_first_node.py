#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node

#laver en node klasse ud fra rcly lib set ovenfor, rcly.node.Node
class MyNode(Node):
    # standard constructor
    def __init__(self):
        # sætter navn på noden
        super().__init__("first_node")
        # printer en besked i ROS2 terminalen
        self.get_logger().info("My first node has been started successfully!")

        self.countrer_ = 0
        self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info("Hello World: "+ str(self.countrer_))
        self.countrer_ += 1

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    #køre noden indtil den bliver stoppet af ctrl+c eller andet, hvorefter rclpy.shutdown() kaldes
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
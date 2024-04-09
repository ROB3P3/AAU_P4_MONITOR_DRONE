#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyListenere(Node):
    def __init__(self):
        super().__init__("my_listener")
        self.subscriber_ = self.create_subscription(String,"/we_are_talking",self.on_msg,10)

    def on_msg(self,msg: String):
        self.get_logger().info(str(msg))



def main(args=None):
    rclpy.init()
    node = MyListenere()

    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
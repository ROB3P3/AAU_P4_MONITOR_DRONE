#!/usr/bin/env python3 
import rclpy
from my_cpp_py_pkg.moduel_to_import import MyNode

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    #køre noden indtil den bliver stoppet af ctrl+c eller andet, hvorefter rclpy.shutdown() kaldes
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
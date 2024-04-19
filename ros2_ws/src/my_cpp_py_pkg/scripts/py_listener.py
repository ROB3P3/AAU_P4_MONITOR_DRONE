#!/usr/bin/env python3 
import rclpy
from my_cpp_py_pkg.moduel_to_import import MyListener

def main(args=None):
    rclpy.init(args=args)
    node = MyListener()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()


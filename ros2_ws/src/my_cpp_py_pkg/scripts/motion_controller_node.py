#!/usr/bin/env python3 
import rclpy
from my_cpp_py_pkg.motion_controller_module import MotionControllerNode

def main(args=None):
    rclpy.init(args=args)
    node = MotionControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
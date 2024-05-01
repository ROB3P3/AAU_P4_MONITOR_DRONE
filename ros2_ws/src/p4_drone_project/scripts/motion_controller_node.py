#!/usr/bin/env python3 
import rclpy
from p4_drone_project.motion_controller_module import MotionControllerNode

def main(args=None):
    rclpy.init(args=args)
    node = MotionControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
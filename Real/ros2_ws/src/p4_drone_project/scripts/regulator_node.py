#!/usr/bin/env python3 
import rclpy
from p4_drone_project.regulator_module import RegulatorListener

def main(args=None):
    rclpy.init(args=args)
    node = RegulatorListener()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


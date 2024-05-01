#!/usr/bin/env python3 
import rclpy
from p4_drone_project.vicon_test_module import ViconTalker

def main(args=None):
    rclpy.init(args=args)
    node = ViconTalker()
    #køre noden indtil den bliver stoppet af ctrl+c eller andet, hvorefter rclpy.shutdown() kaldes
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
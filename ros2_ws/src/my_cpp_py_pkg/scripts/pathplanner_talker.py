#!/usr/bin/env python3 
import rclpy
from my_cpp_py_pkg.pathplanner_test_module import PathPlannerTalker

def main(args=None):
    rclpy.init(args=args)
    node = PathPlannerTalker()
    #køre noden indtil den bliver stoppet af ctrl+c eller andet, hvorefter rclpy.shutdown() kaldes
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
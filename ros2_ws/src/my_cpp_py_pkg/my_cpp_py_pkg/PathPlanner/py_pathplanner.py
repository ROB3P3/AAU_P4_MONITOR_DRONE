#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from my_cpp_py_pkg.PathPlanner.GUI.path_gen_vp import path_generator
import my_cpp_py_pkg.PathPlanner.LOGIK.Path_generator_v2_vp_4 as pg
import numpy as np

class PyPathPlanner(Node):
    
    def __init__(self):
        super().__init__("python_path_planner")
        self.get_logger().info("Starting python_path_planner")
        positions = path_generator()
        print('Positions:', positions)
        positions =  pg.length_of_trajectory(positions)
        positions = pg.velocity(positions)
        #print('Positions:', positions)
        All_polynomials = pg.Cubic_polynomial_trajectory_vp(positions)
        #print('All_polynomials:', All_polynomials)
        pg.plot_polynomial(All_polynomials)
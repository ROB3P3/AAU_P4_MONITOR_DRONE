#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from my_robot_interfaces.msg import PathPlannerMessage
import numpy as np
import json
from p4_drone_project.PathPlanner.GUI.path_gen_vp import path_generator
import p4_drone_project.PathPlanner.LOGIK.Path_generator_v2_vp_4 as pg

class PyPathPlanner(Node):
    def __init__(self):
        super().__init__("python_path_planner")
        self.get_logger().info("PathPlanner node initialized.")
        self.pathPlannerPublisher_ = self.create_publisher(PathPlannerMessage, "/pid_regulator_pathplanner", 10)
        self.pathPositions = path_generator()
        self.pathPositions =  pg.length_of_trajectory(self.pathPositions)
        self.pathPositions = pg.velocity(self.pathPositions)
        #print('Positions:', positions)
        self.pathPolynomials = pg.cubicPolynomialTrajectory(self.pathPositions)
        #print('Path polynomials:', pathPolynomials)
        print("Positions:", self.pathPositions)
        print("Polynomials:", self.pathPolynomials)
        #pg.plot_polynomial(pathPolynomials)
        
        self.broadcastMsg = PathPlannerMessage()
        self.broadcastMsg.polynomials = self.serializeData()
        points1D = [float(item) for sublist in self.pathPositions for item in sublist]
        self.broadcastMsg.points = points1D
        self.broadcastMsg.point_row = len(self.pathPositions)
        self.broadcastMsg.point_col = 8
        
        self.broadcastTimer_ = self.create_timer(1, self.broadcast)

    def serializeData(self):
        jsonStringArr = []
        for poly in self.pathPolynomials:
            jsonStringArr.append(json.dumps({'poly_x': str(poly[0]), 'poly_y': str(poly[1]), 'poly_z': poly[2].coeffs.tolist(), 't_inter': poly[3], 't_start': poly[4], 't_end': poly[5]}))
        return jsonStringArr

    def broadcast(self):
        self.get_logger().info("Attempt to send PathPlanner polynomials to Regulator node.")
        self.pathPlannerPublisher_.publish(self.broadcastMsg)
        if self.pathPlannerPublisher_.get_subscription_count() >= 1:
            self.get_logger().info("PathPlanner polynomials sent to Regulator node.")
            self.broadcastTimer_.cancel()
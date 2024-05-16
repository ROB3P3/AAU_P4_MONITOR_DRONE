#!/usr/bin/env python3
import rclpy
import numpy as np
import math
import random
import json
from sympy import parse_expr
from rclpy.node import Node

from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
from my_robot_interfaces.msg import PathPlannerMessage
from my_robot_interfaces.msg import RegulatedVelocity

PATHPLANNER_DELTA_T = 0.5
DEFAULT_HEIGHT = 1.0
BASE_VELOCITY = 0.05
REGULATOR_VALUE = 2000.0
VELOCITY_RANGE = 0.05
ERROR_RANGE = 5.0

class RegulatorListener(Node):
    def __init__(self):
        super().__init__("compare_listener")
        self.viconSubscriber_ = self.create_subscription(Float64MultiArray, "/pid_regulator_vicon", self.onViconMsg, 10)
        self.pathPlannerSubscriber_ = self.create_subscription(PathPlannerMessage, "/pid_regulator_pathplanner", self.onPathPlannerMsg, 10)
        self.regulatorPublisher_ = self.create_publisher(RegulatedVelocity, "/motioncontroller_regulator", 10)

        self.get_logger().info("Regulator node initialized.")

        self.viconPoint = []
        self.pathPlannerPoints = []
        self.pathPlannerPolynomials = [] 
        self.nextPoint = []
        self.nextPointIndex = 1
        self.error = 0
        self.flightStatus = True
    
    def onViconMsg(self, msg):
        self.viconPoint = [msg.data[0] / 10.0, msg.data[1] / 10.0, msg.data[2] / 10.0, math.degrees(msg.data[3])]
        self.get_logger().info("Received position from VICON: " + str(self.viconPoint))

        # only start sending velocity commands to the crazyflie once the pathplanner has sent points
        if self.pathPlannerPoints != [] and self.flightStatus == True:
            # Calculate error vector between current position and desired position
            self.error = [self.pathPlannerPoints[self.nextPointIndex][0] - self.viconPoint[0], self.pathPlannerPoints[self.nextPointIndex][1] - self.viconPoint[1], self.pathPlannerPoints[self.nextPointIndex][2] - self.viconPoint[2]]

            # If the error is within ERROR_RANGE on the x- and y-axis go to the next point
            if self.error[0] < ERROR_RANGE and self.error[0] > -ERROR_RANGE and self.error[1] < ERROR_RANGE and self.error[1] > -ERROR_RANGE:
                self.nextPointIndex += 1

                # If it is the last point in the list tell the motion controller to stop flying else move to next point in list
                if self.nextPointIndex == len(self.pathPlannerPoints):
                    self.flightStatus = False
                else:
                    self.error = [self.pathPlannerPoints[self.nextPointIndex][0] - self.viconPoint[0], self.pathPlannerPoints[self.nextPointIndex][1] - self.viconPoint[1], self.pathPlannerPoints[self.nextPointIndex][2] - self.viconPoint[2]]
                    self.get_logger().info("---------------------------------------------------- flying to next point: " + str(self.pathPlannerPoints[self.nextPointIndex]) + " ---------------------------------------------------------------------------")

            # Convert to a numpy vector
            errorVector = np.array([self.error[0], self.error[1]])
            # Calculate length of error vector
            errorLength = math.sqrt(self.error[0] ** 2 + self.error[1] ** 2)
            # Normalize error vector so it has a length of 1
            normErrorVector = errorVector / errorLength
            normErrorVectorLength = math.sqrt(normErrorVector[0] ** 2 + normErrorVector[1] ** 2)
            # Multiply normalized error vector by 0.1 to get the velocity
            normErrVelocityVector = normErrorVector * 0.1
            velocityX = normErrVelocityVector[0]
            velocityY = normErrVelocityVector[1]

            self.get_logger().info("Error: " + str(self.error))
            self.get_logger().info("Velocity: " + str([float(velocityX), float(velocityY), 0.0, 0.0]))
            self.get_logger().info("Error length: " + str(errorLength))
            self.get_logger().info("Normalized error vector: " + str(normErrorVector))
            self.get_logger().info("Normalized error vector length: " + str(normErrorVectorLength))
            self.get_logger().info("Normalized error velocity vector: " + str(normErrVelocityVector))
            self.get_logger().info("Normalized error velocity vector (0.1): " + str(normErrorVector * 0.1))

            # Send velocity and flight status to motion controller
            msg = RegulatedVelocity()
            msg.data = [float(velocityX), float(velocityY), 0.0, 0.0]
            msg.status = self.flightStatus
            self.regulatorPublisher_.publish(msg)
            self.get_logger().info("Velocity message sent to motion controller!")

    def onPathPlannerMsg(self, msg):
        #self.pathPlannerPoints = np.delete(np.array(msg.points).reshape(msg.point_row, msg.point_col), 0, 0)
        # ask rasmus if the last polynomial describes movement directly to [0, 0, 0] or movement to [0, 0, 100]
        # if it describes movement directly to [0, 0, 0] it needs to be removed
        # currently the last polynomial is fucked
        if self.pathPlannerPolynomials == []:
            # Deserialize polynomials to get back into symp expr
            self.pathPlannerPolynomials = self.deserializeData(msg.polynomials)
            # Remove first and last polynomials as they describe (0, 0, 0) -> (0, 0, 100) and (0, 0, 100) -> (0, 0, 0) and are not needed
            self.pathPlannerPolynomials.pop(0)
            self.pathPlannerPolynomials.pop()

            # Create list of points based on polynomials with an interval of PATHPLANNER_DELTA_T
            for poly in self.pathPlannerPolynomials:
                for i in range(0, math.ceil(poly[3] / PATHPLANNER_DELTA_T)):
                    self.pathPlannerPoints.append([poly[0].subs('t', poly[4] + i * PATHPLANNER_DELTA_T), poly[1].subs('t', poly[4] + i * PATHPLANNER_DELTA_T), np.polyval(poly[2], poly[4] + i * PATHPLANNER_DELTA_T), poly[4] + i * PATHPLANNER_DELTA_T])
            
            # Append last point (0, 0, 100)
            self.pathPlannerPoints.append([self.pathPlannerPolynomials[-1][0].subs('t', self.pathPlannerPolynomials[-1][5]), self.pathPlannerPolynomials[-1][1].subs('t', self.pathPlannerPolynomials[-1][5]), np.polyval(self.pathPlannerPolynomials[-1][2], self.pathPlannerPolynomials[-1][5]), self.pathPlannerPolynomials[-1][5]])
            self.nextPointIndex = 0

            self.get_logger().info("Received polynomials from PathPlanner: " + str(self.pathPlannerPolynomials)) 
            self.get_logger().info("Derived points from polynomials: " + str(self.pathPlannerPoints))

    def deserializeData(self, stringData):
        polyArray = []
        for i in stringData:
            i = json.loads(i)
            poly = [parse_expr(i['poly_x']), parse_expr(i['poly_y']), np.poly1d(i['poly_z']), i['t_inter'], i['t_start'], i['t_end']]
            polyArray.append(poly)

        return polyArray#
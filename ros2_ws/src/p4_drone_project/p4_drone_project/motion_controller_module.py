#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from my_robot_interfaces.msg import RegulatedVelocity

import logging
import time
from threading import Event

import sys
from select import select
import termios
import tty

import math
import numpy as np
import sympy

import cflib
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

DEFAULT_HEIGHT = 1.0
BASE_VELOCITY = 0.085
REGULATOR_VALUE = 2000.0
SLOWDOWN_VELOCITY_MAX = 0.015
ERROR_RANGE = 5.0
POLY_DELTA_T = 0.5
deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)

class MotionControllerNode(Node):
    def __init__(self):
        super().__init__("motion_controller")
        self.get_logger().info("Motion Controller node initialized.")
        self.timePublisher_ = self.create_publisher(Float64, "/motioncontroller_time", 10)

        cflib.crtp.init_drivers()

        self.receivedVelocity = [0.0, 0.0, 0.0, 0.0]
        self.flightStatus = True
        self.start_time = None
        self.prevViconPoint = []

        self.velocityNode = VelocityRecipientNode()
        self.startFlight()

    def param_deck_flow(self, _, value_str):
        value = int(value_str)

        if value:
            deck_attached_event.set()
            print("Deck is attached!")
        else:
            print("Deck is not attached.")
    
    def flightVelocity(self, cf):
        with MotionCommander(cf, default_height=DEFAULT_HEIGHT) as mc:
            # has a time difference of start until sent time of 8.13 - 8.23 seconds with the default height
            # has a time difference of start until sent time ~4.7 seconds without default heigh
            while (self.flightStatus):
                """ if self.start_time == None:
                    self.start_time = self.get_clock().now().nanoseconds / 1e+9
                    self.timePublisher_.publish(Float64(data=self.start_time))
                    self.get_logger().info("Time published: " + str(self.start_time)) """

                rclpy.spin_once(self.velocityNode)
                self.receivedVelocity = self.velocityNode.receivedVelocity
                self.flightStatus = self.velocityNode.flightStatus

                mc.start_linear_motion(self.receivedVelocity[0], self.receivedVelocity[1], self.receivedVelocity[2], self.receivedVelocity[3])
                print("Changing direction to: " + str(self.receivedVelocity))
  
    def startFlight(self):
        self.get_logger().info("Starting flight!")
        with SyncCrazyflie(URI, cf = Crazyflie(rw_cache='./cache')) as scf:
            #self.flightVelocity(scf)
            self.testFlight(scf)

    
    def testFlight(self, cf):
        fly = True
        points = [[0, 0, 100.0, 0.0, 5.0], [-50.0, 50.0, 100.0, 5.0, 8.54], [-150.0, 50.0, 100.0, 8.54, 13.54], [-150.0, -150.0, 100.0, 13.54, 18.54], [-50.0, -150.0, 100.0, 18.54, 23.54], [0, 0, 100.0, 23.54, 28.54]]


        #positions = [(0, 0, 100.0, 10, 10, 0, 122.96232256791887, 10.0), (63.99009900990099, 105.0, 100.0, 10, 10, 0, 86.69139470353151, 22.29623225679189)]
        #polynomials = [[sympy.parse_expr('10*t + 63.4397299691071*(0.1*t - 1)**3 - 117.010448101245*(0.1*t - 1)**2 - 100.0'), sympy.parse_expr('10*t + 19.3230782998319*(0.1*t - 1)**3 - 35.6401588036363*(0.1*t - 1)**2 - 100.0'), np.poly1d([100.]), 12.296232256791889, 10.0, 22.29623225679189]]

        polynomials = [[sympy.parse_expr('10*t + 597.173216392375*(0.1*t - 1)**3 - 370.036945411831*(0.1*t - 1)**2 - 100.0'), sympy.parse_expr('10*t + 150.643661949852*(0.1*t - 1)**3 - 93.3459823438381*(0.1*t - 1)**2 - 100.0'), np.poly1d([100.]), 4.130983945186367, 10.0, 14.130983945186367], [sympy.parse_expr('10*t + 0.672769597394732*(0.070766480513952*t - 1)**3 - 1.02230533205856*(0.070766480513952*t - 1)**2 - 121.048969886646'), sympy.parse_expr('10*t + 256.157161954894*(0.070766480513952*t - 1)**3 - 389.242964494189*(0.070766480513952*t - 1)**2 - 105.309839451864'), np.poly1d([100.]), 14.315133829214536, 14.130983945186367, 28.446117774400903], [sympy.parse_expr('10*t + 4618.333691805*(0.0351541819495634*t - 1)**3 - 3429.82754194849*(0.0351541819495634*t - 1)**2 - 121.398677744009'), sympy.parse_expr('10*t + 1991.33836672659*(0.0351541819495634*t - 1)**3 - 1478.87693512857*(0.0351541819495634*t - 1)**2 - 238.461177744009'), np.poly1d([100.]), 14.083763353476073, 28.446117774400903, 42.529881127876976]]#, [sympy.parse_expr('10*t + 101.381452132356*(0.0235128802028213*t - 1)**3 - 47.2637753886203*(0.0235128802028213*t - 1)**2 - 401.646637365726'), sympy.parse_expr('10*t + 7473.39308446182*(0.0235128802028213*t - 1)**3 - 3484.07686717418*(0.0235128802028213*t - 1)**2 - 359.29881127877'), np.poly1d([100.]), 13.218215013060508, 42.529881127876976, 55.748096140937484], [sympy.parse_expr('10*t + 42226.3573117115*(0.017937832306809*t - 1)**3 - 14510.5666932341*(0.017937832306809*t - 1)**2 - 403.168461409375'), sympy.parse_expr('10*t + 17917.3955437145*(0.017937832306809*t - 1)**3 - 6157.09191031772*(0.017937832306809*t - 1)**2 - 471.480961409375'), np.poly1d([100.]), 12.771430272051752, 55.748096140937484, 68.51952641298924], [sympy.parse_expr('10*t + 155.441929306996*(0.0145943799140216*t - 1)**3 - 40.8322031625586*(0.0145943799140216*t - 1)**2 - 657.021351086414'), sympy.parse_expr('10*t + 40960.6553335233*(0.0145943799140216*t - 1)**3 - 10759.7339257587*(0.0145943799140216*t - 1)**2 - 579.195264129892'), np.poly1d([100.]), 11.9993502206718, 68.51952641298924, 80.51887663366104], [sympy.parse_expr('10*t + 52860.9418994023*(0.0124194479829833*t - 1)**3 - 18498.2246214525*(0.0124194479829833*t - 1)**2 - 657.43876633661'), sympy.parse_expr('10*t + 47859.8820925436*(0.0124194479829833*t - 1)**3 - 16748.1474505113*(0.0124194479829833*t - 1)**2 - 689.18876633661'), np.poly1d([100.]), 18.784584770497318, 80.51887663366104, 99.30346140415836], [sympy.parse_expr('10*t + 195849.810798509*(0.0100701424286719*t - 1)**3 - 29583.5323405415*(0.0100701424286719*t - 1)**2 - 993.034614041584'), sympy.parse_expr('10*t + 195849.810798509*(0.0100701424286719*t - 1)**3 - 29583.5323405415*(0.0100701424286719*t - 1)**2 - 993.034614041584a'), np.poly1d([  0.2,  -3. ,   0. , 100. ]), 10.0, 99.30346140415836, 109.30346140415836]]

        polyPoints = []
        polyXY = []

        for poly in polynomials:
            for i in range(0, math.ceil(poly[3] / POLY_DELTA_T)):
                polyXY.append([poly[0].subs('t', poly[4] + i * POLY_DELTA_T), poly[1].subs('t', poly[4] + i * POLY_DELTA_T)])
                polyPoints.append([poly[0].subs('t', poly[4] + i * POLY_DELTA_T), poly[1].subs('t', poly[4] + i * POLY_DELTA_T), np.polyval(poly[2], poly[4] + i * POLY_DELTA_T), [sympy.diff(poly[0], 't').subs('t', poly[4] + i * POLY_DELTA_T), sympy.diff(poly[1], 't').subs('t', poly[4] + i * POLY_DELTA_T)], poly[4] + i * POLY_DELTA_T])

        polyPoints.append([polynomials[-1][0].subs('t', polynomials[-1][5]), polynomials[-1][1].subs('t', polynomials[-1][5]), polynomials[-1][2](polynomials[-1][5]), [sympy.diff(polynomials[-1][0], 't').subs('t', polynomials[-1][4] + i * POLY_DELTA_T), sympy.diff(polynomials[-1][1], 't').subs('t', polynomials[-1][4] + i * POLY_DELTA_T)], polynomials[-1][5]])

        print(polyXY)
        print(polyPoints)

        time.sleep(300)

        points = polyPoints

        flyingTo = 0
        velocity = [0.1, 0.1, 0.0, 0.0]
        with MotionCommander(cf, default_height=DEFAULT_HEIGHT) as mc:
            # has a time difference of start until sent time of 8.13 - 8.23 seconds with the default height
            # has a time difference of start until sent time ~4.7 seconds without default heigh
            start_time = self.get_clock().now().nanoseconds / 1e+9
            viconPoint = [0.0, 0.0, 0.0]
            while (fly):
                keyInput = self.getKey()

                rclpy.spin_once(self.velocityNode)
                self.prevViconPoint = viconPoint
                viconPoint 
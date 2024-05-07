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
from sympy import symbols, parse_expr

import cflib
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

DEFAULT_HEIGHT = 1.0
BASE_VELOCITY = 0.2
REGULATOR_VALUE = 50.0
SLOWDOWN_RANGE = 15.0
SLOWDOWN_REGULATOR_VALUE = 30.0
SLOWDOWN_VELOCITY_MAX = 0.1
ERROR_RANGE = 5.0
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
                if self.start_time == None:
                    self.start_time = self.get_clock().now().nanoseconds / 1e+9
                    self.timePublisher_.publish(Float64(data=self.start_time))
                    self.get_logger().info("Time published: " + str(self.start_time))

                rclpy.spin_once(self.velocityNode)
                self.receivedVelocity = self.velocityNode.receivedVelocity
                self.flightStatus = self.velocityNode.flightStatus

                if self.receivedVelocity[0] == 0.0 and self.receivedVelocity[1] == 0.0 and self.receivedVelocity[2] == 0.0 and self.receivedVelocity[3] != 0.0:
                    while(abs(self.receivedVelocity[4] - self.receivedVelocity[5]) > 2):
                        mc.start_linear_motion(0.0, 0.0, 0.0, self.receivedVelocity[3])
                        rclpy.spin_once(self.velocityNode)
                        self.receivedVelocity = self.velocityNode.receivedVelocity
                        self.flightStatus = self.velocityNode.flightStatus

                mc.start_linear_motion(self.receivedVelocity[0], self.receivedVelocity[1], self.receivedVelocity[2], self.receivedVelocity[3])
                print(self.receivedVelocity[0], self.receivedVelocity[1], self.receivedVelocity[2], self.receivedVelocity[3])
                print("Changing direction to: " + str(self.receivedVelocity))
  
    def startFlight(self):
        self.get_logger().info("Starting flight!")
        with SyncCrazyflie(URI, cf = Crazyflie(rw_cache='./cache')) as scf:
            #self.flightVelocity(scf)
            self.testFlight(scf)

    
    def testFlight(self, cf):
        fly = True
        points = [[0, 0, 100.0, 0.0, 5.0], [-50.0, 50.0, 100.0, 5.0, 8.54], [-150.0, 50.0, 100.0, 8.54, 13.54], [-150.0, -150.0, 100.0, 13.54, 18.54], [-50.0, -150.0, 100.0, 18.54, 23.54], [0, 0, 100.0, 23.54, 28.54]]


        positions = [(0, 0, 100.0, 10, 10, 0, 122.96232256791887, 10.0), (63.99009900990099, 105.0, 100.0, 10, 10, 0, 86.69139470353151, 22.29623225679189)]
        polynomials = [parse_expr('10*t + 63.4397299691071*(0.1*t - 1)**3 - 117.010448101245*(0.1*t - 1)**2 - 100.0'), parse_expr('10*t + 19.3230782998319*(0.1*t - 1)**3 - 35.6401588036363*(0.1*t - 1)**2 - 100.0'), np.poly1d([100.]), 12.296232256791889, 10.0, 22.29623225679189]

        print(polynomials[0].subs('t', polynomials[5]), polynomials[1].subs('t', polynomials[5]), polynomials[2](polynomials[5]), polynomials[3], polynomials[4], polynomials[5])

        flyingTo = 0
        velocity = [0.1, 0.1, 0.0, 0.0]
        with MotionCommander(cf, default_height=DEFAULT_HEIGHT) as mc:
            # has a time difference of start until sent time of 8.13 - 8.23 seconds with the default height
            # has a time difference of start until sent time ~4.7 seconds without default heigh
            start_time = self.get_clock().now().nanoseconds / 1e+9
            while (fly):
                keyInput = self.getKey()

                rclpy.spin_once(self.velocityNode)
                viconPoint = self.velocityNode.viconPoint
                error = [points[flyingTo][0] - viconPoint[0], points[flyingTo][1] - viconPoint[1], points[flyingTo][2] - viconPoint[2]]

                #velocity = [max(min(0.2, error[0] / 50.0), -0.2), max(min(0.2, error[1] / 50.0), -0.2), 0.0, 0.0]
                #velocity = [max(min(VELOCITY_MAX, error[0] / REGULATOR_VALUE), -VELOCITY_MAX), max(min(VELOCITY_MAX, error[1] / REGULATOR_VALUE), -VELOCITY_MAX), 0.0, 0.0]
                velocity = [-BASE_VELOCITY if error[0] < 0 else BASE_VELOCITY, -BASE_VELOCITY if error[1] < 0 else BASE_VELOCITY, 0.0, 0.0]

                self.get_logger().info("Error: " + str(error))
                self.get_logger().info("Velocity: " + str(velocity))

                if error[0] < SLOWDOWN_RANGE and error[0] > -SLOWDOWN_RANGE and error[1] < SLOWDOWN_RANGE and error[1] > -SLOWDOWN_RANGE:
                    velocity = [max(min(SLOWDOWN_VELOCITY_MAX, error[0] / REGULATOR_VALUE), -SLOWDOWN_VELOCITY_MAX), max(min(SLOWDOWN_VELOCITY_MAX, error[1] / REGULATOR_VALUE), -SLOWDOWN_VELOCITY_MAX), 0.0, 0.0]
                    current_time = self.get_clock().now().nanoseconds / 1e+9 - start_time
                    self.get_logger().info("Time till slowmode: " + str(current_time))
                    if error[0] < ERROR_RANGE and error[0] > -ERROR_RANGE and error[1] < ERROR_RANGE and error[1] > -ERROR_RANGE:
                        flyingTo += 1
                        if flyingTo == len(points):
                            self.get_logger().info("flight ended")
                            fly = False
                        self.get_logger().info("---------------------------------------------------- flying to next point: " + str(points[flyingTo]) + " ---------------------------------------------------------------------------")

                mc.start_linear_motion(velocity[0], velocity[1], velocity[2], velocity[3])
                
                if keyInput == 'q':
                    fly = False
            self.get_logger().info("Flight ended!")


    def getKey(self):
        settings = termios.tcgetattr(sys.stdin)
        timeout = 0.1
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key



# motion commander node step-by-step :
# first initiate connection to crazyflie + crazyradio
# then initiate subscriber connection to regulator
# when receiving information from regulator start flying
# use the command start_linear_motion to start flying
# run the flying command in a while loop? where the condition is that it has not yet reached the last point?
# if the start_linear_motion command runs in a while loop a separate node is needed to subscribe to the regulator
# having a separate node and spinning this node can take some time so the publisher timer of the regulator needs to be significantly lower
# when out of the while loop finish the 'with' context and land

class VelocityRecipientNode(Node):
    def __init__(self):
        super().__init__("velocity_recipient_node")
        #self.regulatorSubscriber_ = self.create_subscription(RegulatedVelocity, "/motioncontroller_regulator", self.onRegulatorMsg, 10)
        self.viconSubscriber_ = self.create_subscription(Float64MultiArray, "/pid_regulator_vicon", self.onViconMsg, 10)
        self.receivedVelocity = []
        self.flightStatus = True
        self.viconPoint = []
    
    def onRegulatorMsg(self, msg):
        """Callback function for subscription to '/motioncontroller_regulator' topic"""
        self.get_logger().info("Velocity Recipient Node received message from regulator topic.")
        self.get_logger().info("Received message: " + str(msg.data))
        self.get_logger().info("Received status: " + str(msg.status))
        self.receivedVelocity = msg.data
        self.flightStatus = msg.status
    
    def onViconMsg(self, msg):
        self.viconPoint = [msg.data[0] / 10.0, msg.data[1] / 10.0, msg.data[2] / 10.0, math.degrees(msg.data[3])]
        self.get_logger().info("Received position from VICON: " + str(self.viconPoint))
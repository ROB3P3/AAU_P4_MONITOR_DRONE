#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import RegulatedVelocity

import logging
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
deck_attached_event = Event()
logging.basicConfig(level=logging.ERROR)

class MotionControllerNode(Node):
    def __init__(self):
        super().__init__("motion_controller_node")
        self.get_logger().info("Motion Controller node initialized.")

        cflib.crtp.init_drivers()

        self.receivedVelocity = [0.0, 0.0, 0.0, 0.0]
        self.flightStatus = True

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
            while (self.flightStatus):
                # Run velocity receiver node
                rclpy.spin_once(self.velocityNode)
                # Set received velocity and flight status
                self.receivedVelocity = self.velocityNode.receivedVelocity
                self.flightStatus = self.velocityNode.flightStatus

                # Change drone's velocity to the received velocity
                mc.start_linear_motion(self.receivedVelocity[0], self.receivedVelocity[1], self.receivedVelocity[2], self.receivedVelocity[3])
                print("Changing direction to: " + str(self.receivedVelocity))
  
    def startFlight(self):
        self.get_logger().info("Starting flight!")
        with SyncCrazyflie(URI, cf = Crazyflie(rw_cache='./cache')) as scf:
            self.flightVelocity(scf)

class VelocityRecipientNode(Node):
    def __init__(self):
        super().__init__("motion_controller_velocity_node")
        self.regulatorSubscriber_ = self.create_subscription(RegulatedVelocity, "/command_topic", self.onRegulatorMsg, 10)
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
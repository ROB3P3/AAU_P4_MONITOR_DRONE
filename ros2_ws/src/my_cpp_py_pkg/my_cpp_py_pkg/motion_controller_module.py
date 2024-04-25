#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from my_robot_interfaces.msg import RegulatedVelocity

import logging
import time
from threading import Event

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
        super().__init__("motion_controller")
        self.get_logger().info("Motion Controller node initialized.")
        self.timePublisher_ = self.create_publisher(Float64, "/motioncontroller_time", 10)

        cflib.crtp.init_drivers()

        self.receivedVelocity = [0, 0, 0]
        self.flightStatus = True
        self.start_time = None

        self.velocityNode = VelocityRecipientNode()
        self.testFlight()

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
                if self.start_time == None:
                    self.start_time = self.get_clock().now().nanoseconds / 1e+9
                    self.timePublisher_.publish(Float64(data=self.start_time))
                    self.get_logger().info("Time published: " + str(self.start_time))
                rclpy.spin_once(self.velocityNode)
                self.receivedVelocity = self.velocityNode.receivedVelocity
                self.flightStatus = self.velocityNode.flightStatus
                mc.start_linear_motion(self.receivedVelocity[0], self.receivedVelocity[1], self.receivedVelocity[2])
                print(self.receivedVelocity[0], self.receivedVelocity[1], self.receivedVelocity[2])
                print("Changing direction to: " + str(self.receivedVelocity))
  
    def testFlight(self):
        self.get_logger().info("Starting flight!")
        with SyncCrazyflie(URI, cf = Crazyflie(rw_cache='./cache')) as scf:
            self.flightVelocity(scf)

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
        self.regulatorSubscriber_ = self.create_subscription(RegulatedVelocity, "/motioncontroller_regulator", self.onRegulatorMsg, 10)
        self.receivedVelocity = []
        self.flightStatus = True
    
    def onRegulatorMsg(self, msg):
        """Callback function for subscription to '/motioncontroller_regulator' topic"""
        self.get_logger().info("Velocity Recipient Node received message from regulator topic.")
        self.get_logger().info("Received message: " + str(msg.data))
        self.get_logger().info("Received status: " + str(msg.status))
        self.receivedVelocity = msg.data
        self.flightStatus = msg.status
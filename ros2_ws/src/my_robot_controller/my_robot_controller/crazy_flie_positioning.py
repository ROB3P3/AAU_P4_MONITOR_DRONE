#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node

import logging
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

DEFAULT_HEIGHT = 0.5

deck_attached_event = Event()

logging.basicConfig(level=logging.ERROR)

class CrazyNode(Node):
    def __init__(self):
        # sætter navn på noden
        super().__init__("crazy_node")
        # printer en besked i ROS2 terminalen
        self.get_logger().info("Crazy node has been started successfully!")

        self.create_timer(1, self.timer_callback)

    def take_off_simple(self, scf):
        with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
            time.sleep(3)
            mc.stop()

    def param_deck_flow(self, _, value_str):
        value = int(value_str)
        print(value)
        if value:
            deck_attached_event.set()
            self.get_logger().info('Deck is attached!')
        else:
            self.get_logger().info('Deck is NOT attached!')

    def timer_callback(self):   
        with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

            scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                            cb=self.param_deck_flow)
            time.sleep(1) 

            if not deck_attached_event.wait(timeout=5):
                print('No flow deck detected!')
                while True:
                    time.sleep(1)
                    self.get_logger().info("No flow deck detected! Not taking off! Trying again in 1 second")
                    if deck_attached_event.wait(timeout=5):
                        break

            self.take_off_simple(scf)

            while True:
                time.sleep(1)
                self.get_logger().info("Program has ended!")
                    

def main(args=None):
    rclpy.init(args=args)
    cflib.crtp.init_drivers()

    node = CrazyNode()
    #køre noden indtil den bliver stoppet af ctrl+c eller andet, hvorefter rclpy.shutdown() kaldes
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()



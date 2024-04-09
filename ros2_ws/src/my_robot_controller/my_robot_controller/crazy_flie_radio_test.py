#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node

import logging
import time
from threading import Event

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

deck_attached_event = Event()

logging.basicConfig(level=logging.ERROR)

class CrazyNode(Node):
    def __init__(self):
        # sætter navn på noden
        super().__init__("crazy_node")
        # printer en besked i ROS2 terminalen
        self.get_logger().info("Crazy node has been started successfully!")

        self.create_timer(1, self.timer_callback)

    def param_deck_flow(self, _, value_str):
        value = int(value_str)
        print(value)
        if value:
            deck_attached_event.set()
            print('Deck is attached!')
        else:
            print('Deck is NOT attached!')

    def timer_callback(self):
        cflib.crtp.init_drivers()   

        with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

            scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                            cb=self.param_deck_flow)
            time.sleep(1) 

def main(args=None):
    rclpy.init(args=args)
    node = CrazyNode()
    #køre noden indtil den bliver stoppet af ctrl+c eller andet, hvorefter rclpy.shutdown() kaldes
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()



#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pyvicon_datastream as pv

class MyTalker(Node):
    def __init__(self):
        super().__init__("vicon_node")
        self.cmd_publisher_ = self.create_publisher(String , "/Vicon_Data" ,10)
        self.get_logger().info("vicon_node has been initialized")

        self.vicon_init("127.0.0.1")


    def vicon_init (self, ip):
        """Initialize the Vicon client at the given IP address."""

        self.client = pv.PyViconDatastream()
        self.get_logger().info("Vicon Datastream client version: " + self.client.__version__)
        try:
            self.client.connect(ip)
            self.get_logger().info("Client is connected?: " + str(self.client.is_connected()))
            """
            #Disse tal deffinere en retning for systemet.
            Up = 0 
            Down = 1
            Left = 2
            Right = 3
            Forward = 4
            Backward = 5
            self.client.set_axis_mapping(4, 2, 0)"""
            self.get_logger().info("The mapping of axis: " + str(self.client.get_axis_mapping()))


        except Exception as e:
            self.get_logger().error("Failed to connect to Vicon Datastream: " + str(e))
            return False
        
        self.client.disconnect()
        self.get_logger().info("Client is connected?: " + str(self.client.is_connected()))


    def broadcast(self):
        msg = String()
        msg.data = "POS[x0,y0,z0]"
        self.cmd_publisher_.publish(msg)

def main(args=None):
    rclpy.init()

    node = MyTalker()

    rclpy.spin(node)

    rclpy.shutdown()
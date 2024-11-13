import os
import math
import sys
import pytest
import time
import unittest
import numpy as np

import launch
import launch_ros
import launch_ros.actions
import launch_testing.actions

import rclpy

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray

#@pytest.mark.unit
#def test_math():
#    assert 2 + 2 == 4  # This should fail for most mathematical systems

@pytest.mark.integration
@pytest.mark.rostest
def generate_test_description():
    file_path = os.path.dirname(__file__)
    tested_node = launch_ros.actions.Node(
        executable=sys.executable,
        arguments=[os.path.join(file_path, "..", "ros_testing_py", "tested_node.py")],
        additional_env={"PYTHONUNBUFFERED":"1"},
        parameters=[]
    )
    
    return (
        launch.LaunchDescription([
            tested_node,
            launch_testing.actions.ReadyToTest(),
        ]),
        {
            "tested_node":tested_node
        }
    )
    
class TestOfNode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def setUp(self):
        self.node = rclpy.create_node('t_node')

    def tearDown(self):
        self.node.destroy_node()
    
    def test_node(self, tested_node, proc_output):
        rec_data = []
        sub = self.node.create_subscription(Float32MultiArray,
            'out_vel', lambda msg: rec_data.append(msg), 1)
        pub = self.node.create_publisher(Twist, 'cmd_vel', 1)
        
        msg = Twist()
        msg.linear.x = 0.1
        pub.publish(msg)
        
        factor = 60/(2*math.pi*0.1)
        expected_value = [0.1*factor, 0.1*factor, 0.1*factor, 0.1*factor]
        
        try:
            end_time = time.time() + 10
            while time.time()<end_time:
                rclpy.spin_once(self.node, timeout_sec=0.1)
                if rec_data:
                    break
                pub.publish(msg)

            np.testing.assert_almost_equal(rec_data[0].data, expected_value, 6)
            
        finally:
            self.node.destroy_subscription(sub)
            self.node.destroy_publisher(pub)
        

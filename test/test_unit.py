import math
import pytest
from geometry_msgs.msg import Twist
from ros_testing_py.tested_node import *

@pytest.mark.unit
def test_math():
    assert 2 + 2 == 4  # This should fail for most mathematical systems


@pytest.mark.unit
def test_vel_calc():
    test_msg = Twist()
    test_msg.linear.x = 0.1
    factor = 60/(2*math.pi*0.1)
    expected_values = [0.1*factor, 0.1*factor, 0.1*factor, 0.1*factor]
    vels = calc_vels(test_msg)
    for i,x in enumerate(vels):
        assert x == expected_values[i]


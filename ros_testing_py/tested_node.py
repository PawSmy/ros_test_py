import math
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray

def calc_vels(msg):
    """Calculates wheel welocities for mecanum drive robot

    Parameters
    ----------
    msg : geometry_msgs.msg.Twist
        ROS2 message with linear and angular velocity

    Returns
    -------
    tuple
        tuple: tupe with value of wheel velocities
    """
    v_x = msg.linear.x
    v_y = msg.linear.y
    w = msg.angular.z
    x = 0.255
    y = 0.29
    r = (x**2 + y**2)**0.5
    wheel_r = 0.1
    v_x_f_r = v_x + w*r*math.sin(math.atan2(-y,x)+math.pi)
    v_y_f_r = v_y + w*r*math.cos(math.atan2(-y,x)+math.pi)
    v_x_f_l = v_x + w*r*math.sin(math.atan2(y,x)+math.pi)
    v_y_f_l = v_y + w*r*math.cos(math.atan2(y,x)+math.pi)
    v_x_b_r = v_x + w*r*math.sin(math.atan2(-y,-x)+math.pi)
    v_y_b_r = v_y + w*r*math.cos(math.atan2(-y,-x)+math.pi)
    v_x_b_l = v_x + w*r*math.sin(math.atan2(y,-x)+math.pi)
    v_y_b_l = v_y + w*r*math.cos(math.atan2(y,-x)+math.pi)
    
    w_f_r = (v_x_f_r - v_y_f_r)/(2*math.pi*wheel_r)*60
    w_f_l = (v_x_f_l + v_y_f_l)/(2*math.pi*wheel_r)*60
    w_b_r = (v_x_b_r + v_y_b_r)/(2*math.pi*wheel_r)*60
    w_b_l = (v_x_b_l - v_y_b_l)/(2*math.pi*wheel_r)*60
    
    return (w_f_r, w_f_l, w_b_r, w_b_l)

class TestedNode(Node):
    """Example ROS2 node for testing

    Attributes
    ----------
    __test__ : bool
        Special attribute that lets pytest know that this class is not test
    subscription: Subscription
        ROS2 subscriber for cmd_vel topic
    publisher: Publisher
        ROS2 publisher for computed wheel velcities
    """
    __test__ = False
    def __init__(self):
        """Class constructor
        """
        super().__init__('tested_node')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10)
        self.subscription  # prevent unused variable warning        
        self.publisher = self.create_publisher(Float32MultiArray, 'out_vel', 10)

    def cmd_vel_callback(self, msg):
        """Subscriber callback function, computes and publishes wheel velocities

        Parameters
        ----------
        msg : geometry_msgs.msg.Twist
            ROS2 message with linear and angular velocity to be transformed 
        """
        new_msg = Float32MultiArray()
        vels = calc_vels(msg)
        for v in vels:
            new_msg.data.append(v)
        self.publisher.publish(new_msg)


def main(args=None):
    rclpy.init(args=args)

    test_node = TestedNode()

    try:
        rclpy.spin(test_node)
    except KeyboardInterrupt:
        pass

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    test_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

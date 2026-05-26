#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class DrawController(Node):
    def __init__(self):
        super().__init__('draw_controller')
        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.joint_state = JointState()
        self.joint_state.name = ['x_joint', 'y_joint']

        # Define a square path (within joint limits)
        self.path = [
            (-0.2, -0.2),
            (0.2, -0.2),
            (0.2, 0.2),
            (-0.2, 0.2)
        ]
        self.step = 0

        # Timer fires every 0.5 seconds
        self.timer = self.create_timer(0.5, self.move)

    def move(self):
        x, y = self.path[self.step]
        self.joint_state.position = [x, y]
        self.joint_state.header.stamp = self.get_clock().now().to_msg()
        self.pub.publish(self.joint_state)

        self.get_logger().info(f'Publishing: x={x}, y={y}')
        self.step = (self.step + 1) % len(self.path)

def main(args=None):
    rclpy.init(args=args)
    node = DrawController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

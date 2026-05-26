#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point
from .image_processor import process_image
from .path_optimizer import optimize_path
import sys

class ImageDrawController(Node):
    def __init__(self, image_path):
        super().__init__('image_draw_controller')

        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.marker_pub = self.create_publisher(MarkerArray, '/drawing_trail', 10)

        self.joint_state = JointState()
        self.joint_state.name = ['x_joint', 'y_joint']

        self.contours = optimize_path(process_image(image_path))
        self.contour_index = 0
        self.point_index = 0
        self.marker_id = 0
        self.all_markers = MarkerArray()
        self.current_marker = None

        self.timer = self.create_timer(0.02, self.move)
        self.get_logger().info(f'Loaded {len(self.contours)} contours. Starting to draw...')

    def move(self):
        if self.contour_index >= len(self.contours):
            self.get_logger().info('Drawing complete!')
            self.marker_pub.publish(self.all_markers)
            return

        contour = self.contours[self.contour_index]

        if self.point_index == 0:
            # Start new marker for this contour
            self.current_marker = Marker()
            self.current_marker.header.frame_id = 'base_link'
            self.current_marker.header.stamp = self.get_clock().now().to_msg()
            self.current_marker.ns = 'drawing'
            self.current_marker.id = self.marker_id
            self.marker_id += 1
            self.current_marker.type = Marker.LINE_STRIP
            self.current_marker.action = Marker.ADD
            self.current_marker.scale.x = 0.008
            self.current_marker.color.r = 1.0
            self.current_marker.color.g = 0.0
            self.current_marker.color.b = 0.0
            self.current_marker.color.a = 1.0
            self.current_marker.lifetime.sec = 0
            self.all_markers.markers.append(self.current_marker)

        if self.point_index >= len(contour):
            # Move to next contour
            self.publish_point(0.0, 0.0)
            self.contour_index += 1
            self.point_index = 0
            return

        x, y = contour[self.point_index]
        self.publish_point(x, y)

        # Add point to current marker in real time
        p = Point()
        p.x = x
        p.y = y
        p.z = 0.0
        self.current_marker.points.append(p)
        self.current_marker.header.stamp = self.get_clock().now().to_msg()

        # Publish all markers every frame
        self.marker_pub.publish(self.all_markers)
        self.point_index += 1

    def publish_point(self, x, y):
        self.joint_state.header.stamp = self.get_clock().now().to_msg()
        self.joint_state.position = [x, y]
        self.pub.publish(self.joint_state)

def main(args=None):
    rclpy.init(args=args)
    if len(sys.argv) < 2:
        print("Usage: ros2 run drawing_robot_controller image_draw_controller <image_path>")
        return
    node = ImageDrawController(sys.argv[1])
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

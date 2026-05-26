import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time

class DrawingRobot(Node):
    def __init__(self):
        super().__init__('drawing_robot')
        self.x_pub = self.create_publisher(Float64, '/x_joint_position_controller/commands', 10)
        self.y_pub = self.create_publisher(Float64, '/y_joint_position_controller/commands', 10)

    def move_to(self, x, y):
        self.x_pub.publish(Float64(data=x))
        self.y_pub.publish(Float64(data=y))
        time.sleep(0.5)  # slows movement so you can see it

def main():
    rclpy.init()
    robot = DrawingRobot()

    # Example path: a square
    square_path = [
        (0.0, 0.0),
        (0.1, 0.0),
        (0.1, 0.1),
        (0.0, 0.1),
        (0.0, 0.0)
    ]

    for point in square_path:
        robot.move_to(point[0], point[1])

    rclpy.shutdown()

if __name__ == "__main__":
    main()

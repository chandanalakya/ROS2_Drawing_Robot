#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

```
package_name = 'drawing_robot_description'

urdf_file = os.path.join(
    get_package_share_directory(package_name),
    'urdf',
    'drawing_robot.urdf'
)

with open(urdf_file, 'r') as infp:
    robot_description = infp.read()

return LaunchDescription([

    Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description
        }]
    ),

    Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    ),

    Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

])
```

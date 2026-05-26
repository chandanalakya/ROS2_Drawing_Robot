from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    # --- Gazebo with ROS Factory Plugin ---
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    world_file = '/usr/share/gazebo-11/worlds/empty.world'

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={
            'world': world_file,
            'verbose': 'true'
        }.items()
    )

    # --- Robot State Publisher ---
    pkg_robot = get_package_share_directory('drawing_robot_description')
    urdf_file = os.path.join(pkg_robot, 'urdf', 'drawing_robot.urdf')
    with open(urdf_file, 'r') as f:
        robot_desc = f.read()

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc}],
        output='screen'
    )

    # --- Spawn Robot after 3s delay ---
    spawn_robot = TimerAction(
        period=3.0,
        actions=[Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-topic', 'robot_description',
                '-entity', 'drawing_robot',
                '-x', '0', '-y', '0', '-z', '0.05'
            ],
            output='screen'
        )]
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot
    ])

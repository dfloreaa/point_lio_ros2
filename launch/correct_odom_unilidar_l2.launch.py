from launch import LaunchDescription
from launch.actions import GroupAction, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Node parameters, including those from the YAML configuration file
    laser_mapping_params = [
        PathJoinSubstitution([
            FindPackageShare('point_lio'),
            'config', 'unilidar_l2.yaml'
        ]),
        {
            'use_imu_as_input': False,  # Change to True to use IMU as input of Point-LIO
            'prop_at_freq_of_imu': True,
            'check_satu': True,
            'init_map_size': 10,
            'point_filter_num': 1,  # Options: 1, 3
            'space_down_sample': True,
            'filter_size_surf': 0.1,  # Options: 0.5, 0.3, 0.2, 0.15, 0.1
            'filter_size_map': 0.1,  # Options: 0.5, 0.3, 0.15, 0.1
            'cube_side_length': 1000.0,  # Option: 1000
            'runtime_pos_log_enable': False,  # Option: True
            'odom_only': True, # Option: False
            'odom_header_frame_id': "odom",     # Default: "camera_init"
            'odom_child_frame_id': "base_link", # Default: "aft_mapped"
        }
    ]

    # Node definition for laserMapping with Point-LIO
    laser_mapping_node = Node(
        package='point_lio',
        executable='pointlio_mapping',
        name='laserMapping',
        output='screen',
        parameters=laser_mapping_params,
        # prefix='gdb -ex run --args'
    )

    # Assemble the launch description
    ld = LaunchDescription([
        laser_mapping_node,
    ])

    return ld

# Point-LIO-ROS2 (with Unitree Unilidar L1/L2 support)
## Point-LIO: Robust High-Bandwidth Lidar-Inertial Odometry

*(Pay attention to modifying the parameters for IMU in .yaml file, according to the IMU you use.)*

ROS2 port of [Point-LIO](https://github.com/hku-mars/Point-LIO) with support for the Unitree Unilidar L1/L2 as implemented on the ROS1 [point_lio_unilidar](https://github.com/unitreerobotics/point_lio_unilidar) package.

## 1. Introduction

`Point-LIO` is a robust and high-bandwidth lidar inertial odometry (LIO) with the capability to provide accurate, high-frequency odometry and reliable mapping under severe vibrations and aggressive motions. If you need further information about the `Point-LIO` algorithm, you can refer to their official website and paper:
- <https://github.com/hku-mars/Point-LIO>
- [Point‐LIO: Robust High‐Bandwidth Light Detection and Ranging Inertial Odometry](https://onlinelibrary.wiley.com/doi/epdf/10.1002/aisy.202200459)

<div align="center">
    <div align="center">
        <img src="https://github.com/hku-mars/Point-LIO/raw/master/image/toc4.png" width = 75% >
    </div>
    <font color=#a0a0a0 size=2>The framework and key points of the Point-LIO.</font>
</div>

<br>

The codes of this repo are contributed by:
[Dongjiao He (贺东娇)](https://github.com/Joanna-HE) and [Wei Xu (徐威)](https://github.com/XW-HKU) as well as [Daniel Florea](https://github.com/dfloreaa) for the ROS2 port and Unitree LiDAR support.

**Important notes:**

A. Please make sure the IMU and LiDAR are **Synchronized**, that's important.

B. Please obtain the saturation values of your used IMU (i.e., accelerator and gyroscope), and the units of the accelerator of your used IMU, then modify the .yaml file according to those settings, including values of 'satu_acc', 'satu_gyro', 'acc_norm'. That's improtant.

C. The warning message "Failed to find match for field 'time'." means the timestamps of each LiDAR points are missed in the rosbag file. That is important because Point-LIO processes at the sampling time of each LiDAR point.

D. We recommend to set the **extrinsic_est_en** to false if the extrinsic is given. As for the extrinsic initiallization, please refer to our recent work: [**Robust and Online LiDAR-inertial Initialization**](https://github.com/hku-mars/LiDAR_IMU_Init).

E. If a high odometry output frequency without downsample is required, set `publish_odometry_without_downsample` as true. Then the warning message of tf `"TF_REPEATED_DATA"` will pop up in the terminal window, because the time interval between two publish odometery is too small. The following command could be used to suppress this warning to a smaller frequency:

in your `catkin_ws/src`,

```bash
git clone --branch throttle-tf-repeated-data-error git@github.com:BadgerTechnologies/geometry2.git
```

Then rebuild, source `setup.bash`, run and then it should be reduced down to once every 10 seconds. If 10 seconds is still too much log output then change the ros::Duration(10.0) to 10000 seconds or whatever you like.

F. If you want to use Point-LIO without imu, set the `"imu_en"` as false, and provide a predefined value of gavity in `"gravity_init"` as true as possible in the yaml file, and keep the `"use_imu_as_input"` as 0.

## **2. Videos**
An set of accompaning videos are available on **YouTube**.
### 2.1 Point-LIO original demo
Original video demostration, straight from the original repo
<div align="center">
    <a href="https://youtu.be/oS83xUs42Uw" target="_blank"><img src="https://github.com/hku-mars/Point-LIO/raw/master/image/final.png" width=60% /></a>
</div>

### 2.2 L1 LiDAR
Official demo by Unitree using their [`point_lio_unilidar`](https://github.com/unitreerobotics/point_lio_unilidar) implementation for the L1 LiDAR:
<div align="center">
    <a href="https://oss-global-cdn.unitree.com/static/c0bd0ac7d1e147e7a7eaf909f1fc214f.mp4" target="_blank"><img src="https://github.com/unitreerobotics/point_lio_unilidar/raw/main/doc/video.png" width=60% /></a>
</div>

### 2.3 L2 LiDAR
Official demo by Unitree using their [`point_lio_unilidar`](https://github.com/unitreerobotics/point_lio_unilidar) implementation for the L2 LiDAR:
<div align="center">
    <a href="https://youtu.be/juAfGrg2xBg?si=IVTWM9shEmHsKKJ_" target="_blank"><img src="https://github.com/unitreerobotics/point_lio_unilidar/raw/main/doc/l2-demo-video-bilibili.png" width=60% /></a>
</div>

## **3. Prerequisites**

### **3.1 Ubuntu and [ROS](https://www.ros.org/)**
We tested our code on Ubuntu 22.04 with Humble. Other versions may have problems of environments to support the Point-LIO, try to avoid using Point-LIO in those systems.

Additional ROS package is required:

- For ROS2 Humble:
    ```bash
    sudo apt-get install ros-humble-pcl-ros
    sudo apt-get install ros-humble-pcl-conversions
    sudo apt-get install ros-humble-visualization-msgs
    ```

### **3.2 Eigen**
Following the official [Eigen installation](eigen.tuxfamily.org/index.php?title=Main_Page), or directly install Eigen by:
```bash
sudo apt-get install libeigen3-dev
```

### **3.3 `livox_ros_driver2`**
Follow [livox_ros_driver2 Installation](https://github.com/Livox-SDK/livox_ros_driver2).

*Remarks:*
- Since the Point-LIO supports Livox serials LiDAR, so the **livox_ros_driver2** must be installed and **sourced** before run any Point-LIO launch file.
- How to source? The easiest way is add the line ``` source $Licox_ros_driver_dir$/install/setup.bash ``` to the end of file ``` ~/.bashrc ```, where ``` $Licox_ros_driver_dir$ ``` is the directory of the livox ros driver workspace (should be the ``` ws_livox ``` directory if you completely followed the livox official document).

### 3.4 `unilidar_sdk`

For using lidar `L1`, you should download and build [unilidar_sdk](https://github.com/unitreerobotics/unilidar_sdk) follwing these steps:

```bash
git clone https://github.com/unitreerobotics/unilidar_sdk.git

cd unilidar_sdk/unitree_lidar_ros2

colcon build
```

### 3.5 `unilidar_sdk2`

For using lidar `L2`, you should download and build [unilidar_sdk2](https://github.com/unitreerobotics/unilidar_sdk2) follwing these steps:

```bash
git clone https://github.com/unitreerobotics/unilidar_sdk2.git

cd unilidar_sdk/unitree_lidar_ros2

colcon build
```

## 4. Build
Clone the repository and colcon build:

```bash
    mkdir -p catkin_point_lio_unilidar/src
    cd catkin_point_lio_unilidar/src
    git clone https://github.com/dfloreaa/point_lio_ros2.git
    cd ..
    colcon build --symlink-install
    source install/setup.bash
```
- Remember to source the livox_ros_driver before build (follow 3.3 `livox_ros_driver2`)
- If you want to use a custom build of PCL, add the following line to ~/.bashrc
```export PCL_ROOT={CUSTOM_PCL_PATH}```

## 5. Directly run

### 5.1 For Avia
Connect to your PC to Livox Avia LiDAR by following  [Livox-ros-driver installation](https://github.com/Livox-SDK/livox_ros_driver), then
```
    cd ~/$Point_LIO_ROS_DIR$
    source install/setup.bash
    ros2 launch point_lio mapping_avia.launch.py
    ros2 launch livox_ros_driver msg_HAP_launch.py
```
- For livox serials, Point-LIO only support the data collected by the ``` msg_HAP_launch.py ``` since only its ``` livox_ros_driver/CustomMsg ``` data structure produces the timestamp of each LiDAR point which is very important for Point-LIO. ``` livox_lidar.launch.py ``` can not produce it right now.
- If you want to change the frame rate, please modify the **publish_freq** parameter in the [msg_HAP_launch.py](https://github.com/Livox-SDK/livox_ros_driver2/blob/master/launch_ROS2/msg_HAP_launch.py) of [Livox-ros-driver](https://github.com/Livox-SDK/livox_ros_driver) before make the livox_ros_driver pakage.

### 5.2 For Livox serials with external IMU

mapping_avia.launch theratically supports mid-70, mid-40 or other livox serial LiDAR, but need to setup some parameters befor run:

Edit ``` config/avia.yaml ``` to set the below parameters:

1. LiDAR point cloud topic name: ``` lid_topic ```
2. IMU topic name: ``` imu_topic ```
3. Translational extrinsic: ``` extrinsic_T ```
4. Rotational extrinsic: ``` extrinsic_R ``` (only support rotation matrix)
- The extrinsic parameters in Point-LIO is defined as the LiDAR's pose (position and rotation matrix) in IMU body frame (i.e. the IMU is the base frame). They can be found in the official manual.
5. Saturation value of IMU's accelerator and gyroscope: ```satu_acc```, ```satu_gyro```
6. The norm of IMU's acceleration according to unit of acceleration messages: ``` acc_norm ```

### 5.3 For Velodyne or Ouster (Velodyne as an example)

Step A: Setup before run

Edit ``` config/velodyne.yaml ``` to set the below parameters:

1. LiDAR point cloud topic name: ``` lid_topic ```
2. IMU topic name: ``` imu_topic ``` (both internal and external, 6-aixes or 9-axies are fine)
3. Set the parameter ```timestamp_unit``` based on the unit of **time** (Velodyne) or **t** (Ouster) field in PoindCloud2 rostopic
4. Line number (we tested 16, 32 and 64 line, but not tested 128 or above): ``` scan_line ```
5. Translational extrinsic: ``` extrinsic_T ```
6. Rotational extrinsic: ``` extrinsic_R ``` (only support rotation matrix)
- The extrinsic parameters in Point-LIO is defined as the LiDAR's pose (position and rotation matrix) in IMU body frame (i.e. the IMU is the base frame).
7. Saturation value of IMU's accelerator and gyroscope: ```satu_acc```, ```satu_gyro```
8. The norm of IMU's acceleration according to unit of acceleration messages: ``` acc_norm ```

Step B: Run below
```
    cd ~/$Point_LIO_ROS_DIR$
    source install/setup.bash
    ros2 launch point_lio mapping_velody16.launch.py
```

Step C: Run LiDAR's ros driver or play rosbag.

### 5.4 For Unitree LiDAR (L1 as an example)

Step A: Run below
```
    cd ~/catkin_point_lio_unilidar
    source install/setup.bash
    ros2 launch point_lio mapping_unilidar_l1.py
```

Step B: Run LiDAR's ros driver or play rosbag.

### 5.5 PCD file save

Set ``` pcd_save_enable ``` in launchfile to ``` 1 ```. All the scans (in global frame) will be accumulated and saved to the file ``` Point-LIO/PCD/scans.pcd ``` after the Point-LIO is terminated. ```pcl_viewer scans.pcd``` can visualize the point clouds.

*Tips for pcl_viewer:*
- change what to visualize/color by pressing keyboard 1,2,3,4,5 when pcl_viewer is running. 
```
    1 is all random
    2 is X values
    3 is Y values
    4 is Z values
    5 is intensity
```

# **6. Examples**

The example datasets could be downloaded through [onedrive](https://connecthkuhk-my.sharepoint.com/:f:/g/personal/hdj65822_connect_hku_hk/EmRJYy4ZfAlMiIJ786ogCPoBcGQ2BAchuXjE5oJQjrQu0Q?e=igu44W). Pay attention that if you want to test on racing_drone.bag, [0.0, 9.810, 0.0] should be input in 'mapping/gravity_init' in avia.yaml, and set the 'start_in_aggressive_motion' as true in the yaml. Because this bag start from a high speed motion. And for PULSAR.bag, we change the measuring range of the gyroscope of the built-in IMU to 17.5 rad/s. Therefore, when you test on this bag, please change 'satu_gyro' to 17.5 in avia.yaml.

## **6.1. Example-1: SLAM on datasets with aggressive motions where IMU is saturated**
<div align="center">
<img src="https://github.com/hku-mars/Point-LIO/raw/master/image/example1.gif"  width="40%" />
<img src="https://github.com/hku-mars/Point-LIO/raw/master/image/example2.gif"  width="54%" />
</div>

## **6.2. Example-2: Application on FPV and PULSAR**
<div align="center">
<img src="https://github.com/hku-mars/Point-LIO/raw/master/image/example3.gif"  width="58%" />
<img src="https://github.com/hku-mars/Point-LIO/raw/master/image/example4.gif"  width="35%" />
</div>

PULSAR is a self-rotating UAV actuated by only one motor, [PULSAR](https://github.com/hku-mars/PULSAR)

## 7. Contact us
If you have any questions about this work, please feel free to contact me <dflorea@uc.cl> via email.

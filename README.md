## Setup
Install Ubuntu and ROS according to these instructions (skip network configuration): https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/    
(On the HK computers, this will have been done ahead of time)   

At a convenient location in the file system (for example in the home directory), create a new catkin workspace by entering the following terminal commands   
`mkdir -p catkin_ws/src`   
`cd catkin_ws/`   
`catkin_make`   

Create your own fork of this repository (instructions on ho to do this: https://docs.github.com/en/github/getting-started-with-github/fork-a-repo)   
Move to the newly created src directory and clone your fork of the repository   
`cd src`   
`git clone url-to-your-fork-of-the-repo/hk_ros_2021.git`   

Then move back up to the workspace root and build   
`cd ..`   
`catkin_make`   


## Test

Download the folder of test rosbags from (insert box link here) and save at a convenient location (not in a .git repository because git does not like large binary files)   

In a terminal, run   
`roslaunch hk_ros_2021 hk_ros_2021.launch`   
This will start a new Rviz window.   

In a second terminal, `cd` to the directory where you downloaded the bagfile and run   
`rosbag play --clock name-of-bagfile.bag`   
Now the Rviz window will start visualizing sensor data.   


## Moving forward from here

hk_ros_2021.launch is a skeleton launch file that in its initial form will only run some preprocessing of sensor data, and launch rviz. The idea here is that you sequentially add launch commands for downloaded and custom written nodes to this launch file to build your solution to the task.   

Hint 1: The comments in hk_ros_2021.launch will give you an idea of what nodes you need to add. Also, notice that some markers in the Rviz configuration are not getting data ("SLAM map and tag detections") this gives you an indication about which nodes you may want to add to your .launch file   

Hint 2: Your april tag detector needs to be configured to look for the specific tags we used when setting up the task. For this purpose we have provided the detector setting files in "hk_ros_2021/april_tag_detector_config"   

## Various Tips and tricks
* Terminator - alternative terminal emulator that is convenient when working with multiple terminal windows
* copy and paste does work to and from terminal windows. Just hit shift + ctrl instead of just ctrl

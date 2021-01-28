#!/usr/bin/env python2

# Example how to generate the output file

import yaml
import rospkg

# 1 create an empty list to store the detections
detections = []

# 2 append detections during the run
# remember to add logic to avoid duplicates

# first dummy detection (apriltag)
detections.append({"obj_type": "A", "XY_pos": [0.756,3.332]})

# second dummy detection (geometric shape)
detections.append({"obj_type": "B", "XY_pos": [3.396,0.123]})

# third dummy detection (animal)
detections.append({"obj_type": "C", "XY_pos": [6.001,2.987]})   
    
# 3 save the file
filename = "latest_output_file.yaml"
filepath = rospkg.RosPack().get_path('hk_ros_2021') + '/exported_detection_logs/' 

with open(filepath + filename, 'w') as outfile:
    yaml.dump_all(detections, outfile,explicit_start=True)

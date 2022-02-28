#!/usr/bin/env python
import os
import sys
import time
from subprocess import Popen, PIPE, STDOUT

data_array = ["","","","","",""]
i = 0
script_path = os.path.join("/home/student/catkin_ws/src/it_project/src/camera_subscriber.py")
p = Popen([sys.executable, '-u', script_path],
          stdout=PIPE, stderr=STDOUT, bufsize=1)
with p.stdout:
    for line in iter(p.stdout.readline, ''):
        i = i + 1
        input_string = str(line)
        input_string = input_string[2:]
        input_string = input_string[:-3]
        input_string = input_string + "\n"

        print(input_string)

        if "tag=ipcam_1" in input_string:
            data_array[0] = input_string
        elif "tag=ipcam_2" in input_string:
            data_array[1] = input_string
        elif "tag=ipcam_3" in input_string:
            data_array[2] = input_string
        elif "tag=ipcam_4" in input_string:
            data_array[3] = input_string
        elif "tag=ipcam_5" in input_string:
            data_array[4] = input_string
        elif "tag=robotcam" in input_string:
            data_array[5] = input_string

        if i == 20:
            i = 0
            print("Writing to file")
            datafile = open("datafiles/ip_cam_data", "w")
            datafile.writelines(data_array)
            datafile.close()
            time.sleep(4)

p.wait()

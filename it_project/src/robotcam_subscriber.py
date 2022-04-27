#!/usr/bin/env python

import cv2
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import multiprocessing
from PIL import Image
import sys

# Daten zur Initialisierung von Influx
token = "9G91tixjWebo4IJtglvai5DpIorw7jy8UXk-CplP7TkR_-D2wJ6Dfqm5PkS6mw5kIzZxc_-T3RNsjaEz0rLW6Q=="
org = "Hochschule-Stralsund"
bucket = "Data-Monitoring"

client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)


prev_frame_time_robot_cam = 0

def robot_cam():

    try:
        cv2_robot_cam = cv2.VideoCapture("http://0.0.0.0:8080/stream?topic=/robot_1/cv_camera/image_raw")
        global prev_frame_time_robot_cam

        while (True):
            ret, frame = cv2_robot_cam.read()

            new_frame_time_robot_cam = time.time()
            fps = 1 / (new_frame_time_robot_cam - prev_frame_time_robot_cam)
            prev_frame_time_robot_cam = new_frame_time_robot_cam

            fps = fps * 6
            fps = str(fps)[:4]

            # Schreibt die Bilddatei ins Lokale System und ruft sie danach auf um die größe zu berechnen
            file = '/home/student/Pictures/robot_%s_cam_image.jpeg' % (sys.argv[1])
            cv2.imwrite(file, frame)
            size = os.path.getsize(file) / 1000
            im = Image.open(file)
            width, height = im.size
            im.close()

            data = "robotcamera,tag=robot_%s fps=" % (sys.argv[1]) + str(fps) + ",size=" + str(size) + ",height=" + str(height) + ",width=" +str(width)
            write_api.write(bucket, org, data)

            time.sleep(1)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
    except:
        # if any error occurs then this block of code will run
        print("RobotCam Video-Source not found..")

def save_map_data():
    time.sleep(3)
    try:
        while(True):
            print("saving map")
            os.system('rosrun map_server map_saver -f /home/student/catkin_ws/src/it_project/maps/robot_%s_map __ns:=robot_%s' % (sys.argv[1], sys.argv[1]))
            new_file = "{}.jpeg".format("/home/student/catkin_ws/maps/robot_%s_map_jpeg" % (sys.argv[1]))
            with Image.open("/home/student/catkin_ws/maps/robot_%s_map.pgm" % (sys.argv[1])) as im:
                im.save(new_file)
            os.system('cp /home/student/catkin_ws/src/it_project/maps/robot_%s_map_jpeg.jpeg /home/student/catkin_ws/src/it_project/src/datafiles/robot_%s_map_jpeg.jpeg' % (sys.argv[1], sys.argv[1]))
            time.sleep(2)
    except KeyboardInterrupt:
        pass



if __name__ == '__main__':
    process_1 = multiprocessing.Process(target=robot_cam)
    process_1.start()

    process_2 = multiprocessing.Process(target=save_map_data)
    process_2
    .start()

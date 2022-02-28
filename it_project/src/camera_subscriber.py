
#!/usr/bin/env python

import cv2
import time
import os
import multiprocessing
from PIL import Image


# Globale Variablen für den FPS berechnung
prev_frame_time_ip_cam_1 = 0
prev_frame_time_ip_cam_2 = 0
prev_frame_time_ip_cam_3 = 0
prev_frame_time_ip_cam_4 = 0
prev_frame_time_ip_cam_5 = 0

new_frame_time_robot_cam = 0

# Methode zum berechnen der FPS, Bilddateigröße, Höhe und Breite der Roboter Cam welche über die angegebene IP-Adresse
# erreicht werden kann, sobald der Ros-Webvideo-Server gestartet wurde Befehl:"rosrun web_video_server web_video_server"

def ip_cam_1():

    try:
        cv2_robot_cam = cv2.VideoCapture("rtsp://root:AxisDistLab21@192.168.50.160:554/axis-media/media.amp")
        global prev_frame_time_ip_cam_1

        while (True):
            ret, frame = cv2_robot_cam.read()

            new_frame_time_ip_cam_1 = time.time()
            fps = 1 / (new_frame_time_ip_cam_1 - prev_frame_time_ip_cam_1)
            prev_frame_time_ip_cam_1 = new_frame_time_ip_cam_1

            fps = str(fps)[:4]

            # Schreibt die Bilddatei ins Lokale System und ruft sie danach auf um die größe zu berechnen
            file = '/home/student/Pictures/ipcam_1.jpeg'
            cv2.imwrite(file, frame)
            size = os.path.getsize(file) / 1000
            im = Image.open(file)
            width, height = im.size
            im.close()

            print('ipcamera,tag=ipcam_1 fps=%s,size=%s,height=%s,width=%s' % (fps, size, height, width))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
    except:
        # if any error occurs then this block of code will run
        print("IPCam_1 Video-Source not found..")

def ip_cam_2():

    try:
        cv2_robot_cam = cv2.VideoCapture("rtsp://root:AxisDistLab21@192.168.50.160:554/axis-media/media.amp")
        global prev_frame_time_ip_cam_2

        while (True):
            ret, frame = cv2_robot_cam.read()

            new_frame_time_ip_cam_2 = time.time()
            fps = 1 / (new_frame_time_ip_cam_2 - prev_frame_time_ip_cam_2)
            prev_frame_time_ip_cam_2 = new_frame_time_ip_cam_2

            fps = str(fps)[:4]

            # Schreibt die Bilddatei ins Lokale System und ruft sie danach auf um die größe zu berechnen
            file = '/home/student/Pictures/ipcam_2.jpeg'
            cv2.imwrite(file, frame)
            size = os.path.getsize(file) / 1000
            im = Image.open(file)
            width, height = im.size
            im.close()

            print('ipcamera,tag=ipcam_2 fps=%s,size=%s,height=%s,width=%s' % (fps, size, height, width))


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
    except:
        # if any error occurs then this block of code will run
        print("IPCam_2 Video-Source not found..")

def ip_cam_3():

    try:
        cv2_robot_cam = cv2.VideoCapture("rtsp://root:AxisDistLab21@192.168.50.160:554/axis-media/media.amp")
        global prev_frame_time_ip_cam_3

        while (True):
            ret, frame = cv2_robot_cam.read()

            new_frame_time_ip_cam_3 = time.time()
            fps = 1 / (new_frame_time_ip_cam_3 - prev_frame_time_ip_cam_3)
            prev_frame_time_ip_cam_3 = new_frame_time_ip_cam_3

            fps = str(fps)[:4]

            # Schreibt die Bilddatei ins Lokale System und ruft sie danach auf um die größe zu berechnen
            file = '/home/student/Pictures/ipcam_3.jpeg'
            cv2.imwrite(file, frame)
            size = os.path.getsize(file) / 1000
            im = Image.open(file)
            width, height = im.size
            im.close()

            print('ipcamera,tag=ipcam_3 fps=%s,size=%s,height=%s,width=%s' % (fps, size, height, width))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
    except:
        # if any error occurs then this block of code will run
        print("IPCam_3 Video-Source not found..")


def ip_cam_4():

    try:
        cv2_robot_cam = cv2.VideoCapture("rtsp://root:AxisDistLab21@192.168.50.160:554/axis-media/media.amp")
        global prev_frame_time_ip_cam_4

        while (True):
            ret, frame = cv2_robot_cam.read()

            new_frame_time_ip_cam_4 = time.time()
            fps = 1 / (new_frame_time_ip_cam_4 - prev_frame_time_ip_cam_4)
            prev_frame_time_ip_cam_4 = new_frame_time_ip_cam_4

            fps = str(fps)[:4]

            # Schreibt die Bilddatei ins Lokale System und ruft sie danach auf um die größe zu berechnen
            file = '/home/student/Pictures/ipcam_4.jpeg'
            cv2.imwrite(file, frame)
            size = os.path.getsize(file) / 1000
            im = Image.open(file)
            width, height = im.size
            im.close()

            print('ipcamera,tag=ipcam_4 fps=%s,size=%s,height=%s,width=%s' % (fps, size, height, width))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
    except:
        # if any error occurs then this block of code will run
        print("IPCam_4 Video-Source not found..")

def ip_cam_5():

    try:
        cv2_robot_cam = cv2.VideoCapture("rtsp://root:AxisDistLab21@192.168.50.160:554/axis-media/media.amp")
        global prev_frame_time_ip_cam_5

        while (True):
            ret, frame = cv2_robot_cam.read()

            new_frame_time_ip_cam_5 = time.time()
            fps = 1 / (new_frame_time_ip_cam_5 - prev_frame_time_ip_cam_5)
            prev_frame_time_ip_cam_5 = new_frame_time_ip_cam_5

            fps = str(fps)[:4]

            # Schreibt die Bilddatei ins Lokale System und ruft sie danach auf um die größe zu berechnen
            file = '/home/student/Pictures/ipcam_5.jpeg'
            cv2.imwrite(file, frame)
            size = os.path.getsize(file) / 1000
            im = Image.open(file)
            width, height = im.size
            im.close()


            print('ipcamera,tag=ipcam_5 fps=%s,size=%s,height=%s,width=%s' % (fps, size, height, width))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
    except:
        # if any error occurs then this block of code will run
        print("IPCam_5 Video-Source not found..")


# Aufruf der verschiedenen Prozesse, über Multiprocessing können die Daten von verschiedenen Methoden gelichzeitig
# verarbeitet werden
if __name__ == '__main__':

    queue = multiprocessing.Queue()

    process_1 = multiprocessing.Process(target=ip_cam_1)
    process_1.start()

    process_2 = multiprocessing.Process(target=ip_cam_2)
    process_2.start()

    process_3 = multiprocessing.Process(target=ip_cam_3)
    process_3.start()

    process_4 = multiprocessing.Process(target=ip_cam_4)
    process_4.start()

    process_5 = multiprocessing.Process(target=ip_cam_5)
    process_5.start()

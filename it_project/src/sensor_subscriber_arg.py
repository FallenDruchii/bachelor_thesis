#! /usr/bin/python
import os
import time

import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import LaserScan, BatteryState
from nav_msgs.msg import Odometry
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import math
from geometry_msgs.msg import Twist
import sys

# Daten zur Initialisierung von Influx
token = "9G91tixjWebo4IJtglvai5DpIorw7jy8UXk-CplP7TkR_-D2wJ6Dfqm5PkS6mw5kIzZxc_-T3RNsjaEz0rLW6Q=="
org = "Hochschule-Stralsund"
bucket = "Data-Monitoring"

client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Globale Variablen
total_distance = 0
prev_x_dist = 0
prev_y_dist = 0
prev_x_dist_2 = 0
prev_y_dist_2 = 0


# Methode zur Erstellung des Laserscan Koordinatensystems, hierbei werden alle Laserdaten eingelesen, je nach Position
# 0-359 wird es dann verarbeitet, über Trigonometrie wird die Position des Laserscan-Punktes berechnet und in X-Y
# Koordinaten ausgegeben. X-Y Daten werden mit Position in die Data-Datei geschrieben um vom Telegraf Agenten ausgelesen zu werden
def callback_Laserscan(msg):
    try:
        datafile = open("/home/student/catkin_ws/src/it_project/src/datafiles/robot_%s_laserscan" % (sys.argv[1]), "r")
        list_of_lines = datafile.readlines()
    except:
        print("Please copy datafile in it_project/src/data")

    # Entfernung und kleinster WInkel, ranges array 360 Werte, jeder Wert = 1 Grad
    for i in range(360):

        num = i

        if msg.ranges[i] < 10:

            # i entspricht dem Winkel 0-359
            distance = msg.ranges[i]  # Laserscan gemessene Entfernung

            # Berechnet ueber Trigonemetrie die Position des Objekts, a und b stellen die X,Y in einem Kooord. System dar
            # Quadrant zeigt in Welchem Quadranten sich das Objekt im Koord. System relativ zum Roboter befindet
            # Falls Winkel Zwischen 90 und 180 Grad liegt
            if 180 >= i > 90:
                radiant = math.pi / 180 * (180 - i)
                x = distance * math.cos(radiant)
                y = distance * math.sin(radiant)
                x = -x
            # Falls Winkel zwischen 180 und 270 Grad liegt
            elif 270 >= i > 180:
                radiant = math.pi / 180 * (270 - (i - 90))
                x = distance * math.cos(radiant)
                y = distance * math.sin(radiant)
                y = -y
            # Falls Winkel zwischen 270 und 360 Grad liegt
            elif 360 >= i > 270:
                radiant = math.pi / 180 * (360 - (i - 180))
                x = distance * math.cos(radiant)
                y = distance * math.sin(radiant)
                x = -x
            # Falls Winkel 0, 90, 180, 270 oder 360 Grad ist
            elif i == 0 | 90 | 180 | 270 | 360:
                if i == 0 | 360:
                    x = 0
                    y = distance
                    quadrant = 2
                elif i == 90:
                    x = -distance
                    y = 0
                    quadrant = 3
                elif i == 180:
                    x = 0
                    y = -distance
                    quadrant = 4
                elif i == 270:
                    x = distance
                    y = 0
                    quadrant = 1
            # Falls Winkel zwischen 0 und 90 Grad liegt
            else:
                radiant = math.pi / 180 * i
                x = distance * math.cos(radiant)
                y = distance * math.sin(radiant)
        else:
            x = 0
            y = 0
        # X-Y Koordinaten werden auf 2 Nachkommastellen gerundet
        x_round = round(x, 2)
        y_round = round(y, 2)

        list_of_lines[i] = 'coordinates,tag=robot_%s,num=%s x=%s,y=%s \n' % (sys.argv[1], num, x_round, y_round)

    datafile = open("/home/student/catkin_ws/src/it_project/src/datafiles/robot_%s_laserscan" % (sys.argv[1]), "w")
    datafile.writelines(list_of_lines)
    datafile.close()


# Methode zur Erfassung der Odometrie Daten, hierbei werden die Momentane X-Y Position, der zurückgelegte Weg und
# mögliche Rotationen gespeichert und an Influx weitergegeben
def callback_Odom(msg):
    global total_distance
    global prev_x_dist
    global prev_y_dist
    global prev_x_dist_2
    global prev_y_dist_2

    # momentane X-Y Position des Odom-Topics
    x_dist = msg.pose.pose.position.x
    y_dist = msg.pose.pose.position.y

    # Berechnung zu unterschieden zu vorherigen Werten
    increase = math.sqrt(
        (x_dist - prev_x_dist) * (x_dist - prev_x_dist) + (y_dist - prev_y_dist) * (y_dist - prev_y_dist))
    total_distance = total_distance + increase
    prev_x_dist = x_dist
    prev_y_dist = y_dist

    # Rotationswerte des Odometrie-Topics
    x_orientation = msg.pose.pose.orientation.x
    y_orientation = msg.pose.pose.orientation.y
    z_orientation = msg.pose.pose.orientation.z
    w_orientation = msg.pose.pose.orientation.w

    # Berechnung der Rotation in Grad über Quaternition ->
    # https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
    t0 = +2.0 * (w_orientation * x_orientation + y_orientation * z_orientation)
    t1 = +1.0 - 2.0 * (x_orientation * x_orientation + y_orientation * y_orientation)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w_orientation * y_orientation - z_orientation * x_orientation)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w_orientation * z_orientation + x_orientation * y_orientation)
    t4 = +1.0 - 2.0 * (y_orientation * y_orientation + z_orientation * z_orientation)
    yaw_z = math.atan2(t3, t4)

    roll_x = math.degrees(roll_x)
    pitch_y = math.degrees(pitch_y)
    yaw_z = math.degrees(yaw_z)

    # Da es negative Werte geben kann müssen diese in Positive umgewandelt werden
    if (roll_x < 0):
        roll_x = 360 + roll_x
    if (pitch_y < 0):
        pitch_y = 360 + pitch_y
    if (yaw_z < 0):
        yaw_z_edit = abs(yaw_z)
    if (yaw_z > 0):
        yaw_z_edit = 360 - yaw_z

    data = "Odometry,tag=robot_%s xpos=" % (sys.argv[1]) + str(x_dist) + ",ypos=" + str(
        y_dist) + ",travelleddistance=" + str(total_distance)
    write_api.write(bucket, org, data)

    data = "Odometry,tag=robot_%s zorientation=" % (sys.argv[1]) + str(yaw_z_edit)
    write_api.write(bucket, org, data)


#    if x_dist - prev_x_dist_2 > 0.1 or prev_x_dist_2 - x_dist > 0.1 or y_dist - prev_y_dist_2 > 0.1 or prev_y_dist_2 - y_dist > 0.1:
#        data = "Odometry,tag=robot_%s xmappos=" % (sys.argv[1]) + str(x_dist) + ",ymappos=" + str(y_dist)
#        write_api.write(bucket, org, data)
#        prev_x_dist_2 = x_dist
#        prev_y_dist_2 = y_dist

# Methode zur Erfassung der Geschwindigkeitsdaten des Twist/cmdvel-Topics
def callback_Cmdvel(msg):
    # Lineare und Angulare Geschwindigkeiten, für unseren Roboter nur x_vel und z_ang_vel interessant, da der Roboter,
    # sich nicht anderweitig bewegen kann
    x_vel = msg.linear.x
    y_vel = msg.linear.y
    z_vel = msg.linear.z
    x_ang_vel = msg.angular.x
    y_ang_vel = msg.angular.y
    z_ang_vel = msg.angular.z

    data = "Velocity,tag=robot_%s x_velocity=" % (sys.argv[1]) + str(x_vel)
    write_api.write(bucket, org, data)
    data = "Velocity,tag=robot_%s z_velocity=" % (sys.argv[1]) + str(z_ang_vel)
    write_api.write(bucket, org, data)


def callback_Batterystate(msg):
    batterystate = msg.voltage
    data = "Batterystate,tag=robot_%s volageleft=" % (sys.argv[1]) + str(batterystate)
    write_api.write(bucket, org, data)


# Main Methode in welche die verschiedenen Subscriber der Topics definiert werden
def main():
    rospy.init_node('it_project_main_robot_%s' % (sys.argv[1]))
    # Subscriber mit den jeweiligen Callback Methoden
    rospy.Subscriber("/robot_%s/scan" % (sys.argv[1]), LaserScan, callback_Laserscan)
    rospy.Subscriber("/robot_%s/odom" % (sys.argv[1]), Odometry, callback_Odom)
    rospy.Subscriber("/robot_%s/cmd_vel" % (sys.argv[1]), Twist, callback_Cmdvel)
    rospy.Subscriber("/robot_%s/battery_state" % (sys.argv[1]), BatteryState, callback_Batterystate)

    # Spin until ctrl + c
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

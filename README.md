Projektdateien für die Bachelorarbeit

Im maps Ordner befinden sich die pgm-Dateien welche durch den Map-Server/Map-Saver erstellt wurden.
Im src Ordner befindet sich der Code für die Kamera, Sensor und IP-Kamera Skripte


Durchführung:

  - Start von Influx mittels "influxd"
  - Start von Roscore mittels "roscore"
  - Start der Restreamer Container falls diese nicht bereits laufen mittels "docker start restreamer_x" (1-5)
  - Start des Python-Servers mittels "python3 -m http.server
  - Start des Webvideo-Servers mittels "rosrun web_video_server web_video_server _port:=8888"
  - Start der Skripte mittels "python3 x y" x = Skriptname, y = Roboter Namespace -> 1-5
  - Start des Telegraf Agenten mittels "telegraf --config /home/student/Documents/telegraf.conf"

from lidar.MyLidarClass import MyLidar
from wifi_com.ServeurClass import Server
from flask import send_file, abort, jsonify, Response
from picamera2 import Picamera2
import os
import cv2
import numpy as np
import time

class Robot(Server):
    def __init__(self, LidarPort = '/dev/ttyUSB0'):
        super().__init__()
        self.lidar = MyLidar(LidarPort)
        self.picam2 = Picamera2() #Init de la cam
        self.picam2.configure(self.picam2.create_video_configuration(
        main={"size": (640, 480), "format": "RGB888"}
        ))
        self.picam2.start()

        self.run()
        
    def take_Lidar(self):
        data = self.lidar.getScanData(360, format=1)
        return jsonify(data.tolist())

    def take_picture(self):
        image_path = "/home/gp3/Desktop/Images/imageRequete.jpg"
        self.picam2.capture_file(image_path) #Prendre une photo

        image = cv2.imread(image_path) #Charger image avec OpenCV

        if image is not None:
            image_path = "/home/gp3/Desktop/Images/imageRequete.jpg"
            cv2.imwrite(image_path, image)

            # Retourner l'image pivotée
            return send_file(image_path, mimetype='image/jpg')
        else:
            return abort(404, description="Image non trouvée")       

    def generate_frames(self):
        while True:
            time.sleep(0.2)
            frame = self.picam2.capture_array()
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    
    def video_feed(self):
        return Response(self.generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':    
    # Création d'un client et récupération du message
    Robot = Robot(LidarPort = '/dev/ttyUSB0')
    print(f"Serveur démarré sur {Robot.host}:{Robot.port}")
    

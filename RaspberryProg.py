from lidar.MyLidarClass import MyLidar
from wifi_com.ServeurClass import Server
from flask import send_file, abort, jsonify
from picamera2 import Picamera2
import os
import cv2
import numpy as np

class Robot(Server):
    def __init__(self, LidarPort = '/dev/ttyUSB0'):
        super().__init__()
        self.lidar = MyLidar(LidarPort)
        self.picam2 = Picamera2() #Init de la cam
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
            rotated_image = cv2.rotate(image, cv2.ROTATE_180) #Et la faire tourner de 180°
            rotated_image_path = "/home/gp3/Desktop/Images/imageRequete_rotated.jpg"
            cv2.imwrite(rotated_image_path, rotated_image)

            # Retourner l'image pivotée
            return send_file(rotated_image_path, mimetype='image/jpg')
        else:
            return abort(404, description="Image non trouvée")       
        
    
    
if __name__ == '__main__':    
    # Création d'un client et récupération du message
    Robot = Robot(LidarPort = '/dev/ttyUSB0')
    print(f"Serveur démarré sur {Robot.host}:{Robot.port}")
    

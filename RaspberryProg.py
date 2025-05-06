from lidar.MyLidarClass import MyLidar
from wifi_com.ServeurClass import Server
import subprocess
import os


class Robot(Server):
    def __init__(self, LidarPort = '/dev/ttyUSB0'):
        super().__init__()
        self.lidar = MyLidar(LidarPort)
        self.run()
        
    def take_Lidar(self):
        data = self.lidar.getScanData(360, format=1)
        return jsonify(data.tolist())

    def take_picture(self):    
        image_path = "/home/gp3/Desktop/Images/imageRequete.jpg"
        #Prendre une photo
        subprocess. run(["libcamera-still","-o","/home/gp3/Desktop/Images/imageRequete.jpg"])
        
        if os.path.exists(image_path):
            return send_file(image_path, mimetype='image/jpg')
        else :
            return abort(404,description = "Image non trouvée")
        
        
    
    
if __name__ == '__main__':    
    # Création d'un client et récupération du message
    Robot = Robot(LidarPort = '/dev/ttyUSB0')
    print(f"Serveur démarré sur {Robot.host}:{Robot.port}")
    

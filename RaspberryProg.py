from lidar.MyLidarClass import MyLidar
from wifi_com.ServeurClass import Server

from flask import jsonify

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
        json_file_path = "/home/gp3/Desktop/Images/image_data.json"
        #Prendre une photo
        subprocess. run(["libcamera-still","-o","/home/gp3/Desktop/Images/imageRequete.jpg"])
        # Ouvrir l'image
        with Image.open(image_path) as img:
            # Convertir l'image en bytes
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_bytes = buffered.getvalue()
        # Convertir les bytes en base64
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        # Créer un dictionnaire avec les informations de l'image
        image_data = {
            "image": img_base64,
            "format": "JPEG",
            "width": img.width,
            "height": img.height
        }
        # Sauvegarder dans un fichier JSON
        with open(json_file_path, "w") as json_file:
            json.dump(image_data, json_file, indent=4)
   
        
    
    
if __name__ == '__main__':    
    # Création d'un client et récupération du message
    Robot = Robot(LidarPort = '/dev/ttyUSB0')
    print(f"Serveur démarré sur {Robot.host}:{Robot.port}")
    

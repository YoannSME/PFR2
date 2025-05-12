from flask import Flask

"""
Date : 28 mars 2025
Auteur : Axel Sichi
Classe Server qui crée un serveur Flask simple pour répondre à deux endpoints : 
- `/take_picture` pour prendre une photo
- `/take_Lidar` pour prendre un scan Lidar

Attributs:
- app : Flask - L'application Flask pour gérer les requêtes HTTP.
- host : str - L'adresse IP sur laquelle le serveur écoute (par défaut '0.0.0.0').
- port : int - Le port sur lequel le serveur écoute (par défaut 5000).

Méthodes:
- take_picture(self) : Retourne la photo qui a été prise.
- take_Lidar(self) : Retourne le scan Lidar qui a été effectué.
- run(self) : Démarre le serveur Flask pour commencer à écouter les requêtes.
"""

class Server:
    def __init__(self, host='0.0.0.0', port=5000):
        # Initialisation de l'application Flask
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        # Définir la route pour envoyer un message
        self.app.add_url_rule('/take_picture', 'take_picture', self.take_picture)
        self.app.add_url_rule('/take_Lidar', 'take_Lidar', self.take_Lidar)
        self.app.add_url_rule('/video_feed', 'video_feed', self.video_feed)
        self.app.add_url_rule('/save_picture', 'save_picture', self.save_picture)


    def take_picture(self):
        return "Voici une photo"
    
    def take_Lidar(self):
        return "Voici un scan lidar"
    
    def video_feed(self):
        return "Voici le flux vidéo"
    
    def save_picture(self):
        return "Voici le chemin de sauvegarde de l'image a traiter"

    def run(self):
        """Démarre le serveur Flask"""
        self.app.run(host=self.host, port=self.port)



from flask import Flask

class Server:
    def __init__(self, host='0.0.0.0', port=5000):
        # Initialisation de l'application Flask
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        # Définir la route pour envoyer un message
        self.app.add_url_rule('/take_picture', 'take_picture', self.take_picture)
        self.app.add_url_rule('/take_Lidar', 'take_Lidar', self.take_Lidar)

    def take_picture(self):
        return "Voici une photo"
    
    def take_Lidar(self):
        return "Voici un scan lidar"

    def run(self):
        """Démarre le serveur Flask"""
        self.app.run(host=self.host, port=self.port)



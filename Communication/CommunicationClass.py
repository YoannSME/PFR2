import serial
import requests
import cv2
import json
import numpy as np
import os

class Bluetooth():
    def __init__(self, port="COM7", baud=9600, timeout=1):
        self.isBt = True
        try:
            self.bt = serial.Serial(port, baud, timeout=timeout)
        except serial.SerialException as e:
            print(f"Erreur d'ouverture du port série : {e}")
            self.bt = None

    def send(self, message):
        if self.bt and self.bt.is_open:
            try:
                self.bt.write(message.encode())
            except Exception as e:
                print(f"Erreur lors de l'envoi : {e}")
        else:
            print("Connexion Bluetooth non disponible.")

    def read(self):
        if self.bt and self.bt.is_open and self.bt.readable():
            try:
                data = self.bt.read_until(size=1)
                self.bt.reset_input_buffer()
                return data.decode(errors='ignore')  # ignore ou replace pour éviter les plantages
            except Exception as e:
                print(f"Erreur de lecture : {e}")
                return ""
        else:
            print("Connexion Bluetooth non disponible ou non lisible.")
            return ""

"""
Date : 28 mars 2025
Auteur : Axel Sichi

Classe Client qui permet d'interagir avec un serveur en envoyant des requêtes GET.
Elle permet de récupérer des données depuis le serveur via une API RESTful en utilisant l'adresse IP du serveur et un port par défaut de 5000.

Attributs:
- server_ip : str - L'adresse IP du serveur avec lequel l'interface client communique.
- port : int - Le port de connexion au serveur, par défaut 5000.

Méthodes:
- getFromServeur(self, endPoint) : Envoie une requête GET au serveur et récupère la réponse sous forme de texte.
"""

class FlaskClient:
    def __init__(self, server_ip, port=5000):
        self.server_ip = server_ip
        self.port = port

    def getLidarFromServeur(self):
        """Envoie une requête GET et récupère la réponse"""
        url = f'http://{self.server_ip}:{self.port}/take_Lidar'
        response = requests.get(url)
        return self.json_to_numpy(response.text)
    
    def getVideoFromServeur(self):
        """Envoie une requête GET et récupère la réponse"""
        url = f'http://{self.server_ip}:{self.port}/video_feed'
        cap = cv2.VideoCapture(url)
        return cap
    
    def takePictureClient(self):
        url = f'http://{self.server_ip}:{self.port}/save_picture'
        response = requests.get(url)
        image_path = "imageRequete.jpg"

        with open(image_path, 'wb') as f:
          f.write(response.content)
        return os.path.abspath(image_path)
    
    def json_to_numpy(self, json_str):
        try:
            return np.array(json.loads(json_str))
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Erreur lors de la conversion: {e}")
            return None
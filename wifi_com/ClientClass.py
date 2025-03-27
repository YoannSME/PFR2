import requests

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

class Client:
    def __init__(self, server_ip, port=5000):
        self.server_ip = server_ip
        self.port = port

    def getFromServeur(self, endPoint):
        """Envoie une requête GET et récupère la réponse"""
        url = f'http://{self.server_ip}:{self.port}/{endPoint}'
        response = requests.get(url)
        return response.text



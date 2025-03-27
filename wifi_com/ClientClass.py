import requests

class Client:
    def __init__(self, server_ip, port=5000):
        self.server_ip = server_ip
        self.port = port

    def getFromServeur(self, endPoint):
        """Envoie une requête GET et récupère la réponse"""
        url = f'http://{self.server_ip}:{self.port}/{endPoint}'
        response = requests.get(url)
        return response.text



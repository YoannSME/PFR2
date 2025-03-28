from ClientClass import Client

if __name__ == '__main__':    
    # Création d'un client et récupération du message
    client = Client('192.168.0.36')  # Remplace par l'IP du Raspberry Pi
    message = client.getFromServeur('take_picture')
    print(f"Message reçu du serveur : {message}")
    message = client.getFromServeur('take_Lidar')
    print(f"Message reçu du serveur : {message}")
    
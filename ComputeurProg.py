from wifi_com.ClientClass import Client
# from lidar.CartographieClass import Cartographie
# from lidar.FindTransformationClass import FindTransformation

if __name__ == '__main__':    
    # Création d'un client et récupération du message
    client = Client('192.168.0.36')  # Remplace par l'IP du Raspberry Pi
    while True:
        input("Press Entrer")
        message = client.getFromServeur('take_Lidar')
        print(message)
from wifi_com.ClientClass import Client
from lidar.CartographieClass import Cartographie
import pygame
import serial
# from lidar.FindTransformationClass import FindTransformation

def Deplacement():
    pygame.init()
    pygame.joystick.init()
    
    arduino = serial.Serial('COM6', 9600)
    
    if pygame.joystick.get_count() == 0:
        print("Aucune manette détectée.")
        return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    print(f"Manette détectée: {joystick.get_name()}")
    cpt = 0
    running = True
    status = b'S'
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        axesX = joystick.get_axis(1)
        axesY = joystick.get_axis(0)
        PressA = joystick.get_button(0)
        
        if   axesX <= -0.5:
            status = (b"F")
        elif axesX >= 0.5:
            status = (b"B")
        elif axesY <= -0.5:
            status = (b"L")
        elif axesY >= 0.5:
            status = (b"R")
        else :
            status = (b"S")
        
        cpt += 1
        if cpt%5000 == 0:
            print(status)
            arduino.write(status)


        # if PressA:
        #     message = client.json_to_numpy(client.getFromServeur('take_Lidar'))
        #     cartographie.update_carte(message, ploting=True)  
        
        
    pygame.quit()

if __name__ == '__main__':    
    # # Création d'un client et récupération du message
    # client = Client('192.168.0.36')  # Remplace par l'IP du Raspberry Pi
    # cartographie = Cartographie()
    Deplacement()
        
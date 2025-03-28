from lidar.MyLidarClass import MyLidar
from wifi_com.ServeurClass import Server
import pygame
import serial

from flask import jsonify

class Robot(Server):
    def __init__(self, LidarPort = '/dev/ttyUSB0'):
        super().__init__()
        self.lidar = MyLidar(LidarPort)
        self.run()
        
    def take_Lidar(self):
        data = self.lidar.getScanData(360, format=1)
        return jsonify(data.tolist())
    
def main():
    pygame.init()
    pygame.joystick.init()
    
    arduino = serial.Serial('COM3', 9600)
    
    if pygame.joystick.get_count() == 0:
        print("Aucune manette détectée.")
        return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    print(f"Manette détectée: {joystick.get_name()}")
    
    running = True
    status = b'S'
    oldstatus = b'S'
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        axesX = joystick.get_axis(1)
        axesY = joystick.get_axis(0)
        
        if   axesX <= -0.9:
            status = (b"B")
        elif axesX >= 0.9:
            status = (b"F")
        elif axesY <= -0.9:
            status = (b"R")
        elif axesY >= 0.9:
            status = (b"L")
        else :
            status = (b"S")
        
        if status != oldstatus:
            print(status)
            arduino.write(status)
            oldstatus = status

    pygame.quit()

    
if __name__ == '__main__':    
    # Création d'un client et récupération du message
    Robot = Robot(LidarPort = '/dev/ttyUSB0')
    print(f"Serveur démarré sur {Robot.host}:{Robot.port}")
    
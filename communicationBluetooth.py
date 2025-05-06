import pygame
import serial
# from lidar.FindTransformationClass import FindTransformation

def Deplacement():
    pygame.init()
    pygame.joystick.init()
    
    arduino = serial.Serial('/dev/tty.RobotG4', 9600)
    
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
        
    pygame.quit()

if __name__ == '__main__':    
    Deplacement()
        
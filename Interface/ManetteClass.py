import pygame

class Manette:
    def __init__(self):
        pygame.joystick.init()
        self.joystick = None
        self.previous_buttons = []
        self.previous_dpad = (0, 0)
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.previous_buttons = [0] * self.joystick.get_numbuttons()
        else:
            print("⚠️ Aucune manette détectée !")
    
    def get_dpad(self):
        if self.joystick:
            return self.joystick.get_hat(0)  # Retourne (x, y) de la croix directionnelle
        return (0, 0)
    
    def get_buttons(self):
        if self.joystick:
            return [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        return []
    
    def get_button_pressed(self):
        current_buttons = self.get_buttons()
        pressed_buttons = [i for i in range(len(current_buttons)) if current_buttons[i] and not self.previous_buttons[i]]
        self.previous_buttons = current_buttons
        return pressed_buttons
    
    def get_dpad_pressed(self):
        current_dpad = self.get_dpad()
        pressed_dpad = (current_dpad[0] if current_dpad[0] != self.previous_dpad[0] else 0,
                        current_dpad[1] if current_dpad[1] != self.previous_dpad[1] else 0)
        self.previous_dpad = current_dpad
        return pressed_dpad

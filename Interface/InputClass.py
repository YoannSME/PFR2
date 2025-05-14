import pygame


class Manette:
    """
    Classe Manette

    Date : Avril 2025
    Auteur : Axel Sichi

    Cette classe gère l'interaction avec une manette de jeu via Pygame. Elle permet de récupérer les boutons et les directions du D-Pad, ainsi que de détecter les boutons et directions pressés.

    Méthodes principales :
    - __init__ : Initialise la manette, en vérifiant la présence d'un périphérique connecté. Si une manette est détectée, elle est initialisée avec ses boutons et son D-Pad.
    - get_dpad : Récupère la direction actuelle du D-Pad de la manette.
    - get_buttons : Récupère l'état des boutons de la manette.
    - get_button_pressed : Retourne les indices des boutons pressés (détection du front descendant).
    - get_dpad_pressed : Retourne l'état des directions du D-Pad pressées (détection du front descendant).
    - get_joystick : Récupère les valeurs des axes des joysticks.
    """
    def __init__(self):
        pygame.joystick.init()
        self.joystick = None
        self.previous_buttons = []
        self.previous_dpad = (0, 0)
        self.isManette = False
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.previous_buttons = [0] * self.joystick.get_numbuttons()
            self.isManette = True
            
    def get_dpad(self):
        try :
            return self.joystick.get_hat(0)
        except:
            return (0, 0)
    
    def get_buttons(self):
        try:
            return [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        except:
            return []
    
    def get_button_pressed(self):
        try:
            current_buttons = self.get_buttons()
            pressed_buttons = [i for i in range(len(current_buttons)) if current_buttons[i] and not self.previous_buttons[i]]
            self.previous_buttons = current_buttons
            return pressed_buttons
        except:
            return []
    
    def get_dpad_pressed(self):
        try:
            current_dpad = self.get_dpad()
            pressed_dpad = (current_dpad[0] if current_dpad[0] != self.previous_dpad[0] else 0,
                            current_dpad[1] if current_dpad[1] != self.previous_dpad[1] else 0)
            self.previous_dpad = current_dpad
            return pressed_dpad
        except:
            return (0, 0)
    
    def get_joystick(self):
        try:
            return [self.joystick.get_axis(i) for i in range(self.joystick.get_numaxes())]
        except:
            return []

class Keyboard:
    """
    Classe Keyboard (via Pygame)

    Date : Avril 2025
    Auteur : Axel Sichi (modifiée pour Pygame)

    Cette classe gère la détection des entrées clavier via Pygame. Elle permet de suivre l'état des touches et de détecter les pressions spécifiques (front descendant).
    """

    def __init__(self):
        # Initialiser Pygame (nécessaire pour gérer les événements)
        pygame.init()
        self.previous_keys = {}
        self.tracked_keys = {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "enter": pygame.K_RETURN,
            "esc": pygame.K_ESCAPE,
            "backspace": pygame.K_BACKSPACE,
            "space": pygame.K_SPACE,
        }

        # Lettres a-z
        for c in "abcdefghijklmnopqrstuvwxyz":
            self.tracked_keys[c] = getattr(pygame, f"K_{c}")

        # Chiffres 0-9
        for i in range(10):
            self.tracked_keys[str(i)] = getattr(pygame, f"K_{i}")

        # État initial
        self.previous_state = pygame.key.get_pressed()

    def update(self):
        """
        Met à jour l'état des touches et détecte les fronts descendants.
        """
        pygame.event.pump()  # Nécessaire pour mettre à jour l'état clavier
        current_state = pygame.key.get_pressed()
        pressed_keys = []

        for name, key in self.tracked_keys.items():
            if self.previous_state[key] and not current_state[key]:
                pressed_keys.append(name)

        self.previous_state = current_state
        return pressed_keys

    def get_press(self):
        """
        Retourne les touches actuellement maintenues.
        """
        pygame.event.pump()
        current_state = pygame.key.get_pressed()
        pressed_keys = []

        for name, key in self.tracked_keys.items():
            if current_state[key]:
                pressed_keys.append(name)

        self.previous_state = current_state
        return pressed_keys

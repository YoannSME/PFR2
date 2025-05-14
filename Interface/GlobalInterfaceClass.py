from Interface.AllInterfaceClass import *
import pygame

class InterfaceGlobale():
    """
    Classe InterfaceGlobale

    Date : Avril 2025
    Auteur : Axel Sichi

    Cette classe implémente l'interface principale de l'application, en gérant l'affichage et les événements de l'interface graphique, ainsi que l'interaction avec l'utilisateur via la manette et le clavier. Elle initialise les composants nécessaires, tels que la fenêtre d'affichage et les entrées utilisateur.

    Méthodes principales :
    - __init__ : Initialise l'interface graphique, les entrées utilisateur, et les composants nécessaires (manette, clavier, traduction, etc.).
    - run : Lance la boucle principale de l'application, gérant les événements et l'affichage.
    """
    def __init__(self, width=1920, height=1080, utils=None):
        self.utils = utils            
        
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("PFR")
        
        self.running = True
        self.clock = pygame.time.Clock()
        self.root_interface = MenuPrincipal(self, self.screen, self.utils)
    
    def run(self):
        while self.running:
            self.root_interface.handle_events()
            self.root_interface.render()
            self.clock.tick(30)
        pygame.quit()
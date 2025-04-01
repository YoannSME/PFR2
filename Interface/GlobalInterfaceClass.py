import pygame
from Interface.TraductionClass import Traduction
from Interface.ManetteClass import Manette
from Interface.AllInterfaceClass import *

class InterfaceGlobale():
    def __init__(self, width=1920, height=1080):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Interface PFR")
        
        self.running = True
        self.clock = pygame.time.Clock()
        self.manette = Manette()
        
        self.traduction = Traduction()
        self.root_interface = MenuPrincipal(self, self.traduction)
    
    def run(self):
        while self.running:
            self.root_interface.handle_events(self.manette)
            self.root_interface.render(self.screen)
            self.clock.tick(30)
        pygame.quit()
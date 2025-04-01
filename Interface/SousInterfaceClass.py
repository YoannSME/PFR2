import pygame
import keyboard

class SousInterface:
    def __init__(self, parent=None, traduction=None):
        self.traduction = traduction
        self.parent = parent
        self.children = []
        self.active_child = None
        self.running = True
    
    def add_child(self, child):
        self.children.append(child)
    
    def set_active_child(self, child):
        self.active_child = child
    
    def handle_events(self, manette, keyboard):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        if self.active_child:
            self.active_child.handle_events(manette, keyboard)
    
    def on_select(self):
        pass
    
    def render(self, screen):
        if self.active_child:
            self.active_child.render(screen)
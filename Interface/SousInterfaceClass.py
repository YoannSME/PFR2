import pygame

class SousInterface:
    """
    Classe SousInterface

    Date : Avril 2025
    Auteur : Sichi Axel
    Cette classe représente une interface qui peut contenir des sous-interfaces ou des composants enfants. Elle permet de gérer la sélection d'éléments, la gestion des événements et l'affichage des sous-composants.

    Méthodes principales :
    - __init__ : Initialise une sous-interface avec des paramètres facultatifs pour le parent, la traduction, l'écran, la manette, et le clavier. Définit les enfants et l'enfant actif de l'interface.
    - add_child : Ajoute un enfant à la sous-interface.
    - set_active_child : Définit l'enfant actif à afficher et manipuler.
    - handle_events : Gère les événements Pygame pour l'interface et ses enfants.
    - on_select : Méthode à implémenter pour gérer les actions lors de la sélection d'un élément.
    - render : Affiche l'interface active (ou l'enfant actif si défini).
    """
    def __init__(self, parent=None, screen=None, utils=None):
        self.parent = parent
        self.active_child = None
        self.children = []
        
        self.running = True
        self.screen = screen
        self.utils = utils
    
    def add_child(self, child):
        self.children.append(child)
    
    def set_active_child(self, child):
        self.active_child = child
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        if self.active_child:
            self.active_child.handle_events(self.manette, self.keyboard)
    
    def on_select(self):
        pass
    
    def render(self):
        if self.active_child:
            self.active_child.render()



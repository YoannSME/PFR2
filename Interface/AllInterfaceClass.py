import pygame
from Interface.SousInterfaceClass import SousInterface

class DeplacementMenu(SousInterface):
    def __init__(self, parent=None, traduction=None):
        super().__init__(parent, traduction=traduction)
        self.selected_index = 0
    
    def handle_events(self, manette):
        if self.active_child:
            self.active_child.handle_events(manette)
            return        
        
        super().handle_events(manette)
        dpad_x, dpad_y = manette.get_dpad_pressed()
        buttons = manette.get_button_pressed()
        
        if dpad_y == 1:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif dpad_y == -1:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        if 1 in buttons:  # Bouton A
            self.parent.set_active_child(None)
            
        elif 0 in buttons:  # Bouton A
            self.on_select()
    
    def on_select(self):
        selected_option = self.options[self.selected_index]
        print(f"Option sélectionnée: {selected_option}")
    
    def render(self, screen):
        if self.active_child:
            self.active_child.render(screen)
            return
        
        self.options = [
            self.traduction.traduire("option_automatique"),
            self.traduction.traduire("option_manette"),
            self.traduction.traduire("option_commande"),
        ]
        
        # Récupération de la taille de l'écran
        screen_width, screen_height = screen.get_size()
        
        # Nettoyage de l'écran
        screen.fill((30, 30, 30))

        # Affichage du titre
        font_title = pygame.font.Font(None, screen_height // 12)  # Taille adaptative
        title_surface = font_title.render(self.traduction.traduire("menu_deplacement"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        screen.blit(title_surface, title_rect)

        # Affichage des options
        font = pygame.font.Font(None, screen_height // 15)  # Taille adaptative
        option_spacing = screen_height // 10  # Espacement adaptatif
        start_y = screen_height // 3  # Début des options

        for i, option in enumerate(self.options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

class ConfigurationMenu(SousInterface):
    def __init__(self, parent=None, traduction=None):
        super().__init__(parent, traduction=traduction)
        self.options = ["Configuration1", "Configuration2", "Configuration3"]
        self.selected_index = 0
    
    def handle_events(self, manette):
        if self.active_child:
            self.active_child.handle_events(manette)
            return
        
        super().handle_events(manette)
        dpad_x, dpad_y = manette.get_dpad_pressed()
        buttons = manette.get_button_pressed()
        
        if dpad_y == 1:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif dpad_y == -1:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        if 1 in buttons:  # Bouton A
            self.parent.set_active_child(None)
            
        elif 0 in buttons:  # Bouton A
            self.on_select()
    
    def on_select(self):
        selected_option = self.options[self.selected_index]
        print(f"Option sélectionnée: {selected_option}")
    
    def render(self, screen):
        if self.active_child:
            self.active_child.render(screen)
            return
        
        # Récupération de la taille de l'écran
        screen_width, screen_height = screen.get_size()
        
        # Nettoyage de l'écran
        screen.fill((30, 30, 30))

        # Affichage du titre
        font_title = pygame.font.Font(None, screen_height // 12)  # Taille adaptative
        title_surface = font_title.render(self.traduction.traduire("menu_configuration"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        screen.blit(title_surface, title_rect)

        # Affichage des options
        font = pygame.font.Font(None, screen_height // 15)  # Taille adaptative
        option_spacing = screen_height // 10  # Espacement adaptatif
        start_y = screen_height // 3  # Début des options

        for i, option in enumerate(self.options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

class LangueMenu(SousInterface):
    def __init__(self, parent=None, traduction=None):
        super().__init__(parent, traduction=traduction)
        self.options = ["English", "Français"]
        self.selected_index = 0
    
    def handle_events(self, manette):
        super().handle_events(manette)
        dpad_x, dpad_y = manette.get_dpad_pressed()
        buttons = manette.get_button_pressed()
        
        if dpad_y == 1:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif dpad_y == -1:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        if 1 in buttons:  # Bouton A
            self.parent.set_active_child(None)
            
        elif 0 in buttons:  # Bouton A
            self.on_select()
    
    def on_select(self):
        nouvelle_langue = "en" if self.selected_index == 0 else "fr"
        self.traduction.changer_langue(nouvelle_langue)
        print(self.traduction.langue)
        print(f"Langue changée en {nouvelle_langue}")
    
    def render(self, screen):
        if self.active_child:
            self.active_child.render(screen)
            return
        
        # Récupération de la taille de l'écran
        screen_width, screen_height = screen.get_size()
        
        # Nettoyage de l'écran
        screen.fill((30, 30, 30))

        # Affichage du titre
        font_title = pygame.font.Font(None, screen_height // 12)  # Taille adaptative
        title_surface = font_title.render(self.traduction.traduire("menu_langue"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        screen.blit(title_surface, title_rect)

        # Affichage des options
        font = pygame.font.Font(None, screen_height // 15)  # Taille adaptative
        option_spacing = screen_height // 10  # Espacement adaptatif
        start_y = screen_height // 3  # Début des options

        for i, option in enumerate(self.options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

class MenuPrincipal(SousInterface):
    def __init__(self, parent=None, traduction=None):
        super().__init__(parent, traduction=traduction)
        self.selected_index = 0
        self.add_child(DeplacementMenu(self, traduction=traduction))
        self.add_child(ConfigurationMenu(self, traduction=traduction))
        self.add_child(LangueMenu(self, traduction=traduction))
    
    def handle_events(self, manette):
        if self.active_child:
            self.active_child.handle_events(manette)
            return
        
        super().handle_events(manette)
        dpad_x, dpad_y = manette.get_dpad_pressed()
        buttons = manette.get_button_pressed()
        
        if dpad_y == 1:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif dpad_y == -1:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        if 1 in buttons:  # Bouton A
            self.parent.running = False
            
        elif 0 in buttons:  # Bouton A
            self.on_select()
    
    def on_select(self):
        selected_option = self.options[self.selected_index]
        print(f"Option sélectionnée: {selected_option}")
        self.set_active_child(self.children[self.selected_index])
    
    def render(self, screen):
        if self.active_child:
            self.active_child.render(screen)
            return

        # Mise à jour dynamique des options traduites
        self.options = [
            self.traduction.traduire("menu_deplacement"),
            self.traduction.traduire("menu_configuration"),
            self.traduction.traduire("menu_langue"),
        ]

        # Récupération de la taille de l'écran
        screen_width, screen_height = screen.get_size()
        
        # Nettoyage de l'écran
        screen.fill((30, 30, 30))

        # Affichage du titre
        font_title = pygame.font.Font(None, screen_height // 12)  # Taille adaptative
        title_surface = font_title.render(self.traduction.traduire("menu_principal"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        screen.blit(title_surface, title_rect)

        # Affichage des options
        font = pygame.font.Font(None, screen_height // 15)  # Taille adaptative
        option_spacing = screen_height // 10  # Espacement adaptatif
        start_y = screen_height // 3  # Début des options

        for i, option in enumerate(self.options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

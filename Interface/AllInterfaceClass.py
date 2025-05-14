import pygame
import cv2
import numpy as np
import requests
import threading
from Interface.SousInterfaceClass import SousInterface

class PopUpConfirm(SousInterface):
    def __init__(self, parent, utils, message, on_confirm, on_cancel=None):
        super().__init__(parent, parent.screen, utils)
        self.message = message
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel or (lambda: self.parent.set_active_child(None))
        self.selected_index = 0

        # Création de l'overlay une seule fois
        screen_width, screen_height = parent.screen.get_size()
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    def handle_events(self):
        """Gestion des entrées utilisateur (flèches haut/bas et validation)."""
        super().handle_events()
        dpad_x, dpad_y = self.utils.manette.get_dpad_pressed()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.update()

        # Navigation entre "Oui" et "Non"
        if dpad_x == 1 or "right" in pressed_keys:
            self.selected_index = (self.selected_index - 1) % 2
        elif dpad_x == -1 or "left" in pressed_keys:
            self.selected_index = (self.selected_index + 1) % 2

        # Validation de l'option sélectionnée
        if 0 in buttons or "enter" in pressed_keys:  # Bouton A ou Enter
            if self.selected_index == 0:
                self.on_confirm()  # Exécuter l'action confirmée
            else:
                self.on_cancel()  # Annuler et fermer la pop-up

    def render(self):
        self.screen.blit(self.overlay, (0, 0))

        # Dessiner la pop-up (cadre gris foncé)
        screen_width, screen_height = self.screen.get_size()
        popup_width, popup_height = screen_width // 2, screen_height // 3
        popup_rect = pygame.Rect(
            (screen_width - popup_width) // 2,
            (screen_height - popup_height) // 2,
            popup_width,
            popup_height
        )
        pygame.draw.rect(self.screen, (50, 50, 50), popup_rect, border_radius=1000)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, 3, border_radius=1000)

        # Affichage du message
        font = pygame.font.Font(None, screen_height // 20)
        message_surface = font.render(self.message, True, (255, 255, 255))
        message_rect = message_surface.get_rect(center=(screen_width // 2, popup_rect.top + popup_height // 3))
        self.screen.blit(message_surface, message_rect)

        # Affichage des options "Oui" et "Non"
        options = [self.utils.traduction.traduire("oui"), self.utils.traduction.traduire("non")]
        option_y = popup_rect.top + popup_height * 2 // 3
        for i, option in enumerate(options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            option_surface = font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(screen_width // 2 - 50 + i * 100, option_y))
            self.screen.blit(option_surface, option_rect)

        pygame.display.flip()

class PopUpPassword(SousInterface):
    def __init__(self, parent, utils, message, correct_password, on_confirm=None, on_cancel=None):
        super().__init__(parent, parent.screen, utils)
        self.message = message
        self.correct_password = correct_password
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel or (lambda: self.parent.set_active_child(None))
        self.input_password = ""
        self.selected_index = 0
        self.badChar = [str(i) for i in range(10)] + ["q", "w"]

        screen_width, screen_height = parent.screen.get_size()
        self.overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 0))

    def handle_events(self):
        super().handle_events()
        dpad_x, dpad_y = self.utils.manette.get_dpad_pressed()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.update()
        for key in pressed_keys:
            if key == "backspace":
                self.input_password = self.input_password[:-1]
            elif len(key) == 1 and key.isalnum() and not key in self.badChar and len(self.input_password) < 20:  # Accepter les caractères alphanumériques et supprime des carac à problème
                self.input_password += key
                
        if dpad_x == 1 or "right" in pressed_keys:
            self.selected_index = (self.selected_index - 1) % 2
        elif dpad_x == -1 or "left" in pressed_keys:
            self.selected_index = (self.selected_index + 1) % 2

        if self.selected_index == 0:
            if 0 in buttons or "enter" in pressed_keys:
                if self.input_password == self.correct_password:
                    self.on_confirm()
                else:
                    self.input_password = ""
        else:
            if 0 in buttons or "enter" in pressed_keys:
                self.on_cancel()
                
        if 1 in buttons or "escape" in pressed_keys:
            self.on_cancel()

    def render(self):
        self.screen.blit(self.overlay, (0, 0))

        screen_width, screen_height = self.screen.get_size()
        popup_width, popup_height = screen_width // 2, screen_height // 3
        popup_rect = pygame.Rect(
            (screen_width - popup_width) // 2,
            (screen_height - popup_height) // 2,
            popup_width,
            popup_height
        )
        pygame.draw.rect(self.screen, (50, 50, 50), popup_rect, border_radius=1000)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, 3, border_radius=1000)

        font = pygame.font.Font(None, screen_height // 20)
        message_surface = font.render(self.message, True, (255, 255, 255))
        message_rect = message_surface.get_rect(center=(screen_width // 2, popup_rect.top + popup_height // 5))
        self.screen.blit(message_surface, message_rect)

        password_surface = font.render('*' * len(self.input_password), True, (255, 255, 255))
        password_rect = password_surface.get_rect(center=(screen_width // 2, popup_rect.top + popup_height // 2))
        self.screen.blit(password_surface, password_rect)

        option_font = pygame.font.Font(None, screen_height // 25)
        options = [self.utils.traduction.traduire("valider"), self.utils.traduction.traduire("annuler")]
        option_y = popup_rect.bottom - 50
        for i, option in enumerate(options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            option_surface = option_font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(screen_width // 2 - 100 + i * 200, option_y))
            self.screen.blit(option_surface, option_rect)

        pygame.display.flip()

class DeplacementManette(SousInterface):
    def __init__(self, parent=None, screen=None, utils=None):
        super().__init__(parent, screen=screen, utils=utils)
        self.options = []
        self.selected_index = 0
        
        self.image_surface = None
        self.surface_lock = threading.Lock()
        self.running = True
        threading.Thread(target=self.update_image_loop, daemon=True).start()
    
    def update_image_loop(self):
        url = f'http://{self.utils.rasp.server_ip}:{self.utils.rasp.port}/video_feed'
        stream = requests.get(url, stream=True)

        bytes_data = b''
        for chunk in stream.iter_content(chunk_size=1024):
            if not self.running:
                break
            
            # Merci StackOverflow ----------------------------
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')  # SOI JPEG
            b = bytes_data.find(b'\xff\xd9')  # EOI JPEG
            if a != -1 and b != -1:
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]
            # Merci StackOverflow ----------------------------

                try:
                    img_array = np.frombuffer(jpg, dtype=np.uint8)
                    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = np.rot90(frame, k=3)
                    frame = np.fliplr(frame)
                    with self.surface_lock:
                        self.image_surface = pygame.surfarray.make_surface(frame)
                        self.image_surface = pygame.transform.scale(self.image_surface, self.screen.get_size())

                except Exception as e:
                    print(f"Erreur de décodage MJPEG : {e}")
    
    def handle_events(self):
        if self.active_child:
            self.active_child.handle_events()
            return        
        
        super().handle_events()
        joystick = self.utils.manette.get_joystick()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.get_press()
        
        if self.utils.manette.isManette :
            if   (joystick[1] <= -0.5 and joystick[0] >= -0.5 and joystick[0] <= 0.5) or "up" in pressed_keys:
                status = ("F\n")
            elif (joystick[1] >= 0.5 and joystick[0] >= -0.5 and joystick[0] <= 0.5) or "down" in pressed_keys:
                status = ("B\n")
            elif (joystick[0] <= -0.5 and joystick[1] >= -0.5 and joystick[1] <= 0.5) or "left" in pressed_keys:
                status = ("L\n")
            elif (joystick[0] >= 0.5 and joystick[1] >= -0.5 and joystick[1] <= 0.5) or "right" in pressed_keys:
                status = ("R\n")
            elif joystick[1] <= -0.5 and joystick[0] <= -0.5:
                status = ("P\n")
            elif joystick[1] <= -0.5 and joystick[0] >= 0.5:
                status = ("A\n")
            elif joystick[1] >= 0.5 and joystick[0] <= -0.5:
                status = ("W\n")
            elif joystick[1] >= 0.5 and joystick[0] >= 0.5:
                status = ("N\n")
            else :
                status = ("S\n")
        else :
            if  "up" in pressed_keys:
                status = ("F\n")
            elif "down" in pressed_keys:
                status = ("B\n")
            elif "left" in pressed_keys:
                status = ("L\n")
            elif "right" in pressed_keys:
                status = ("R\n")
            else :
                status = ("S\n")

        try:
            self.utils.bt.send(status)
        except:
            self.set_active_child(None)
            self.parent.set_active_child(None)           
        
        if 5 in buttons or "space" in pressed_keys:
            self.utils.bt.send("S\n")
            new_data = self.utils.rasp.getLidarFromServeur()
            try :
                self.utils.cartographie.update_carte(new_data)
            except:
                pass
            
        if 1 in buttons or "esc" in pressed_keys:
            def quitter():
                self.set_active_child(None)
                self.parent.set_active_child(None)

            try:
                self.utils.bt.send("S\n")
            except:
                pass
            self.set_active_child(PopUpConfirm(self, self.utils, self.utils.traduction.traduire("voulez_vous_quitter"), quitter))
            
            self.active_child.handle_events()
    
    def render(self):
        if self.active_child:
            self.active_child.render()
            return

        screen_width, screen_height = self.screen.get_size()
        self.screen.fill((30, 30, 30))

        # Titre
        font_title = pygame.font.Font(None, screen_height // 12)
        title_surface = font_title.render(self.utils.traduction.traduire("deplacement_joystick"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        self.screen.blit(title_surface, title_rect)

        # Affichage de l'image (si elle a été chargée)
        if self.image_surface:
            with self.surface_lock:
                self.screen.blit(self.image_surface, (0, 0))
                
        # Taille de la mini-carte
        minimap_size = min(screen_width // 2, screen_height // 2)
        minimap_surface = pygame.Surface((minimap_size, minimap_size))
        minimap_surface.fill((10, 10, 10)) 
        
        # Récupération des points LIDAR globaux
        points = self.utils.cartographie.carte.copy()
        T_robot = self.utils.cartographie.pos.copy() 

        # Si le robot est quelque part sur la carte
        if points is not None and len(points) > 100:
            # Centrage de la mini-map sur le robot
            robot_pos = T_robot[:2, 2]
            
            # Fenêtre à afficher autou du robot
            visible_radius = 5000  # rayon autour du robot
            scale = minimap_size / (2 * visible_radius)
            
            for x, y in points:
                dx, dy = x - robot_pos[0], y - robot_pos[1]
                if abs(dx) > visible_radius or abs(dy) > visible_radius:
                    continue

                px = int(minimap_size // 2 + dx * scale)
                py = int(minimap_size // 2 - dy * scale)
                if 0 <= px < minimap_size and 0 <= py < minimap_size:
                    minimap_surface.set_at((px, py), (0, 255, 0))  # point vert

            # Dessin du robo
            pygame.draw.circle(minimap_surface, (255, 0, 0), (minimap_size // 2, minimap_size // 2), 3)
            # Indicateur d'orientation
            orientation = T_robot[:2, 0]  # vecteur "forward"
            end_x = int(minimap_size // 2 + orientation[0] * 10)
            end_y = int(minimap_size // 2 - orientation[1] * 10)
            pygame.draw.line(minimap_surface, (255, 0, 0), (minimap_size // 2, minimap_size // 2), (end_x, end_y), 2)

        # Affichage en haut à droite
        self.screen.blit(minimap_surface, (screen_width - minimap_size - 10, 10))

        pygame.display.flip()

class DeplacementAutomatique(SousInterface):
    def __init__(self, parent=None, screen=None, utils=None):
        super().__init__(parent, screen=screen, utils=utils)
        self.options = []
        self.selected_index = 0
        self.cpt = 0
        
        self.image_surface = None
        self.surface_lock = threading.Lock()
        self.running = True
        threading.Thread(target=self.update_image_loop, daemon=True).start()
    
    def update_image_loop(self):
        url = f'http://{self.utils.rasp.server_ip}:{self.utils.rasp.port}/video_feed'
        stream = requests.get(url, stream=True)

        bytes_data = b''
        for chunk in stream.iter_content(chunk_size=1024):
            if not self.running:
                break
            
            # Merci StackOverflow ----------------------------
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')  # SOI JPEG
            b = bytes_data.find(b'\xff\xd9')  # EOI JPEG
            if a != -1 and b != -1:
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]
            # Merci StackOverflow ----------------------------

                try:
                    img_array = np.frombuffer(jpg, dtype=np.uint8)
                    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = np.rot90(frame, k=3)
                    frame = np.fliplr(frame)
                    with self.surface_lock:
                        self.image_surface = pygame.surfarray.make_surface(frame)
                        self.image_surface = pygame.transform.scale(self.image_surface, self.screen.get_size())
                except Exception as e:
                    print(f"Erreur de décodage MJPEG : {e}")
    
    def handle_events(self):
        if self.active_child:
            self.active_child.handle_events()
            return        
        
        super().handle_events()
        joystick = self.utils.manette.get_joystick()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.update()

        self.cpt = self.cpt + 1
        if self.cpt%6 == 0:
            try:
                self.utils.bt.send("S\n")
                self.utils.bt.send("Z\n")
            except:
                self.set_active_child(None)
                self.parent.set_active_child(None)    
                
        if 5 in buttons or "space" in pressed_keys or self.cpt%60 == 0:
            while(self.utils.bt.read() == '1'):
                self.utils.bt.send("Y\n")
                self.utils.bt.send("S\n")
                
            while(self.utils.bt.read() == '1'):
                    self.utils.bt.send("Y\n")
                    self.utils.bt.send("S\n")
                
            new_data = self.utils.rasp.getLidarFromServeur()
            try:
                self.utils.cartographie.update_carte(new_data)
            except:
                pass
        
        if 1 in buttons or "esc" in pressed_keys:
            def quitter():
                self.set_active_child(None)
                self.parent.set_active_child(None)

            try:
                while(self.utils.bt.read() == '1'):
                    self.utils.bt.send("Y\n")
                    self.utils.bt.send("S\n")
                while(self.utils.bt.read() == '1'):
                    self.utils.bt.send("Y\n")
                    self.utils.bt.send("S\n") 
            except:
                pass
            self.set_active_child(PopUpConfirm(self, self.utils, self.utils.traduction.traduire("voulez_vous_quitter"), quitter))
            
            self.active_child.handle_events()
    
    def render(self):
        if self.active_child:
            self.active_child.render()
            return

        screen_width, screen_height = self.screen.get_size()
        self.screen.fill((30, 30, 30))

        # Titre
        font_title = pygame.font.Font(None, screen_height // 12)
        title_surface = font_title.render(self.utils.traduction.traduire("deplacement_joystick"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        self.screen.blit(title_surface, title_rect)

        # Affichage de l'image (si elle a été chargée)
        if self.image_surface:
            with self.surface_lock:
                self.screen.blit(self.image_surface, (0, 0))
                
        # Taille de la mini-carte
        minimap_size = min(screen_width // 2, screen_height // 2)
        minimap_surface = pygame.Surface((minimap_size, minimap_size))
        minimap_surface.fill((10, 10, 10)) 
        
        # Récupération des points LIDAR globaux
        points = self.utils.cartographie.carte.copy()
        T_robot = self.utils.cartographie.pos.copy() 

        # Si le robot est quelque part sur la carte
        if points is not None and len(points) > 100:
            # Centrage de la mini-map sur le robot
            robot_pos = T_robot[:2, 2]
            
            # Fenêtre à afficher autou du robot
            visible_radius = 5000  # rayon autour du robot
            scale = minimap_size / (2 * visible_radius)
            
            for x, y in points:
                dx, dy = x - robot_pos[0], y - robot_pos[1]
                if abs(dx) > visible_radius or abs(dy) > visible_radius:
                    continue

                px = int(minimap_size // 2 + dx * scale)
                py = int(minimap_size // 2 - dy * scale)
                if 0 <= px < minimap_size and 0 <= py < minimap_size:
                    minimap_surface.set_at((px, py), (0, 255, 0))  # point vert

            # Dessin du robo
            pygame.draw.circle(minimap_surface, (255, 0, 0), (minimap_size // 2, minimap_size // 2), 3)
            # Indicateur d'orientation
            orientation = T_robot[:2, 0]  # vecteur "forward"
            end_x = int(minimap_size // 2 + orientation[0] * 10)
            end_y = int(minimap_size // 2 - orientation[1] * 10)
            pygame.draw.line(minimap_surface, (255, 0, 0), (minimap_size // 2, minimap_size // 2), (end_x, end_y), 2)

        # Affichage en haut à droite
        self.screen.blit(minimap_surface, (screen_width - minimap_size - 10, 10))

        pygame.display.flip()
       
class RequestMenu(SousInterface):
    def __init__(self, parent=None, screen=None, utils=None):
        super().__init__(parent, screen=screen, utils=utils)
        self.selected_index = 0
        self.add_child(RequestText(self, screen=screen, utils=utils))
        self.add_child(RequestVocal(self, screen=screen, utils=utils))
        
        self.running = True
    
    def handle_events(self):
        if self.active_child:
            self.active_child.handle_events()
            return        
        
        super().handle_events()
        dpad_x, dpad_y = self.utils.manette.get_dpad_pressed()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.update() 
        
        if dpad_y == 1 or "up" in pressed_keys:
            self.selected_index = (self.selected_index - 1) % len(self.options)
            
        elif dpad_y == -1 or "down" in pressed_keys:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        if 1 in buttons or "esc" in pressed_keys:
            self.parent.set_active_child(None)
            
        elif 0 in buttons or "enter" in pressed_keys:
            self.on_select()
    
    def on_select(self):
        self.set_active_child(self.children[self.selected_index])
    
    def render(self):
        if self.active_child:
            self.active_child.render()
            return
        
        self.options = [
            self.utils.traduction.traduire("option_text"),
            self.utils.traduction.traduire("option_voca")
        ]
        
        screen_width, screen_height = self.screen.get_size()
        
        self.screen.fill((30, 30, 30))

        font_title = pygame.font.Font(None, screen_height // 12)
        title_surface = font_title.render(self.utils.traduction.traduire("chosir_mode_deplacement"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        self.screen.blit(title_surface, title_rect)

        font = pygame.font.Font(None, screen_height // 15)
        option_spacing = screen_height // 10
        start_y = screen_height // 3

        for i, option in enumerate(self.options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

class RequestVocal(SousInterface):
    def __init__(self, parent=None, screen=None, utils=None):
        super().__init__(parent, screen=screen, utils=utils)
        self.vocal_started = False  # Flag pour éviter plusieurs threads

    def handle_events(self):
        if self.active_child:
            self.active_child.handle_events()
            return        
        
        super().handle_events()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.update() 

        if 1 in buttons or "esc" in pressed_keys:
            self.parent.set_active_child(None)
            return  # Sortir directement

        # Lancer le traitement vocal une seule fois
        if not self.vocal_started:
            self.vocal_started = True
            threading.Thread(
                target=self.lancer_pilotage_vocal,
                daemon=True
            ).start()

    def lancer_pilotage_vocal(self):
        self.utils.gestionRequest.pilotageVocal()
        self.parent.set_active_child(None)
        self.vocal_started = False  # Remettre à False pour relancer plus tard si besoin

    def render(self):
        if self.active_child:
            self.active_child.render()
            return
        
        screen_width, screen_height = self.screen.get_size()
        self.screen.fill((30, 30, 30))

        font_title = pygame.font.Font(None, screen_height // 8)
        title_surface = font_title.render(self.utils.traduction.traduire("parle"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        self.screen.blit(title_surface, title_rect)

        pygame.display.flip()

class RequestText(SousInterface):
    def __init__(self, parent=None, screen=None, utils=None):
        super().__init__(parent, screen=screen, utils=utils)
        self.selected_index = 0        
        self.running = True
        self.message = ""
    
    def handle_events(self):
        if self.active_child:
            self.active_child.handle_events()
            return        
        
        
        super().handle_events()
        dpad_x, dpad_y = self.utils.manette.get_dpad_pressed()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.update() 
        
        if 1 in buttons or "esc" in pressed_keys:
            self.message = ""
            self.parent.set_active_child(None)
            return ":D"
        
        #threading.Thread(target=self.update_image_loop, daemon=True).start()
        
        if self.selected_index == 0:
            if 0 in buttons or "enter" in pressed_keys:
                threading.Thread(target=self.utils.gestionRequest.pilotageTextuel,args=(self.message,),
                                 daemon=True).start()

                self.parent.set_active_child(None)
                self.message = ""
                self.parent.set_active_child(None)
                return ":D"
        else:
            if 0 in buttons or "enter" in pressed_keys:
                self.message = ""
                self.parent.set_active_child(None)
                return ":D"
                
        if dpad_x == 1 or "right" in pressed_keys:
            self.selected_index = (self.selected_index - 1) % 2
            
        elif dpad_x == -1 or "left" in pressed_keys:
            self.selected_index = (self.selected_index + 1) % 2
        else:
            for key in pressed_keys:
                if key == "backspace":
                    self.message = self.message[:-1]
                elif key.isalnum() and len(self.message) < 60:
                    if key == "up" or key == "down":
                        pass
                    elif key == "space":
                        self.message += " "
                    else:
                        self.message += key
    
    def on_select(self):
        self.set_active_child(self.children[self.selected_index])
    
    def render(self):
        if self.active_child:
            self.active_child.render()
            return
        
        self.options = [
            self.utils.traduction.traduire("valider"),
            self.utils.traduction.traduire("annuler")
        ]
        
        screen_width, screen_height = self.screen.get_size()
        
        self.screen.fill((30, 30, 30))

        font_title = pygame.font.Font(None, screen_height // 12)
        title_surface = font_title.render(self.utils.traduction.traduire("enter_text_request"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        self.screen.blit(title_surface, title_rect)
        
        font_title = pygame.font.Font(None, screen_height // 20)
        title_surface = font_title.render(self.message, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        self.screen.blit(title_surface, title_rect)

        font = pygame.font.Font(None, screen_height // 15)
        option_spacing = screen_width // 3

        for i, option in enumerate(self.options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=((i+1) * option_spacing , screen_height*0.8))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

class DeplacementMenu(SousInterface):
    def __init__(self, parent=None, screen=None, utils=None):
        super().__init__(parent, screen=screen, utils=utils)
        self.selected_index = 0
        self.add_child(DeplacementAutomatique(self, screen=screen, utils=utils))
        self.add_child(DeplacementManette(self, screen=screen, utils=utils))
        self.add_child(RequestMenu(self, screen=screen, utils=utils))
        
    def handle_events(self):
        if self.active_child:
            self.active_child.handle_events()
            return        
        
        super().handle_events()
        dpad_x, dpad_y = self.utils.manette.get_dpad_pressed()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.update() 
        
        if dpad_y == 1 or "up" in pressed_keys:
            self.selected_index = (self.selected_index - 1) % len(self.options)
            
        elif dpad_y == -1 or "down" in pressed_keys:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        if 1 in buttons or "esc" in pressed_keys:
            self.parent.set_active_child(None)
            
        elif 0 in buttons or "enter" in pressed_keys:
            self.on_select()
    
    def on_select(self):
        self.set_active_child(self.children[self.selected_index])
         
    def render(self):
        if self.active_child:
            self.active_child.render()
            return
        
        self.options = [
            self.utils.traduction.traduire("option_automatique"),
            self.utils.traduction.traduire("option_manette"),
            self.utils.traduction.traduire("option_commande"),
        ]
        
        screen_width, screen_height = self.screen.get_size()
        
        self.screen.fill((30, 30, 30))

        font_title = pygame.font.Font(None, screen_height // 12)
        title_surface = font_title.render(self.utils.traduction.traduire("chosir_mode_deplacement"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        self.screen.blit(title_surface, title_rect)

        font = pygame.font.Font(None, screen_height // 15)
        option_spacing = screen_height // 10
        start_y = screen_height // 3

        for i, option in enumerate(self.options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

class ConfigurationMenu(SousInterface):
    def __init__(self, parent=None, screen=None, utils=None):
        super().__init__(parent, screen=screen, utils=utils)
        self.options = ["Configuration1", "Configuration2", "Configuration3"]
        self.selected_index = 0
    
    def handle_events(self):
        if self.active_child:
            self.active_child.handle_events()
            return        
        
        super().handle_events()
        dpad_x, dpad_y = self.utils.manette.get_dpad_pressed()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.update() 
        
        if dpad_y == 1 or "up" in pressed_keys:
            self.selected_index = (self.selected_index - 1) % len(self.options)
            
        elif dpad_y == -1 or "down" in pressed_keys:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        if 1 in buttons or "esc" in pressed_keys:
            self.parent.set_active_child(None)
            
        elif 0 in buttons or "enter" in pressed_keys:
            self.on_select()
    
    def on_select(self):
        selected_option = self.options[self.selected_index]
    
    def render(self):
        if self.active_child:
            self.active_child.render()
            return
        
        screen_width, screen_height = self.screen.get_size()
        
        self.screen.fill((30, 30, 30))

        font_title = pygame.font.Font(None, screen_height // 12)
        title_surface = font_title.render(self.utils.traduction.traduire("menu_configuration"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        self.screen.blit(title_surface, title_rect)

        font = pygame.font.Font(None, screen_height // 15)
        option_spacing = screen_height // 10
        start_y = screen_height // 3

        for i, option in enumerate(self.options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

class LangueMenu(SousInterface):
    def __init__(self, parent=None, screen=None, utils=None):
        super().__init__(parent, screen=screen, utils=utils)
        self.options = ["English", "Français"]
        self.selected_index = 0
    
    def handle_events(self):
        if self.active_child:
            self.active_child.handle_events()
            return        
        
        super().handle_events()
        dpad_x, dpad_y = self.utils.manette.get_dpad_pressed()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.update() 
        
        if dpad_y == 1 or "up" in pressed_keys:
            self.selected_index = (self.selected_index - 1) % len(self.options)
            
        elif dpad_y == -1 or "down" in pressed_keys:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        if 1 in buttons or "esc" in pressed_keys:
            self.parent.set_active_child(None)
            
        elif 0 in buttons or "enter" in pressed_keys:
            self.on_select()
    
    def on_select(self):
        nouvelle_langue = "en-EN" if self.selected_index == 0 else "fr-FR"
        self.utils.traduction.changer_langue(nouvelle_langue)
        self.utils.configuration.set("langue", nouvelle_langue)
    
    def render(self):
        if self.active_child:
            self.active_child.render()
            return
        
        screen_width, screen_height = self.screen.get_size()
        
        self.screen.fill((30, 30, 30))

        font_title = pygame.font.Font(None, screen_height // 12)
        title_surface = font_title.render(self.utils.traduction.traduire("menu_langue"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        self.screen.blit(title_surface, title_rect)

        font = pygame.font.Font(None, screen_height // 15) 
        option_spacing = screen_height // 10
        start_y = screen_height // 3

        for i, option in enumerate(self.options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

class MenuPrincipal(SousInterface):
    def __init__(self, parent=None, screen=None, utils=None):
        super().__init__(parent, screen=screen, utils=utils)
        self.selected_index = 0
        self.add_child(DeplacementMenu(self, screen=screen, utils=utils))
        self.add_child(ConfigurationMenu(self, screen=screen, utils=utils))
        self.add_child(LangueMenu(self, screen=screen, utils=utils))
    
    def handle_events(self):
        if self.active_child:
            self.active_child.handle_events()
            return        
        
        super().handle_events()
        dpad_x, dpad_y = self.utils.manette.get_dpad_pressed()
        buttons = self.utils.manette.get_button_pressed()
        pressed_keys = self.utils.keyboard.update() 
        
        if dpad_y == 1 or "up" in pressed_keys:
            self.selected_index = (self.selected_index - 1) % len(self.options)
            
        elif dpad_y == -1 or "down" in pressed_keys:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        
        if 1 in buttons or "esc" in pressed_keys:
            def quitter():
                self.parent.running = False

            self.set_active_child(PopUpConfirm(self, self.utils, self.utils.traduction.traduire("voulez_vous_quitter"), quitter))
            
            self.active_child.handle_events()
            
        elif 0 in buttons or "enter" in pressed_keys:
            self.on_select()
    
    def on_select(self):
        def correct_password():
            self.set_active_child(self.children[self.selected_index])
            
        selected_option = self.options[self.selected_index]
        if self.options[self.selected_index] == self.utils.traduction.traduire("menu_configuration"):
            self.set_active_child(PopUpPassword(self, self.utils, self.utils.traduction.traduire("entrer_mdp"), "admin", correct_password))
        else:
            self.set_active_child(self.children[self.selected_index])
    
    def render(self):
        if self.active_child:
            self.active_child.render()
            return
        
        self.options = [
            self.utils.traduction.traduire("menu_deplacement"),
            self.utils.traduction.traduire("menu_configuration"),
            self.utils.traduction.traduire("menu_langue"),
        ]

        screen_width, screen_height = self.screen.get_size()
        
        self.screen.fill((30, 30, 30))

        font_title = pygame.font.Font(None, screen_height // 12)
        title_surface = font_title.render(self.utils.traduction.traduire("menu_principal"), True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 8))
        self.screen.blit(title_surface, title_rect)

        font = pygame.font.Font(None, screen_height // 15)
        option_spacing = screen_height // 10 
        start_y = screen_height // 3 

        for i, option in enumerate(self.options):
            color = (200, 200, 0) if i == self.selected_index else (255, 255, 255)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, start_y + i * option_spacing))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

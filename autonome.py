""" 
Leo AHMED MUSHTAQ 6 mai 2025
Ce module définit la classe autonome qui représente un robot autonome.
"""
import pygame
import serial
import time

class Autonome : 
   
    #arduino = serial.Serial('COM6', 9600)
    # arduino.write(etatPresent.encode()) pour envoyer l'état au robot via le BT
    
    def __init__(self, etatPresent : str, obstacle : bool):
        self.etatPresent = etatPresent
        self.obstacle = obstacle
    
    ############################ deplacement basique ############################
    def avancer(self, distance : float):
        self.etatPresent = f"F({distance})"
        return self.etatPresent
    
    def reculer(self, distance : float):
        self.etatPresent = f"B({distance})"
        return self.etatPresent
    
    def gauche(self, angle : float):
        self.etatPresent = f"L({angle})"
        return self.etatPresent
    
    def droite(self, angle : float):
        self.etatPresent = f"R({angle})"
        return self.etatPresent
    
    def arreter(self):
        self.etatPresent = "S"
        print("Robot ARRETE.")
        return self.etatPresent
    
    ############################ fin deplacement basique ############################
    
    ############################ fonction à changer et remplacer par les bonnes ############################
    def obtenirImage(self):
        """
        Simule l'obtention d'une image depuis la caméra.
        Cette méthode devra être remplacée par une fonction réelle pour capturer une image.
        """
        # Exemple : return self.camera.get_image()
        print("Obtention d'une image depuis la caméra...")
        return "image_simulee"

    def detecterObjet(self, image):
        """
        Simule la détection d'un objet dans une image.
        Cette méthode devra être remplacée par une fonction réelle pour analyser l'image.
        """
        # Exemple : analyser l'image pour détecter une balle
        print(f"Analyse de l'image : {image}")
        if image == "image_simulee":  # Remplacer par une vraie analyse
            return "balle"  # Simule la détection d'une balle
        return None
    
    def calculerAngleObjet(self, image, objet_detecte)-> float:
        """
        Simule le calcul de l'angle entre le robot et l'objet détecté.
        Cette méthode devra être remplacée par une fonction réelle pour calculer l'angle.
        """
        # Exemple : calculer l'angle en fonction de la position de l'objet dans l'image
        print(f"Calcul de l'angle pour l'objet détecté : {objet_detecte} dans l'image {image}")
        angle = 45
        return angle  # Simule un angle de 45° pour l'objet détecté
    
    def distanceObjetRobot(self)-> float:
        """
        Simule le calcul de la distance entre le robot et l'objet détecté.
        Cette méthode devra être remplacée par une fonction réelle pour mesurer la distance.
        """
        # Exemple : mesurer la distance à l'aide d'un capteur
        print("Calcul de la distance entre le robot et l'objet...")
        distance = 100
        return distance  # Simule une distance de 100 cm entre le robot et l'objet
    
    ############################ fin de fonction à changer et remplacer par les bonnes ##########################
    
    ############################ recherche d'objects (balles, cubes, etc) via camera ############################
    def objetRecherche(self):
        """
        Recherche un objet spécifique (par exemple, une balle) en utilisant la caméra.
        """
        objet_detecte = None  # Initialisation de l'objet détecté
        compteur = 0
        cptEstAtteint = False

        # Vérifier si un objet est détecté
        objet_detecte = self.detecterObjet(self.obtenirImage())
        if objet_detecte == "balle":
            print("Objet trouvé : balle")

        elif objet_detecte is None:
            print("Pas d'objet trouvé\nMise en place du mode recherche d'objets")
            self.arreter()

            # Mode recherche d'objets
            while objet_detecte is None and not cptEstAtteint:
                print("Recherche d'objets en cours...")
                if compteur == 12:  # 12 * 30° = 360°, on arrête après un tour complet
                    cptEstAtteint = True
                    print("Recherche terminée : aucun objet trouvé après 360°.")
                else:
                    self.gauche(30)  # Tourner de 30° à gauche
                    self.arreter()
                    time.sleep(0.5) # Pause pour image non floue
                    objet_detecte = self.detecterObjet(self.obtenirImage())
                    
                compteur += 1

        return objet_detecte

    
    
    ############################ aller vers objet ############################
    def orienterVersObjet(self, image) ->bool:
        """
        réorientation du robot vers un objet détecté.
        """
        estOriente : bool = False
        
        objet_detecte = self.detecterObjet(image) # à modifier
        
        if objet_detecte:
            # Simuler la détection de l'angle de l'objet (à remplacer par une vraie analyse)
            angle = self.calculerAngleObjet(image, objet_detecte)  # Méthode à implémenter
            print(f"Orientation vers l'objet à un angle de {angle}°.")
            
            if angle > 0: # faire une verification pour savoir si le robot est au centre de l'image ou non
                self.droite(angle)
            elif angle < 0:
                self.gauche(abs(angle))
            elif angle == 0:
                print("Robot déjà orienté vers l'objet.")
                estOriente = True
            
            time.sleep(1)  # Pause pour permettre au robot de s'orienter
        else:
            print("Aucun objet détecté pour l'orientation.")
            estOriente = False
        return estOriente
       
    
    
    def allerVersObjet(self):
        """
        Simule le déplacement vers un objet détecté.
        """
        image = self.obtenirImage() # à modifier
        if not self.orienterVersObjet(image):
            print("Erreur : le robot n'est pas orienté vers l'objet.")
            return
        
        distance = distanceObjetRobot() # à modifier (fontction permettant de calculer la distance entre le robot et l'objet)
        print(f"Déplacement vers l'objet à une distance de {distance} cm.")
        self.avancer(distance)
        time.sleep(1)  # Simule le temps de déplacement
        self.arreter()
            

def main():
    #
        pygame.init()

        # Initialize a display surface
        screen = pygame.display.set_mode((800, 600))
        
        robot = Autonome("S", False)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Exemple d'utilisation des méthodes de la classe autonome
            robot.avancer(10)
            time.sleep(1)
            robot.gauche(90)
            time.sleep(1)
            robot.objetRecherche()
            
            pygame.display.flip()
        
        pygame.quit()

main()
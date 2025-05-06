""" 
Leo AHMED MUSHTAQ 6 mai 2025
Ce module définit la classe autonome qui représente un robot autonome.
"""
import pygame
import serial
import time

class autonome : 
   
    arduino = serial.Serial('COM6', 9600)
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
            return objet_detecte

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
                    objet_detecte = self.detecterObjet(self.obtenirImage())
                    time.sleep(0.5) # Pause pour image non floue
                compteur += 1

        return objet_detecte

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
    
    ############################ fin de fonction à changer et remplacer par les bonnes ############################        
          
        
    
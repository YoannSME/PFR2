import sys
import subprocess
import json 
import time
import os
import pyaudio
from gtts import gTTS


class AlgorithmeRecherche:
    def __init__(self,bt,flask):
        self.bt = bt
        self.flask = flask
        
        
    def chercher(self, mode: int, forme=None, couleur=None):
        """ Cherche un objet en fonction de la forme et/ou de la couleur.
        :param mode: 1 pour couleur, 2 pour forme, 3 pour les deux
        :param forme: La forme à chercher (si mode 2 ou 3)
        :param couleur: La couleur à chercher (si mode 1 ou 3)
        
        :return: None
        """
        fin = False
        tries = 1
        max_tries = 50
        lastOrientation = None

        while not fin and tries < max_tries:
            if tries % 8 == 0:
                self.bt.send("F(50) \n")
                while self.bt.read() != "1":
                    self.bt.send("S\n")

            print("[Info] Début de la recherche")
            pathImage = self.flask.takePictureClient()
            commande = ["TraitementImage/detection", pathImage, str(mode)]
            if mode == 1 and couleur:
                commande.append(couleur)
            elif mode == 2 and forme:
                commande.append(forme)
            elif mode == 3 and forme and couleur:
                commande.extend([forme, couleur])

            try:
                subprocess.run(commande, capture_output=True, text=True)
            except Exception as e:
                print("Erreur subprocess :", e)
                return

            objPresent, obj = self.getObjetPresent(forme, couleur)

            if objPresent:
                distX = obj["distX"]
                if abs(distX) > 15:
                    angle = (distX / 480) * 30
                    direction = "R" if angle > 0 else "L"
                    lastOrientation = direction
                    print(f"[INFO] Je dois tourner de {angle}° vers {direction}")
                    self.bt.send(f"{direction}({abs(angle)}) S\n")
                    while self.bt.read() != "1":
                        self.bt.send("S\n")

                    pathImage = self.flask.takePictureClient()
                    commande[1] = pathImage
                    subprocess.run(commande, capture_output=True, text=True)
                    objPresent, obj = self.getObjetPresent(forme, couleur)
                    if not objPresent:
                        print("[Info] Objet perdu après recentrage.")
                        continue

                # Phase d'approche
                while objPresent and obj["aire"] < 15000:
                    print("[Info] Début approche")
                    self.bt.send("F(50) S\n")
                    while self.bt.read() != "1":
                        self.bt.send("S\n")
                    pathImage = self.flask.takePictureClient()
                    commande[1] = pathImage
                    subprocess.run(commande, capture_output=True, text=True)
                    objPresent, obj = self.getObjetPresent(forme, couleur)

                    if objPresent:
                        lastOrientation = "R" if obj["distX"] > 0 else "L"
                    else:
                        print("[Info] Objet perdu pendant l'approche. Réorientation vers dernière direction")
                        max_reorientation = 6
                        step_angle = 20
                        for i in range(max_reorientation):
                            print(f"[Reorientation] Tentative {i+1} vers {lastOrientation}")
                            self.bt.send(f"{lastOrientation}({step_angle}) S\n")
                            while self.bt.read() != "1":
                                self.bt.send("S\n")
                            pathImage = self.flask.takePictureClient()
                            commande[1] = pathImage
                            subprocess.run(commande, capture_output=True, text=True)
                            objPresent, obj = self.getObjetPresent(forme, couleur)
                            if objPresent:
                                print("[Info] Objet retrouvé après réorientation.")
                                break
                        if not objPresent:
                            print("[Info] Objet non retrouvé après plusieurs tentatives.")
                            break

                if objPresent and obj["aire"] >= 15000:
                    angle = (obj["distX"] / 480) * 30
                    direction = "R" if angle > 0 else "L"
                    print(f"[INFO] Alignement final de {angle:.2f}° vers {direction}")
                    self.bt.send(f"{direction}({abs(angle)}) S\n")
                    while self.bt.read() != "1":
                        self.bt.send("S\n")

                    self.robotVocal("Houra ! Objet trouvé")
                    fin = True
                    return

            else:
                print("[Info] Objet non trouvé. Rotation d'exploration")
                self.bt.send("R(60) S\n")
                while self.bt.read() != "1":
                    self.bt.send("S\n")
                time.sleep(1)

            tries += 1

        print("FIN TRAITEMENT")


    def robotVocal(self, text):
            speech = gTTS(text, lang="fr", slow=False)
            # Save the audio file to a temporary file
            speech_file = 'speech.mp3'
            speech.save(speech_file)
            # Play the audio file
            os.system('mpg123 ' + speech_file)

    def chercherForme(self, forme):
        print("Debut recherche de forme")
        self.chercher(mode=2, forme=forme)

    def chercherCouleur(self, couleur):
        print("Debut recherche de couleur")
        self.chercher(mode=1, couleur=couleur)

    def chercherFormeAvecCouleur(self, forme, couleur):
        print("Debut recherche de forme et couleur")
        self.chercher(mode=3,forme=forme,couleur=couleur)



    def getObjetPresent(self, forme: str, couleur: str):
        """ Récupère l'objet présent dans l'image traitée.
        :param forme: La forme à chercher
        :param couleur: La couleur à chercher
        :return: Un tuple (bool, dict) où le bool indique si l'objet a été trouvé et le dict contient les informations de l'objet
        """
        with open("TraitementImage/retour/resultats.json", "r") as f:
            data = json.load(f)
        if(data is None):
            return False,None
        objets = []
        for obj in data.values():
            if forme and couleur:
                if obj["forme"] == forme and obj["couleur"] == couleur:
                    objets.append(obj)
            elif forme:
                if obj["forme"] == forme:
                    objets.append(obj)
            elif couleur:
                if obj["couleur"] == couleur:
                    objets.append(obj)

        if objets:
            objetRetour = objets[0]
            for obj in objets:
                if obj["aire"] > objetRetour["aire"]:
                    objetRetour = obj
            return True, objetRetour

        return False, None


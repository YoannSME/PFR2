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
        fin = False
        tries = 1
        max_tries = 50

        while not fin and tries < max_tries:
            if(tries%8==0):
                self.bt.send("F(50) \n")
                while(self.bt.read()!="1"):
                    self.bt.send("S\n")
                
            print("[Info] Debut de la recherche")
            pathImage = self.flask.takePictureClient()
            print(pathImage)
            commande = ["TraitementImage/detection", pathImage, str(mode)]
            if mode == 1 and couleur:
                commande.append(couleur)
            elif mode == 2 and forme:
                commande.append(forme)
            elif mode == 3 and forme and couleur:
                commande.extend([forme, couleur])
            print("Commande exécutée :", commande)
            try: 
               result = subprocess.run(commande, capture_output=True, text=True)
               
            except Exception as e:
                print("erreur subprocess")
                return
           
            objPresent, obj = self.getObjetPresent(forme, couleur)
            
            if objPresent:
                distX = obj["distX"]
                if objPresent and abs(distX) > 15:
                    #print("[Info] Je ne suis pas axé : Rotation")
                    angle = (distX/480)*30
                    print("[INFO] je dois tourner de ", angle)
                    direction = "R" if angle > 0 else "L"
                    lastOrientation = direction
                    self.bt.send(f"{direction}({abs(angle)}) S\n")
                    #print("[Info] J'ai tourné")
                    while(self.bt.read()!="1"):
                        self.bt.send("S\n")   
                     
                    pathImage = self.flask.takePictureClient()
                    commande[1] = pathImage
                    result = subprocess.run(commande, capture_output=True, text=True)
                    distX = obj["distX"]
                    #print("suivant")
                    
                while obj["aire"] < 15000:
                    print("[Info] Debut approche")
                    self.bt.send("F(50) S\n")
                    while(self.bt.read()!="1"):
                        self.bt.send("S\n")
                    pathImage = self.flask.takePictureClient()
                    commande[1] = pathImage
                    result = subprocess.run(commande, capture_output=True, text=True)
                    #print("result", result)
                    #print("result stdout", result.stdout)
                    #print("result stderr", result.stderr)
                    objPresent, obj = self.getObjetPresent(forme, couleur)
                    if not objPresent:
                        #print("[Info] Objet perdu pendant l'approche.")
                        break
                if(objPresent and obj["aire"]>=15000):
                    angle = (distX/480)*30
                    print("[INFO] je dois tourner de ", angle)
                    direction = "R" if angle > 0 else "L"
                    lastOrientation = direction
                    self.bt.send(f"{direction}({abs(angle)}) S\n")
                    while(self.bt.read()!="1"):
                        self.bt.send("S\n")
                    
                    self.robotVocal("Houra ! Objet trouvé")
                    fin = True
                    return
            else:
                print(f"[Info] Objet non trouvé. Rotation...")
                self.bt.send("R(60) S\n")
                while(self.bt.read()!="1"):
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
    
    
# if __name__ == '__main__':
#     algo = AlgorithmeRecherche()

#     algo.chercherForme("balle")

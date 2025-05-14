import sys
import subprocess
import json 

class AlgorithmeRecherche:
    def __init__(self,bt,flask):
        self.bt = bt
        self.flask = flask

    def chercher(self, mode: int, forme=None, couleur=None):
        fin = False
        tries = 0
        max_tries = 12

        while not fin and tries < max_tries:
            print("debut recherche")
            pathImage = self.flask.takePictureClient()
            print(pathImage)
            # Construction dynamique de la commande à chaque image
            commande = ["TraitementImage/detection.exe", "imageRequete.jpg", str(mode)]
            if mode == 1 and couleur:
                commande.append(couleur)
            elif mode == 2 and forme:
                commande.append(forme)
            elif mode == 3 and couleur and forme:
                commande.extend([couleur, forme])
            print("Commande exécutée :", commande)
            try: 
               result = subprocess.run(commande, capture_output=True, text=True)
               
               print("Code retour :", result.returncode)
               print("STDOUT :", result.stdout)
               print("STDERR :", result.stderr)

            except Exception as e:
                print("erreur subprocess")
                return

            objPresent, obj = self.getObjetPresent(forme, couleur)

            if objPresent:
                distX = obj["distX"]
                if abs(distX) > 15:
                    print("je ne suis pas axé")
                    angle = abs(distX)
                    direction = "R" if distX > 0 else "L"
                    self.bt.send(f"{direction}({angle}) S\n")
                    print("je suis axé")
                    while(self.bt.read()!="1"):
                        pass
                    print("suivant")
                    
                while obj["aire"] < 30000:
                    print("je commence à avancer")
                    self.bt.send("F(30) S\n")
                    while(self.bt.read()!="1"):
                        pass
                    
                    pathImage = self.flask.takePictureClient()
                    commande[1] = pathImage
                    result = subprocess.run(commande, capture_output=True, text=True)

                    objPresent, obj = self.getObjetPresent(forme, couleur)
                    if not objPresent:
                        print("[Info] Objet perdu pendant l'approche.")
                        break
                if(objPresent and obj["aire"]>=45000):
                    print("J'AI TROUVE LA BALLE")
                    return
            else:
                print(f"[Info] Objet non trouvé. Rotation...")
                self.bt.send("R(60) S\n")
                while(self.bt.read()!="1"):
                    pass

            tries += 1
        print("FIN TRAITEMENT")


    def chercherForme(self, forme):
        print("Debut recherche de forme")
        self.chercher(mode=2, forme=forme)

    def chercherCouleur(self, couleur):
        print("Debut recherche de couleur")
        self.chercher(mode=1, couleur=couleur)

    def chercherFormeAvecCouleur(self, forme, couleur):
        print("Debut recherche de forme et couleur")
        self.chercher(mode=3, forme=forme, couleur=couleur)

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
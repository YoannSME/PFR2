import os
import json
import speech_recognition as sr
import pyaudio
from gtts import gTTS
from GestionRequest.AlgorithmeRechercheClass import AlgorithmeRecherche
import subprocess

class GestionRequest:
    def __init__(self, pathRequete, pathDico, bt, flask):
        self.pathRequete = os.path.abspath(pathRequete)
        self.pathDico = os.path.abspath(pathDico)
        print(self.pathDico)
        self.distance_defaut = 100
        self.angle_defaut = 90
        self.angle_defaut_zigzag = 45
        self.dico = self.chargerDictionnaire(self.pathDico)
        self.algorithmes = AlgorithmeRecherche(bt, flask)
        
        
        self.bt = bt
        self.flask = flask

    def chargerDictionnaire(self, path: str) -> dict:
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Le fichier {path} n'existe pas.")
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def recupererNombre(self, mot: str) -> int:
        mot = str(mot)
        i = 0
        while i < len(mot) and mot[i].isdigit():
            i += 1

        partie_nombre = mot[:i]
        partie_unite = None
        if(len(mot) != len(partie_nombre)):
            partie_unite = mot[i:]

        if not partie_nombre:
            return 0

        nombre = int(partie_nombre)
        
        if partie_unite:
            print(partie_unite)
            typeMotSuivant = self.associerMot(partie_unite)
            if(typeMotSuivant and typeMotSuivant["categorie"] == "unites"):
                nombre = self.convertirUnite(nombre, typeMotSuivant["cle"])

        print("verif : ",mot," nb = ",nombre)
        return nombre
   
    def convertirUnite(self, nombre:int, unite:str) -> int:
        print("convert : nb = ",nombre, " unite = ", unite)
        if(unite == "centimetres" or unite == "c"):
            return nombre
        elif(unite == "metre" or unite == "m"):
            return nombre*100

        return nombre

    def associerMot(self, mot: str) -> dict | None:
        if mot in self.dico.get('commandesSpeciales', {}):#Si c'est une commande spéciale : la clé est le mot est les valeurs sont la suite de commande à réaliser
            return {
                "categorie": "commandesSpeciales",
                "cle": mot,
                "valeur": self.dico['commandesSpeciales'][mot]
            }
        for categorie, sous_dico in self.dico.items():
            if categorie == 'commandesSpeciales':
                continue
            if isinstance(sous_dico, dict):
                for cle, valeurs in sous_dico.items(): 
                    if isinstance(valeurs, list):
                        for valeur in valeurs:
                            if mot == valeur.lower():
                                return { 
                                    "categorie": categorie,
                                    "cle": cle,
                                    "valeur": valeur
                                }
                    elif isinstance(valeurs, str):
                        if mot == valeurs.lower():
                            return {
                                "categorie": categorie,
                                "cle": cle,
                                "valeur": valeurs
                            }
            elif isinstance(sous_dico, list):
                for valeur in sous_dico:
                    if mot == valeur.lower():
                        return {
                            "categorie": categorie,
                            "cle": None,
                            "valeur": valeur
                        }
        return None

    def recupererParametreSuivant(self, requete_filtree: list, indice: int, defaut: int) -> int:
        if indice + 1 < len(requete_filtree) and isinstance(requete_filtree[indice + 1], int):
            return self.recupererNombre(requete_filtree[indice + 1])
        return defaut

    def filtrerMots(self, requete: list) -> list:
        retour = []
        i = 0
        while i < len(requete):
            mot = requete[i]
            typeMot = self.associerMot(mot)

            if typeMot:
                retour.append(mot)
            else:
                nb = self.recupererNombre(mot)
                if nb !=0:
                    
                    if (i + 1) < len(requete):
                        typeMotSuivant = self.associerMot(requete[i + 1])
                        if typeMotSuivant and typeMotSuivant["categorie"] == "unites":
                            nb = self.convertirUnite(nb, typeMotSuivant["cle"])
                            i += 1 
                    retour.append(nb)
                else:
                    pass

            i += 1
        return retour


    def traitementNegations(self, requete: list) -> list:
        i = 0
        while i < len(requete):
            if requete[i] in self.dico.get('negations', []):
                del requete[i]
                if i < len(requete):
                    del requete[i]
            else:
                i += 1
        return requete

    def transformationRequeteCommande(self, requete_filtree: list) -> list:
        commandes_finales = []
        indice = 0
        while indice < len(requete_filtree):
            dict_retour = self.associerMot(requete_filtree[indice])
            param_suivant = self.recupererParametreSuivant(requete_filtree, indice, None)

            if dict_retour:
                categorie = dict_retour['categorie']

                if categorie == 'commandesSpeciales':
                    distance = param_suivant if param_suivant else self.distance_defaut
                    for cmd in dict_retour['valeur']:
                        param = distance if cmd in ["F", "B"] else self.angle_defaut_zigzag
                        commandes_finales.append(f"{cmd}({param})")
                    if param_suivant:
                        indice += 1

                elif categorie == 'deplacementLineaire':
                    distance = param_suivant if param_suivant else self.distance_defaut
                    commandes_finales.append(f"{dict_retour['cle']}({distance})")
                    if param_suivant:
                        indice += 1

                elif categorie == 'deplacementAngulaire':
                    angle = param_suivant if param_suivant else self.angle_defaut
                    commandes_finales.append(f"{dict_retour['cle']}({angle})")
                    if param_suivant:
                        indice += 1

                else:
                    if(categorie !='unites'):
                        commandes_finales.append(requete_filtree[indice])

            indice += 1
        commandeSansNegations = self.traitementNegations(commandes_finales)
        return self.commandeAutonome(commandeSansNegations)
    
    def commandeAutonome(self,commande : list):
        retour = []
        indexMot = 0
        while(indexMot<len(commande)):
            mot = commande[indexMot]
            if mot in self.dico.get('actions',[]):
                fonction = ["chercher"]
                indexMot +=1
                if(indexMot<len(commande)):
                    #Si le mot est un objet
                    mot_info = self.associerMot(commande[indexMot])
                    if (mot_info and mot_info["categorie"] == "objets"):
                        fonction.append(mot_info["cle"])
                        indexMot +=1
                        
                        #Si objet trouvé , regarder si il y a une couleur juste après
                        if(indexMot<len(commande)):
                            couleur_info = self.associerMot(commande[indexMot])
                            if(couleur_info and couleur_info["categorie"] == "couleurs"):
                                fonction.append(couleur_info["cle"])
                                indexMot +=1
                        retour.append(fonction)
                    #Si le mot est une couleur
                    elif (mot_info and mot_info["categorie"] == "couleurs"):
                        fonction.append(mot_info["cle"])
                        indexMot+=1
                        retour.append(fonction)
            #Si le mot est une couleur toute seule, sans action à faire "ex : jusqu'à, cherche ...  : la sortir"
            elif mot in self.dico.get('couleurs',[]):
                indexMot+=1
            else:
                retour.append(mot)
                indexMot+=1
                
        return retour
    
    #dans envoyer : if(isinstance mot, list)
    def traiterAction(self,commandeComplexe : list): #On sait qu'on est dans une requête action
        #On est dans le cas ou la commande a déjà été filtrée ect.. les fonction à réaliser sont de la forme ["chercher","balle","rouge"]
        if len(commandeComplexe) < 2:
            print("Commande incomplète :", commandeComplexe)
            return
    
        premierMot = commandeComplexe[1]
        
        typePremierMot = self.associerMot(premierMot) #chercher balle => balle
        if not typePremierMot:
            print(f"Mot non reconnu : {premierMot}")
            return
        if(typePremierMot):
            if(typePremierMot["categorie"] == "couleurs"):
                self.algorithmes.chercherCouleur(premierMot)
            elif(typePremierMot["categorie"]=="objets" and len(commandeComplexe)==2):
                self.algorithmes.chercherForme(premierMot)
            elif(typePremierMot["categorie"]=="objets" and len(commandeComplexe)==3):
                self.algorithmes.chercherFormeAvecCouleur(premierMot,commandeComplexe[2])
                  
    def ecrireCommande(self, path: str,commande: list):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Le fichier {path} n'existe pas.")
        commande = ' '.join(commande)
        commande = commande + " S\n"
        with open(path, 'w', encoding='utf-8') as file:
            file.write(commande)

    def pilotageVocal(self, language="fr-FR"):
    
        print("Démarrage de la reconnaissance vocale...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Parlez maintenant...")
            audio_data = r.listen(source)
            print("Traitement de l'audio...")

        try:
            result = r.recognize_google(audio_data, language="fr-FR")
            print(result)  # On imprime dans stdout au lieu d’écrire dans un fichier
        except Exception as e:
            print(f"[ERREUR] {e}")
            exit(1)  # code d'erreur en cas d'échec

        texte = result.strip().replace("'", " ").lower().split()
        print("Texte reconnu :", texte)

        motsFiltres = self.filtrerMots(texte)
        print(" Mots filtrés :", motsFiltres)

        text = " ".join(str(c) for c in motsFiltres)
        self.robotVocal(text)
        requete = self.transformationRequeteCommande(motsFiltres)
        print(" Requête à envoyer :", requete, "| taille :", len(requete))

        self.envoyerCommande(requete)



    def recupererCommandeVocale(self, path: str) -> list: #Non traitée
            if not os.path.exists(path):
                raise FileNotFoundError(f"Le fichier {path} n'existe pas.")
            with open(path, 'r', encoding='utf-8') as file:
                commande = file.read().strip().replace("'", " ").split()
            return commande

    def pilotageTextuel(self, commande):
        #print(sr.Microphone.list_microphone_names())
        print(sr.__file__)
        commande = commande.strip().replace("'", " ").split()
        print("commande : ",commande)
        commandeFiltree = self.filtrerMots(commande)
        print("Commande filtree : ",commandeFiltree)
        
        #text = " ".join(str(c) for c in commandeFiltree)
        requeteCommande = self.transformationRequeteCommande(commandeFiltree)
        if(requeteCommande == []):
            self.robotVocal("Je n'ai pas compris la commande")
            return
        print("commande à effectuer : ",requeteCommande)
        self.envoyerCommande(requeteCommande)
        
    def robotVocal(self, text):
            speech = gTTS(text, lang="fr", slow=False)
            speech_file = 'speech.mp3'
            speech.save(speech_file)
            subprocess.run(
                ['mpg123', speech_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
    
        
        
    def envoyerCommande(self, commande):
        #if not os.path.exists(path):
         #   raise FileNotFoundError(f"Le fichier{path} n'existe pas.")
        #with open(path,'r',encoding='utf8') as file:
         #   commande = file.read().strip().split()
        for action in commande:
            if(isinstance(action,list)):
                self.traiterAction(action)
            else:
                print("action a envoyer :",action,"XX")
                action+="\n"
                self.bt.send(action)
                while(not self.bt.read()=="1"):
                    pass
        self.bt.send(" S\n")
        self.robotVocal("J'ai fini.")
        

    def tstAutonome(self):
        commande = "avance de 100m puis avance de 200 centimètres puis cherche une balle, puis cherche un carré bleu puis cherche une couleur verte"
        #commande = "cherche balle"
        commande = commande.strip().replace("'", " ").split()
        print("commande : ",commande)
        commandeFiltree = self.filtrerMots(commande)
        print("Commande filtree : ",commandeFiltree)
        commandeAutonome = self.commandeAutonome(commandeFiltree)
        print("Commande autonome : ",commandeAutonome)
        commandeNeg = self.traitementNegations(commandeAutonome)
        print("Commande neg : ",commandeNeg)
        RC = self.transformationRequeteCommande(commandeFiltree)
        print("RC",RC)
        motRetour = []
        for mots in RC:
            if(isinstance(mots,list)):
                self.traiterAction(mots)
            else:
                print(mots)

        
        
#AJOUTER UNE FONCTION du type : si le mot courant est une liste alors : Si il y a 1 argument et que c'est un objet : appeler code C : chercherObjet, couleur : chercherCouleur, 2 arguments : chercherObjetAvecCouleur
if __name__ == '__main__':
  requete = GestionRequest()
  requete.tstAutonome()

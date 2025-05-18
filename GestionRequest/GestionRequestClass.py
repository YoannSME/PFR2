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
        self.distance_defaut = 100
        self.angle_defaut = 90
        self.angle_defaut_zigzag = 45
        self.dico = self.chargerDictionnaire(self.pathDico)
        self.algorithmes = AlgorithmeRecherche(bt, flask)
        self.bt = bt
        self.flask = flask

    def chargerDictionnaire(self, path: str) -> dict:
        """Charge le dictionnaire (format JSON) contenant tous les mots reconnus par le robot
        :param path: chemin vers le fichier JSON
        :return: dictionnaire contenant les mots et leurs catégories
        """
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Le fichier {path} n'existe pas.")
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def recupererNombre(self, mot: str) -> int:
        """Récupère le potentiel nombre contenu dans une chaîne de caractères
        :param mot: chaîne de caractères contenant un nombre
        :return: le nombre entier contenu dans la chaîne de caractères ou 0 si aucun nombre n'est trouvé
        """
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
        """Convertit une valeur numérique en fonction de son unité
        :param nombre: valeur numérique à convertir 
        :param unite: unité de la valeur numérique
        :return: valeur numérique convertie
        """
        print("convert : nb = ",nombre, " unite = ", unite)
        if(unite == "centimetres" or unite == "c"):
            return nombre
        elif(unite == "metre" or unite == "m"):
            return nombre*100

        return nombre

    def associerMot(self, mot: str) -> dict | None:
        """Cherche le mot dans le dictionnaire et retourne la catégorie, la clé et la valeur associée si il est présent
        :param mot: mot à associer
        :return: dictionnaire contenant la catégorie, la clé et la valeur associée au mot
        """
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
        """Récupère le paramètre suivant dans la requête filtrée
        :param requete_filtree: requête filtrée
        :param indice: indice du mot actuel dans la requête filtrée
        :param defaut: valeur par défaut à retourner si aucun paramètre n'est trouvé
        :return: le paramètre suivant ou la valeur par défaut
        """
        
        if indice + 1 < len(requete_filtree) and isinstance(requete_filtree[indice + 1], int):
            return self.recupererNombre(requete_filtree[indice + 1])
        return defaut

    def filtrerMots(self, requete: list) -> list:
        """ Garde seulement les mots d'intérêts dans une requête.

    :param requete: Liste de mots à filtrer.
    :param dico: Dictionnaire contenant les associations de mots.

    :return: Liste de mots filtrés.
    """
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
        """Traite les négations dans la requête
        :param requete: requête à traiter   
        :return: requête traitée sans les mots affectés par les négations
        """
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
        """Transforme la requête filtrée en une liste de commandes compréhensibles et exécutables par le robot
        :param requete_filtree: requête filtrée
        :return: liste de commandes
        """
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
        return self.hasCommandeComplexeommandeComplexe(commandeSansNegations)
    
    def hasCommandeComplexe(self,commande : list):
        """Vérifie si une commande complexe (de recherche d'objet) est présente dans la liste de commandes
        :param commande: liste de commandes
        :return: liste de commandes avec la ou les commandes complexes mises en forme pour le robot
        """
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
    

    def traiterAction(self,commandeComplexe : list): 
        """Traite une action complexe (de recherche d'objet) et appelle la fonction correspondante dans l'algorithme de recherche
        :param commandeComplexe: liste de commandes complexes
        :return: None
        """
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
                  

    def pilotageVocal(self, language="fr-FR"):
        """Lance la reconnaissance vocale et traite la commande vocale puis l'envoie au robot
        :param language: langue de la reconnaissance vocale 
        :return: None
        """
        print("Démarrage de la reconnaissance vocale...")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Parlez maintenant...")
            audio_data = r.listen(source)
            print("Traitement de l'audio...")
        try:
            result = r.recognize_google(audio_data, language="fr-FR")
        except Exception as e:
            print(f"[ERREUR] {e}")

        self.pilotageTextuel(result)

    def pilotageTextuel(self, commande):
        """
        Traite une commande textuelle et l'envoie au robot.
        :param commande: commande textuelle brute (chaîne de caractères)
        :return: None
        """
        if not commande or not isinstance(commande, str):
            self.robotVocal("Commande invalide.")
            return

        print(f"[INFO] Commande textuelle reçue : {commande}")
        commande = commande.strip().replace("'", " ").lower().split()
        commandeFiltree = self.filtrerMots(commande)
        print(f"[INFO] Mots filtrés : {commandeFiltree}")
        requeteCommande = self.transformationRequeteCommande(commandeFiltree)

        if not requeteCommande:
            print("[INFO] Aucune commande comprise.")
            self.robotVocal("Je n'ai pas compris la commande.")
            return

        print(f"[INFO] Commande envoyée : {requeteCommande}")
        self.envoyerCommande(requeteCommande)
        
    def robotVocal(self, text):
            speech = gTTS(text, lang="fr", slow=False)
            # Save the audio file to a temporary file
            speech_file = 'speech.mp3'
            speech.save(speech_file)
            # Play the audio file
            os.system('mpg123 ' + speech_file)
            
    def envoyerCommande(self, commande : list):
        """Envoie la commande au robot via Bluetooth
        :param commande: liste de commandes à envoyer
        :return: None
        """
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

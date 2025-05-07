import os
import json
import speech_recognition as sr
import pyaudio
from gtts import gTTS

pathRequete = os.path.abspath("requete.txt")
pathDico = os.path.abspath("Dictionnaire.json")

class InterpreteurCommandeVocale:
    def __init__(self, dico_path: str):
        self.distance_defaut = 100
        self.angle_defaut = 90
        self.angle_defaut_zigzag = 45
        self.dico = self.chargerDictionnaire(dico_path)

    def chargerDictionnaire(self, path: str) -> dict:
        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Le fichier {path} n'existe pas.")
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def recupererNombre(self, mot) -> int:
        mot = str(mot)
        nombre = 0
        est_dans_un_nombre = False
        for lettre in mot:
            if lettre.isdigit():
                nombre = nombre * 10 + int(lettre)
                est_dans_un_nombre = True
            elif est_dans_un_nombre:
                break
        return nombre

    def associerMot(self, mot: str) -> dict | None:
        if mot in self.dico.get('commandesSpeciales', {}):
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
        for mot in requete:
            if self.associerMot(mot) is not None:
                retour.append(mot)
            nb = self.recupererNombre(mot)
            if nb != 0:
                retour.append(nb)
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
                        param = distance if cmd in ["avance", "recule"] else self.angle_defaut_zigzag
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
                    commandes_finales.append(requete_filtree[indice])

            indice += 1
        return self.traitementNegations(commandes_finales)
    
    def ecrireCommande(self, path: str,commande: list):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Le fichier {path} n'existe pas.")
        commande = ' '.join(commande)
        print(commande)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(commande)
        
        
    def pilotageVocal(self):
        r = sr.Recognizer()
        micro = sr.Microphone()
        with micro as source:
            print("Speak!")
            audio_data = r.listen(source)
            print("End!")
        result = r.recognize_google(audio_data, language="fr-FR")
        # pour une reconnaissance de la parole en anglais
        # result = r.recognize_google(audio_data, language="en-EN"
        motsFiltres = self.filtrerMots(commande)
        result = self.transformationRequeteCommande(motsFiltres)
        self.ecrireCommande(pathRequete, result)

    def recupererCommandeVocale(self, path: str) -> list: #Non traitée
            if not os.path.exists(path):
                raise FileNotFoundError(f"Le fichier {path} n'existe pas.")
            with open(path, 'r', encoding='utf-8') as file:
                commande = file.read().strip().replace("'", " ").split()
            return commande

    def pilotageManuel(self):
        commande = input("Entrez la commande : ")
        commande = commande.strip().replace("'", " ").split()
        
        commandeFiltree = self.filtrerMots(commande)
        requeteCommande = self.transformationRequeteCommande(commandeFiltree)
        self.ecrireCommande(pathRequete, requeteCommande)


# Exemple d’utilisation
if __name__ == "__main__":
    interpreteur = InterpreteurCommandeVocale(pathDico)

    commande = interpreteur.pilotageVocal()


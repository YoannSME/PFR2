import json

class Traduction:
    """
    Classe Traduction

    Date : Avril 2025
    Auteur : Axel Sichi

    Cette classe permet de gérer les traductions d'une interface en fonction de la langue choisie. Elle charge les traductions depuis un fichier JSON et offre des méthodes pour traduire des chaînes de caractères et changer de langue.

    Méthodes principales :
    - __init__ : Initialise la classe avec une langue par défaut (français) et charge les traductions à partir d'un fichier JSON.
    - charger_traductions : Charge les traductions depuis le fichier JSON spécifié, en cas d'erreur, renvoie un dictionnaire vide.
    - traduire : Renvoie la traduction d'une clé donnée en fonction de la langue active, ou la clé elle-même si la traduction n'est pas disponible.
    - changer_langue : Permet de changer la langue de traduction active si la langue est disponible dans les traductions.
    """
    def __init__(self, langue="fr-FR"):
        self.langue = langue
        self.traductions = self.charger_traductions()

    def charger_traductions(self):
        try:
            with open("Interface/TraductionFile.json", "r", encoding="utf-8") as fichier:
                return json.load(fichier)
        except FileNotFoundError:
            print("Fichier de traduction non trouvé !")
            return {}

    def traduire(self, cle):
        return self.traductions.get(self.langue, {}).get(cle, cle)

    def changer_langue(self, nouvelle_langue):
        if nouvelle_langue in self.traductions:
            self.langue = nouvelle_langue
        else:
            print(f"Langue '{nouvelle_langue}' non disponible !")

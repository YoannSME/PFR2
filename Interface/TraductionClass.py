import json

class Traduction:
    def __init__(self, langue="fr"):
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

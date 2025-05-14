import json

class Configuration:
    def __init__(self, configPath, valuePath):
        self.configPath = configPath
        self.valuePath = valuePath
        self.configuration = self.charger_configuration()
        self.valeurs_possibles = self.charger_valeur_possible()

    def charger_configuration(self):
        try:
            with open(self.configPath, "r", encoding="utf-8") as fichier:
                return json.load(fichier)
        except FileNotFoundError:
            print("Fichier de configuration non trouvé !")
            return {}
        
    def charger_valeur_possible(self):
        try:
            with open(self.valuePath, "r", encoding="utf-8") as fichier:
                return json.load(fichier)
        except FileNotFoundError:
            print("Fichier de configuration non trouvé !")
            return {}

    def sauvegarder_configuration(self):
        try:
            with open(self.configPath, "w", encoding="utf-8") as fichier:
                json.dump(self.configuration, fichier, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    def get(self, cle):
        return self.configuration.get(cle, None)

    def set(self, cle, valeur):
        if cle in self.configuration and valeur not in self.valeurs_possibles[cle]:
            print(f"!!!! : {self.valeurs_possibles[cle]}")
            return None
        self.configuration[cle] = valeur
        self.sauvegarder_configuration()

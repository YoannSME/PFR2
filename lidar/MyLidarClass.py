from rplidar import RPLidar
import numpy as np
import csv


"""
Classe MyLidar

Date : Fev 2025
Auteur : Axel Sichi

Cette classe étend la classe RPLidar (roboticia) pour gérer la communication avec un lidar RPLidar et faciliter la récupération des données de scan.
Elle permet de collecter des mesures à partir du lidar, de les convertir en coordonnées cartésiennes et de les enregistrer sous forme de fichier CSV.

Méthodes principales :
- __convert_lidar_to_cartesian : Convertit les données de mesure polaires (angle, distance) en coordonnées cartésiennes (x, y).
- getScanData : Récupère un nombre spécifié de mesures du lidar et les convertit en coordonnées cartésiennes si nécessaire.
- save_to_csv : Enregistre les données de mesure sous forme de fichier CSV.

Cette classe repose sur la bibliothèque `rplidar` (roboticia) pour la communication avec le lidar et la gestion des mesures.
"""

class MyLidar(RPLidar):
    def __init__(self, port, baudrate=115200, timeout=1, logger=None):
        super().__init__(port, baudrate, timeout, logger)

    def __convert_lidar_to_cartesian(self, data):
        angles_rad = np.radians(data[:, 0])
        distances = data[:, 1]
        
        x = np.cos(angles_rad) * distances
        y = np.sin(angles_rad) * distances

        return np.column_stack((x, y))
      
    def getScanData(self, nbData, format=0):
        data = []
        for measurment in self.iter_measures():
                if measurment[1] >= 10:
                    data.append(measurment)
                if (len(data)>= nbData):
                    break
        self.stop()
        self.stop_motor()
        data = np.array(data)[:, 2:]
        if format == 1: data = self.__convert_lidar_to_cartesian(data)
        return data
    
    def save_to_csv(self, filename, data):
        """Enregistre les données sous forme de CSV."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["X", "Y"])  # En-têtes
            writer.writerows(data)
        print(f"Données enregistrées dans {filename}")
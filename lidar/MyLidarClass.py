from rplidar import RPLidar
import numpy as np
import csv
import matplotlib.pyplot as plt

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
    
    def __clear_islate_pack(self, nuage_points, epsilon=500, min_pts=10):
        def compter_voisins(i):
            """Retourne le nombre de voisins d'un point donné."""
            dist = np.linalg.norm(nuage_points - nuage_points[i], axis=1)
            return np.sum(dist <= epsilon)  # Compter les voisins dans le rayon epsilon
        
        # Filtrer les points qui ont au moins `min_pts` voisins
        voisins = np.array([compter_voisins(i) for i in range(len(nuage_points))])
        points_filtres = nuage_points[voisins >= min_pts]

        return points_filtres        
      
    def getScanData(self, nbData, format=0):
        data = []
        for measurment in self.iter_measures():
            if measurment[1] >= 10 and measurment[3] >=10:
                data.append(measurment)
                if (len(data)>= nbData):
                    break
        self.stop()
        self.stop_motor()
        data = np.array(data)[:, 2:]
        if format == 1: data = self.__clear_islate_pack(self.__convert_lidar_to_cartesian(data))
        return data
    
    def save_to_csv(self, filename, data):
        """Enregistre les données sous forme de CSV."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["X", "Y"])  # En-têtes
            writer.writerows(data)
        print(f"Données enregistrées dans {filename}")
        
# myLidar = MyLidar("COM6")
# data = myLidar.getScanData(200, format=1)

# plt.scatter(data[:, 0], data[:, 1])
# plt.show()
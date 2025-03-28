from FindTransformationClass import FindTransformation

from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import numpy as np
import csv as csv

"""
Classe Cartographie

Date : Mars 2025
Auteur : Axel Sichi

Cette classe permet de gérer la cartographie 2D à partir des données provenant d'un lidar.
Elle inclut des méthodes pour traiter les nuages de points, effectuer des transformations, et 
mettre à jour la carte au fur et à mesure des nouveaux scans. Elle utilise l'algorithme de SLAM 
pour estimer la position et l'orientation du robot dans l'environnement.

Méthodes principales :
- __apply_transformation_matrix : Applique une matrice de transformation sur un ensemble de points.
- __clean_map_by_density : Filtre les points en fonction de leur densité dans l'environnement.
- __convert_cartesian_to_polar : Convertit un nuage de points des coordonnées cartésiennes aux coordonnées polaires.
- __convert_polar_to_cartesian : Convertit un nuage de points des coordonnées polaires aux coordonnées cartésiennes.
- __remove_incoherent_point : Supprime les points incohérents d'un scan en comparant avec la carte actuelle.
- __ajouter_scan : Ajoute un nouveau scan à la carte en appliquant une transformation et un filtrage de densité.
- save_to_csv : Enregistre les données de la carte sous forme de fichier CSV.
- update_carte : Met à jour la carte avec les nouvelles données de scan et ajuste la position du robot.

Cette classe repose sur des outils comme MyLidar pour interagir avec le lidar et FindTransformation pour estimer les transformations entre les scans successifs.
"""


class Cartographie():
    def __init__(self):
        self.pos = np.eye(3)
        self.carte = np.eye(1)
        
        #For Plotting :
        self.estimateSizeOfRoom = None
        self.fig, self.ax = plt.subplots()
        self.scatter = None
        plt.ion()
        
    def __apply_transformation_matrix(self, points, transformation_matrix):
        # Convertir les points en coordonnées homogènes (ajouter une colonne de 1)
        ones = np.ones((points.shape[0], 1))
        points_homogeneous = np.hstack((points, ones))  # Passage en coordonnées homogènes

        # Appliquer la transformation : T * P
        transformed_points_homogeneous = np.dot(transformation_matrix, points_homogeneous.T).T  # Transposé pour correspondre aux dimensions

        # Convertir de retour en coordonnées cartésiennes (en enlevant la colonne homogène)
        transformed_points = transformed_points_homogeneous[:, :2]

        return transformed_points
    
    def __clean_map_by_density(self, k=20, low_percentile=1, high_percentile=90):
        """
        Nettoie un nuage de points 2D en supprimant les points dans les zones
        de forte et faible densité.
        
        Paramètres:
        - scan : np.array de shape (N, 2) contenant les points (x, y)
        - k : Nombre de voisins pour estimer la densité
        - low_percentile : Seuil bas pour supprimer les points isolés
        - high_percentile : Seuil haut pour supprimer les points trop denses
        
        Retourne :
        - scan filtré
        """
        if len(self.carte) < k:
            return self.carte  # Pas assez de points pour estimer la densité
        
        # Calcul des distances aux k plus proches voisins
        nbrs = NearestNeighbors(n_neighbors=k).fit(self.carte)
        distances, _ = nbrs.kneighbors(self.carte)
        
        try: # J'ai pas réussi à fix les warnings
            # Densité estimée comme l'inverse de la distance moyenne aux k voisins
            density = 1 / np.mean(distances[:, 1:], axis=1)  # On ignore la première distance (le point lui-même)
        except:
            pass
        
        # Définition des seuils relatifs
        low_thresh = np.percentile(density, low_percentile)
        high_thresh = np.percentile(density, high_percentile)
        
        # Filtrage des points
        mask = (density > low_thresh) & (density < high_thresh)
        return self.carte[mask]

    def __convert_cartesian_to_polar(self, points):
        angles = np.degrees(np.arctan2(points[:, 1], points[:, 0]))  # Convertit en degrés
        distances = np.sqrt(points[:, 0]**2 + points[:, 1]**2)  # Norme euclidienne
        
        return np.column_stack((angles, distances))

    def __convert_polar_to_cartesian(self, data):
        angles_rad = np.radians(data[:, 0])
        distances = data[:, 1]
        
        x = np.cos(angles_rad) * distances
        y = np.sin(angles_rad) * distances

        return np.column_stack((x, y))

    def __remove_incoherent_point(self, newPoints):
        polar_carte = self.__convert_cartesian_to_polar(self.carte)
        polar_newPoints = self.__convert_cartesian_to_polar(newPoints)  # (angle, dist)

        # Trier la carte par angle pour une recherche plus efficace
        polar_carte = polar_carte[np.argsort(polar_carte[:, 0])]

        for angle_new, dist_new in polar_newPoints:
            # Trouver les points de la carte dont l'angle est proche (±1°)
            mask = (polar_carte[:, 0] >= angle_new - 2) & (polar_carte[:, 0] <= angle_new + 2)
            nearby_points = polar_carte[mask]

            for angle_carte, dist_carte in nearby_points:
                # Si un point de la carte est plus proche que le nouveau point, on le supprime
                if dist_carte < dist_new:
                    polar_carte = polar_carte[~((polar_carte[:, 0] == angle_carte) & (polar_carte[:, 1] == dist_carte))]

        self.carte = self.__convert_polar_to_cartesian(polar_carte)

    def __ajouter_scan(self, newScan, TX):
        
        newScan = self.__apply_transformation_matrix(newScan, TX)
        self.__remove_incoherent_point(newScan)
        
        self.carte = self.__clean_map_by_density()
        
        self.carte = np.vstack((self.carte, newScan))
       
    def __forPlotting(self):
        estimate_rotation, estimate_translation = FindTransformation.extract_rotation_translation(None, self.pos)
        estimateSizeOfRoom = ((np.min(self.carte[0]), np.max(self.carte[0])), (np.min(self.carte[1]), np.max(self.carte[1])))
        x, y = estimate_translation  # Position de l'objet
        theta = estimate_rotation  # Orientation en radians
        
        scale = 300  # Échelle des flèches
        dx, dy = scale * np.cos(theta), scale * np.sin(theta)
        
        # Axe X (rouge) et Axe Y (Vert) de l'objet
        self.ax.clear()
        if (self.estimateSizeOfRoom != None):
            self.ax.set_xlim(self.estimateSizeOfRoom[0][0], self.estimateSizeOfRoom[0][1])
            self.ax.set_ylim(-self.estimateSizeOfRoom[1][0], self.estimateSizeOfRoom[1][1])
            
        plt.quiver(x, y, dx, dy, color='r', angles='xy', scale_units='xy', scale=1, width=0.002)
        plt.quiver(x, y, -dy, dx, color='g', angles='xy', scale_units='xy', scale=1, width=0.002)
        
        self.ax.scatter(*zip(*self.carte), s=5, c='blue')
        plt.scatter(self.carte[:, 0], self.carte[:, 1], color='black')
        plt.title(f"Estimation de la position:\nOrientation: {np.rad2deg(estimate_rotation):.2f}°        "
                f"Position x : {estimate_translation[0]:.2f}mm  y : {estimate_translation[1]:.2f}mm")
        self.fig.canvas.draw()
        plt.pause(1)
    
    def update_carte(self, new_data, ploting=False, debugPloting=False):
        
        if self.carte.shape[0] <= 1:
            self.carte = new_data
        else:
            ft = FindTransformation(new_data, self.carte, filterStrenght=0.1)
            self.pos = ft.get_transform(ploting=debugPloting, initial_transformation_matrix=self.pos)
            self.__ajouter_scan(new_data, self.pos)
        
            if ploting:
                self.__forPlotting()
            
    def save_to_csv(self, filename, data):
        """Enregistre les données sous forme de CSV."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["X", "Y"])  # En-têtes
            writer.writerows(data)
        print(f"Données enregistrées dans {filename}")
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt


"""
Classe FindTransformation

Date : Mars 2025
Auteur : Axel Sichi

Cette classe implémente un algorithme permettant de trouver la transformation rigide (rotation et translation) entre deux nuages de points 2D (scans lidar).
Elle utilise des techniques telles que la rotation brute, le rapprochement des points les plus proches (ICP), et l'estimation de la transformation rigide pour aligner deux scans.

Méthodes principales :
- __remove_farthest_points : Filtre les points les plus éloignés entre deux nuages de points.
- __apply_transformation_matrix : Applique une transformation rigide (matrice de transformation) à un nuage de points.
- __apply_rotation : Applique une rotation 2D à un ensemble de points autour de l'origine.
- __rotate_scan : Effectue une recherche de rotation optimale entre deux scans.
- __apply_icp : Applique l'algorithme ICP pour affiner l'alignement des deux scans.
- __estimate_rigid_transform : Estime la transformation rigide (rotation + translation) entre deux ensembles de points.
- extract_rotation_translation : Extrait la rotation et la translation d'une matrice de transformation.
- get_transform : Calcule la transformation finale en combinant rotation et translation, et affiche les scans alignés.

Cette classe repose sur des méthodes de géométrie 2D et d'optimisation pour résoudre le problème d'alignement de nuages de points lidar.
"""

class FindTransformation():
    def __init__(self, scan1, scan2, filterStrenght=0.2):
        self.src = scan1
        self.dst = scan2
        self.filterStrenght = filterStrenght
        
        self.scan1 = None
        self.scan2 = None

    def __remove_farthest_points(self, points1, points2, percentage=0.1):
        """
        Supprime un pourcentage donné des points les plus éloignés entre deux nuages de points.
        
        Paramètres :
            points1 : np.ndarray de forme (N,2) - Premier nuage de points
            points2 : np.ndarray de forme (M,2) - Deuxième nuage de points
            percentage : float - Pourcentage de points à supprimer
        
        Retourne :
            points1_filtered, points2_filtered : np.ndarray - Nuages de points filtrés
        """
        distances = cdist(points1, points2)  # Calcul des distances entre chaque paire de points
        min_distances_1 = np.min(distances, axis=1)  # Distance minimale de chaque point de points1 à points2
        min_distances_2 = np.min(distances, axis=0)  # Distance minimale de chaque point de points2 à points1

        # Déterminer le nombre de points à garder
        n_keep_1 = int(len(points1) * (1 - percentage))
        n_keep_2 = int(len(points2) * (1 - percentage))

        # Trier les indices des points en fonction de leur distance et ne garder que les plus proches
        keep_indices_1 = np.argsort(min_distances_1)[:n_keep_1]
        keep_indices_2 = np.argsort(min_distances_2)[:n_keep_2]

        filtered_scan1 = points1[keep_indices_1]
        filtered_scan2 = points2[keep_indices_2]
        
        return filtered_scan1, filtered_scan2

    def __apply_transformation_matrix(self, points, transformation_matrix):
        # Convertir les points en coordonnées homogènes (ajouter une colonne de 1)
        ones = np.ones((points.shape[0], 1))
        points_homogeneous = np.hstack((points, ones))  # Passage en coordonnées homogènes

        # Appliquer la transformation : T * P
        transformed_points_homogeneous = np.dot(transformation_matrix, points_homogeneous.T).T  # Transposé pour correspondre aux dimensions

        # Convertir de retour en coordonnées cartésiennes (en enlevant la colonne homogène)
        transformed_points = transformed_points_homogeneous[:, :2]

        return transformed_points

    def __apply_rotation(self, points, rotation_angle):
        """ Applique une rotation autour de l'origine (0, 0) pour un ensemble de points. """
        # Calcul de la matrice de rotation 2D
        rotation_matrix = np.array([[np.cos(rotation_angle), -np.sin(rotation_angle)], 
                                    [np.sin(rotation_angle), np.cos(rotation_angle)]])
        # Appliquer la rotation aux points
        return np.dot(points, rotation_matrix.T)

    def __rotate_scan(self, points1, points2, rotation_steps):
        min_error = float('inf')
        best_rotation = 0

        for rotation in np.linspace(0, 2 * np.pi, rotation_steps):
            # Appliquer la rotation aux scans centrés
            rotated_points1 = self.__apply_rotation(points1, rotation)

            # Calcul de l'erreur basée sur la distance la plus proche
            distances = cdist(rotated_points1, points2)
            min_distances = np.min(distances, axis=1)  # Distance minimale pour chaque point de scan1
            mean_min_distance = np.mean(min_distances)

            if mean_min_distance < min_error:
                min_error = mean_min_distance
                best_rotation = rotation
            
        return best_rotation, min_error

    def __apply_icp(self, scan1_transform, temp_scan2, nbIter):
        """
        Applique l'algorithme ICP (Iterative Closest Point) pour affiner l'alignement des nuages de points.
        Retourne la matrice de transformation globale (rotation + translation).
        """
        for _ in range(nbIter):
            # Trouver les correspondances (le plus proche voisin)
            distances = cdist(scan1_transform, temp_scan2)
            closest_points_idx = np.argmin(distances, axis=1)
            correspondences = temp_scan2[closest_points_idx]
            
            # Calculer la transformation entre les deux ensembles de points (rotation et translation)
            centroid1 = np.mean(scan1_transform, axis=0)
            centroid2 = np.mean(correspondences, axis=0)
            
            # Calculer la matrice de covariance
            H = np.dot((scan1_transform - centroid1).T, (correspondences - centroid2))
            
            # Calculer la décomposition en valeurs singulières (SVD)
            U, _, Vt = np.linalg.svd(H)
            R = np.dot(Vt.T, U.T)  # Matrice de rotation
            t = centroid2 - np.dot(R, centroid1)  # Vecteur de translation

            # Appliquer la rotation et la translation sur scan1
            scan1_transform = np.dot(scan1_transform, R.T) + t

        
        return scan1_transform

    def __estimate_rigid_transform(self, A, B):
        """
        Estime la transformation rigide (rotation + translation) qui aligne A sur B.
        A et B doivent être des tableaux numpy de taille (N,2), où N est le nombre de points.
        
        Retourne R (matrice de rotation 2x2) et t (vecteur de translation 2x1).
        """
        assert A.shape == B.shape, "Les deux nuages de points doivent avoir la même taille"
        
        # 1. Calcul des centres de gravité
        centroid_A = np.mean(A, axis=0)
        centroid_B = np.mean(B, axis=0)
        
        # 2. Centrage des nuages de points
        A_centered = A - centroid_A
        B_centered = B - centroid_B
        
        # 3. Calcul de la matrice de covariance
        H = A_centered.T @ B_centered
        
        # 4. Décomposition SVD
        U, _, Vt = np.linalg.svd(H)
        
        # 5. Calcul de la rotation
        R = Vt.T @ U.T
        
        # Correction si nécessaire pour éviter la réflexion
        if np.linalg.det(R) < 0:
            Vt[-1, :] *= -1
            R = Vt.T @ U.T
        
        # 6. Calcul de la translation
        t = centroid_B - R @ centroid_A
        
        transformation_matrix = np.eye(3)  # Matrice identité 3×3
        transformation_matrix[:2, :2] = R  # Remplacer la sous-matrice 2×2 par la rotation
        transformation_matrix[:2, 2] = t   # Ajouter la translation
        
        return transformation_matrix

    def extract_rotation_translation(self, T):
        assert T.shape == (3, 3), "La matrice doit être de taille 3x3"
        
        # Extraire la rotation
        R = T[:2, :2]
        
        # Calculer l'angle de rotation (theta)
        theta = np.arctan2(R[1, 0], R[0, 0])
        
        # Extraire la translation
        t = T[:2, 2]
        
        return theta, t

    def get_transform(self, rotation_steps=360, ICP_iter=300, initial_transformation_matrix=np.eye(3), ploting=False):
        """ Applique la translation et la rotation puis affiche les scans alignés. """
        
        # Trouver la meilleure rotation
        self.scan1 = self.__apply_transformation_matrix(self.src, initial_transformation_matrix)
        self.scan1, self.scan2 = self.__remove_farthest_points(self.scan1, self.dst, percentage=0.05)
        best_rotation, _ = self.__rotate_scan(self.scan1, self.scan2, rotation_steps)
        
        # Appliquer la rotation à scan1
        rotated_scan1 = self.__apply_rotation(self.scan1, best_rotation)
        
        ICP_rotated_scan1 = self.__apply_icp(rotated_scan1, self.scan2, nbIter=ICP_iter)
        clean_ICP_rotated_scan1, clean_scan2 = self.__remove_farthest_points(ICP_rotated_scan1, self.scan2, percentage=self.filterStrenght*2)
        clean_ICP2_ratated_scan1 = self.__apply_icp(clean_ICP_rotated_scan1, clean_scan2, nbIter=ICP_iter)
        
        
        first_transformation_matrix = self.__estimate_rigid_transform(self.scan1, ICP_rotated_scan1)
        second_transformation_matrix = self.__estimate_rigid_transform(clean_ICP_rotated_scan1, clean_ICP2_ratated_scan1)
        final_transformation_matrix = np.dot(initial_transformation_matrix,np.dot(first_transformation_matrix, second_transformation_matrix))
        
        if ploting:
            estimate_points = self.__apply_transformation_matrix(self.src, final_transformation_matrix)
            estimate_rotation, estimate_translation = self.extract_rotation_translation(final_transformation_matrix)
        
        
            # Affichage des résultats
            plt.figure(figsize=(6,6))
            
            plt.scatter(self.src[:, 0], self.src[:, 1], color='black', label='Source')
            plt.scatter(self.dst[:, 0], self.dst[:, 1], color='red', label='Destination')
            plt.scatter(estimate_points[:, 0], estimate_points[:, 1], color='green', label='Estimate')
            
            plt.legend()
            plt.title(f"Estimation Du Déplacement:\nRotation : {np.rad2deg(estimate_rotation):.2f}°        "
            f"Translation x : {estimate_translation[0]:.2f}mm  y : {estimate_translation[1]:.2f}mm")
            plt.show()
        
        return final_transformation_matrix

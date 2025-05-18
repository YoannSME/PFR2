#ifndef IMAGE_H
#define IMAGE_H

#include "../Objet/Objet.h"
#include <opencv2/opencv.hpp>
#include <../include/nlohmann/json.hpp>
#include <fstream>
#include <vector>

/**
 * @class GestionTraitementImage
 * @brief Classe chargée de la détection et du traitement d’objets dans une image en fonction de leur couleur et/ou forme.
 */
class GestionTraitementImage
{
private:
    /// Liste des couleurs que le système est capable de détecter.
    /// Cette liste est initialisée dans le Constructeur de la classe à partir du fichier JSON contenant le nom des couleurs et leurs seuils.
    std::vector<Couleur> couleursDetectables;

public:
    /// Constructeur de la classe
    GestionTraitementImage();

    /// Retourne la liste des couleurs détectables par le système
    std::vector<Couleur> getCouleursDetectables();

    /// Associe un nom de couleur à une instance de Couleur
    Couleur getCouleurAssocie(std::string_view nom);

    /// Associe un nom de forme à une instance de Forme
    Forme getFormeAssocie(std::string nomForme);

    /// Traite une image pour détecter tous les objets d'une certaine couleur
    std::vector<Objet> traiterSelonCouleur(cv::Mat &image, Couleur couleur);

    /// Traite une image pour détecter tous les objets d'une certaine forme
    std::vector<Objet> traiterSelonForme(cv::Mat &image, Forme forme);

    /// Traite une image pour détecter tous les objets (peu importe leur forme ou couleur)
    std::vector<Objet> traiterImageAll(cv::Mat &image);

    /// Cherche les objets ayant une couleur et une forme données dans une image
    std::vector<Objet> chercherObjetAvecCouleur(cv::Mat image, const std::string &couleur, const std::string &forme);

    /// Cherche les objets ayant une certaine couleur dans une image
    std::vector<Objet> chercherCouleur(cv::Mat image, const std::string &couleur);

    /// Cherche les objets ayant une certaine forme dans une image
    std::vector<Objet> chercherForme(cv::Mat image, const std::string &forme);

    /**
     * @brief Sauvegarde les résultats d'une détection dans un fichier JSON.
     * @param objets Vecteur d'objets détectés (avec leurs propriétés : position, forme, couleur, aire, etc.).
     * Le fichier JSON généré peut ensuite être utilisé pour des traitements ultérieurs, de la visualisation ou du débogage.
     */
    void sauvegarderResultats(const std::vector<Objet>& objets);
};

#endif

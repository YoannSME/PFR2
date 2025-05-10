#ifndef IMAGE_H
#define IMAGE_H

#include "Objet.h"
#include <opencv2/opencv.hpp>
#include <nlohmann/json.hpp>

#include <fstream>
#include <vector>

class GestionTraitementImage
{
private:
    std::vector<Couleur> couleursDetectables;

public:
    GestionTraitementImage();
    std::vector<Couleur> getCouleursDetectables();
    Couleur getCouleurAssocie(std::string_view nom);

    Forme getFormeAssocie(std::string nomForme);

    std::vector<Objet> traiterSelonCouleur(cv::Mat &image, Couleur);
    std::vector<Objet> traiterSelonForme(cv::Mat &image, Forme forme);
    std::vector<Objet> traiterImageAll(cv::Mat &image);
    std::vector<Objet> chercherObjetAvecCouleur(const std::string &path, const std::string &couleur, const std::string &forme);
    std::vector<Objet> chercherCouleur(const std::string &path,const std::string &couleur);
    std::vector<Objet> chercherForme(const std::string &path,const std::string &forme);
    //std::vector<Objet> chercherObjetAvecCouleurF(cv::Mat &image, const std::string &couleur, const std::string &forme);
 
    void sauvegarderResultats(const std::vector<Objet>& objets);

};

#endif
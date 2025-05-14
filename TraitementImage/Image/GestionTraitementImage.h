#ifndef IMAGE_H
#define IMAGE_H

#include "../Objet/Objet.h"
#include <opencv2/opencv.hpp>
#include <../include/nlohmann/json.hpp>

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
    std::vector<Objet> chercherObjetAvecCouleur(cv::Mat image,const std::string &couleur, const std::string &forme);
    std::vector<Objet> chercherCouleur(cv::Mat image,const std::string &couleur);
    std::vector<Objet> chercherForme(cv::Mat image,const std::string &forme);
    //std::vector<Objet> chercherObjetAvecCouleurF(cv::Mat &image, const std::string &couleur, const std::string &forme);
 
    void sauvegarderResultats(const std::vector<Objet>& objets);

};

#endif
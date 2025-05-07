#ifndef IMAGE_H
#define IMAGE_H

#include "Objet.h"
#include <opencv2/opencv.hpp>
#include <vector>

class Image{
    private:

    public:
        Image();
    std::vector<Objet> traiterSelonCouleur(cv::Mat &image,Couleur);
    std::vector<Objet> traiterSelonForme(cv::Mat &image,std::vector<Couleur> couleurs,Forme forme);
    std::pair<int, int> calculerDistanceCentre(Objet& objet, const cv::Mat &image);
std::pair<bool, std::pair<int, int>> objetPresent(cv::Mat &image, Forme forme, Couleur couleur);


};

#endif
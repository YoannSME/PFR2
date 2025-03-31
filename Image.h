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
    std::vector<Objet> traiterSelonForme(cv::Mat &image,std::vector<Couleur> couleurs);

};

#endif
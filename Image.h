#ifndef IMAGE_H
#define IMAGE_H

#include <opencv2/opencv.hpp>

enum Forme{
    BALLE,
    CARRE
};

class Image{
    private:

    public Image();


    cv::Mat traiterSelonCouleur(cv::Mat,Couleur);

    cv::Mat recupererForme(cv::Mat,Forme)

}
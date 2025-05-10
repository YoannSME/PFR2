#ifndef COULEUR_H
#define COULEUR_H

#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>

class Couleur
{
private:
    std::string nom;
    cv::Scalar couleurMin;
    cv::Scalar couleurMax;

public:
    Couleur(std::string nom,cv::Scalar couleurMin, cv::Scalar couleurMax);
    ~Couleur();
    std::string getNom() const;
    const cv::Scalar& getCouleurMin() const;
    const cv::Scalar& getCouleurMax() const;

    void setNom(std::string nom);
    void setCouleurMin(const cv::Scalar &couleurMin);
    void setCouleurMax(const cv::Scalar &couleurMax);
};

#endif

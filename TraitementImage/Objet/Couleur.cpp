#include "Couleur.h"

Couleur::Couleur(std::string nom,cv::Scalar couleurMin, cv::Scalar couleurMax)
    : nom(nom),couleurMin(couleurMin), couleurMax(couleurMax) {}

Couleur::~Couleur() {}


std::string Couleur::getNom() const {
    return nom;
}
const cv::Scalar& Couleur::getCouleurMin() const {
    return couleurMin;
}

const cv::Scalar& Couleur::getCouleurMax() const {
    return couleurMax;
}

void Couleur::setCouleurMin(const cv::Scalar &couleurMin) {
    this->couleurMin = couleurMin;
}

void Couleur::setCouleurMax(const cv::Scalar &couleurMax) {
    this->couleurMax = couleurMax;
}

void Couleur::setNom(std::string nom){
    this->nom = nom;
}

#include "Objet.h"

// Constructeur avec initialisation directe des attributs
Objet::Objet(int area, int x, int y, int w, int h, double cx, double cy,std::pair<int,int> distanceCentre,Forme forme,Couleur couleur)
    : area(area), x(x), y(y), w(w), h(h), cx(cx), cy(cy),distanceCentre(distanceCentre), forme(forme),couleur(couleur) {}

    Forme Objet::getFormeAssociee(std::string forme) {
        // Convertit la chaîne de caractères en minuscules pour une comparaison insensible à la casse
        std::transform(forme.begin(), forme.end(), forme.begin(), ::tolower);
        if (forme == "balle") {
            return Forme::BALLE;
        } else if (forme == "carre") {
            return Forme::CARRE;
        } else {
            return Forme::INCONNUE;
        }
    }


    std::string Objet::getNomAssociee(Forme forme) {
        switch (forme) {
            case Forme::BALLE: return "balle";
            case Forme::CARRE: return "carre";
            default: return "inconnue";
        }
    }

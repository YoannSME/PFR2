#ifndef OBJET_H
#define OBJET_H
#include "Couleur.h"

enum class Forme {
    INCONNUE,
    BALLE,
    CARRE
};


class Objet {
    private:
public:
    int area;
    int x, y, w, h;
    double cx, cy;   // Centroïde (centre géométrique)
    Forme forme;
    Couleur couleur;
    Objet(int area, int x, int y, int w, int h, double cx, double cy, Forme forme,Couleur couleur);

    std::string getForme(Forme forme){
        switch(forme){
            case Forme::BALLE:return "Balle";
            case Forme::CARRE:return "CARRE";
            case Forme::INCONNUE:return "INCONNUE";
            default: return"?";
        }
    }
};

#endif // OBJET_H

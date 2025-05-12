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
    std::pair<int,int> distanceCentre;
    Forme forme;
    Couleur couleur;
     // Distance entre le centre de l'image et le centre de l'objet
    Objet(int area, int x, int y, int w, int h, double cx, double cy,std::pair<int,int> distanceCentre, Forme forme,Couleur couleur);

    static Forme getFormeAssociee(std::string forme);

    static std::string getNomAssociee(Forme forme);
};

#endif // OBJET_H

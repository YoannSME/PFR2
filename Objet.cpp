#include "Objet.h"

// Constructeur avec initialisation directe des attributs
Objet::Objet(int area, int x, int y, int w, int h, double cx, double cy, Forme forme,Couleur couleur)
    : area(area), x(x), y(y), w(w), h(h), cx(cx), cy(cy), forme(forme),couleur(couleur) {}

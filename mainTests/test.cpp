#include "Objet.h"
#include "GestionTraitementImage.h"
#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>
#include "Couleur.h"

// SEUILS DE DETECTION A ADAPTER UNE FOIS QU'ON AURA LES DONNES DE LA CAMEAR
Couleur jaune("Jaune", cv::Scalar(13, 97, 67), cv::Scalar(42, 255, 255));
Couleur bleu("Bleu", cv::Scalar(96, 105, 70), cv::Scalar(114, 231, 186));
Couleur orange("Orange", cv::Scalar(2, 113, 27), cv::Scalar(16, 255, 148));
Couleur vert("Vert", cv::Scalar(40, 54, 57), cv::Scalar(70, 255, 209));

int main(int argc, char **argv)
{
    GestionTraitementImage controleImage;

    cv::Mat frame;
    cv::VideoCapture cap;
    cap.open(0);
    if (!cap.isOpened())
    {
        std::cerr << "Erreur : Impossible d'ouvrir la caméra !" << std::endl;
        return -1;
    }

    //std::vector<Couleur> couleurs = {jaune, bleu, orange,vert};
    while (1)
    {
        cap >> frame;
        if (frame.empty())
            break;

        std::vector<Objet> objets = controleImage.chercherObjetAvecCouleurF(frame,"vert","balle");
        std::cout<<"Nombre d'objets trouvés : " << objets.size() << std::endl;
        //Couleur couleurRecherchee = controleImage.getCouleurAssocie("vert");
        //std::vector<Objet> objets = controleImage.traiterSelonCouleur(frame,couleurRecherchee);
        //std::vector<Objet> objets = controleImage.traiterSelonForme(frame,Forme::BALLE);
        for (size_t i = 0; i < objets.size(); i++)
        {
            Objet obj = objets[i];

            cv::rectangle(frame, cv::Rect(obj.x, obj.y, obj.w, obj.h),
                          cv::Scalar(255, 255, 255), 2);

            cv::circle(frame, cv::Point(obj.cx, obj.cy), 4, cv::Scalar(0, 255, 0), -1);

            cv::putText(frame, std::to_string(obj.area),
                        cv::Point(obj.x, obj.y - 5), cv::FONT_HERSHEY_SIMPLEX,
                        0.5, cv::Scalar(255, 255, 255), 1);

            cv::putText(frame, (obj.couleur.getNom()),
                        cv::Point(obj.x, obj.y + 20), cv::FONT_HERSHEY_SIMPLEX,
                        0.5, cv::Scalar(255, 255, 255), 1);

            cv::putText(frame, (obj.getNomAssociee(obj.forme)),
                        cv::Point(obj.x, obj.y + 100), cv::FONT_HERSHEY_SIMPLEX,
                        0.5, cv::Scalar(255, 255, 255), 1);

            std::pair<int, int> pos = controleImage.calculerDistanceCentre(obj, frame);

            std::string texte = "(" + std::to_string(pos.first) + ", " + std::to_string(pos.second) + ")";

            cv::putText(frame, texte,
                        cv::Point(obj.x, obj.y - 50),
                        cv::FONT_HERSHEY_SIMPLEX, 0.5,
                        cv::Scalar(255, 255, 255), 1);
        }

        cv::Mat seuille;
        cv::cvtColor(frame, seuille, cv::COLOR_BGR2HSV);

        cv::imshow("flux vidéo", frame);
        if (cv::waitKey(30) == 27)
        { // TOUCHE ESC
            break;
        }
    }
    cap.release();
    cv::destroyAllWindows();
    return 0;
}
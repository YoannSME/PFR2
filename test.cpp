#include "Objet.h"
#include "Image.h"
#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>
#include "Couleur.h"

// SEUILS DE DETECTION A ADAPTER UNE FOIS QU'ON AURA LES DONNES DE LA CAMEAR
Couleur jaune("Jaune", cv::Scalar(13, 97, 67), cv::Scalar(42, 255, 255));
Couleur bleu("Bleu", cv::Scalar(74, 56, 0), cv::Scalar(117, 255, 255));
Couleur orange("Orange", cv::Scalar(2, 163, 64), cv::Scalar(13, 255, 255));

int main(int argc, char **argv)
{
    Image controleImage;
    /*color bleu = creerCouleur(cv::Scalar(90, 50, 50), cv::Scalar(130, 255, 255));
    color jaune = creerCouleur(cv::Scalar(15, 50, 50), cv::Scalar(40, 255, 255));
    color orange = creerCouleur(cv::Scalar(10, 100, 100),cv::Scalar(20, 255, 255));*/

    cv::Mat frame;
    cv::VideoCapture cap;
    cap.open(0);
    if (!cap.isOpened())
    {
        std::cerr << "Erreur : Impossible d'ouvrir la caméra !" << std::endl;
        return -1;
    }

    std::vector<Couleur> couleurs = {jaune, bleu, orange};
    while (1)
    {
        cap >> frame;
        if (frame.empty())
            break;

        std::vector<Objet> objets = controleImage.traiterSelonForme(frame, couleurs);
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

            cv::putText(frame, (obj.getForme(obj.forme)),
                        cv::Point(obj.x, obj.y + 100), cv::FONT_HERSHEY_SIMPLEX,
                        0.5, cv::Scalar(255, 255, 255), 1);

            std::pair<int, int> pos = controleImage.calculerPosition(obj, frame);

            std::string texte = "(" + std::to_string(pos.first) + ", " + std::to_string(pos.second) + ")";

            cv::putText(frame, texte,
                        cv::Point(obj.x, obj.y - 50), // Position du texte (juste au-dessus de l'objet)
                        cv::FONT_HERSHEY_SIMPLEX, 0.5,
                        cv::Scalar(255, 255, 255), 1);
        }

        cv::Mat hsvSH;
        cv::cvtColor(frame, hsvSH, cv::COLOR_BGR2HSV);

        cv::imshow("flux vidéo", hsvSH);
        if (cv::waitKey(30) == 27)
        { // TOUCHE ESC
            break;
        }
    }
    cap.release();
    cv::destroyAllWindows();
    return 0;
}
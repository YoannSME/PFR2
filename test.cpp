#include "Objet.h"
#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>
#include "Couleur.h"

//SEUILS DE DETECTION A ADAPTER UNE FOIS QU'ON AURA LES DONNES DE LA CAMEAR
Couleur jaune("Jaune",cv::Scalar(15, 50, 50),  cv::Scalar(40, 255, 255));
Couleur bleu("Bleu",cv::Scalar(90, 95, 95),  cv::Scalar(125, 255, 255));
Couleur orange("Orange",cv::Scalar(3, 100, 100), cv::Scalar(14, 255, 255));

struct retour {
    cv::Mat image;
    std::vector<Objet> obj;
};


retour traiterSelonCouleur(cv::Mat &image, Couleur &couleur)
{
    cv::Mat seuille, open, labels, stats, centroids;

    cv::cvtColor(image, seuille, cv::COLOR_BGR2HSV);

    cv::inRange(seuille, couleur.getCouleurMin(), couleur.getCouleurMax(), seuille);

    cv::morphologyEx(seuille, open, cv::MORPH_OPEN, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(9, 9)));

    int nb_objets = cv::connectedComponentsWithStats(open, labels, stats, centroids, 8, CV_32S);
    std::vector<Objet> objetsDetectes;

    for (int i = 1; i < nb_objets; i++)
    {
        int area = stats.at<int>(i, cv::CC_STAT_AREA);

        //A CHANGER UNE FOIS QU'ON RECEVRA DONNEES DE LA CAMERA
        if (area >= 1000)
        {
            int x = stats.at<int>(i, cv::CC_STAT_LEFT);
            int y = stats.at<int>(i, cv::CC_STAT_TOP);
            int w = stats.at<int>(i, cv::CC_STAT_WIDTH);
            int h = stats.at<int>(i, cv::CC_STAT_HEIGHT);
            double cx = centroids.at<double>(i, 0);
            double cy = centroids.at<double>(i, 1);

            
            Objet obj(area, x, y, w, h, cx, cy,Forme::BALLE,couleur);
            objetsDetectes.push_back(obj);
        }
    }


    retour r;
    r.image = open;
    r.obj = objetsDetectes;

    return r;
}

retour traiterSelonForme(cv::Mat &image){
    //AMELIORATIONS POSSIBLES
    retour objJaune = traiterSelonCouleur(image, jaune);
    retour objBleu  = traiterSelonCouleur(image, bleu);
    retour objOrange= traiterSelonCouleur(image, orange);

    retour tousObj;
    
    
    cv::bitwise_or(objJaune.image, objBleu.image, tousObj.image);
    cv::bitwise_or(tousObj.image, objOrange.image, tousObj.image);

    tousObj.obj.insert(tousObj.obj.end(), objJaune.obj.begin(), objJaune.obj.end());
    tousObj.obj.insert(tousObj.obj.end(), objBleu.obj.begin(),  objBleu.obj.end());
    tousObj.obj.insert(tousObj.obj.end(), objOrange.obj.begin(),objOrange.obj.end());

    return tousObj;
}




int main(int argc, char** argv) {

    /*color bleu = creerCouleur(cv::Scalar(90, 50, 50), cv::Scalar(130, 255, 255));
    color jaune = creerCouleur(cv::Scalar(15, 50, 50), cv::Scalar(40, 255, 255));
    color orange = creerCouleur(cv::Scalar(10, 100, 100),cv::Scalar(20, 255, 255));*/

    cv::Mat frame;
    cv::VideoCapture cap;
    cap.open(0);
    if (!cap.isOpened()) {
        std::cerr << "Erreur : Impossible d'ouvrir la caméra !" << std::endl;
        return -1;
    }


    cv::RNG rng(12345);

    while(1){
        cap >> frame;
        if (frame.empty()) break;

        
        retour objets = traiterSelonForme(frame);
        for (size_t i = 0; i < objets.obj.size(); i++) {
            Objet obj = objets.obj[i];

            // Rectangle englobant
            cv::rectangle(frame, cv::Rect(obj.x, obj.y, obj.w, obj.h), 
                          cv::Scalar(rng.uniform(0,255),rng.uniform(0,255),rng.uniform(0,255)), 2);

            // Centroïde
            cv::circle(frame, cv::Point(obj.cx, obj.cy), 4, cv::Scalar(0,255,0), -1);

            // Aire
            cv::putText(frame, std::to_string(obj.area), 
                        cv::Point(obj.x, obj.y - 5), cv::FONT_HERSHEY_SIMPLEX, 
                        0.5, cv::Scalar(255,255,255), 1);

            // Nom couleur
            cv::putText(frame,(obj.couleur.getNom()), 
                        cv::Point(obj.x+10, obj.y), cv::FONT_HERSHEY_SIMPLEX, 
                        0.5, cv::Scalar(255,255,255), 1);
        }

        cv::Mat hsvSH;
        cv::cvtColor(frame, hsvSH, cv::COLOR_BGR2HSV);
        
        cv::imshow("flux vidéo",hsvSH);
        if (cv::waitKey(30) == 27) {  // TOUCHE ESC
            break;
        }

    }
    cap.release();
    cv::destroyAllWindows();
    return 0;



}

/*int main(int argc,char** argv){

    cv::Mat frame;
    cv::VideoCapture cap;
    cap.open(0);
    if (!cap.isOpened()) {
        std::cerr << "Erreur : Impossible d'ouvrir la caméra !" << std::endl;
        return -1;
    }


    cv::RNG rng(12345);

    while(1){
        cap >> frame;
        if (frame.empty()) break;
        cv::Mat hsv;
        cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

        cv::imshow("flux vidéo",hsv);
        if (cv::waitKey(30) == 27) {  // Quitter avec touche ESC
            break;
        }
    }

    cap.release();
    cv::destroyAllWindows();
    return 0;


}*/
#include "GestionTraitementImage.h"
#include <opencv2/opencv.hpp>
#include <iostream>

int main(int argc, char** argv)
{
    // => REALISER INTERFACE PYTHON => CHERCHER BALLE => SCRIPT QUI APPELLE chercherObjet..
    // CHERCHER COULEUR => chercherCouleur
    // Chercher une balle de couleur => chercherObjetAvecCouleur
    /*ex : int main(int argc,char** argv){
    argv[1] sera le chemin vers l'iamge
        switch(atoi(argv[2])){
        si 1 : chercherObjet
        si2...
        si3 ...}
    }*/
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cerr << "Erreur : impossible d’ouvrir la caméra" << std::endl;
        return -1;
    }

    GestionTraitementImage controleImage;

    std::cout << "Appuyez sur 'K' pour capturer et traiter une image." << std::endl;
    std::cout << "Appuyez sur 'Q' pour quitter." << std::endl;

    cv::Mat frame;
    while (true)
    {
        cap >> frame;
        if (frame.empty()) {
            std::cerr << "Erreur : frame vide" << std::endl;
            break;
        }

        cv::imshow("Camera", frame);

        char key = (char)cv::waitKey(30);
        if (key == 'q' || key == 'Q')
        {
            break;
        }
        else if (key == 'k' || key == 'K')
        {
            std::string path = "capture.jpg";
            
            
            //std::vector<Objet> objets = controleImage.chercherObjetAvecCouleur(path, "vert", "balle");
            std::vector<Objet> objets = controleImage.chercherForme(path, "balle");
            controleImage.sauvegarderResultats(objets);
            for(Objet &obj : objets){
                cv::rectangle(frame, cv::Rect(obj.x, obj.y, obj.w, obj.h),cv::Scalar(255, 255, 255), 2);
            }
            cv::imwrite(path, frame);
            std::cout << "Image capturée et traitée avec couleur=vert et forme=balle." << std::endl;
        }
    }

    cap.release();
    cv::destroyAllWindows();
    return 0;
}

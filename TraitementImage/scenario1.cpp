#include "../Image/GestionTraitementImage.h"
#include <iostream>


int main(int argc,char** argv){
    GestionTraitementImage controleImage;

    if(argc>2 || argc<2){
        fprintf(stderr,"Usage[%s] <image_path> <1:chercherCouleur {couleur}>\n<2:chercherForme {forme}>\n<3:chercherObjetAvecCouleur {couleur;forme}>\n",argv[0]);
        return -1;
    }
    std::vector<Objet> objets;
    cv::VideoCapture cap("http://192.168.252.222:5000/video_feed");

    while(1){
        cv::Mat image;
        cap >> image;
        if(image.empty()){
            std::cerr << "Erreur : impossible de capturer l'image." << std::endl;
            break;
        }
        
        objets = controleImage.traiterImageAll(image);
        for(Objet &obj : objets){
            cv::rectangle(image, cv::Rect(obj.x, obj.y, obj.w, obj.h), cv::Scalar(255, 255, 255), 2);
        }
        cv::imshow("Image Traitee", image);
        std::string pathRetour = "TraitementImage/retour/retour.jpg";
        cv::imwrite(pathRetour, image);

        if(cv::waitKey(30) >= 0) break; // Sortir si une touche est pressée
    }

    cap.release();
    cv::destroyAllWindows();
    return 0;
}
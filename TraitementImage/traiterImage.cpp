#include "../Image/GestionTraitementImage.h"
#include <iostream>

GestionTraitementImage controleImage;
void enregistrerEtAfficher(std::vector<Objet> objets, cv::Mat &image, std::string path)
{
    controleImage.sauvegarderResultats(objets);
    for (Objet &obj : objets)
    {
        cv::rectangle(image, cv::Rect(obj.x, obj.y, obj.w, obj.h), cv::Scalar(255, 255, 255), 2);
    }
    std::string pathRetour = "../TraitementImage/retour/retour.jpg";
    cv::imwrite(pathRetour, image);
}
int main(int argc, char **argv)
{
    if (argc > 5 || argc < 2)
    {
        fprintf(stderr,"Usage[%s] <image_path> <1:chercherCouleur {couleur}>\n<2:chercherForme {forme}>\n<3:chercherObjetAvecCouleur {couleur;forme}>\n", argv[0]);
        return -1;
    }
    std::vector<Objet> objets ;

    std::string path = argv[1];
    cv::Mat image = cv::imread(path);
    switch (atoi(argv[2]))
    {
    case 1: // cas 1 : chercher à partir d'une couleur
        objets= controleImage.chercherCouleur(image, argv[3]);
        enregistrerEtAfficher(objets, image, path);
        break;
    case 2: // chercher à partir d'une forme
        objets = controleImage.chercherForme(image, argv[3]);
        enregistrerEtAfficher(objets, image, path);
        break;
    case 3: // chercher à partir d'une couleur et d'une forme argv3 = forme argv4 = couleur
       objets = controleImage.chercherObjetAvecCouleur(image, argv[4], argv[3]);
        enregistrerEtAfficher(objets, image, path);
        break;
    default:
        std::cerr << "Erreur : argument non reconnu" << std::endl;
        return -1;
    }
    printf("FIN CODE C++");
}
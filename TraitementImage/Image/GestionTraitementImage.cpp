#include "GestionTraitementImage.h"

using json = nlohmann::json;
GestionTraitementImage::GestionTraitementImage()
{
    
    std::ifstream fichier("TraitementImage/Image/seuils.json");
    if (!fichier.is_open())
    {
        std::cerr << "Erreur : impossible d’ouvrir seuils.json" << std::endl;
        exit(1);
    }

    json j;
    fichier >> j;

    for (auto &[nom, plages] : j["CouleursHSV"].items())
    {
        auto min = plages[0];
        auto max = plages[1];
        cv::Scalar minHSV(min[0], min[1], min[2]);
        cv::Scalar maxHSV(max[0], max[1], max[2]);
        couleursDetectables.emplace_back(nom, minHSV, maxHSV);
    }
}
std::vector<Couleur> GestionTraitementImage::getCouleursDetectables()
{
    return couleursDetectables;
}

Couleur GestionTraitementImage::getCouleurAssocie(std::string_view nom)
{
    for (Couleur &c : couleursDetectables)
    {
        if (c.getNom() == nom)
        {
            return c;
        }
    }
    std::cerr << "Erreur : couleur non trouvée" << std::endl;
    exit(1);
}

Forme GestionTraitementImage::getFormeAssocie(std::string nomForme)
{
    return Objet::getFormeAssociee(nomForme);
}
std::vector<Objet> GestionTraitementImage::traiterImageAll(cv::Mat &image)
{

    std::vector<Objet> tousObj;
    for (Couleur &c : couleursDetectables)
    {
        std::vector<Objet> objetsCouleur = traiterSelonCouleur(image, c);
        tousObj.insert(tousObj.end(), objetsCouleur.begin(), objetsCouleur.end());
    }
    return tousObj;
}

std::vector<Objet> GestionTraitementImage::traiterSelonForme(cv::Mat &image, Forme forme)
{
    std::vector<Objet> tousObj;
    std::vector<Objet> objetsInterets;
    for (Couleur &c : couleursDetectables)
    {
        std::vector<Objet> objetsCouleur = traiterSelonCouleur(image, c);
        tousObj.insert(tousObj.end(), objetsCouleur.begin(), objetsCouleur.end());
    }
    for (Objet &obj : tousObj)
    {
        if (obj.forme == forme)
        {
            objetsInterets.push_back(obj);
        }
    }
    return objetsInterets;
}

std::vector<Objet> GestionTraitementImage::traiterSelonCouleur(cv::Mat &image, Couleur couleur)
{
    cv::Mat imageFiltree, hsv, masque, open, closed, labels, stats, centroids;

    //Ajout de bruit
    cv::medianBlur(image, imageFiltree, 3);

    // Passage en HSV
    cv::cvtColor(imageFiltree, hsv, cv::COLOR_BGR2HSV);

    // Seuillage
    cv::inRange(hsv, couleur.getCouleurMin(), couleur.getCouleurMax(), masque);

    // Ouverture et fermeture
    cv::morphologyEx(masque, open, cv::MORPH_OPEN, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(7, 7)));
    cv::morphologyEx(open, closed, cv::MORPH_CLOSE, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(9, 9)));

    //Labellisation + récupération des données de l'objet
    int nb_objets = cv::connectedComponentsWithStats(closed, labels, stats, centroids, 8, CV_32S);
    std::vector<Objet> objetsDetectes;

    //RAPPEL : i = 0 est le fond
    for (int i = 1; i < nb_objets; i++)
    {
        int area = stats.at<int>(i, cv::CC_STAT_AREA); //aire objet
        if (area >= 450)
        {
            int x = stats.at<int>(i, cv::CC_STAT_LEFT); //X Haut gauche boite englobante dan sl'image
            int y = stats.at<int>(i, cv::CC_STAT_TOP);//Y Haut gauche boite englobante dans l'image
            int w = stats.at<int>(i, cv::CC_STAT_WIDTH); // longueur boite englobante
            int h = stats.at<int>(i, cv::CC_STAT_HEIGHT);//hauteur boite englobante
            double cx = centroids.at<double>(i, 0); //Centre gravité X
            double cy = centroids.at<double>(i, 1);//centre gravité Y
            std::pair<int, int> distanceCentre = {cx-image.cols / 2, cy - image.rows / 2}; //Distance des composantes X,Y de obj par rapport au centre de l'image

            cv::Mat objetMask = (labels == i); //On récupère seulement l'objet i
            objetMask.convertTo(objetMask, CV_8U);
            std::vector<std::vector<cv::Point>> contours;
            cv::findContours(objetMask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE); //Recupération des contours exacts

            Forme forme = Forme::INCONNUE;

            if (!contours.empty())
            {
                auto contour = contours[0];
                double aireContour = cv::contourArea(contour);
                double perimetre = cv::arcLength(contour, true);
                double circularite = (perimetre > 0) ? 4 * CV_PI * aireContour / (perimetre * perimetre) : 0.0; //Calcul circularité

                std::vector<cv::Point> approx;
                cv::approxPolyDP(contour, approx, 0.04 * perimetre, true);

                double aspectRatio = static_cast<double>(w) / h;

               
                if ((approx.size() == 4 && aspectRatio >= 0.9) && aspectRatio <= 1.1)
                {
                    forme = Forme::CARRE;
                }
                else if (circularite > 0.55)
                {
                    forme = Forme::BALLE;
                }
                else
                {
                    continue; // Ignore les objets qui ne correspondent pas aux formes recherchées;
                }
            }

            Objet obj(area, x, y, w, h, cx, cy, distanceCentre, forme, couleur);
            objetsDetectes.push_back(obj);
        }
    }
    return objetsDetectes;
}


void to_json(nlohmann::json &j, const Objet &obj)
{
    j = json{
        {"aire", obj.area},
        {"x", obj.x},
        {"y", obj.y},
        {"largeur", obj.w},
        {"hauteur", obj.h},
        {"cx", obj.cx},
        {"cy", obj.cy},
        {"forme", Objet::getNomAssociee(obj.forme)},
        {"couleur", obj.couleur.getNom()},
        {"distX",obj.distanceCentre.first},
        {"distY",obj.distanceCentre.second}
    };
}

std::vector<Objet> GestionTraitementImage::chercherObjetAvecCouleur(cv::Mat image, const std::string &couleur, const std::string &forme)
{
    //cv::Mat image = cv::imread(path);
    if (image.empty())
    {
        std::cerr << "Erreur : impossible d’ouvrir l’image" << std::endl;
        exit(2);
    }
    Couleur couleurRecherchee = getCouleurAssocie(couleur);
    Forme formeRecherchee = getFormeAssocie(forme);
    std::vector<Objet> objets = traiterSelonCouleur(image, couleurRecherchee);
    std::vector<Objet> objetsInterets;
    for (Objet &obj : objets)
    {
        if (obj.forme == formeRecherchee)
        {
            objetsInterets.push_back(obj);
        }
    }
    return objets;
}

std::vector<Objet> GestionTraitementImage::chercherForme(cv::Mat image,const std::string &forme)
{
    //cv::Mat image = cv::imread(path);
    if (image.empty())
    {
        std::cerr << "Erreur : impossible d’ouvrir l’image" << std::endl;
        exit(2);
    }
    Forme formeRecherchee = getFormeAssocie(forme);
    return traiterSelonForme(image, formeRecherchee);
}

std::vector<Objet> GestionTraitementImage::chercherCouleur(cv::Mat image,const std::string &couleur)
{
    //cv::Mat image = cv::imread(path);
    if (image.empty())
    {
        std::cerr << "Erreur : impossible d’ouvrir l’image" << std::endl;
        exit(2);
    }
    Couleur couleurAssociee = getCouleurAssocie(couleur);
    return traiterSelonCouleur(image, couleurAssociee);
}

/*std::vector<Objet> GestionTraitementImage::chercherObjetAvecCouleurVIDEO(cv::Mat &image, const std::string &couleur, const std::string &forme)
{
    Couleur couleurRecherchee = getCouleurAssocie(couleur);
    Forme formeRecherchee = getFormeAssocie(forme);
    std::vector<Objet> objets = traiterSelonCouleur(image, couleurRecherchee);
    std::vector<Objet> objetsInterets;
    for (Objet &obj : objets)
    {
        if (obj.forme == formeRecherchee)
        {
            objetsInterets.push_back(obj);
        }
    }
    return objetsInterets;
}*/

void GestionTraitementImage::sauvegarderResultats(const std::vector<Objet> &objets)
{
    json j;
    int index = 1;
    for (const Objet &obj : objets)
    {
        j["objet" + std::to_string(index)] = json(obj);
        index++;
    }

    std::ofstream fichier("TraitementImage/retour/resultats.json");
    if (!fichier.is_open())
    {
        std::cerr << "Erreur : impossible d’écrire dans resultats.json" << std::endl;
        exit(1);
    }
    fichier << j.dump(4);
    fichier.close();
}

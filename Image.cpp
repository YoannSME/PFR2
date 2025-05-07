#include "Image.h"

Image::Image()
{
}

std::vector<Objet> Image::traiterSelonForme(cv::Mat &image, std::vector<Couleur> couleurs,Forme forme)
{
    std::vector<Objet> tousObj;
    std::vector<Objet> objetsInterets;
    for (const Couleur &c : couleurs)
    {
        std::vector<Objet> objetsCouleur = traiterSelonCouleur(image, c);
        tousObj.insert(tousObj.end(), objetsCouleur.begin(), objetsCouleur.end());
    }
    for(const Objet &obj: tousObj){
        if(obj.forme == forme){
            objetsInterets.push_back(obj);
        }
    }
    return objetsInterets;
}


std::vector<Objet> Image::traiterSelonCouleur(cv::Mat &image, Couleur couleur)
{
    cv::Mat seuille, open, labels, stats, centroids;

    //cv::GaussianBlur(image, image, cv::Size(5, 5), 0);


    cv::cvtColor(image, seuille, cv::COLOR_BGR2HSV);
    cv::inRange(seuille, couleur.getCouleurMin(), couleur.getCouleurMax(), seuille);
    cv::morphologyEx(seuille, open, cv::MORPH_OPEN, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(13, 13)));

    int nb_objets = cv::connectedComponentsWithStats(open, labels, stats, centroids, 8, CV_32S);
    std::vector<Objet> objetsDetectes;

    for (int i = 1; i < nb_objets; i++)
    {
        int area = stats.at<int>(i, cv::CC_STAT_AREA);
        if (area >= 350)
        {
            int x = stats.at<int>(i, cv::CC_STAT_LEFT);
            int y = stats.at<int>(i, cv::CC_STAT_TOP);
            int w = stats.at<int>(i, cv::CC_STAT_WIDTH);
            int h = stats.at<int>(i, cv::CC_STAT_HEIGHT);
            double cx = centroids.at<double>(i, 0);
            double cy = centroids.at<double>(i, 1);

            cv::Mat objetMask = (labels == i);
            objetMask.convertTo(objetMask, CV_8U);
            std::vector<std::vector<cv::Point>> contours;
            cv::findContours(objetMask, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

            Forme forme = Forme::INCONNUE;

            if (!contours.empty())
            {
                auto contour = contours[0];
                double aireContour = cv::contourArea(contour);
                double perimetre = cv::arcLength(contour, true);
                double circularite = (perimetre > 0) ? 4 * CV_PI * aireContour / (perimetre * perimetre) : 0.0;

                std::vector<cv::Point> approx;
                cv::approxPolyDP(contour, approx, 0.04 * perimetre, true);

                double aspectRatio = static_cast<double>(w) / h;

                if (circularite > 0.6)
                {
                    forme = Forme::BALLE;
                }
                else if (approx.size() == 4 && aspectRatio >= 0.9 || aspectRatio <= 1.1)
                {
                    forme = Forme::CARRE;
                }
                else
                {
                    forme = Forme::INCONNUE;
                }
            }

            Objet obj(area, x, y, w, h, cx, cy, forme, couleur);
            objetsDetectes.push_back(obj);
        }
    }
    return objetsDetectes;
}

std::pair<int, int> Image::calculerDistanceCentre(Objet& objet, const cv::Mat &image) {
    int centreImX = image.cols / 2;
    int centreImY = image.rows / 2;
    return {centreImX -objet.cx, centreImY - objet.cy};
}
//Poser un coefficient => Si l'objet est trop loin => (Y élevé) il faut avancer d'une certaine distance

std::pair<bool,std::pair<int,int>> Image::objetPresent(cv::Mat &image, Forme forme, Couleur couleur) {
    std::vector<Couleur> couleurTraitee= {couleur};
    std::vector<Objet> objets = traiterSelonForme(image, couleurTraitee,forme);
    for (Objet &obj : objets) {
        if (obj.forme == forme) {
            return {true, calculerDistanceCentre(obj, image)};
        }
    }
    return {false, {0, 0}};
}

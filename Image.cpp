#include "Image.h"
#include <vector>

Image::Image()
{
}

Image::~Image()
{
}

std::vector<Objet> traiterSelonCouleur(cv::Mat &image, Couleur &couleur)
{
    cv::Mat seuille, open, labels, stats, centroids;

    cv::cvtColor(image, seuille, cv::COLOR_BGR2HSV);

    cv::inRange(seuille, couleur.getMin(), couleur.getMax(), seuille);

    cv::morphologyEx(seuille, open, cv::MORH_OPEN, cv::getStructuringElement(cv::MORPH_RECT, cv::Scalar(9, 9)));

    int nb_objets = cv::connectedComponentsWithStats(ouverture, labels, stats, centroids, 8, CV_32S);
    std::vector<Objet> objetsDetectes;

    for (int i = 1; i < nb_objets; i++)
    {
        int area = stats.at<int>(i, cv::CC_STAT_AREA);

        // Seulement si l'objet est suffisamment grand
        if (area >= 50)
        {
            int x = stats.at<int>(i, cv::CC_STAT_LEFT);
            int y = stats.at<int>(i, cv::CC_STAT_TOP);
            int w = stats.at<int>(i, cv::CC_STAT_WIDTH);
            int h = stats.at<int>(i, cv::CC_STAT_HEIGHT);
            double cx = centroids.at<double>(i, 0);
            double cy = centroids.at<double>(i, 1);

            // Création d'un objet et ajout à la liste
            Objet obj(area, x, y, w, h, cx, cy);
            objetsDetectes.push_back(obj);
        }
    }

    // Retourne la liste complète d'objets
    return objetsDetectes;
}
#include "Image.h"

Image::Image()
{
}

std::vector<Objet> Image::traiterSelonForme(cv::Mat &image, std::vector<Couleur> couleurs)
{
    std::vector<Objet> tousObj;
    for (const Couleur &c : couleurs)
    {
        std::vector<Objet> objetsCouleur = traiterSelonCouleur(image, c);
        tousObj.insert(tousObj.end(), objetsCouleur.begin(), objetsCouleur.end());
    }

    return tousObj;
}

std::vector<Objet> Image::traiterSelonCouleur(cv::Mat &image, Couleur couleur)
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
        if (area >= 1000)
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

std::pair<int, int> Image::calculerPosition(Objet& objet, const cv::Mat &image) {
    int centreImX = image.cols / 2;
    int centreImY = image.rows / 2;
    return {centreImX -objet.cx, centreImY - objet.cy};
}

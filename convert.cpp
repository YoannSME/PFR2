#include "Objet.h"
#include "Image.h"
#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>

int main(int argc, char **argv)
{
    cv::Mat frame;
    cv::VideoCapture cap;
    cap.open(0);
    if (!cap.isOpened())
    {
        std::cerr << "Erreur : Impossible d'ouvrir la caméra !" << std::endl;
        return -1;
    }

    while (1)
    {
        cap >> frame;
        if (frame.empty())
            break;

        cv::Mat imGREY;

        cv::cvtColor(frame, imGREY, cv::COLOR_BGR2GRAY);
        cv::GaussianBlur(imGREY, imGREY, cv::Size(5, 5), 0);
        cv::Mat imCanny;
        cv::Canny(imGREY, imCanny, 50, 150);
        

        cv::imshow("flux vidéo", imCanny);
        if (cv::waitKey(30) == 27)
        { // TOUCHE ESC
            break;
        }
    }
}
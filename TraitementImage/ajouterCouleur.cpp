#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    cv::VideoCapture cap("http://172.20.10.5:5000/video_feed");

    if (!cap.isOpened()) {
        std::cerr << "Erreur : impossible d'ouvrir la webcam." << std::endl;
        return -1;
    }

    int h_min = 2, s_min = 163, v_min = 64;
    int h_max = 13, s_max = 255, v_max = 255;

    cv::namedWindow("Trackbars", cv::WINDOW_AUTOSIZE);
    cv::createTrackbar("H Min", "Trackbars", &h_min, 179);
    cv::createTrackbar("H Max", "Trackbars", &h_max, 179);
    cv::createTrackbar("S Min", "Trackbars", &s_min, 255);
    cv::createTrackbar("S Max", "Trackbars", &s_max, 255);
    cv::createTrackbar("V Min", "Trackbars", &v_min, 255);
    cv::createTrackbar("V Max", "Trackbars", &v_max, 255);

    cv::Mat frame, hsv, mask;

    while (true) {
        cap >> frame;
        if (frame.empty()) break;

        cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

        cv::Scalar lower(h_min, s_min, v_min);
        cv::Scalar upper(h_max, s_max, v_max);

        cv::inRange(hsv, lower, upper, mask);

        cv::imshow("Webcam", frame);
        cv::imshow("Masque", mask);

    
        std::cout << "Min: (" << h_min << ", " << s_min << ", " << v_min << ") "
                  << "Max: (" << h_max << ", " << s_max << ", " << v_max << ")\r";
        std::cout.flush();

        // esc
        if (cv::waitKey(1) == '27') break;
    }

    cap.release();
    cv::destroyAllWindows();
    return 0;
}

#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    cv::Mat frame = cv::imread("imageRequete.jpg", cv::IMREAD_COLOR);
    //cv::VideoCapture cap(0);



    int h_min = 2, s_min = 163, v_min = 64;
    int h_max = 13, s_max = 255, v_max = 255;

    cv::namedWindow("Trackbars", cv::WINDOW_AUTOSIZE);
    cv::createTrackbar("H Min", "Trackbars", &h_min, 179);
    cv::createTrackbar("H Max", "Trackbars", &h_max, 179);
    cv::createTrackbar("S Min", "Trackbars", &s_min, 255);
    cv::createTrackbar("S Max", "Trackbars", &s_max, 255);
    cv::createTrackbar("V Min", "Trackbars", &v_min, 255);
    cv::createTrackbar("V Max", "Trackbars", &v_max, 255);

    cv::Mat hsv, mask;

    while (true) {
      
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


    cv::destroyAllWindows();
    return 0;
}

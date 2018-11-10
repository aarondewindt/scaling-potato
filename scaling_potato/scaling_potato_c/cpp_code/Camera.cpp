//
// Created by elviento on 3/18/17.
//

#include "Camera.h"
#include <opencv2/opencv.hpp>
#include <panda3d/pointerToArray.h>

using namespace cv;


Camera::Camera() {}

void Camera::set_image(long pointer, unsigned int x_size, unsigned int y_size) {
    image_pointer = *(PointerToArray<unsigned char>*)pointer;
    this->x_size = x_size;
    this->y_size = y_size;
}

bool Camera::is_set() {
    return image_pointer != nullptr;
}

void Camera::show_image() {
    Mat image =  Mat(y_size, x_size, CV_8UC3, image_pointer);
    flip(image, image, 0);
    namedWindow("Display Image", WINDOW_AUTOSIZE);
    imshow("Display Image", image);
    waitKey(0);
}

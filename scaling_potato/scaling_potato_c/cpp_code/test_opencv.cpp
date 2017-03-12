//
// Created by elviento on 3/9/17.
//

#include <iostream>

#include "test_opencv.h"
#include <opencv2/opencv.hpp>


int i = 0;

using namespace cv;


void test_opencv() {

    Mat image;
    image = imread( "/home/elviento/stuff/projects/rnd/scaling-potato/resources/Lenna.png", 1 );

    if ( !image.data )
    {
        printf("No image data \n");
        return;
    }
    namedWindow("Display Image", WINDOW_AUTOSIZE );
    imshow("Display Image", image);

    waitKey(0);
}


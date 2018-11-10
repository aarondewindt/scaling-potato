//
// Created by elviento on 3/9/17.
//

#include <iostream>
#include <stdint.h>

#include "test_opencv.h"
#include <opencv2/opencv.hpp>
#include <panda3d/pointerToArray.h>


int i = 0;

using namespace cv;
using namespace std;


void test_opencv() {

    Mat image;
    image = imread( "/home/elviento/stuff/projects/rnd/scaling-potato/resources/Lenna.png", 1 );

    if ( !image.data )
    {
        printf("No image data \n");
        return;
    }
    namedWindow("Display Image", WINDOW_AUTOSIZE);
    imshow("Display Image", image);

    waitKey(0);
}

void test_read_texture_from_memory(long ptr_long, int x_size, int y_size) {
    unsigned char *texture = *(PointerToArray<unsigned char>*)ptr_long;

    cout << (int*)texture << " " << (int*)(*(PointerToArray<unsigned char>*)ptr_long).p() << endl;

    Mat image =  Mat(y_size, x_size, CV_8UC3, texture);
    flip(image, image, 0);
    namedWindow("Display Image", WINDOW_AUTOSIZE);
    imshow("Display Image", image);
    waitKey(0);
}

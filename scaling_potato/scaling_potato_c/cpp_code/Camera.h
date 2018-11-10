//
// Created by elviento on 3/18/17.
//

#ifndef SCALING_POTATO_QUADCOPTERCAMERAS_H
#define SCALING_POTATO_QUADCOPTERCAMERAS_H

#include <stdint.h>
#include <thread>



class Camera {
public:
    Camera();

    void set_image(long pointer, unsigned int x_size, unsigned int y_size);
    bool is_set();

    void show_image();

private:
    uint8_t *image_pointer = nullptr;
    uint32_t x_size = 0;
    uint32_t y_size = 0;

    std::thread video_update_thread;
    
    

};


#endif //SCALING_POTATO_QUADCOPTERCAMERAS_H

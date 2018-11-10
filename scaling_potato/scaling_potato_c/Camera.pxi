cdef extern from "Camera.h":
    cdef cppclass _Camera "Camera":
        _Camera()

        void set_image(long pointer, unsigned int x_size, unsigned int y_size)
        bool is_set()
        void show_image()

cdef class Camera:
    cdef _Camera *_thisptr

    def __cinit__(self):
        self._thisptr = new _Camera()

    def __dealloc__(self):
        del self._thisptr

    cpdef void set_image(self, long pointer, unsigned int x_size, unsigned int y_size):
        self._thisptr.set_image(pointer, x_size, y_size)

    cpdef show_image(self):
        self._thisptr.show_image() 


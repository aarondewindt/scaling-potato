from libcpp cimport bool
from libc.stdint cimport uint8_t, uint16_t, uint32_t, uint64_t, int8_t, int16_t, int32_t, int64_t
from libc.stddef cimport wchar_t, size_t
from libc.stdint cimport uintptr_t


cdef extern from "test_opencv.h":
    cpdef void test_opencv()
    cpdef void test_read_texture_from_memory(long, int, int)


include "Camera.pxi"
import os
import os.path
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension


def main():
    scaling_potato_ext = create_scaling_potato_ext()

    setup(name="scaling_potato",
          ext_modules=scaling_potato_ext)


def create_scaling_potato_ext():
    sc = SourcesCollectorClass()

    cython_source = "./scaling_potato/scaling_potato_c/scaling_potato_c.pyx"

    sc.add_c_source_dir("./scaling_potato/scaling_potato_c/cpp_code")
    sc.add_include_dir("./scaling_potato/scaling_potato_c/cpp_code")

    # OpenCV Include
    # sc.add_library_dir(os.environ["OPENCV_LIB"])
    sc.add_include_dir(os.environ["OPENCV_INC"])
    sc.add_library("opencv_core")
    sc.add_library("opencv_imgproc")
    sc.add_library("opencv_imgcodecs")
    sc.add_library("opencv_highgui")
    sc.add_library("opencv_ml")
    sc.add_library("opencv_videoio")
    sc.add_library("opencv_video")
    sc.add_library("opencv_features2d")
    sc.add_library("opencv_calib3d")
    sc.add_library("opencv_objdetect")
    sc.add_library("opencv_flann")

    # Python include
    sc.add_include_dir("/usr/include/python2.7")

    # Panda3d include
    # sc.add_include_dir("/usr/include/panda3d")
    sc.add_library_dir("/usr/lib/x86_64-linux-gnu/panda3d")
    sc.add_library('p3framework')
    sc.add_library('panda')
    sc.add_library('pandafx')
    sc.add_library('pandaexpress')
    sc.add_library('p3dtoolconfig')
    sc.add_library('p3dtool')
    # sc.add_library('p3pystub')
    sc.add_library('p3direct')

    printb("scaling_potato_c")
    print("="*80)
    sc.print_lists()
    print('\n'*2)

    ext = None

    ext = Extension("scaling_potato.scaling_potato_c",
                    sources=[cython_source]+sc.c_sources_list,
                    include_dirs=sc.includes,
                    library_dirs=sc.lib_dirs,
                    libraries=sc.libraries,
                    language="c++",
                    extra_compile_args=["-g", "-std=c++11"], #, "/Od", "/MDd"], # for release version change /Od compile arg to /O2 (optimization for maximum speed)
                    # extra_link_args=["-debug"], # leave this enabled for release! :)))
                    define_macros = [('PYTHON_EXT', '1')]
                    )

    ext = cythonize([ext], gdb_debug=True)
    print('\n'*4)
    return ext


class SourcesCollectorClass(object):
    def __init__(self):
        self.c_sources_list = []
        self.cython_sources_list = []
        self.includes = []
        self.libraries = []
        self.lib_dirs = []

    def print_lists(self):
        print("Cython sources")
        for src in self.cython_sources_list:
            print(src)

        print('\nC sources')
        for src in self.c_sources_list:
            print(src)

        print('\nInclude directories')
        for src in self.includes:
            print(src)

        print('\nLibrary dirs')
        for src in self.lib_dirs:
            print(src)

        print('\nLibraries')
        for src in self.libraries:
            print(src)

    def add_library_dir(self, path):
        self.lib_dirs.append(path)

    def add_library(self, lib_name):
        self.libraries.append(lib_name)

    def add_include_dir(self, path):
        self.includes.append(os.path.abspath(path))

    def add_c_source(self, path):
        exts = ['.c', '.cpp']
        path = os.path.abspath(path)
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1]
            if ext in exts:
                self.c_sources_list.append(path)

    def add_c_source_dir(self, path):
        for file in os.listdir(path):
            self.add_c_source(os.path.join(path, file))

    def add_cython_source(self, path):
        exts = ['.pyx'];
        path = os.path.abspath(path)
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1]
            if ext in exts:
                self.cython_sources_list.append(path)

    def add_cython_source_dir(self, path):
        for root, _, files in os.walk(path):
            for file in files:
                self.add_cython_source(os.path.join(root, file))


try:
    from pyfiglet import Figlet
    figlet = Figlet(font='small')
except:
    figlet = None


def printb(s):
    if figlet is not None:
        print(figlet.renderText(s))
    else:
        print(s)



if __name__ == "__main__":
    main()

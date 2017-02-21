from setuptools import setup, find_packages
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('scaling_potato/__init__.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='scaling_potato',
    version=main_ns['__version__'],
    description='Project for testing computer vision algorithms to control a quadcopter.',
    author='Aaron de Windt',
    author_email='aaron.dewindt@gmail.com',

    install_requires=['numpy', 'scipy'],  # panda3d as well but you'll have to do this seperately.
    packages=find_packages('.', exclude=["test"]),

    classifiers=[
        'Programming Language :: Python :: 2 :: Only',
        'Development Status :: 2 - Pre-Alpha'],
)

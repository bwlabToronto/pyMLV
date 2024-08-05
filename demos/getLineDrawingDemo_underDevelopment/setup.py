from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'ucm_mean_pb',
        ['ucm_mean_pb.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['-std=c++11'],  # Specify the C++ standard
    ),
]

setup(
    name='ucm_mean_pb',
    version='0.1',
    description='Ultrametric Contour Maps',
    ext_modules=ext_modules,
)

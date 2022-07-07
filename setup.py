from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize('Solving_Methods/*.pyx'))
setup(ext_modules = cythonize('Inputs_Outputs/*.pyx'))
setup(ext_modules = cythonize('User_interface/*.pyx'))
from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(ext_modules = cythonize('Solving_Methods/*.pyx'),include_dirs=[numpy.get_include()], compiler_directives={'language_level' : "3"})
setup(ext_modules = cythonize('Inputs_Outputs/*.pyx'),include_dirs=[numpy.get_include()], compiler_directives={'language_level' : "3"})
setup(ext_modules = cythonize('User_interface/*.pyx'),include_dirs=[numpy.get_include()], compiler_directives={'language_level' : "3"})

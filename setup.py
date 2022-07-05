from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize('Solving_Methods/OrderedSubGen.pyx'))
setup(ext_modules = cythonize('Solving_Methods/SmartSubGenerator.pyx'))
setup(ext_modules = cythonize('Inputs_Outputs/Inputs.pyx'))
setup(ext_modules = cythonize('User_interface/Command_interface.pyx'))
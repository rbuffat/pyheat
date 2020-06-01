from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Build import cythonize
except ImportError:
    use_cython = False
else:
    use_cython = True

ext_modules = []
if use_cython:
    extensions = [
        Extension("pyheat.sia380cy", ['pyheat/sia380cy.pyx']),
    ]
    ext_modules = cythonize(extensions)

setup(
    name='pyheat',
    version="0.3.dev",
    ext_modules=ext_modules,
    install_requires=['numpy', 'setuptools']
)

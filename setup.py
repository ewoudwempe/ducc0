from setuptools import setup, Extension
import sys
import os.path
import itertools
from glob import iglob

pkgname = 'ducc_0_1'

class _deferred_pybind11_include(object):
    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


def _get_files_by_suffix(directory, suffix):
    path = directory
    iterable_sources = (iglob(os.path.join(root, '*.'+suffix))
                        for root, dirs, files in os.walk(path))
    return list(itertools.chain.from_iterable(iterable_sources))


include_dirs = ['.', './src/',
                _deferred_pybind11_include(True),
                _deferred_pybind11_include()]
extra_compile_args = ['--std=c++17', '-march=native', '-ffast-math', '-O3']
python_module_link_args = []
define_macros = [("PKGNAME", pkgname)]

if sys.platform == 'darwin':
    import distutils.sysconfig
    extra_compile_args += ['-mmacosx-version-min=10.9']
    python_module_link_args += ['-mmacosx-version-min=10.9', '-bundle']
    vars = distutils.sysconfig.get_config_vars()
    vars['LDSHARED'] = vars['LDSHARED'].replace('-bundle', '')
elif sys.platform == 'win32':
    extra_compile_args = ['/Ox', '/EHsc', '/std:c++17']
else:
    extra_compile_args += ['-Wfatal-errors', '-Wfloat-conversion', '-W', '-Wall', '-Wstrict-aliasing=2', '-Wwrite-strings', '-Wredundant-decls', '-Woverloaded-virtual', '-Wcast-qual', '-Wcast-align', '-Wpointer-arith']
    python_module_link_args += ['-march=native', '-Wl,-rpath,$ORIGIN']

# if you want debugging info, remove the "-s" from python_module_link_args

def get_extension_modules():
    depfiles = _get_files_by_suffix('.', 'h') + _get_files_by_suffix('.', 'cc') + ['setup.py']
    return [Extension(pkgname,
                      language='c++',
                      sources=['python/ducc.cc'],
                      depends=depfiles,
                      include_dirs=include_dirs,
                      define_macros=define_macros,
                      extra_compile_args=extra_compile_args,
                      extra_link_args=python_module_link_args)]


setup(name=pkgname,
      version='0.1.0',
      description='Definitely useful code collection',
      url='https://gitlab.mpcdf.mpg.de/mtr/cxxbase',
      include_package_data=True,
      author='Martin Reinecke',
      author_email='martin@mpa-garching.mpg.de',
      packages=[],
      setup_requires=['numpy>=1.17.0', 'pybind11>=2.5.0'],
      ext_modules=get_extension_modules(),
      install_requires=['numpy>=1.17.0', 'pybind11>=2.5.0'],
      license="GPLv2",
      )

import os
import sys
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


requirements = []
if sys.version_info < (2, 7):
    requirements.append('argparse')


setup(
    name = 'Stencil',
    version = '0.1',
    license = 'BSD',
    description = 'Creates files and directories from templates',
    long_description = read('README.rst') + '\n\n' + read('HISTORY.rst'),
    url = 'https://github.com/trilan/stencil',
    author = 'Mike Yumatov',
    author_email = 'mike@yumatov.org',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = requirements,
    test_suite = 'nose.collector',
    tests_require = ['nose'],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    entry_points = {
        'console_scripts': [
            'stencil = stencil.main:run',
        ],
        'stencils': [
            'new = stencil.stencils:New',
        ],
    }
)

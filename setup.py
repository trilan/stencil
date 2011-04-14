import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name = 'Stencil',
    version = '0.1.dev',
    license = 'BSD',
    description = 'Creates files and directories from stencils.',
    long_description = read('README.rst'),
    url = 'https://github.com/trilan/stencil',
    author = 'Mike Yumatov',
    author_email = 'mike@yumatov.org',
    packages = find_packages(),
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    entry_points = {
        'console_scripts': [
            'stencil = stencil.main:run',
        ],
    }
)

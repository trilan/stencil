from setuptools import setup, find_packages


setup(
    name = 'Stencil',
    version = '0.1.dev',
    description = 'Creates files and directories from stencils.',
    url = 'https://github.org/trilan/stencil',
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

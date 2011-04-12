from setuptools import setup, find_packages


setup(
    name = 'Stencil',
    version = '0.1.dev',
    description = 'Creates files and directories from stencils.',
    url = 'https://github.org/trilan/stencil',
    author = 'Mike Yumatov',
    author_email = 'mike@yumatov.org',
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'stencil = stencil.main:run',
        ],
    }
)

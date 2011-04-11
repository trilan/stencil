from setuptools import setup


setup(
    name = 'Stencil',
    version = '0.1.dev',
    description = 'Creates files and directories from stencils.',
    url = 'https://github.org/trilan/stencil',
    author = 'Mike Yumatov',
    author_email = 'mike@yumatov.org',
    entry_points = {
        'console_scripts': [
            'stencil = stencil.main:run',
        ],
    }
)

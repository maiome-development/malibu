from setuptools import setup, find_packages

import malibu

setup(
    name = 'malibu',
    version = malibu.__version__,
    description = "maiome's library of utilities",

    url = "http://phabricator.maio.me/tag/malibu",
    author = "Sean Johnson",
    author_email = "sean.johnson@maio.me",
    
    license = "Unlicense",
    
    classifiers = [
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    packages = ['malibu'],
    package_dir = {'malibu': 'malibu'},
    zip_safe = True
)

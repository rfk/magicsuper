
import sys
setup_kwds = {}

from distutils.core import setup

import autosuper

NAME = "autosuper"
PACKAGES = ["autosuper"]
VERSION = autosuper.__version__
DESCRIPTION = "backport the magical zero-argument super() to python2"
LONG_DESC = autosuper.__doc__
AUTHOR = "Ryan Kelly"
AUTHOR_EMAIL = "ryan@rfk.id.au"
URL="http://github.com/rfk/autosuper"
LICENSE = "MIT"
KEYWORDS = "super mro"
CLASSIFIERS = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "License :: OSI Approved",
    "License :: OSI Approved :: MIT License",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
]

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      description=DESCRIPTION,
      long_description=LONG_DESC,
      license=LICENSE,
      keywords=KEYWORDS,
      packages=PACKAGES,
      classifiers=CLASSIFIERS,
      **setup_kwds
     )


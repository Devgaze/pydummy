# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pydummy/pydummy.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "pydummy",
    packages = ["pydummy"],
    entry_points = {
        "console_scripts": ['pydummy = pydummy.pydummy:main']
        },
    version = version,
    description = "Python command line application for generating dummy data.",
    long_description = long_descr,
    author = "Alen Novakovic (a.k.a Devgaze)",
    author_email = "alen@devgaze.com",
    url = "https://github.com/Devgaze/pydummy",
    )
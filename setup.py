# -*- coding: utf-8 -*-
#
# you can install this to a local test virtualenv like so:
#   virtualenv venv
#   ./venv/bin/pip install --editable .
#   ./venv/bin/pip install --editable .[dev]  # with dev requirements, too

import shdw

import glob
import setuptools
import sys

with open("README.md") as fd:
    long_description = fd.read()

if sys.platform == "win32":
    data_files = []
else:
    data_files = []

included_packages = ["shdw"] + ["shdw." + p for p in setuptools.find_packages("shdw")]

setuptools.setup(
    name="shdw",
    version=shdw.__version__,
    maintainer=shdw.__maintainer__,
    maintainer_email=shdw.__email__,
    author=shdw.__author__,
    author_email=shdw.__email__,
    license=shdw.__license__,
    url="https://github.com/wbrandenburger/DataVisualization",
    install_requires=[
        # - python project packages - 
        "colorama>=0.4",
        "click>=7.0.0",
        "stevedore>=1.30",
        "configparser>=3.0.0",
        "pyyaml>=3.12",
        "pandas",
        # - python image processing packages -
        # "opencv-python",
        # "pillow",
        # "tifffile",
        # - python numerical analysis packages -
        # "matplotlib",
        # "numpy"
        # "scipy"
    ],
    python_requires=">=3",
    classifiers=[
        "Development Status :: 1 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    extras_require=dict(
        # List additional groups of dependencies here (e.g. development
        # dependencies). You can install these using the following syntax,
        # for example:
        # $ pip install -e .[develop]
        optional=[
        ],
        develop=[
        ]
    ),
    description=(
        "Visualization tool for exploring remote sensing data and view processing results"
    ),
    long_description=long_description,
    keywords=[
        "visualization", "remote sensing", "images", "aerial", "satellite", "viewer", "explorer", "science", "research", "command-line", "tui"
    ],
    package_data=dict(
        shdw=[
        ],
    ),
    data_files=data_files,
    packages=included_packages,
    entry_points={
        "console_scripts": [
            "shdw=shdw.commands.default:run",
        ],
        "shdw.command": [
            "run=shdw.commands.run:cli"
        ],
    },
    platforms=["linux", "osx", "windows"],
)

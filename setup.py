import os
import re
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def find_version(*file_paths):
    try:
        f = codecs.open(os.path.join(here, *file_paths), "r", "latin1")
        version_file = f.read()
        f.close()
    except:
        raise RuntimeError("Unable to find version string.")

    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


try:
    f = codecs.open("README.rst", encoding="utf-8")
    long_description = f.read()
    f.close()
except:
    long_description = ""

setup(
    name="shareinator",
    version=find_version("shareinator/shareinator.py"),
    description="Share files using ssh on same network",
    long_description=long_description,
    url="https://github.com/GDGVIT/ssh",
    author="GDGVIT",
    author_email="gdgvitvellore@gmail.com",
    packages=find_packages(include=[
        "shareinator",
        "shareinator.*"
    ]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "shareinator=shareinator.shareinator:main"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Console",
        "Environment :: X11 Applications :: Qt",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Communications :: File Sharing"
    ],
    install_requires=[
        "pyqt5>=5.6, <5.16"
    ],
    python_requires='~=3.5'
)

import os
from setuptools import find_packages, setup

this_directory = os.path.abspath(os.path.dirname(__file__))
path_to_main = os.path.abspath(this_directory)

with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="utils-test-app",
    version="0.1.0",
    python_requires="~=3.6",
    install_requires=["requests"],
    packages=find_packages(),
    include_package_data=True,
    license="tbd",
    description="tbd",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Erik Kalkoken",
    author_email="kalkoken87@gmail.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)

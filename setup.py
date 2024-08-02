"""Setup script for the sanitize_ml_labels package."""

import os
import re

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with open(os.path.join(here, "README.md"), encoding="utf8") as f:
    long_description = f.read()


def read(*parts):
    with open(os.path.join(here, *parts), "r", encoding="utf8") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("sanitize_ml_labels", "__version__.py")

setup(
    name="sanitize_ml_labels",
    version=__version__,
    description="Python package to sanitize in a standard way ML-related labels.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LucaCappelletti94/sanitize_ml_labels",
    author="Luca Cappelletti,Tommaso Fontana",
    author_email="cappelletti.luca94@gmail.com,tommaso.fontana.96@gmail.com",
    # Choose your license
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    tests_require=[
        "pytest",
        "pytest-readme",
        "validate_version_code",
    ],
    # Add here the package dependencies
    install_requires=[
        "compress-json",
    ],
    extras_require={
        "test": [
            "pytest",
            "pytest-readme",
            "validate_version_code",
        ],
    },
)

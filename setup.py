"""Setup for pyproprop package."""

import setuptools

from pyproprop import __version__


if __name__ == "__main__":

    PACKAGE_NAME = "pyproprop"
    VERSION = __version__
    AUTHOR = "Sam Brockie"
    AUTHOR_EMAIL = "sambrockie@icloud.com"
    URL = "https://github.com/brocksam/pyproprop"
    LICENSE = "MIT License"
    DESCRIPTION = ("Package for aiding writing classes with lots of similar"
                   "simple properties without the boilerplate.")
    LONG_DESCRIPTION = open("README.rst").read()
    KEYWORDS = ["property", "type-checking", "bound-checking", "type-casting"]
    CLASSIFIERS = [
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
    PYTHON_REQUIRES = ">=3.8"
    INSTALL_REQUIRES = []
    EXTRAS_REQUIRE = ["sphinx>=3.2"]
    TESTS_REQUIRE = ["pytest>=6.0", "hypothesis>=5.26"]

    setuptools.setup(
        name=PACKAGE_NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        license=LICENSE,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        packages=setuptools.find_packages(),
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        tests_require=TESTS_REQUIRE,
    )

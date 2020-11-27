"""Setup for pyproprop package.

Attributes
----------
AUTHOR : str
    Hardcoded package author.
AUTHOR_EMAIL : str
    Hardcoded package author email.
CLASSIFIERS : List[str, ...]
    PyPI classifiers for project.
DESCRIPTION : str
    Short description of package.
KEYWORDS : List[str, ...]
    Keywords describing package to aid search on PyPI.
LICENSE : str
    License under which package is licensed.
PACKAGE_NAME : str
    PyPI name for package.
PYTHON_REQUIRES : str
    Version of Python required for package.
URL : str
    Project GitHub URL.
VERSION : str
    Version number for current build.

"""
import setuptools


def get_contents_from_file(filepath, by_line=False, strip=""):
    """Helper function to read 'requires' info from :dir:`requirements/`.

    Will process strings, lists or dicts as needed by the kwargs for
    :func:`setup`.

    Parameters
    ----------
    filepath : str
        Absolute filepath to file to be read and processed.
    by_line : bool, optional
        Should the file be read as a whole or on a line-by-line basis.
    strip : str, optional
        What should be stripped from the read file

    Returns
    -------
    str
        Processed file contents.

    """

    def process_file_contents(filepath):
        """Open, read and process the specified file.

        One of the two following functions, :func:`process_to_list` or
        :func:`process_to_str` is applied to format the read file correctly for
        the :func:`setuptools.setup` call.

        Parameters
        ----------
        filepath : str
            Absolute filepath to file to be read and processed.

        Returns
        -------
        Union[str, List[str, ...]]
            Processed file contents.

        """
        with open(filepath) as file:
            file_contents = file.read()
        if by_line:
            return process_to_list(file_contents)
        else:
            return process_to_str(file_contents)

    def process_to_list(file_contents):
        """Process file split by line with each one a separate list entry.

        Parameters
        ----------
        file_contents : str
            Unprocessed file contents that has just been read in.

        Returns
        -------
        List[str, ...]
            File contents split by line as separate entries in the :obj:`list`.

        """
        file_contents_by_line = str(file_contents).split("\n")
        return [str(line).strip() for line in file_contents_by_line]

    def process_to_str(file_contents):
        """File contents with specified :obj:`str` stripped.

        Parameters
        ----------
        file_contents : str
            Unprocessed file contents that has just been read in.

        Returns
        -------
        str
            Processed file contents.

        """
        return str(file_contents).strip(strip)

    if isinstance(filepath, dict):
        return_var = {}
        for key, value in filepath.items():
            return_var[key] = process_file_contents(value)
        return return_var
    else:
        return process_file_contents(filepath)


PACKAGE_NAME = "pyproprop"
VERSION = "0.4.4"
AUTHOR = "Sam Brockie"
AUTHOR_EMAIL = "sambrockie@icloud.com"
DESCRIPTION = ("Package for aiding writing classes with lots of similar "
               "simple properties without the boilerplate")
LICENSE = "MIT"
URL = "https://pypi.org/project/pyproprop/"
KEYWORDS = ["property", "type-checking", "bound-checking", "type-casting"]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Topic :: Utilities",
]
PYTHON_REQUIRES = ">=3.6"

if __name__ == "__main__":
    setuptools.setup(
        name=PACKAGE_NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        packages=setuptools.find_packages(),
        url=URL,
        license=LICENSE,
        description=DESCRIPTION,
        long_description=get_contents_from_file("README.rst"),
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        python_requires=PYTHON_REQUIRES,
        install_requires=get_contents_from_file("requirements.txt", True),
        extras_require=get_contents_from_file(
            {"docs": "docs/requirements.txt"}, True),
        tests_require=get_contents_from_file("tests/requirements.txt", True),
    )

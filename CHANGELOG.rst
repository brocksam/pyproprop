*******************
pyproprop Changelog
*******************

:Info: Changelog for pyproprop releases.
:Authors: Sam Brockie (sambrockie@icloud.com), Jack Irvine (jack.irvine97@outlook.com)
:Date: 2020-08-19
:Version: 0.4.3

GitHub holds releases, too
==========================

More information can be found on GitHub in the `releases section
<https://github.com/brocksam/pyoproprop/releases>`_.

About this Changelog
====================

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Dates should be (year-month-day) to conform with [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html).

Formatting a New Version
========================

Include sections:

- Added - for new features.
- Changed - for changes in existing functionality.
- Depricated - for soon-to-be removed features.
- Removed - for now removed features.
- Fixed - for any bug fixes.
- Security - in case of vulnerabilities.

Version History
===============

Unreleased
----------

- None

[0.4.4] - 2020-11-27
--------------------

Fixed
~~~~~

- Fix bug which caused `iterable_allowed` `processed_property` objects to be cast incorrectly.
- Add tests for `iterable_allowed` `processed_property` objects to new test module `tests/unit/processed_property/test_iterable.py`.

[0.4.3] - 2020-11-06
--------------------

Added
~~~~~

- Add `is_optimisable` and `is_read_only` boolean attributes to `processed_property` class attributes.
- Add tests to `tests/unit/processed_property/test_optimisable.py` testing optimisable processed properties.

[0.4.2] - 2020-11-06
--------------------

Added
~~~~~

- New test module `tests/unit/processed_property/test_default.py` for processed properties with default values.
- Add docstring to `pypropprop/processed_property.py` with further detail about allowable kwargs for the function.

Fixed
~~~~~

- Fix `DepricationWarning` from ambiguous boolean of empty iterable for default in processed properties.
- Fix bug in default value for default argument in processed properties.
- Fix failing test due to conflict between casting and iterable supported in processed properties.
- Fix bug causing incorrect operation of optional, iterable-allowed, no default processed properties.


[0.4.1] - 2020-09-22
--------------------

Fixed
~~~~~

- Fix bug which raises error when using the `method` kwarg with `processed_property`, as reported in issue #48. Was caused by variables being out of scope in the function `apply_method` with `pyproprop/processed_property.py`.

[0.4.0] - 2020-09-22
--------------------

Added
~~~~~

- A new `Options` utility class is now provided, as requested by issue #40. which allows groupings of options that are supported or unsupported. Default options for can be specified. Handles can also be provided and linked to options so that a dispatcher can be automatically generated for a set of options with associated functions/classes that are callable.
- String formatted is supported by Options, as requested in issue #41.
- Casting to Numpy ndarrays is now supported, as requested by issue #46.
- Processed properties can now be marked as "read-only", raising an `AttributeError` if they are tried to be set more than once.

Changed
~~~~~~~

- `processed_property`'s setter now uses a dispatcher (which is greated during the initial function call) to build the setter method improving performance, as requested by issue #18.


[0.3.0] - 2020-09-16
--------------------

Added
~~~~~

- Expose string formatting capability as stand-alone function as requested by issue #32.
- Add new "hyphen" string formatting type to give "hyphen-case", like "snake_case" but with a hyphen instead of an underscore, related to issue #32.
- Improve coverage from test suite.

Changed
~~~~~~~

- Reformat README with additional badges.

[0.2.2] - 2020-09-05
--------------------

Added
~~~~~

- Added coverage report from codecov.io to README.rst as requested by issue #22.
- Added test coverage for the `pyproprop/utils.py` module.

Changed
~~~~~~~

- Added backtick formatting around values in `processed_property`s with min and max values as requested by issue #21.

Fixed
~~~~~

- Fixed a bug relating to correctly processing and formatting `processed_property` descriptions in error messages, relating to issue #24.

[0.2.1] - 2020-09-02
--------------------

Added
~~~~~

- Support start of sentence capitalisation as requested in issue #19.
- Use `__repr__`s in error messages to help user distinguish between types as requested in issue #20.

[0.2.0] - 2020-09-02
--------------------

Added
~~~~~

- Created new `pyproprop/utils.py` module.
- Add functionality for comparing values of processed properties to one another as requested in issue #11. This comes with a new test module `tests/test_processed_property_comparison.py`.
- Improved case formatting of strings within proessed properties. PyPI package "titlecase" now a project requirement.

Changes
~~~~~~~

- Both Travis CI and AppVeyor now contain logic to first try to install requirements using conda, but if a package is not available on the set-up channels, it falls back to trying to use pip and PyPI.

[0.1.2] - 2020-08-25
--------------------

Added
~~~~~

- `named_iterable` functionality that allows for dot-indexible attributes to be created as requested in issue #5. This is implemented in the `pyproprop/named_iterable.py` module and comes with tests.

Fixes
~~~~~

- PR #6 fixes the bug in issue #3 whereby user-supplied default values were being cast to an expected type, causing an error when used with `uncastable` objects within processed properties.
- PR #9 fixes the bug in issue #4 where error messages for processed properties with non-string options were not formatting correctly.

[0.1.1] - 2020-08-24
--------------------

Added
~~~~~

- Basic user and development documentation.

Changed
~~~~~~~

- Descriptiveness of error messages improved.
- Hyperlinks in README reformatted to ReST.
- Remove `pyproprop/version.py` module with version number hardcoded as a string in `setup.py` because this fixes a problem with conda recipe requiring Numpy as a host dependency.

[0.1.0] - 2020-08-21
--------------------

Changed
~~~~~~~

- Development status classifier upgraded from "4 - Beta" to "5 - Production/Stable.

[0.0.5] - 2020-08-20
--------------------

Added
~~~~~

- Include pyproprop/*, setup.py, LICENSE, CHANGELOG.rst, LICENSE.rst, requirements.txt, docs/* and tests/* in MANIFEST.in.

[0.0.4] - 2020-08-20
--------------------

Added
~~~~~

- ``optimisable`` processed properties (#1).

Changed
~~~~~~~

- Increase Python 3 usage to include older versions 3.6 and 3.7.

[0.0.3] - 2020-08-19
--------------------

Added
~~~~~

- Initial release to PyPI.

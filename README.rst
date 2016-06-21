flake8-strict
=============

.. image:: https://travis-ci.org/smarkets/flake8-strict.png?branch=master
   :alt: Build status
   :target: https://travis-ci.org/smarkets/flake8-strict

Flake8 plugin that checks Python code against a set of opinionated style rules.

Compatible with Python 2.7, 3.3+, PyPy 2.6+ and PyPy 2.4+.

PyPI page: https://pypi.python.org/pypi/flake8_strict

GitHub page: https://github.com/smarkets/flake8-strict

To install using PyPI and pip::

    pip install flake8-strict


Error codes
-----------

* ``S100``: First argument on the same line
* ``S101``: Multi-line construct missing trailing comma


Limitations
-----------

* only source code without print statements is supported, this means:

  * all valid Python 3 code
  * Python 2 code with ``print_function`` enabled

* the existing checks are quite basic, they'll be improved and new
  ones will added
* line/column numbers are off currently


Versioning and backwards compatibility
--------------------------------------

Below 1.0.0: no guarantees.
Above 1.0.0, given a version number MAJOR.MINOR.PATCH:

* MAJOR is updated when backwards incompatible changes happen
* MINOR is updated when a new, backwards compatible, features are introduced
* PATCH is updated when a backwards compatible bug fixes are applied

Changes
-------

0.1.3
'''''

* Fixed reading from stdin
* Fixed not being able to run when pycodestyle, not pep8, is installed (pep8
  has been renamed to pycodestyle and flake8 2.6.0+ doesn't trigger pep8
  installation anymore)
* Added support for set, list and dict literals and comprehensions
* Function calls with single, multi-line arguments are now treated more reasonably

0.1.2
'''''

* Fixed a "ValueError: need more than 2 values to unpack" error (GitHub issue #1).
* Fixed handling argument lists with keyword-only arguments
  (compatibility with PEP 3102), this now doesn't raise S101 in this
  case as it would be a syntax error.

0.1.1
'''''

* Fixed few ``AttributeError: 'Node' object has no attribute 'lineno'`` errors

0.1.0
'''''

First release


License
-------

Copyright (C) 2015 Smarkets Limited <support@smarkets.com>

This module is released under the MIT License: http://www.opensource.org/licenses/mit-license.php (or see the LICENSE file)

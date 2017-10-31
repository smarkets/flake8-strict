import platform
import re

from distutils.version import LooseVersion

from nose.tools import eq_

from flake8_strict import _process_code


def test_processing():
    with open('test_data.py', 'rt') as f:
        code = f.read()

    code = code.strip()

    expected_errors = set()
    for lineno, line in enumerate(code.splitlines()):
        include_errors = True
        match = re.search(r'  # (.*)$', line.strip('\n'))
        if match:
            for code_or_version in match.group(1).split():
                version_match = re.search(r'py(.*):', code_or_version)
                if version_match:
                    include_errors = (
                        LooseVersion(platform.python_version()) >=
                        LooseVersion(version_match.group(1))
                    )
                elif include_errors:
                    expected_errors.add((lineno + 1, code_or_version))

    actual_errors = {
        (line, error_code.name)
        for line, column, error_code in _process_code(code)
    }

    not_caught = expected_errors - actual_errors
    false_negatives = actual_errors - expected_errors

    eq_((not_caught, false_negatives), (set(), set()))

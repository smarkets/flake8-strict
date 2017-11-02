import re

from nose.tools import eq_

from flake8_strict import _process_code


def test_processing():
    with open('test_data.py', 'rt') as f:
        code = f.read()

    code = code.strip()

    expected_errors = set()
    for lineno, line in enumerate(code.splitlines()):
        match = re.search(r'  # (.*)$', line.strip('\n'))
        if match:
            for error_code in match.group(1).split():
                expected_errors.add((lineno + 1, error_code))

    actual_errors = {
        (line, error_code.name)
        for line, column, error_code in _process_code(code)
    }

    not_caught = expected_errors - actual_errors
    false_negatives = actual_errors - expected_errors

    eq_((not_caught, false_negatives), (set(), set()))

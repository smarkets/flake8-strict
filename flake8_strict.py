#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import enum
import itertools
import sys

try:
    import pycodestyle
except ImportError:
    import pep8 as pycodestyle


# Use lib2to3 fork from black (https://github.com/ambv/black.git)
try:
    import black  # noqa: F401
    from blib2to3 import pytree
    from blib2to3.pgen2.driver import Driver
    from blib2to3.pgen2 import token
    from blib2to3.pygram import python_grammar_no_print_statement
except ImportError:
    from lib2to3 import pytree
    from lib2to3.pgen2.driver import Driver
    from lib2to3.pgen2 import token
    from lib2to3.pygram import python_grammar_no_print_statement


__version__ = '0.2.1'


@enum.unique
class ErrorCode(enum.Enum):
    S100 = 'First argument on the same line'
    S101 = 'Multi-line construct missing trailing comma'


class Flake8Checker(object):
    name = __name__
    version = __version__

    def __init__(self, tree, filename):
        self._filename = filename

    def run(self):
        errors = _process_file(self._filename)
        for line, column, error_code in errors:
            yield (line, column, '%s %s' % (error_code.name, error_code.value), type(self))


_driver = Driver(
    grammar=python_grammar_no_print_statement,
    convert=pytree.convert,
)


def _process_file(filename):
    if filename == 'stdin':
        code = pycodestyle.stdin_get_value()
    else:
        with open(filename, 'rb') as f:
            code = f.read().decode('utf-8')
    return _process_code(code)


def _process_code(code):
    tree = _driver.parse_string(
        '%s%s' % (code, '\n' if code and code[-1] != '\n' else ''),
    )
    return _process_tree(tree)


def _process_tree(tree):
    iterables = []
    nice_type = pytree.type_repr(tree.type)
    if nice_type == 'parameters':
        iterables.append(_process_parameters(tree))
    elif nice_type == 'trailer':
        iterables.append(_process_trailer(tree))
    elif nice_type == 'atom':
        iterables.append(_process_atom(tree))
    elif nice_type == 'decorator':
        iterables.append(_process_decorator(tree))
    elif nice_type == 'import_from':
        iterables.append(_process_import_from(tree))
    elif nice_type == 'classdef':
        iterables.append(_process_classdef(tree))

    iterables.extend(_process_tree(c) for c in tree.children)

    return itertools.chain.from_iterable(iterables)


def _process_parameters(parameters):
    if not _is_multi_line(parameters):
        return

    open_parenthesis, args_list, close_parenthesis = parameters.children

    elements = args_list.children
    if not elements:
        # TODO complain about multi-line argument list with nothing in it
        return

    first_element = elements[0]
    if open_parenthesis.lineno == first_element.get_lineno():
        yield _error(first_element, ErrorCode.S100)

    last_element = elements[-1]

    # We only accept lack of trailing comma in case of the parameter
    # list containing any use of * or ** as adding the trailing comma
    # is a syntax error (in Python versions below 3.6).
    no_variadic_arguments = all(
        [
            element.type not in (token.STAR, token.DOUBLESTAR)
            for element in elements
        ]
    ) and not _is_unpacking_element(last_element)

    # We're allowed trailing commas here if we're on Python 3.6 +.
    variadic_comma_allowed = no_variadic_arguments or sys.version_info >= (3, 6)

    if last_element.type != token.COMMA and variadic_comma_allowed:
        yield _error(last_element, ErrorCode.S101)


def _is_unpacking_element(element):
    element_type = pytree.type_repr(element.type)
    if element_type == 'argument':
        return element.children[0].type in [token.STAR, token.DOUBLESTAR]
    return element_type == 'star_expr'


def _is_multi_line(tree):
    return len(set(t.get_lineno() for t in tree.children)) > 1


def _process_trailer(trailer):
    # The definition of trailer node:
    # trailer: '(' [arglist] ')' | '[' subscriptlist ']' | '.' NAME
    children = trailer.children
    if len(children) == 3:
        middle = children[1]
        if pytree.type_repr(middle.type) == 'atom':
            return _process_atom(middle)
        else:
            return _process_parameters(trailer)
    else:
        return []


def _process_atom(atom):
    # The definition of atom node:
    # atom: ('(' [yield_expr|testlist_gexp] ')' |
    #        '[' [listmaker] ']' |
    #        '{' [dictsetmaker] '}' |
    #        '`' testlist1 '`' |
    #        NAME | NUMBER | STRING+ | '.' '.' '.')
    if len(atom.children) < 3 or not _is_multi_line(atom):
        return

    left = atom.children[0]
    if left.value not in {'{', '['}:
        return
    open_parenthesis, maker, close_parenthesis = atom.children
    if open_parenthesis.lineno == maker.get_lineno():
        yield _error(maker, ErrorCode.S100)

    if maker.children:
        last_maker_element = maker.children[-1]
    else:
        # If we're dealing with a one element list we'll land here
        last_maker_element = maker

    # Enforcing trailing commas in list/dict/set comprehensions seems too strict
    # so we won't do it for now even if it is syntactically allowed.
    has_comprehension_inside = not {'comp_for', 'old_comp_for'}.isdisjoint({
        pytree.type_repr(node.type) for node in maker.children
    })
    if last_maker_element.type != token.COMMA and not has_comprehension_inside:
        yield _error(last_maker_element, ErrorCode.S101)


def _process_decorator(decorator):
    # The definition of decorator node:
    # decorator: '@' dotted_name [ '(' [arglist] ')' ] NEWLINE
    copied_decorator = copy.copy(decorator)
    copied_decorator.children = decorator.children[2:5]
    return _process_trailer(copied_decorator)


def _process_import_from(import_from):
    # The definition of import_from node:
    # import_from: ('from' (('.' | '...')* dotted_name | ('.' | '...')+)
    #              'import' ('*' | '(' import_as_names ')' | import_as_names))
    last_element = import_from.children[-1]
    last_element_type = pytree.type_repr(last_element.type)
    if last_element_type == token.RPAR:
        copied_import_from = copy.copy(import_from)
        copied_import_from.children = import_from.children[-3:]
        return _process_parameters(copied_import_from)
    return []


def _process_classdef(classdef):
    # The definition of classdef node:
    # classdef: 'class' NAME ['(' [arglist] ')'] ':' suite
    copied_classdef = copy.copy(classdef)
    copied_classdef.children = classdef.children[2:5]
    return _process_trailer(copied_classdef)


def _error(element, error_code):
    return (element.get_lineno(), _get_column(element), error_code)


def _get_column(node):
    while not isinstance(node, pytree.Leaf):
        if not node.children:
            return
        node = node.children[0]
    return node.column


if __name__ == '__main__':
    exit_code = 0
    for filename in sys.argv[1:]:
        errors = list(_process_file(filename))
        if errors:
            exit_code = 1

        for line, column, error in errors:
            print(
                '%s:%s:%s %s %s' % (
                    filename,
                    line,
                    column,
                    error.name,
                    error.value,
                ),
            )

    sys.exit(exit_code)

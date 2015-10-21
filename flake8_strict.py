import enum
import itertools

from lib2to3 import pytree
from lib2to3.pgen2.driver import Driver
from lib2to3.pgen2 import token
from lib2to3.pygram import python_grammar_no_print_statement

__version__ = '0.1.0'


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
        with open(self._filename, 'rt') as f:
            code = f.read()
        errors = _process_code(code)
        for line, column, error_code in errors:
            yield (line, column, '%s %s' % (error_code.name, error_code.value), type(self))


_driver = Driver(
    grammar=python_grammar_no_print_statement,
    convert=pytree.convert,
)


def _process_code(code):
    tree = _driver.parse_string(code)
    return _process_tree(tree)


def _process_tree(tree):
    iterables = []
    nice_type = pytree.type_repr(tree.type)
    if nice_type in ('parameters', 'trailer'):
        iterables.append(_process_parameters(tree))

    iterables.extend(_process_tree(c) for c in tree.children)

    return itertools.chain.from_iterable(iterables)


def _process_parameters(parameters):
    multi_line = len(set(t.get_lineno() for t in parameters.children)) > 1
    if not multi_line:
        return

    open_parenthesis, args_list, close_parenthesis = parameters.children
    elements = args_list.children
    if not elements:
        # TODO complain about multi-line argument list with nothing in it
        return

    first_element = elements[0]
    if open_parenthesis.lineno == first_element.lineno:
        yield _error(first_element, ErrorCode.S100)

    last_element = elements[-1]

    # We only accept lack of trailing comma in case of parameter list ending
    # with *args or **kwargs because trailing comma there is a syntax error
    if (
        last_element.type != token.COMMA and
        (
            len(elements) < 2 or
            elements[-2].type not in (token.STAR, token.DOUBLESTAR)
        )
    ):
        yield _error(last_element, ErrorCode.S101)


def _error(element, error_code):
    return (element.lineno, element.column, error_code)

from fluffy.patterns.case import *
from fluffy.patterns.errors import *
from fluffy.patterns.expressions import *
from fluffy.patterns.match import *
from fluffy.patterns.patterns import *
from fluffy.patterns.variables import *
from fluffy.patterns.variables import _


def error(value: Any) -> Error:
    """Returns an instance of `Error` with the specified value."""
    return Error(value)


def apply(f_: Callable, *x_: Any) -> Function:
    """Returns an instance of `Function` with the specified arguments."""
    return Function(f_, *x_)


def of(type_: Type, variable: Optional[Variable] = None) -> TypePattern:
    """Returns a `Type` pattern for the specified variable."""
    return TypePattern(type_, variable.name if variable is not None else None)

from fun.patterns.case import *
from fun.patterns.errors import *
from fun.patterns.expressions import *
from fun.patterns.match import *
from fun.patterns.patterns import *
from fun.patterns.variables import *
from fun.patterns.variables import _


def error(value: Any) -> Error:
    """Returns an instance of `Error` with the specified value."""
    return Error(value)


def apply(f_: Callable, *x_: Any) -> Function:
    """Returns an instance of `Function` with the specified arguments."""
    return Function(f_, *x_)


def of(type_: Type, variable: Optional[Variable] = None) -> TypePattern:
    """Returns a `Type` pattern for the specified variable."""
    return TypePattern(type_, variable.name if variable is not None else None)

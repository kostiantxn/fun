from fluffy.patterns.case import *
from fluffy.patterns.errors import *
from fluffy.patterns.expressions import *
from fluffy.patterns.match import *
from fluffy.patterns.patterns import *
from fluffy.patterns.variables import *
from fluffy.patterns.variables import _


def raises(error) -> Raises:
    """Returns an instance of `Raises` with the specified `error`."""
    return Raises(error)


def apply(func, *args) -> Function:
    """Returns an instance of `Function` with the specified arguments."""
    return Function(func, *args)


def of(cls, variable: Optional[expressions.Variable] = None) -> TypePattern:
    """Returns a `Type` pattern for the specified variable."""
    return TypePattern(cls, variable.name if variable is not None else None)

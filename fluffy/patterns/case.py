from fluffy.patterns.patterns import as_pattern
from fluffy.patterns.expressions import as_expression


class Case:
    """Contains a pair of (<pattern>, <expression>)."""

    def __init__(self, pattern, expression):
        self.pattern = as_pattern(pattern)
        self.expression = as_expression(expression)

    def __iter__(self):
        return iter([self.pattern, self.expression])


class Create:
    """Defines operators that allow to create `Case` instances
    using the following syntax:
        case = Create()
        case | pattern > expression"""

    class Pattern:
        def __init__(self, pattern):
            self.pattern = pattern

        def __gt__(self, expression) -> Case:
            return Case(self.pattern, expression)

    def __or__(self, pattern) -> 'Create.Pattern':
        return Create.Pattern(pattern)


case = Create()

from fluffy.patterns.patterns import as_pattern
from fluffy.patterns.expression import as_expression


class Case:
    """Contains a pair of (<pattern>, <expression>)."""

    def __init__(self, pattern, result):
        self._pattern = as_pattern(pattern)
        self._expression = as_expression(result)

    def __iter__(self):
        return self._pattern, self._expression


class Create:
    """Defines operators that allow to create `Case` instances."""

    class Pattern:
        def __init__(self, pattern):
            self.pattern = pattern

        def __gt__(self, expression):
            return Case(self.pattern, expression)

    def __or__(self, pattern):
        return Create.Pattern(pattern)


case = Create()

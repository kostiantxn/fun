class Case:
    """Contains a pair of (<pattern>, <expression>)."""

    def __init__(self, pattern, result):
        self._pattern = pattern
        self._expression = result

    def __iter__(self):
        return self._pattern, self._expression

    def __repr__(self):
        return f'Case({repr(self._pattern)}, {repr(self._expression)})'


class Creation:
    """Defines operators that allow to create `Case` instances."""

    class Pattern:
        def __init__(self, pattern):
            self.pattern = pattern

        def __gt__(self, expression):
            return Case(self.pattern, expression)

    def __or__(self, pattern):
        return Creation.Pattern(pattern)


case = Creation()

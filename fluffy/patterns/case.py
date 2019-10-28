from fluffy.patterns.patterns import pattern
from fluffy.patterns.expressions import expression


class Case:
    """Contains a pair of (`pattern`, `expression`)."""

    def __init__(self, pattern, expression):
        self.pattern = pattern
        self.expression = expression

    def __iter__(self):
        return iter([pattern(self.pattern),
                     expression(self.expression)])

    def __repr__(self):
        return f'Case(' \
                    f'pattern={repr(self.pattern)}, ' \
                    f'expression={repr(self.expression)}' \
               f')'


class Creation:
    """Provides pretty syntax to create instances of `Case`.

    Examples:
        >>> case = Creation()
        >>> case | 1 > '1'
        Case(pattern=1, expression='1')
    """

    class First:
        def __init__(self, pattern):
            self.pattern = pattern

        def __gt__(self, expression) -> Case:
            return Case(self.pattern, expression)

    def __or__(self, pattern) -> 'Creation.First':
        return Creation.First(pattern)


case: Creation = Creation()

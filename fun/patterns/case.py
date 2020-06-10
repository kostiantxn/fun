from fun.patterns.patterns import pattern
from fun.patterns.expressions import expression


class Case:
    """Contains a pair of (`pattern`, `expression`)."""

    def __init__(self, pattern_, expression_):
        self.pattern = pattern_
        self.expression = expression_

    def __iter__(self):
        return iter([pattern(self.pattern),
                     expression(self.expression)])

    def __repr__(self):
        return f'Case(' \
                    f'pattern_={repr(self.pattern)}, ' \
                    f'expression_={repr(self.expression)}' \
               f')'


class Creation:
    """Provides pretty syntax to create instances of `Case`.

    Examples:
        >>> case = Creation()
        >>> case | 1 > '1'
        Case(pattern_=1, expression_='1')
    """

    class First:
        def __init__(self, pattern_):
            self.pattern = pattern_

        def __gt__(self, expression_) -> Case:
            return Case(self.pattern, expression_)

    def __or__(self, pattern_) -> 'Creation.First':
        return Creation.First(pattern_)


case: Creation = Creation()

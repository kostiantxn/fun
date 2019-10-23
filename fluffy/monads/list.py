class List:

    @classmethod
    def unit(cls, x):
        return Node(x)

    @classmethod
    def bind(cls, m, g):
        def concat(x, y):
            if isinstance(x, Empty):
                return y
            if isinstance(x, Node):
                return Node(x.value, concat(x.tail, y))

        def join(x):
            if isinstance(x, Empty):
                return Empty()
            if isinstance(x, Node):
                return concat(x.value, join(x.tail))

        def fmap(x, f):
            if isinstance(x, Empty):
                return Empty()
            if isinstance(x, Node):
                return Node(f(x.value), fmap(x.tail, f))

        return join(fmap(m, g))


class Node(List):

    def __init__(self, value, tail=None):
        self.value = value
        self.tail = tail or Empty()

    def __str__(self):
        return f'Node {self.value} ({self.tail})'


class Empty(List):

    def __str__(self):
        return 'Empty'


class L:

    def __class_getitem__(cls, items):
        """Creates a `List` instance from a Python list."""

        if not isinstance(items, tuple):
            items = (items, )

        if len(items) == 0:
            return Empty()
        else:
            return Node(items[0], L[items[1:]])

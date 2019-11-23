from typing import Any, Callable, Optional, Iterable

from fluffy.monads.monad import Monad


class List(Monad):
    """A linked list.

    An implementation of the linked list data structure. The implementation has
    the following form:

        data List a = Empty | Node a (List a)
    """

    def __class_getitem__(cls, items: Any) -> 'List':
        """Creates a `List` instance from a Python list.

        Creates an instance of `List` from the specified value. A value may
        be either a single value or a tuple. A tuple may have one of the
        following forms:
            - [1, 2, 3]: creates a list with values 1, 2 and 3;
            - [1, ..., 5]: creates a list with values 1, 2, 3, 4 and 5;
            - [1, 3, ..., 7]: creates a list with values 1, 3, 5 and 7.

        Args:
            items: A value to create an instance of `List` from.

        Examples:
            >>> List[1]
            Node(1, Empty())

            >>> List[1, 2, 3]
            Node(1, Node(2, Node(3, Empty())))

            >>> List[1, ..., 5]
            Node(1, Node(2, Node(3, Node(4, Node(5, Empty())))))

            >>> List[1, 3, ..., 9]
            Node(1, Node(3, Node(5, Node(7, Node(9, Empty())))))
        """

        if not isinstance(items, tuple):
            items = (items, )

        def progression(start, end, step):
            while start <= end:
                yield start
                start += step

        if len(items) == 3:
            # Sequences like [a, ..., c].
            if items[1] is ...:
                a = items[0]
                c = items[2]

                return List.new(progression(a, c, step=1))

        if len(items) == 4:
            # Sequences like [a, b, ..., c].
            if items[2] is ...:
                a = items[0]
                b = items[1]
                c = items[3]

                return List.new(progression(a, c, step=b - a))

        return List.new(items)

    @classmethod
    def empty(cls) -> 'List':
        """Creates an empty `List`."""
        return Empty()

    @classmethod
    def new(cls, items: Iterable[Any]) -> 'List':
        """Creates a new `List` from the specified items.

        Example:
            >>> List.new([1, 2, 3])
            Node(1, Node(2, Node(3, Empty())))

            >>> List.new([])
            Empty()
        """

        def new(iterator):
            try:
                return Node(next(iterator), new(iterator))
            except StopIteration:
                return Empty()

        return new(iter(items))

    @classmethod
    def unit(cls, x: Any) -> 'List':
        return Node(x)

    @classmethod
    def bind(cls, m: 'List', g: Callable) -> 'List':
        def concat(x, y):
            if isinstance(x, Empty):
                return y
            if isinstance(x, Node):
                return Node(x.value, concat(x.next, y))

        def join(x):
            if isinstance(x, Empty):
                return Empty()
            if isinstance(x, Node):
                return concat(x.value, join(x.next))

        def fmap(f, x):
            if isinstance(x, Empty):
                return Empty()
            if isinstance(x, Node):
                return Node(f(x.value), fmap(f, x.next))

        return join(fmap(g, m))


class Node(List):
    """Represents a node of a linked list.

    A node contains a value and a reference to the next node of a list.
    """

    def __init__(self, value: Any, next_: Optional[List] = None):
        """Initialises the node.

        Args:
            value: A value to store in the node.
            next_: A reference to the next node.
        """

        self._value = value
        self._next = next_ or Empty()

    @property
    def value(self) -> Any:
        """Returns the value stored in the node."""
        return self._value

    @property
    def next(self) -> List:
        """Returns the next node."""
        return self._next

    def __iter__(self):
        node = self
        while not isinstance(node, Empty):
            yield node._value
            node = node._next

    def __repr__(self):
        return f'Node({repr(self._value)}, {repr(self._next)})'

    def __str__(self):
        return 'List[' + ', '.join(map(str, self)) + ']'


class Empty(List):
    """Represents an empty list."""

    def __iter__(self):
        return iter(())

    def __repr__(self):
        return 'Empty()'

    def __str__(self):
        return 'List[]'

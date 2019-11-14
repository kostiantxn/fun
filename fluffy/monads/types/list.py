from typing import Any, Callable, Optional


class List:
    """A linked list.

    An implementation of the linked list data structure. The implementation has
    the following form:

        data List a = Empty | Node a (List a)

    The type implements the `Functor`, `Applicative`, `Monoid` and the `Monad`
    type classes.
    """

    def __class_getitem__(cls, items: Any):
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

        def succ(item):
            if not isinstance(item, int):
                raise NotImplemented

            return item + 1

        def progression(start, next_, end):
            if next_ is None:
                next_ = succ(start)

            item = start
            step = 0

            while item != next_:
                item = succ(item)
                step += 1

            yield start
            yield item

            while item != end:
                for _ in range(step - 1):
                    item = succ(item)
                    if item == end:
                        return

                item = succ(item)
                yield item

        def new(iterable):
            iterator = iter(iterable)
            result = None
            node = None

            while True:
                try:
                    item = next(iterator)

                    if result is None:
                        result = node = Node(item)
                    else:
                        node._next = Node(item)
                        node = node.next
                except StopIteration:
                    break

            return result or Empty()

        if len(items) == 3:
            # Sequences like [a, ..., c].
            if items[1] is ...:
                return new(progression(items[0], None, items[2]))

        if len(items) == 4:
            # Sequences like [a, b, ..., c].
            if items[2] is ...:
                return new(progression(items[0], items[1], items[3]))

        return new(items)

    @classmethod
    def empty(cls) -> 'List':
        """Creates an empty `List`."""
        return Empty()

    @classmethod
    def unit(cls, x: Any) -> 'List':
        """Implementation of the `unit :: a -> m a` function.

        The same as `return x` in Haskell.

        Args:
            x: Any value to wrap into `List`.

        Returns:
            An instance of `List` containing a single `x`.
        """
        return Node(x)

    @classmethod
    def bind(cls, m: 'List', g: Callable) -> 'List':
        """Implementation of the `bind :: m a -> (a -> m b) -> m b` function.

        The same as `m >>= g` in Haskell.

        Args:
            m: An instance of `List` to apply the function `g` to.
            g: A function `a -> m b` to apply to each element of `m`.
        """

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

        def fmap(x, f):
            if isinstance(x, Empty):
                return Empty()
            if isinstance(x, Node):
                return Node(f(x.value), fmap(x.next, f))

        return join(fmap(m, g))


class Node(List):
    """Represents a node of a linked list.

    A node contains a value and a reference to the next node of the list.
    """

    def __init__(self, value: Any, next_: Optional['Node'] = None):
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
    def next(self) -> 'Node':
        """Returns the next node."""
        return self._next

    def __iter__(self):
        node = self
        while not isinstance(node, Empty):
            yield node._value
            node = node._next

    def __repr__(self):
        return f'Node(value={repr(self._value)}, next_={repr(self._next)})'

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

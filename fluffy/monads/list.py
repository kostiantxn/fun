from typing import Any, Callable


class List:
    """A linked list.

    A linked list data type. Implements `Functor`, `Applicative` and `Monad`
    type classes.
    """

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
                    if (item := succ(item)) == end:
                        return

                yield (item := succ(item))

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
                        node.tail = Node(item)
                        node = node.tail
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


class Node(List):

    def __init__(self, value, tail=None):
        self.value = value
        self.tail = tail or Empty()

    def __iter__(self):
        node = self
        while not isinstance(node, Empty):
            yield node.value
            node = node.tail

    def __repr__(self):
        return f'Node({repr(self.value)}, {repr(self.tail)})'

    def __str__(self):
        return 'List[' + ', '.join(map(str, self)) + ']'


class Empty(List):

    def __iter__(self):
        return iter(())

    def __repr__(self):
        return 'Empty()'

    def __str__(self):
        return 'List[]'

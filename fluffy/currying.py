import inspect
from typing import Callable, Any


class Curried:
    """A curried function.

    Defines `__call__` in the following way:
        1. If the underlying `func` can be called with supplied arguments,
           then it will be called and it's value returned.
        2. If supplied arguments can partially be bound to the arguments
           of the underlying `func` then an new instance of `Curried` with
           new arguments is returned.
        3. Otherwise, an exception is thrown.

    Examples:
        def add(x, y):
            return x + y

        add = Curried(add)

        # Returns `Curried(add, args=[1])` since `args=[1]` can be partially
        # bound to `add` as `add(x=1).
        increment = add(1)

        # Returns 10 since `add` can be called with `args=[1, 9]`.
        ten = increment(9)

        # Raises an error since `args=[1, 2, 3]` cannot be bound
        # (because `add` has only two arguments, not three).
        add(1, 2, 3)
    """

    def __init__(self, func: Callable, args: Any, kwargs: Any):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __repr__(self):
        return f'Curried(' \
               f'func={repr(self._func)}, ' \
               f'args={repr(self._args)}, ' \
               f'kwargs={repr(self._kwargs)}' \
               f')'

    def __call__(self, *args, **kwargs):
        if args and self._kwargs:
            raise ValueError('Cannot use `args` when '
                             '`kwargs` have been specified.')
        for key in kwargs:
            if key in self._kwargs:
                raise ValueError(f'Key {key} has already been specified.')

        args = self._args + list(args)
        kwargs.update(self._kwargs)

        signature = inspect.signature(self._func)

        try:
            signature.bind(*args, **kwargs)
        except TypeError:
            try:
                signature.bind_partial(*args, **kwargs)
            except TypeError:
                raise
            else:
                # Means that all arguments can partially be bound
                # to the signature and we can proceed currying.
                return Curried(self._func, args, kwargs)
        else:
            # Means that all arguments can be bound to the signature
            # and the function can safely be called.
            return self._func(*args, **kwargs)


def curry(func: Callable) -> Curried:
    """Returns an instance of `Curried` with the specified `func`.

    Examples:
        @curry
        def add(x, y):
            return x + y

        increment = add(1)
        ten = increment(9)

        print(ten)  # Prints 10.
    """
    return Curried(func, [], {})

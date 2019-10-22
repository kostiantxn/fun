import ast
import inspect
from copy import deepcopy
from functools import wraps


def monad(cls):
    """A decorator that converts the decorated function to a monadic one."""

    def decorator(func):
        tree = ast.parse(inspect.getsource(func))
        tree.body[0].decorator_list = []

        validate(tree)

        @wraps(func)
        def decorated(*args, **kwargs):
            return Computation(cls, tree, func(*args, **kwargs)).reduce()

        return decorated

    return decorator


def appropriate(statement):
    """Checks whether the statement is appropriate for a monad."""

    if isinstance(statement, ast.Assign):
        return True

    if isinstance(statement, ast.Expr):
        if isinstance(statement.value, ast.Str):
            return True  # Documentation.
        if isinstance(statement.value, ast.Yield):
            return True

    if isinstance(statement, ast.Return):
        return True

    return False


def validate(tree):
    """Checks the syntax tree of a function to ensure
    that it is a appropriate for a monadic function."""

    func = tree.body[0]
    code = func.body

    for statement in code:
        if not appropriate(statement):
            raise SyntaxError(f'Inappropriate statement: {statement}.')


def copy(tree, gen, offset):
    """Compiles a function from the tree and the generator
    with the specified offset."""

    tree = deepcopy(tree)
    func = tree.body[0]
    name = func.name

    if offset > 0:
        # Remove already executed rows.
        rows = func.body[offset - 1:]

        # Replace the following code:
        #       x = yield y()
        # with this:
        #       x = yield
        # to prevent multiple evaluations of `y` but to
        # leave the ability to send a value to `x`.

        if isinstance(rows[0], ast.Assign) and \
           isinstance(rows[0].value, ast.Yield):
            rows[0].value.value = None
        else:
            raise ValueError(f'Inappropriate statement: {rows[0]}.')

        func.body = rows

    source = compile(tree, '<source>', 'exec')

    scope = {}
    scope.update(gen.gi_frame.f_globals)
    scope.update(gen.gi_frame.f_locals)

    # The compiled function will be stored here.
    def_ = {}

    # Compile the truncated source code.
    exec(source, scope, def_)

    return def_[name]


class Computation:

    def __init__(self, type_, tree, gen, offset=0):
        self._type = type_
        self._tree = tree
        self._func = copy(tree, gen, offset)
        self._offset = offset

    def __call__(self, x):
        f = self._func()

        # The first invocation does not do anything,
        # it just allows to send the first value.
        f.send(None)

        try:
            m = f.send(x)
            g = Computation(self._type,
                            self._tree,
                            f,
                            self._offset + 1)

            return self._type.bind(m, g)

        except StopIteration as result:
            if result.value is not None:
                return self._type.unit(result.value)
            else:
                raise NotImplemented

    def reduce(self):
        f = self._func()
        m = f.send(None)
        g = Computation(self._type,
                        self._tree,
                        f,
                        offset=1)

        return self._type.bind(m, g)

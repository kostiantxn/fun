import ast
import inspect
from functools import wraps
from importlib import import_module
from typing import Type, Callable


def monad(type_: Type) -> Callable:
    """Converts the decorated function to a monad.

    Converts the function to a monadic evaluation of the specified type. The
    function must consist of the following statements:

        x = g(y)     # The same as 'let x = g y' in Haskell.
        x = yield m  # The same as 'x <- m' in Haskell.
        yield m      # The same as 'm' in Haskell.
        return x     # The same as 'return x' in Haskell.

    A decorated function must end with either a monadic value of the specified
    type or a return statement. In a case, if a function has any other
    statements or the last statement is not valid (neither a monadic value nor
    a return statement), an exception is raised.

    The decorator converts a function with statements defined above to a chain
    of bindings of monadic operations. For example, the following code:

        @monad(List)
        def triples(n):
            x = yield List[1, ..., n]
            y = yield List[x, ..., n]
            z = yield List[y, ..., n]

            return (x, y, z)

    Will be roughly converted to the following:

        triples = lambda n: (
            List[1, ..., n] >>= (lambda x:
            List[x, ..., n] >>= (lambda y:
            List[y, ..., n] >>= (lambda z:
                List.unit((x, y, z))
            )))
        )

        # Here `>>=` is the `List.bind` function.

    Args:
        type_: A type that is an instance of `Monad`.

    Returns:
        A decorator to wrap a function with.
    """

    def decorator(func):
        tree = _tree(type_, func)
        code = compile(tree, '<source>', 'exec')

        globals_ = vars(import_module(func.__module__))
        locals_ = {}

        exec(code, globals_, locals_)

        @wraps(func)
        def decorated(*args, **kwargs):
            return locals_[func.__name__](*args, **kwargs)

        return decorated

    return decorator


def _tree(type_: Type, func: Callable) -> ast.AST:
    """Constructs an abstract syntax tree of a chain of bindings.

    Args:
        type_: A type that is an instance of `Monad`.
        func: A function to construct a tree from.

    Returns:
        An abstract syntax tree constructed from the specified function.

    Raises:
        SyntaxError: Raised in a case if the specified function contains
            invalid statements.
    """

    def arg(name):
        return ast.arg(arg=name, annotation=None, type_comment=None)

    def args(names):
        if isinstance(names, ast.arguments):
            return names
        else:
            return ast.arguments(posonlyargs=[],
                                 args=[arg(name) for name in names],
                                 vararg=None,
                                 kwonlyargs=[],
                                 kw_defaults=[],
                                 kwarg=None,
                                 defaults=[])

    def attr(name):
        return ast.Attribute(
            value=ast.Name(id=type_.__name__, ctx=ast.Load()),
            attr=name,
            ctx=ast.Load())

    def call(func_, args_):
        return ast.Call(func=func_, args=args_, keywords=[])

    def lambda_(args_, body_):
        return ast.Lambda(args=args(args_), body=body_)

    def assign(name, value):
        return ast.Assign(targets=[ast.Name(id=name, ctx=ast.Store())],
                          value=value,
                          type_comment=None)

    def module(*statements):
        return ast.Module(body=list(statements), type_ignores=[])

    tree = ast.parse(inspect.getsource(func))

    unit = attr('unit')
    bind = attr('bind')

    def monad_(i=0):
        """Converts the code from the i-th line to a monad."""

        line = tree.body[0].body[i]

        if isinstance(line, ast.Return):
            return call(unit, [line.value])

        if isinstance(line, ast.Assign):
            if len(line.targets) != 1:
                raise SyntaxError(f'Only 1 variable can be assigned.')

            # Expressions like `x = yield y`.
            # The same as `x <- y` in Haskell.
            if isinstance(line.value, ast.Yield):
                n = line.targets[0].id  # The name of the variable.
                m = line.value.value    # The value after `yield`.
                g = lambda_([n], monad_(i + 1))

                return call(bind, [m, g])

            # Expressions like `x = y`.
            # The same as `let x = y` in Haskell.
            else:
                n = line.targets[0].id  # The name of the variable.
                x = line.value          # The value being assigned to.
                f = lambda_([n], monad_(i + 1))

                return call(f, [x])

        if isinstance(line, ast.Expr):

            # Expressions like `yield y`.
            # The same as `y` in Haskell.
            if isinstance(line.value, ast.Yield):
                m = line.value.value  # The value after `yield`.
                g = lambda_(['_'], monad_(i + 1))

                return call(bind, [m, g])

            # Documentation.
            if isinstance(line.value, ast.Constant) and \
               isinstance(line.value.value, str):
                return monad_(i + 1)

        raise SyntaxError(f'Invalid statement: {line}.')

    result = lambda_(tree.body[0].args, monad_())
    result = assign(func.__name__, result)
    result = ast.fix_missing_locations(module(result))

    return result

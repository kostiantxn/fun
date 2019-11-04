import ast
import inspect
from functools import wraps
from importlib import import_module
from typing import Type, Callable, List, Union


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

        if func.__name__ in locals_:
            newfunc = locals_[func.__name__]
            newfunc = wraps(func)(newfunc)
        else:
            raise Exception(f'The function "{func.__name__}" '
                            f'was not constructed correctly.')

        return newfunc

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

    tree = ast.parse(inspect.getsource(func))

    unit = _attr(type_.__name__, 'unit')
    bind = _attr(type_.__name__, 'bind')

    def _from(i: int) -> ast.AST:
        """Constructs a tree from the i-th line."""

        line = tree.body[0].body[i]

        if isinstance(line, ast.Return):
            return _call(unit, [line.value])

        if isinstance(line, ast.Assign):
            if len(line.targets) != 1:
                raise SyntaxError(f'Only one variable can be assigned.')

            # Expressions like `x = yield m`.
            # The same as `x <- y` in Haskell.
            if isinstance(line.value, ast.Yield):
                n = line.targets[0].id  # The name of the variable.
                m = line.value.value    # The value after `yield`.
                g = _lambda([n], _from(i + 1))

                return _call(bind, [m, g])

            # Expressions like `x = g(y)`.
            # The same as `let x = g y` in Haskell.
            else:
                n = line.targets[0].id  # The name of the variable.
                x = line.value          # The value being assigned to.
                f = _lambda([n], _from(i + 1))

                return _call(f, [x])

        if isinstance(line, ast.Expr):
            # Expressions like `yield m`.
            # The same as `m` in Haskell.
            if isinstance(line.value, ast.Yield):
                m = line.value.value  # The value after `yield`.
                g = _lambda(['_'], _from(i + 1))

                return _call(bind, [m, g])

            # Documentation.
            if isinstance(line.value, ast.Constant) and \
               isinstance(line.value.value, str):
                return _from(i + 1)

        raise SyntaxError(f'Invalid statement: {line}.')

    result = _lambda(tree.body[0].args, _from(0))
    result = _assign(func.__name__, result)
    result = ast.fix_missing_locations(_module(result))

    return result


def _arg(name: str) -> ast.arg:
    """Creates an instance of `ast.arg` with the specified name."""
    return ast.arg(arg=name, annotation=None, type_comment=None)


def _args(names: List[str]) -> ast.arguments:
    """Creates an instance of `ast.arguments`."""
    return ast.arguments(posonlyargs=[],
                         args=[_arg(name) for name in names],
                         vararg=None,
                         kwonlyargs=[],
                         kw_defaults=[],
                         kwarg=None,
                         defaults=[])


def _attr(value: str, name: str) -> ast.Attribute:
    """Creates an instance of `ast.Attribute`."""
    return ast.Attribute(value=ast.Name(id=value, ctx=ast.Load()),
                         attr=name,
                         ctx=ast.Load())


def _call(func: ast.AST, args: List) -> ast.Call:
    """Creates an instance of `ast.Call`."""
    return ast.Call(func=func, args=args, keywords=[])


def _lambda(args: Union[List, ast.arguments], body: ast.AST) -> ast.Lambda:
    """Creates an instance of `ast.Lambda`."""
    if isinstance(args, ast.arguments):
        return ast.Lambda(args=args, body=body)
    else:
        return ast.Lambda(args=_args(args), body=body)


def _assign(name: str, value: ast.AST) -> ast.Assign:
    """Creates an instance of `ast.Assign`."""
    return ast.Assign(targets=[ast.Name(id=name, ctx=ast.Store())],
                      value=value,
                      type_comment=None)


def _module(*statements: ast.AST) -> ast.Module:
    """Creates an instance of `ast.Module`."""
    return ast.Module(body=list(statements), type_ignores=[])

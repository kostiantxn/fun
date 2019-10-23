import ast
import inspect
from functools import wraps
from importlib import import_module


def monad(cls):
    """A decorator that converts the decorated function to a monad."""

    def decorator(func):
        tree = build(func, cls)
        code = compile(tree, '<source>', 'exec')

        globals_ = vars(import_module(func.__module__))
        locals_ = {}

        exec(code, globals_, locals_)

        @wraps(func)
        def decorated(*args, **kwargs):
            return locals_[func.__name__](*args, **kwargs)

        return decorated

    return decorator


def build(func, cls):
    """Constructs a tree of a monadic lambda from the specified function."""

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
        return ast.Attribute(value=ast.Name(id=cls.__name__, ctx=ast.Load()),
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
            if not isinstance(line.value, ast.Yield):
                raise SyntaxError(f'Only `yield` expressions are allowed.')
            if len(line.targets) != 1:
                raise SyntaxError(f'Only 1 variable can be assigned.')

            n = line.targets[0].id  # The name of the variable.
            m = line.value.value    # The value after `yield`.
            g = lambda_([n], monad_(i + 1))

            return call(bind, [m, g])

        if isinstance(line, ast.Expr):
            # Skip documentation.
            if isinstance(line.value, ast.Constant) and \
               isinstance(line.value.value, str):
                return monad_(i + 1)

            if isinstance(line.value, ast.Yield):
                m = line.value.value  # The value after `yield`.
                g = lambda_(['_'], monad_(i + 1))

                return call(bind, [m, g])

        raise SyntaxError(f'Invalid statement: {line}.')

    result = lambda_(tree.body[0].args, monad_())
    result = assign(func.__name__, result)
    result = ast.fix_missing_locations(module(result))

    return result

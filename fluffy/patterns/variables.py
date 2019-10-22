from typing import List, Union

from fluffy.patterns.expressions import Variable


def variables(name: Union[list, tuple, str]) -> List[Variable]:
    """Creates a list of new variables.

    Example:
          x, y, z = variables('x y z')
          x, y, z = variables(['x', 'y', 'z'])
          x, y, z = variables(('x', 'y', 'z'))
    """

    if not isinstance(name, (list, tuple, str)):
        raise TypeError(f'Unsupported type: {type(name)}.')

    if isinstance(name, str):
        name = name.split()

    return list(map(Variable, filter(None, name)))


x: Variable = Variable('x')
y: Variable = Variable('y')
z: Variable = Variable('z')

m: Variable = Variable('m')
n: Variable = Variable('n')
k: Variable = Variable('k')

f: Variable = Variable('f')
g: Variable = Variable('g')
h: Variable = Variable('h')

_: Variable = Variable(name=None)
otherwise: Variable = Variable(name=None)

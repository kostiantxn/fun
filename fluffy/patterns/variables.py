from typing import List, Union

from fluffy.patterns.expressions import Variable


def variables(names: Union[list, tuple, str]) -> List[Variable]:
    """Creates a list of variables with the specified names.

    Args:
        names: The names of variables to create.

    Returns:
        A list of variables with the specified names.

    Examples:
        >>> variables('a b c')
        [Variable(name='a'), Variable(name='b'), Variable(name='c')]

        >>> variables(['x', 'y', 'z'])
        [Variable(name='x'), Variable(name='y'), Variable(name='z')]
    """

    if not isinstance(names, (list, tuple, str)):
        raise TypeError(f'Unsupported type: {type(names)}.')

    if isinstance(names, str):
        names = names.split()

    return list(map(Variable, filter(None, names)))


a: Variable = Variable('a')
b: Variable = Variable('b')
c: Variable = Variable('c')
d: Variable = Variable('d')
e: Variable = Variable('e')
f: Variable = Variable('f')
g: Variable = Variable('g')
h: Variable = Variable('h')
i: Variable = Variable('i')
j: Variable = Variable('j')
k: Variable = Variable('k')
l: Variable = Variable('l')
m: Variable = Variable('m')
n: Variable = Variable('n')
o: Variable = Variable('o')
p: Variable = Variable('p')
q: Variable = Variable('q')
r: Variable = Variable('r')
s: Variable = Variable('s')
t: Variable = Variable('t')
u: Variable = Variable('u')
v: Variable = Variable('v')
w: Variable = Variable('w')
x: Variable = Variable('x')
y: Variable = Variable('y')
z: Variable = Variable('z')

_: Variable = Variable(name=None)
otherwise: Variable = Variable(name=None)

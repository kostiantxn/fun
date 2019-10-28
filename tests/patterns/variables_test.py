import pytest

from fluffy.patterns import variables, Variable


@pytest.mark.parametrize("value, names", [
    ('x y z',         ['x', 'y', 'z']),
    (['x', 'y', 'z'], ['x', 'y', 'z']),
    (('x', 'y', 'z'), ['x', 'y', 'z']),
])
def test_variables(value, names):
    """Test that `variables` creates correct variables."""

    output = variables(value)

    assert len(output) == len(names)

    for var, name in zip(output, names):
        assert isinstance(var, Variable)
        assert var.name == name

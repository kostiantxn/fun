from dataclasses import dataclass

import pytest
from pytest import mark

from fluffy.patterns import expression, \
    Constant, Variable, Sequence, Dictionary, Function, Error, EvaluationError, \
    Attribute, Call


@mark.parametrize("type_, values", [
    (Constant, [42, 42.0, 42j, True, '451']),
    (Sequence, [(1, 2, 3), [1, 2, 3]]),
    (Dictionary, [{'a': 'b'}])
])
def test_expression_return_value(type_, values):
    """Tests that `expression` returns values of correct type."""

    for value in values:
        expr = expression(value)

        assert isinstance(expr, type_)
        assert expr.value is value


def test_expression_return_value_for_expression():
    """Test that `expression` returns the same value that was passed
    to the function in a case if the type of that value is `Expression`."""

    expr = Variable('x')

    assert expression(expr) is expr


def test_expression_raising_error():
    """Test that `expression` raises an error when the type of the input
    argument is not supported."""

    with pytest.raises(TypeError):
        expression(object())


def test_constant_evaluate_result():
    """Test that `Constant.evaluate` returns correct value."""

    expr = Constant(42)

    assert expr.evaluate({}) == 42


def test_variable_evaluate_result():
    """Test that `Variable.evaluate` returns correct value."""

    expr = Variable('x')

    assert expr.evaluate({'x': 42}) == 42


def test_variable_evaluate_raising_error():
    """Test that `Variable.evaluate` raises an error in a case when
    the name of the variable is not present in the input dictionary."""

    expr = Variable('x')

    with pytest.raises(NameError):
        expr.evaluate({})


def test_function_evaluate_result():
    """Test that `Function.evaluate` returns correct value."""

    x = Variable('x')
    expr = Function(pow, x, 2)

    assert expr.evaluate({'x': 5}) == 25


def test_sequence_evaluate_result():
    """Test that `Sequence.evaluate` returns correct value."""

    x, y = Variable('x'), Variable('y')
    expr = Sequence([1, x, y, 4])

    assert expr.evaluate({'x': 2, 'y': 3}) == [1, 2, 3, 4]


def test_dictionary_evaluate_result():
    """Test that `Dictionary.evaluate` returns correct value."""

    x, y = Variable('x'), Variable('y')
    expr = Dictionary({1: x, y: 4})

    assert expr.evaluate({'x': 2, 'y': 3}) == {1: 2, 3: 4}


def test_attribute_evaluate_result():
    """Test that `Attribute.evaluate` returns correct value."""

    @dataclass
    class Person:
        name: str

    expr = Constant(Person(name='abc'))
    expr = Attribute(expr, 'name')

    assert expr.evaluate({}) == 'abc'


def test_call_evaluate_result():
    """Test that `Call.evaluate` returns correct value."""

    expr = Constant('abc')
    expr = Attribute(expr, 'upper')
    expr = Call(expr, (), {})

    assert expr.evaluate({}) == 'ABC'


def test_error_evaluate_raising_error():
    """Test that `Error.evaluate` raises an error with correct message."""

    expr = Error('message')

    with pytest.raises(EvaluationError, match='message'):
        expr.evaluate({})

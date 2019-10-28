from dataclasses import dataclass

import pytest

from fluffy.patterns import pattern, \
    FixedPattern, SequencePattern, DictionaryPattern, DataclassPattern, \
    VariablePattern, Match


@dataclass
class Vector:
    x: int
    y: int


@pytest.mark.parametrize("type_, values", [
    (FixedPattern, [42, 42.0, 42j, True, '451']),
    (SequencePattern, [(1, 2, 3), [1, 2, 3]]),
    (DictionaryPattern, [{'a': 'b'}]),
    (DataclassPattern, [Vector(1, 2)])
])
def test_pattern_return_value(type_, values):
    """Tests that `pattern` returns values of correct type."""

    for value in values:
        p = pattern(value)

        assert isinstance(p, type_)
        assert p.value is value


def test_pattern_return_value_for_pattern():
    """Test that `pattern` returns the same value that was passed
    to the function in a case if the type of that value is `Pattern`."""

    p = VariablePattern('x')
    assert pattern(p) is p


def test_pattern_raising_error():
    """Test that `pattern` raises an error when the type of the input
    argument is not supported."""

    with pytest.raises(TypeError):
        pattern(object())


def test_match_success():
    """Test successful `Match`."""

    m = Match({})

    assert m.is_success()
    assert not m.is_failure()
    assert m.variables is not None and len(m.variables) == 0


def test_match_failure():
    """Test failed `Match`."""

    m = Match(None)

    assert m.is_failure()
    assert not m.is_success()
    assert m.variables is None


@pytest.mark.parametrize("value", [
    42, 42.0, 42j, True, '451'
])
def test_fixed_pattern_successful_match(value):
    """Test that `FixedPattern` correctly matches input values."""

    p = FixedPattern(value)
    m = p.match(value)

    assert m.is_success()


@pytest.mark.parametrize("value, test", [
    (x, y)
    for x in [451, 4.0, -5j, 'y', False]
    for y in [5, 500, 42.0, 10j, 'x', True]
])
def test_fixed_pattern_failed_match(value, test):
    """Test that `FixedPattern` fails to match input values."""

    p = FixedPattern(value)
    m = p.match(test)

    assert m.is_failure()

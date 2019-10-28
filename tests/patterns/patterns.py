from dataclasses import dataclass

import pytest

from fluffy.patterns import pattern, x, y, z, \
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


def test_match_merge_return_value():
    """Test the result of `Match.merge`."""

    a = Match.success({'x': 1})
    b = Match.success({'y': 2})
    m = Match.merge(a, b)

    assert Match.merge(Match.failure(), Match.failure()).is_failure()
    assert Match.merge(Match.success(), Match.failure()).is_failure()
    assert Match.merge(Match.failure(), Match.success()).is_failure()

    assert m.is_success()
    assert m.variables == {'x': 1, 'y': 2}


def test_match_merge_raising_error():
    """Test that `Match.merge` raises an error in a case when both input
    matches are successful and their sets of variables intersect."""

    a = Match.success({'x': 1, 'y': 2})
    b = Match.success({'x': 1, 'z': 3})

    with pytest.raises(NameError):
        Match.merge(a, b)


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


@pytest.mark.parametrize("value", [
    42, 42.0, 42j, True, '451', [1, 2], (1, 2), {'a': 'b'}
])
def test_fixed_pattern_successful_match(value):
    """Test that `VariablePattern` correctly matches input values."""

    p = VariablePattern('x')
    m = p.match(value)

    assert m.is_success()
    assert len(m.variables) == 1
    assert m.variables['x'] is value


@pytest.mark.parametrize("value, test, variables", [
    ([1, 2, 3],      [1, 2, 3],      {}),
    ([5, '10'],      [5, '10'],      {}),
    ([1, 2, x],      [1, 2, 3],      {'x': 3}),
    ([x, y, z],      [1, 2, 3],      {'x': 1, 'y': 2, 'z': 3}),
    ([1, [2, 3], 4], [1, [2, 3], 4], {}),
    ([x, [2, y], 4], [1, [2, 3], 4], {'x': 1, 'y': 3})
])
def test_sequence_pattern_successful_match(value, test, variables):
    """Test that `SequencePattern` correctly matches input values."""

    p = SequencePattern(value)
    m = p.match(test)

    assert m.is_success()
    assert m.variables == variables


@pytest.mark.parametrize("value, test", [
    ([1, 2, 3],      [1, 2, 5]),
    ([1, x, 3],      [1, 0, 2]),
    ([1, [2, 3], 4], [1, [3, 3], 4]),
    ([x, [2, y], 4], [1, [3, 3], 4])
])
def test_sequence_pattern_failed_match(value, test):
    """Test that `SequenceMatch` fails to match input values."""

    p = SequencePattern(value)
    m = p.match(test)

    assert m.is_failure()


@pytest.mark.parametrize("value, test, variables", [
    ({1: 2},       {1: 2},       {}),
    ({1: 2, 3: 4}, {1: 2, 3: 4}, {}),
    ({1: x},       {1: 2},       {'x': 2}),
    ({x: 2},       {1: 2},       {'x': 1}),
    ({x: 2, 3: y}, {1: 2, 3: 4}, {'x': 1, 'y': 4}),
    ({x: [2, y]},  {1: [2, 3]},  {'x': 1, 'y': 3})
])
def test_dictionary_pattern_successful_match(value, test, variables):
    """Test that `DictionaryPattern` correctly matches input values."""

    p = DictionaryPattern(value)
    m = p.match(test)

    assert m.is_success()
    assert m.variables == variables


@pytest.mark.parametrize("value, test", [
    ({1: 2}, {1: 3}),
    ({1: 2}, {2: 2}),
    ({1: 2}, {1: 2, 3: 4}),
    ({1: x}, {2: 3}),
    ({x: 2}, {2: 3}),
    ({1: [2, x]}, {1: [3, 3]})
])
def test_dictionary_pattern_failed_match(value, test):
    """Test that `DictionaryPattern` fails to match input values."""

    p = DictionaryPattern(value)
    m = p.match(test)

    assert m.is_failure()


@pytest.mark.parametrize("value, test", [
    ({1: 2, x: 2}, {1: 2, 3: 2})
])
def test_dictionary_pattern_raising_error(value, test):
    """Test that `DictionaryPattern` raises an error when there are multiple
    matching key-value pairs."""

    ...

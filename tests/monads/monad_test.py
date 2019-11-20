from fluffy.monads import monad, Maybe, Just


@monad(Maybe)
def just(x):
    return x


def test_monad_with_return():
    """Test that `monad` handles the `return` statement correctly."""

    result = just(42)

    assert isinstance(result, Just)
    assert result.value == 42

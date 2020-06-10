from fun.monads import monad, Maybe, Just


def test_monad_with_return():
    """Test that `monad` handles the `return` statement correctly."""

    @monad(Maybe)
    def just(x):
        return x

    result = just(42)

    assert isinstance(result, Just)
    assert result.value == 42

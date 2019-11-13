class Result:

    @classmethod
    def unit(cls, x):
        return Success(x)

    @classmethod
    def bind(cls, m, g):
        if isinstance(m, Success):
            return g(m.value)
        if isinstance(m, Error):
            return m


class Success(Result):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'Success ({self.value})'


class Error(Result):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'Error "{self.message}"'


def safe(func):
    def decorated(*args, **kwargs):
        try:
            return Success(func(*args, **kwargs))
        except Exception as error:
            return Error(str(error))

    return decorated

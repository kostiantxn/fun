class Maybe:

    @classmethod
    def unit(cls, x):
        return Just(x)

    @classmethod
    def bind(cls, m, g):
        if isinstance(m, Just):
            return g(m.value)
        if isinstance(m, Nothing):
            return Nothing()


class Just(Maybe):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'Just {self.value}'


class Nothing(Maybe):

    def __str__(self):
        return f'Nothing'

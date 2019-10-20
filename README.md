# fluffy

A package for functional programming in Python.

## Pattern matching
You can use `fluffy.patterns` for pattern matching.
Here is a simple example:
``` python
from fluffy.patterns import match, case

language = 'german'

greeting = match(language, case | 'english' > 'hello world!',
                           case | 'french'  > 'bonjour monde!',
                           case | 'german'  > 'hallo welt!')
```

The main syntax for `match` has the following form:
``` python
match(value, case | pattern[0] > expression[0],
             case | pattern[1] > expression[1],
             case | pattern[2] > expression[2],
             ...)
```

You can match values of built-in types, like `int`, `float`, `complex`, `bool` and `str`, as well as `None`:
``` python
value = ...

match(value, case | 42   > '(natural) answer to the ultimate question',
             case | 42j  > '(complex) answer to the ultimate question',
             case | 42.0 > '(real) answer to the ultimate question')
```

But be careful! You may get an error in a case when there are no matching patterns:
``` python
# Raises a `MismatchError`.
match(0, case | +1 > 'positive',
         case | -1 > 'negative')
```

You can use `_` (or its alias `otherwise`) to handle default cases. `_` matches any value:
``` python
match(0, case | +1 > 'positive',
         case | -1 > 'negative',
         case |  _ > 'neutral')
```

You can match lists and tuples:
``` python
from fluffy.patterns import match, case

band = ['Armstrong', 'Dirnt', 'Cool']
name = match(band, case | ['Armstrong', 'Dirnt', 'Cool'] > 'Green Day')

# Or...

band = ('Armstrong', 'Dirnt', 'Cool')
name = match(band, case | ('Armstrong', 'Dirnt', 'Cool') > 'Green Day')
```

You can use wildcards to fetch values and use them later:

``` python
from fluffy.patterns import match, case, x

person = ('Richard', 'Feynman')

surname = match(person, case | ('Albert',  x) > x,
                        case | ('Richard', x) > x)
```

...

## Monads
...

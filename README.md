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

You can match lists and tuples:

``` python
from fluffy.patterns import match, case

band = ['Armstrong', 'Dirnt', 'Cool']
name = match(band, case | ['Armstrong', 'Dirnt', 'Cool'] > 'Green Day')

# or ...

band = ('Armstrong', 'Dirnt', 'Cool')
name = match(band, case | ('Armstrong', 'Dirnt', 'Cool') > 'Green Day')
```

You can use wildcards to fetch values and later use them:

``` python
from fluffy.patterns import match, case, x

person = ('Richard', 'Feynman')

surname = match(person, case | ('Albert',  x) > x,
                        case | ('Richard', x) > x)
```

...

## Monads
...

# fluffy

A package for functional programming in Python.

## Content

1. [Pattern matching](#pattern-matching)
    1. [Design](#design)
    1. [Matching basic data types](#matching-basic-data-types): `int`, `float`, `complex`, `bool`, `str`
    1. [Matching standard collections](#matching-standard-collections): `list`, `tuple`, `dict`
    1. [Variables and expressions](#variables-and-expressions)
    1. [Mismatching](#mismatching)
    1. [Raising errors](#raising-errors)
1. [Monads](#monads)

## Pattern matching
You can use `fluffy.patterns` for pattern matching.
Here is a simple example:
``` python
from fluffy.patterns import match, case

language = 'german'

greeting = match(language, case | 'english' > 'hello world!',
                           case | 'french'  > 'bonjour monde!',
                           case | 'german'  > 'hallo welt!')

print(greeting)  # Prints 'hallo welt!'.
```

### Design
The main syntax for `match` has the following form:
``` python
match(value, case | pattern[0] > expression[0],
             case | pattern[1] > expression[1],
             case | pattern[2] > expression[2],
             ...)
```

The statement `case | pattern > expression` is evaluated as `((case | pattern) > expression)` due to the priority of operators `|` and `>`.
It returns `Case(pattern, expression)` and is used only for stylistic purposes.

You can also simulate Haskell's syntax for pattern matching like this:
``` python
from fluffy.patterns import match as case, case as of
```

### Matching basic data types
You can match values of built-in types, like `int`, `float`, `complex`, `bool` and `str`, as well as `None`:
``` python
value = ...

match(value, case | 42   > '(natural) answer to the ultimate question',
             case | 42j  > '(complex) answer to the ultimate question',
             case | 42.0 > '(real) answer to the ultimate question',
             ...)
```

### Matching standard collections
You can match lists and tuples:
``` python
from fluffy.patterns import match, case

band = ['Armstrong', 'Dirnt', 'Cool']
name = match(band, case | ['Armstrong', 'Dirnt', 'Cool'] > 'Green Day')

# Or...

band = ('Armstrong', 'Dirnt', 'Cool')
name = match(band, case | ('Armstrong', 'Dirnt', 'Cool') > 'Green Day')
```

### Variables and expressions
You can use variables to fetch values and use them later:

``` python
from fluffy.patterns import match, case, x

person = ('Richard', 'Feynman')

surname = match(person, case | ('Albert',  x) > x,
                        case | ('Richard', x) > x)
```

There are plenty of predefined variables: `a`, `b`, `c`, `f`, `g`, `h`, `m`, `n`, `k`, `x`, `y`, `z`.
And special ones: `_` and its alias `otherwise`.

You can define your own variables if you need to:
``` python
from fluffy.patterns import Variable

name = Variable('name')

match(['Richard', 'Feynman'], case | [name, 'Einstein'] > name + ' Einstein',
                              case | [name, 'Feynman']  > name + ' Feynman')
```

You can also define multiple variables at once:
``` python
from fluffy.patterns import variables

apple, orange = variables('apple orange')

...
```

### Mismatching
Be careful! You may get an error in a case when there are no matching patterns:
``` python
# Raises a `MismatchError`.
match(0, case | +1 > 'positive',
         case | -1 > 'negative')
```

You can use `_` (or its alias `otherwise`) to handle default cases.
`_` matches any value:
``` python
match(0, case | +1 > 'positive',
         case | -1 > 'negative',
         case |  _ > 'neutral')
```

### Raising errors
You can raise an error of any type:
``` python
from fluffy.patterns import match, case, raises

match('x', case | 'x' > raises(ValueError(...)))
```

...

## Monads
...

# fluffy

A package for functional programming in Python.

### Contents

1. [Pattern matching](#pattern-matching)
    * [Match basic data types](#match-basic-data-types): `int`, `float`, `complex`, `bool`, `str`
    * [Match standard collections](#match-standard-collections): `list`, `tuple`, `dict`
    * [Variables and expressions](#variables-and-expressions)
    * [Mismatch](#mismatch)
    * [Raise errors](#raise-errors)
    * [How it works](#how-it-works)
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

The main syntax for `match` has the following form:
``` python
match(value, case | pattern[0] > expression[0],
             case | pattern[1] > expression[1],
             case | pattern[2] > expression[2],
             ...)
```

### Match basic data types
You can match basic built-in data types including `int`, `float`, `complex`, `bool` and `str`, as well as `None`:
``` python
value = ...

match(value, case | 42    > '(natural) answer to the ultimate question',
             case | 42j   > '(complex) answer to the ultimate question',
             case | 9.75  > '9¾? think you're being funny do ya?',
             case | '451' > 'fahrenheit',
             case | True  > not False,
             case | None  > 123.4)
```

### Match standard collections
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

### Mismatch
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

### Raise errors
You can raise an error of any type:
``` python
from fluffy.patterns import match, case, error

match('x', case | 'x' > error('message'))
```

### How it works

...

## Monads
You can use `fluffy.monads` to write monadic functions.
Here is an example:
``` python
from fluffy.monads import monad, List

@monad(List)
def example(n):
    x = yield List[1, 2, 3]
    y = yield List[1, 2, 3]
    
    return (x + y) * n

print(example(5))  # Prints `List[5, 10, 15, 10, 20, 30, 15, 30, 45]`.
```

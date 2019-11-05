# fluffy
A package for functional programming in Python.

## Quick examples

#### Pattern matching
``` python
from fluffy.patterns import match, case

language = 'French'

greeting = match(language, case | 'English' > 'Hello, world!',
                           case | 'French'  > 'Bonjour le monde!',
                           case | 'German'  > 'Hallo Welt!')

print(greeting)  # Prints 'Bonjour le monde!'.
```


#### Monads
``` python
from fluffy.monads import monad, List

@monad(List)
def triples(n):
    x = yield List[1, ..., n]
    y = yield List[x, ..., n]
    z = yield List[y, ..., n]

    [(x, y, z)] if x**2 + y**2 == z**2 else \
    []

print(triples(15))  # Prints 'List[(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15)]'.
```

## Installation
...

## Guide
You can read the 
[guide](https://github.com/konstantin-ogulchansky/fluffy/tree/master/docs/guide.md) 
to learn more about the package!

## License
The package is licensed under the 
[MIT](https://github.com/konstantin-ogulchansky/fluffy/blob/master/LICENSE) 
License.

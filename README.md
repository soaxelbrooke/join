# JOIN

SQL-style joins for Python iterables.

```python
>>> from join import join
>>> from collections import namedtuple
>>> Dog = namedtuple('Dog', ['name', 'woof', 'weight'])
>>> Cat = namedtuple('Cat', ['name', 'meow', 'weight'])
>>> dogs = [
...     Dog('gatsby', 'Rruff!', 16),
...     Dog('ein', 'wruf!', 9),
...     Dog('talon', 'woof', 25),
... ]
>>> cats = [
...     Cat('pleo', 'mreeeoww', 16),
...     Cat('xena', 'mreow', 12),
...     Cat('ma\'at', 'meww', 13),
...     Cat('set', 'meow', 13),
...     Cat('gatsby', 'rowr', 15),
...     Cat('gatsby', 'rooooo', 15),
... ]
>>> catdogs = join(cats, dogs, 'inner', 'name')
>>> catdogs[0].meow
'rowr'
>>> catdogs[0].woof
'Rruff!'
```

====
JOIN
====
SQL-style joins for Python iterables.

.. code-block:: python

    >>> from join import join, merge, tuple_join
    >>> dogs = [
    ...     Dog('gatsby', 'Rruff!', 16),
    ...     Dog('ein', 'wruf!', 9),
    ... ]
    >>> cats = [
    ...     Cat('pleo', 'mreeeoww', 16),
    ...     Cat('xena', 'mreow', 12),
    ...     Cat('gatsby', 'rowr', 15),
    ... ]
    >>> catdogs = merge(cats, dogs, key='name')
    >>> catdogs
    [CatDog({'right': Dog(name='gatsby', woof='Rruff!', weight=16), 'name': 'gatsby', 'weight': 15, 'meow': 'rowr', 'woof': 'Rruff!', 'left': Cat(name='gatsby', meow='rowr', weight=15)})]
    >>> catdogs[0].meow
    'rowr'
    >>> catdogs[0].woof
    'Rruff!'

``join`` does the work of associating iterable items together, but gives you all the power for customization, letting you supply your own join function, separate keys for left and right iterables, and even letting you use functions instead of attribute names.

``merge`` used above, for example, is ``join`` using an object union to join matched objects.  You can use a tuple join, which is default for ``join``:

.. code-block:: python

    >>> join(cats, dogs, key='name', join_fn=tuple_join)
    [(Cat(name='gatsby', meow='rowr', weight=15), Dog(name='gatsby', woof='Rruff!', weight=16))]

Supplying your own join function is easy:

.. code-block:: python

    >>> def weight_sum(left, right):
    ...     return left.weight + right.weight
    ...
    >>> join(cats, dogs, key='name', join_fn=weight_sum)
    [31]

Using separate key functions is easy too:

.. code-block:: python

    >>> def cat_key(cat):
    ...     return cat.weight % 3 == 0  # weight divisible by 3
    ... 
    >>> def dog_key(dog):
    ...     return dog.weight % 4 == 0  # weight divisible by 4
    ... 
    >>> def name_join(left, right):
    ...     return left.name + '-' + right.name
    ... 
    >>> join(cats, dogs, left_key=cat_key, right_key=dog_key, join_fn=name_join)
    ['pleo-ein', 'xena-gatsby', 'gatsby-gatsby']


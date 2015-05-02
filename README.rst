====
JOIN
====
SQL-style joins for Python iterables.

.. code-block:: python

    >>> from join import merge
    >>> dogs = [
    ...     Dog('gatsby', 'Rruff!', 16),
    ...     Dog('ein', 'wruf!', 9),
    ... ]
    >>> cats = [
    ...     Cat('pleo', 'mreeeoww', 16),
    ...     Cat('xena', 'mreow', 12),
    ...     Cat('gatsby', 'rowr', 15),
    ... ]
    >>> catdogs = merge(cats, dogs, 'inner', 'name')
    >>> catdogs[0].meow
    'rowr'
    >>> catdogs[0].woof
    'Rruff!'


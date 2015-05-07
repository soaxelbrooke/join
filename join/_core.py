__author__ = 'stuart'

from collections import defaultdict
from ._join_funcs import union_join, tuple_join


def merge(left, right, how='inner', key=None, left_key=None, right_key=None):
    """ Performs a join using the union join function. """
    return join(left, right, how, key, left_key, right_key, join_fn=union_join)


def join(left, right, how='inner', key=None, left_key=None, right_key=None,
         join_fn=tuple_join):
    """
    :param left: left iterable to be joined
    :param right: right iterable to be joined
    :param str | function key: either an attr name, dict key, or function that produces hashable value
    :param how: 'inner', 'left', 'right', or 'outer'
    :param join_fn: function called on joined left and right iterable items to complete join
    :rtype: list
    """
    if key is None and (left_key is None or right_key is None):
        raise ValueError("Must provide either key param or both left_key and right_key")

    if key is not None:
        lkey = rkey = key if callable(key) else make_key_fn(key)
    else:
        lkey = left_key if callable(left_key) else make_key_fn(left_key)
        rkey = right_key if callable(right_key) else make_key_fn(right_key)

    try:
        join_impl = {
            "left": _left_join,
            "right": _right_join,
            "inner": _inner_join,
            "outer": _outer_join,
        }[how]
    except KeyError:
        raise ValueError("Invalid value for how: {}, must be left, right, "
                         "inner, or outer.".format(str(how)))
    else:
        return join_impl(left, right, lkey, rkey, join_fn)


def _inner_join(left, right, left_key_fn, right_key_fn, join_fn=union_join):
    """ Inner join using left and right key functions

    :param left: left iterable to be joined
    :param right: right iterable to be joined
    :param function left_key_fn: function that produces hashable value from left objects
    :param function right_key_fn: function that produces hashable value from right objects
    :param join_fn: function called on joined left and right iterable items to complete join
    :rtype: list
    """
    joiner = defaultdict(list)
    for ele in right:
        joiner[right_key_fn(ele)].append(ele)
    joined = []
    for ele in left:
        for other in joiner[left_key_fn(ele)]:
            joined.append(join_fn(ele, other))
    return joined


def _left_join(left, right, left_key_fn, right_key_fn, join_fn=union_join):
    """
    :param left: left iterable to be joined
    :param right: right iterable to be joined
    :param function left_key_fn: function that produces hashable value from left objects
    :param function right_key_fn: function that produces hashable value from right objects
    :param join_fn: function called on joined left and right iterable items to complete join
    :rtype: list
    """
    joiner = defaultdict(list)
    for ele in right:
        joiner[right_key_fn(ele)].append(ele)
    joined = []
    for ele in left:
        for other in joiner.get(left_key_fn(ele), [None]):
            joined.append(join_fn(ele, other))
    return joined


def _right_join(left, right, left_key_fn, right_key_fn, join_fn=union_join):
    """
    :param left: left iterable to be joined
    :param right: right iterable to be joined
    :param function left_key_fn: function that produces hashable value from left objects
    :param function right_key_fn: function that produces hashable value from right objects
    :param join_fn: function called on joined left and right iterable items to complete join
    :rtype: list
    """
    def reversed_join_fn(left_ele, right_ele):
        return join_fn(right_ele, left_ele)
    return _left_join(right, left, right_key_fn, left_key_fn, reversed_join_fn)


def _outer_join(left, right, left_key_fn, right_key_fn, join_fn=union_join):
    """
    :param left: left iterable to be joined
    :param right: right iterable to be joined
    :param function left_key_fn: function that produces hashable value from left objects
    :param function right_key_fn: function that produces hashable value from right objects
    :param join_fn: function called on joined left and right iterable items to complete join
    :rtype: list
    """
    left_joiner = defaultdict(list)
    for ele in left:
        left_joiner[left_key_fn(ele)].append(ele)
    right_joiner = defaultdict(list)
    for ele in right:
        right_joiner[right_key_fn(ele)].append(ele)
    keys = set(left_joiner.keys()).union(set(right_joiner.keys()))

    def iter_join(l, r, join_keys):
        for join_key in join_keys:
            for ele in l.get(join_key, [None]):
                for other in r.get(join_key, [None]):
                    yield join_fn(ele, other)

    return list(iter_join(left_joiner, right_joiner, keys))

def group(iterable, key=lambda ele: ele):
    """ Groups an iterable by a specified attribute, or using a specified key access function.  Returns tuples of grouped elements.

    >>> dogs = [Dog('gatsby', 'Rruff!', 15), Dog('william', 'roof', 12), Dog('edward', 'hi', 15)]
    >>> groupby(dogs, 'weight')
    [(Dog('gatsby', 'Rruff!', 15), Dog('edward', 'hi', 15)), (Dog('william', 'roof', 12), )]

    :param iterable: iterable to be grouped
    :param key: a key-access function or attr name to be used as a group key
    """
    if callable(key):
        return _group(iterable, key)
    else:
        return _group(iterable, make_key_fn(key))


def _group(iterable, key_fn):
    groups = defaultdict(list)
    for ele in iterable:
        groups[key_fn(ele)].append(ele)
    return map(tuple, groups.values())


def make_key_fn(key):
    def key_fn(ele):
        if isinstance(ele, dict):
            return ele[key]
        else:
            return getattr(ele, key)
    return key_fn

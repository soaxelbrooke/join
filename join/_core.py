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

    def make_key_fn(_key):
        def key_fn(ele):
            if isinstance(ele, dict):
                return ele[_key]
            else:
                return getattr(ele, _key)
        return key_fn

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
        }.get(how)
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
    joiner = defaultdict(list)
    for ele in left:
        joiner[left_key_fn(ele)].append(ele)
    joined = []
    for ele in right:
        for other in joiner.get(right_key_fn(ele), [None]):
            joined.append(join_fn(ele, other))
    return joined


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

__author__ = 'stuart'


def get_object_attrs(obj):
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    elif hasattr(obj, '__slots__'):
        return {key: getattr(obj, key) for key in obj.__slots__}
    else:
        return {}


class Union(object):
    def __init__(self, attributes):
        if isinstance(attributes, dict):
            for name, value in attributes.items():
                setattr(self, name, value)
        else:
            for name, value in attributes:
                setattr(self, name, value)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.__dict__)


def tuple_join(left, right):
    """
    Returns a tuple of the joined objects

        >>> tuple_join(1, '2')
        (1, '2')

    :param left: left object to be joined with right
    :param right: right object to be joined with left
    :return: tuple containing both join parents
    """
    return left, right


def union_join(left, right):
    """
    Join function truest to the SQL style join.  Merges both objects together in a sum-type,
    saving references to each parent in ``left`` and ``right`` attributes.

        >>> Dog = namedtuple('Dog', ['name', 'woof', 'weight'])
        >>> dog = Dog('gatsby', 'Ruff!', 15)
        >>> Cat = namedtuple('Cat', ['name', 'meow', 'weight'])
        >>> cat = Cat('pleo', 'roooowwwr', 12)
        >>> catdog = union_join(cat, dog)
        >>> catdog.name
        pleo
        >>> catdog.woof
        Ruff!
        >>> catdog.right.name
        gatsby

    :param left: left object to be joined with right
    :param right: right object to be joined with left
    :return: joined object with attrs/methods from both parents available
    """
    joined_class = type(left.__class__.__name__ + right.__class__.__name__, (Union,), {})
    attrs = {}
    attrs.update(get_object_attrs(right))
    attrs.update(get_object_attrs(left))
    attrs['left'] = left
    attrs['right'] = right
    return joined_class(attrs)

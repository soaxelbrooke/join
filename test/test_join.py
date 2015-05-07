__author__ = 'stuart'

import unittest
from collections import namedtuple
from join import join
from join import merge
from join import group
from join import tuple_join
from join import union_join


Dog = namedtuple('Dog', ['name', 'woof', 'weight'])
Cat = namedtuple('Cat', ['name', 'meow', 'weight'])
dogs = [
    Dog('gatsby', 'Rruff!', 16),
    Dog('ein', 'wruf!', 9),
    Dog('talon', 'woof', 25),
]
cats = [
    Cat('pleo', 'mreeeoww', 16),
    Cat('xena', 'mreow', 12),
    Cat('ma\'at', 'meww', 13),
    Cat('set', 'meow', 13),
    Cat('gatsby', 'rowr', 15),
    Cat('gatsby', 'rooooo', 15),
]


class JoinTests(unittest.TestCase):

    def test_inner_join(self):
        inner = join(dogs, cats, 'inner', 'name')
        assert len(inner) == 2
        assert inner[0][0].name == 'gatsby'
        assert inner[0][1].meow == 'rowr'
        assert inner[0][0].weight == 16
        assert inner[0][1].weight == 15

    def test_outer_join(self):
        outer = join(dogs, cats, 'outer', 'weight')
        assert len(outer) == 8

    def test_left_join(self):
        left = join(dogs, cats, 'left', 'name')
        assert len(left) == 4

    def test_right_join(self):
        right = join(dogs, cats, 'right', 'name')
        assert len(right) == 6

    def test_inner_merge(self):
        inner = merge(dogs, cats, 'inner', 'name')
        assert len(inner) == 2
        assert inner[0].name == 'gatsby'
        assert inner[0].meow == 'rowr'
        assert inner[0].weight == 16
        assert inner[0].right.weight == 15

    def test_inner_merge_iter(self):
        inner = merge(iter(dogs), iter(cats), 'inner', 'name')
        assert len(inner) == 2
        assert inner[0].name == 'gatsby'
        assert inner[0].meow == 'rowr'
        assert inner[0].weight == 16
        assert inner[0].right.weight == 15

    def test_left_merge(self):
        left = merge(dogs, cats, 'left', 'name')
        assert len(left) == len(dogs) + 1
        assert left[0].meow == 'rowr'

    def test_right_merge(self):
        right = merge(dogs, cats, 'right', 'name')
        assert len(right) == len(cats)
        assert right[-1].woof == 'Rruff!'

    def test_outer_merge(self):
        outer = merge(dogs, cats, 'outer', 'name')
        assert len(outer) == len(dogs) + len(cats) - 1


class GroupByTest(unittest.TestCase):
    
    def test_basic_group(self):
        abcs = 'aabbabccbc'
        self.assertSequenceEqual(set(group(abcs)), 
                                 set([('a', 'a', 'a',), ('b', 'b', 'b', 'b'), ('c', 'c', 'c')]))

    def test_attr_group(self):
        byweight = group(cats, 'weight')
        names = set(map(lambda cats: tuple(cat.name for cat in cats), byweight))
        expected = set([('pleo',), ('xena',), ('ma\'at', 'set'), ('gatsby', 'gatsby')])
        self.assertSequenceEqual(names, expected)

    def test_func_group(self):
        self.assertSequenceEqual(set([(1, 3, 5), (0, 2, 4)]), set(group(range(6), lambda n: n % 2)))


class JoinFuncsTest(unittest.TestCase):
    
    def test_union_join(self):
        catdog = union_join(cats[0], dogs[0])
        assert hasattr(catdog, 'woof')
        assert hasattr(catdog, 'meow')

    def test_union_join_with_none(self):
        catnone = union_join(cats[0], None)
        assert hasattr(catnone, 'meow')

    def test_tuple_join(self):
        joined = tuple_join('a', 'b')
        assert joined == ('a', 'b')

    def test_tuple_join_with_none(self):
        joined = tuple_join('a', None)
        assert joined == ('a', None)

if __name__ == '__main__':
    unittest.main()

__author__ = 'stuart'

import unittest
from collections import namedtuple
from join import join
from join import merge
from join import group


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
        inner = merge(dogs, cats, 'inner', 'name')
        self.assertEqual(len(inner), 2)
        self.assertEqual(inner[0].name, 'gatsby')

    def test_left_join(self):
        left = merge(dogs, cats, 'left', 'name')
        self.assertEqual(len(left), len(dogs) + 1)
        self.assertEqual(left[0].meow, 'rowr')

    def test_right_join(self):
        right = merge(dogs, cats, 'right', 'name')
        self.assertEqual(len(right), len(cats))
        self.assertEqual(right[-1].woof, 'Rruff!')

    def test_outer_join(self):
        outer = merge(dogs, cats, 'outer', 'name')
        self.assertEqual(len(outer), len(dogs) + len(cats) - 1)


class GroupByTest(unittest.TestCase):
    
    def test_basic_group(self):
        abcs = 'aabbabccbc'
        self.assertSequenceEqual(set(group(abcs)), 
                                 set([('a', 'a', 'a',), ('b', 'b', 'b', 'b'), ('c', 'c', 'c')]))

    def test_func_group(self):
        self.assertSequenceEqual(set([(1, 3, 5), (0, 2, 4)]), set(group(range(6), lambda n: n % 2)))


if __name__ == '__main__':
    unittest.main()

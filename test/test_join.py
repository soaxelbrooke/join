__author__ = 'stuart'

import unittest
from collections import namedtuple
from join import join

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
        self.assertEqual(len(inner), 2)
        self.assertEqual(inner[0].name, 'gatsby')

    def test_left_join(self):
        left = join(dogs, cats, 'left', 'name')
        self.assertEqual(len(left), len(dogs) + 1)
        self.assertEqual(left[0].meow, 'rowr')

    def test_right_join(self):
        right = join(dogs, cats, 'right', 'name')
        self.assertEqual(len(right), len(cats))
        self.assertEqual(right[-1].woof, 'Rruff!')

    def test_outer_join(self):
        outer = join(dogs, cats, 'outer', 'name')
        self.assertEqual(len(outer), len(dogs) + len(cats) - 1)

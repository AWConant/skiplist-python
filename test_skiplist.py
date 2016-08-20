import unittest
import random
from skiplist import SkipList

class TestSkipList(unittest.TestCase):
    def test_skiplist(self):
        xs = SkipList()
        MAX = 5000
        sample = range(MAX)
        random.shuffle(sample)
        for i in sample:
            xs.insert(i)
            self.assertTrue(i in xs)

        for i in sample:
            self.assertTrue(i in xs)

        self.assertFalse(-1 in xs)
        self.assertFalse(MAX in xs)
        
        xs.remove(-1)
        self.assertFalse(-1 in xs)

        random.shuffle(sample)
        for i in sample:
            self.assertTrue(i in xs)
            xs.remove(i)
            self.assertFalse(i in xs)

if __name__ == '__main__':
    unittest.main()

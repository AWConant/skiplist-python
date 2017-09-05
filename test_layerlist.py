import unittest
import random
from skiplist import SkipList, LayerList

MAX = 5000

class TestLayerList(unittest.TestCase):
    def test_layerlist(self):
        xs = LayerList(None)
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

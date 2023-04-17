import unittest

from source.DependencyGraph import DependencyGraph
from source.Item import Item

class TestDependencyGraph(unittest.TestCase):
    def setUp(self):
        self.test_graph = DependencyGraph()

    def test_add_items(self):
        item1 = Item('one', ['label'], ['depencency'])
        item2 = Item('two', ['label'], ['depencency'])
        self.test_graph.add_items([item1])
        self.test_graph.add_items([item2])
        self.assertEqual(len(self.test_graph.graph.nodes()), 2)

    def test_add_items_soft(self):
        item1 = Item('one', ['label'], ['depencency'])
        item2 = Item('two', ['label'], ['depencency'])
        item3 = Item('three', ['label'], ['depencency'])
        self.test_graph.add_items([item1], 'soft')
        self.test_graph.add_items([item2], 'soft')
        self.test_graph.add_items([item3], 'soft')
        self.assertEqual(len(self.test_graph.graph.nodes()), 3)

    def test_add_items_hard(self):
        item1 = Item('one', ['label'], ['depencency'])
        self.test_graph.add_items([item1], 'hard')
        self.assertEqual(len(self.test_graph.graph.nodes()), 1)

import unittest

import networkx
from source.DependencyGraph import DependencyGraph
from source.Tree import Tree
from source.Item import Item
from os import path
from PIL import Image, ImageChops

class TestDependencyGraph(unittest.TestCase):
    def setUp(self):
        self.tree_soft = Tree('soft')
        self.tree_hard = Tree()
        self.item1 = Item(1, ['blue'], [])
        self.item2 = Item(2, ['yellow'], [])
        self.item3 = Item(3, ['red'], [])
        self.item4 = Item(4, ['green'], ['blue', 'yellow'])
        self.item5 = Item(5, ['orange'], ['red', 'yellow'])
        self.item6 = Item(6, ['violet'], ['blue', 'red'])
        self.item7 = Item(7, ['russet'], ['orange', 'violet'])
        self.item8 = Item(8, ['one', 'two'], [])
        self.item9 = Item(9, ['four'], ['one', 'two'])
        self.items = [self.item1,self.item2,self.item3,self.item4,self.item5,self.item6,self.item7, self.item8, self.item9]
        
        for item in list(self.items):
            self.tree_hard.add_item(item)
            
        for item in list(self.items):
            self.tree_soft.add_item(item)

        self.test_graph_hard = DependencyGraph(self.tree_hard)
        self.test_graph_soft = DependencyGraph(self.tree_soft)

    def test_constructor(self):
        self.assertTrue(isinstance(self.test_graph_hard.graph, networkx.DiGraph))
        self.assertTrue(isinstance(self.test_graph_hard.tree, Tree))
        self.assertEqual(self.test_graph_hard.node_positions, {})
        self.assertTrue(isinstance(self.test_graph_soft.graph, networkx.DiGraph))
        self.assertTrue(isinstance(self.test_graph_soft.tree, Tree))
        self.assertEqual(self.test_graph_soft.node_positions, {})
        
    def test_process_tree_hard(self):
        self.test_graph_hard.process_tree()
        self.assertEqual(len(self.test_graph_hard.tree.items[7].connections), 1)
        self.assertEqual(len(self.test_graph_hard.tree.items[0].connections), 0)
        self.assertEqual(len(self.test_graph_hard.tree.positions), 9)
        self.assertEqual(len(self.test_graph_hard.graph.nodes()), 9)
        self.assertEqual(len(self.test_graph_hard.graph.edges()), 1)
        self.assertEqual(len(self.test_graph_hard.node_positions), 9)
        
    def test_process_tree_soft(self):
        self.test_graph_soft.process_tree()
        self.assertEqual(len(self.test_graph_soft.tree.items[7].connections), 1)
        self.assertEqual(len(self.test_graph_soft.tree.items[0].connections), 2)
        self.assertEqual(len(self.test_graph_soft.tree.positions), 9)
        self.assertEqual(len(self.test_graph_soft.graph.nodes()), 9)
        self.assertEqual(len(self.test_graph_soft.graph.edges()), 9)
        self.assertEqual(len(self.test_graph_soft.node_positions), 9)

    def test_process_positions(self):
        self.test_graph_hard.tree.process_connections()
        self.test_graph_hard.tree.process_items_positions()
        self.assertEqual(str(self.test_graph_hard.process_positions()), '{1: (-4, 0), 2: (-3, 0), 3: (-2, 0), 4: (-1, 0), 5: (0, 0), 6: (1, 0), 7: (2, 0), 8: (3, 0), 9: (0, -1)}')
        self.test_graph_soft.tree.process_connections()
        self.test_graph_soft.tree.process_items_positions()
        self.assertEqual(str(self.test_graph_soft.process_positions()), '{1: (-2, 0), 2: (-1, 0), 3: (0, 0), 8: (1, 0), 4: (-2, -1), 6: (-1, -1), 5: (0, -1), 9: (1, -1), 7: (0, -2)}')
        self.assertNotEqual(self.test_graph_hard.process_positions(), self.test_graph_soft.process_positions())
        
    def test_create_nodes_by_tree_items(self):
        self.test_graph_hard.create_nodes_by_tree_items()
        self.assertEqual(str(self.test_graph_hard.graph.nodes()), '[1, 2, 3, 4, 5, 6, 7, 8, 9]')
        self.test_graph_soft.create_nodes_by_tree_items()
        self.assertEqual(str(self.test_graph_soft.graph.nodes()), '[1, 2, 3, 4, 5, 6, 7, 8, 9]')
        
    def test_create_edges_by_items(self):
        self.test_graph_hard.tree.process_connections()
        self.test_graph_hard.tree.process_items_positions()
        self.test_graph_hard.create_nodes_by_tree_items()
        self.test_graph_hard.create_edges_by_items()
        self.assertEqual(str(self.test_graph_hard.graph.edges()), '[(8, 9)]')
        
    def test_create_edges_by_items_soft(self):
        self.test_graph_soft.tree.process_connections()
        self.test_graph_soft.tree.process_items_positions()
        self.test_graph_soft.create_nodes_by_tree_items()
        self.test_graph_soft.create_edges_by_items()
        self.assertEqual(str(self.test_graph_soft.graph.edges()),'[(1, 4), (1, 6), (2, 4), (2, 5), (3, 5), (3, 6), (5, 7), (6, 7), (8, 9)]')

    def test_draw_hard(self):
        image_name = 'hard'
        self.test_graph_hard.process_tree()
        self.test_graph_hard.draw(image_name)
        self.assertTrue(path.exists(image_name + '.png'))
        self.compare_images(image_name)
                
    def test_draw_soft(self):
        image_name = 'soft'
        self.test_graph_soft.process_tree()
        self.test_graph_soft.draw(image_name)
        self.assertTrue(path.exists(image_name + '.png'))
        self.compare_images(image_name)
        
    def compare_images(self, image_name):
        base_image = Image.open(path.join('tests','base_images', image_name + '.png')).convert('RGB')
        generated_image = Image.open(image_name + ".png").convert('RGB')
        diff = ImageChops.difference(base_image, generated_image).getbbox()
        self.assertIsNone(diff)
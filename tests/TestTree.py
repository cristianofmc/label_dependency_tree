import unittest

from source import Tree, Item

class TestTree(unittest.TestCase):
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
        
    def add_items_by_list(self, tree):
            for item in self.items:
                tree.add_item(item)
                
    def test_constructor(self):
        self.assertEqual(self.tree_hard.items, [])
        self.assertEqual(self.tree_soft.items, [])
        self.assertEqual(self.tree_hard.positions, {})
        self.assertEqual(self.tree_soft.positions, {})
        self.assertEqual(self.tree_hard.connection_type, 'hard')
        self.assertEqual(self.tree_soft.connection_type, 'soft')
        
    def test_add_item(self):
        self.add_items_by_list(self.tree_soft)
        self.assertEqual(self.tree_soft.items, self.items)
        self.add_items_by_list(self.tree_hard)
        self.assertEqual(self.tree_hard.items, self.items)

    def test_process_connections_hard(self):
        self.add_items_by_list(self.tree_hard)
        self.tree_soft.process_connections()
        self.assertEqual([], self.item1.connections)

    def test_process_connections_soft(self):
        self.add_items_by_list(self.tree_soft)
        self.tree_soft.process_connections()
        self.assertIn(self.item4, self.item1.connections)
  
    def test_has_dependency_hard(self):
        self.add_items_by_list(self.tree_hard)
        result1 = self.tree_hard.has_dependency(self.item1.labels, self.item6.dependencies)
        result2 = self.tree_hard.has_dependency(self.item8.labels, self.item9.dependencies)
        self.assertFalse(result1)
        self.assertTrue(result2)

    def test_has_dependency_soft(self):
        self.add_items_by_list(self.tree_soft)
        result1 = self.tree_soft.has_dependency(self.item1.labels, self.item6.dependencies)
        result2 = self.tree_soft.has_dependency(self.item8.labels, self.item9.dependencies)
        self.assertTrue(result1)
        self.assertTrue(result2)

    def test_verify_dependency_hard(self):
        self.assertTrue(self.tree_hard.verify_dependency_hard(self.item8.labels, self.item9.dependencies))
        self.assertFalse(self.tree_hard.verify_dependency_hard(self.item1.labels, self.item4.dependencies))
        self.assertFalse(self.tree_hard.verify_dependency_hard(self.item1.labels, self.item5.dependencies))

    def test_verify_dependency_soft(self):
        self.assertTrue(self.tree_hard.verify_dependency_soft(self.item8.labels, self.item9.dependencies))
        self.assertTrue(self.tree_hard.verify_dependency_soft(self.item1.labels, self.item4.dependencies))
        self.assertFalse(self.tree_hard.verify_dependency_soft(self.item1.labels, self.item5.dependencies))

    def test_fetch_item_dependents_hard(self):
        self.add_items_by_list(self.tree_hard)
        self.tree_hard.process_connections()
        self.assertEqual(self.tree_hard.fetch_item_dependents(self.item1), [])
        self.assertEqual(self.tree_hard.fetch_item_dependents(self.item4), [])
        self.assertEqual(self.tree_hard.fetch_item_dependents(self.item7), [])
        self.assertEqual(self.tree_hard.fetch_item_dependents(self.item9), [self.item8])
        
    def test_fetch_item_dependents_soft(self):
        self.add_items_by_list(self.tree_soft)
        self.tree_soft.process_connections()
        self.assertEqual(self.tree_soft.fetch_item_dependents(self.item1), [])
        self.assertEqual(self.tree_soft.fetch_item_dependents(self.item4), [self.item1, self.item2])
        self.assertEqual(self.tree_soft.fetch_item_dependents(self.item7), [self.item5, self.item6, self.item2, self.item3, self.item1])
        self.assertEqual(self.tree_soft.fetch_item_dependents(self.item9), [self.item8])
    
    def test_get_roots_hard(self):
        self.add_items_by_list(self.tree_hard)
        self.tree_hard.process_connections()
        self.assertEqual(self.tree_hard.get_roots(), [self.item1, self.item2, self.item3, self.item4, self.item5, self.item6, self.item7, self.item8])

    def test_get_roots_soft(self):
        self.add_items_by_list(self.tree_soft)
        self.tree_soft.process_connections()
        self.assertEqual(self.tree_soft.get_roots(), [self.item1, self.item2, self.item3, self.item8])

    def test_process_items_positions_hard(self):
        self.add_items_by_list(self.tree_hard)
        self.tree_hard.process_connections()
        self.assertEqual(self.tree_hard.positions, {})
        self.tree_hard.process_items_positions()
        self.assertEqual(str(self.tree_hard.positions), '{1: (-4, 0), 2: (-3, 0), 3: (-2, 0), 4: (-1, 0), 5: (0, 0), 6: (1, 0), 7: (2, 0), 8: (3, 0), 9: (0, -1)}')
        self.assertEqual(self.tree_hard.positions, {self.item1: (-4, 0), self.item2: (-3, 0), self.item3: (-2, 0), self.item4: (-1, 0), self.item5: (0, 0), self.item6: (1, 0), self.item7: (2, 0), self.item8: (3, 0), self.item9: (0, -1)})

    def test_process_items_positions_soft(self):
            self.add_items_by_list(self.tree_soft)
            self.tree_soft.process_connections()
            self.assertEqual(self.tree_soft.positions, {})
            self.tree_soft.process_items_positions()
            self.assertEqual(str(self.tree_soft.positions), '{1: (-2, 0), 2: (-1, 0), 3: (0, 0), 8: (1, 0), 4: (-2, -1), 6: (-1, -1), 5: (0, -1), 9: (1, -1), 7: (0, -2)}')
            self.assertEqual(self.tree_soft.positions, {self.item1: (-2, 0), self.item2: (-1, 0), self.item3: (0, 0), self.item8: (1, 0), self.item4: (-2, -1), self.item6: (-1, -1), self.item5: (0, -1), self.item9: (1, -1), self.item7: (0, -2)})

    def test_process_layers_hard(self):
        self.add_items_by_list(self.tree_hard)
        self.tree_hard.process_connections()
        self.assertEqual(self.tree_hard.positions, {})
        self.tree_hard.process_layers(self.tree_hard.get_roots())
        self.assertEqual(str(self.tree_hard.positions), '{1: (-4, 0), 2: (-3, 0), 3: (-2, 0), 4: (-1, 0), 5: (0, 0), 6: (1, 0), 7: (2, 0), 8: (3, 0), 9: (0, -1)}')
        self.assertEqual(self.tree_hard.positions, {self.item1: (-4, 0), self.item2: (-3, 0), self.item3: (-2, 0), self.item4: (-1, 0), self.item5: (0, 0), self.item6: (1, 0), self.item7: (2, 0), self.item8: (3, 0), self.item9: (0, -1)})

    def test_layers_soft(self):
        self.add_items_by_list(self.tree_soft)
        self.tree_soft.process_connections()
        self.assertEqual(self.tree_soft.positions, {})
        self.tree_soft.process_layers(self.tree_soft.get_roots())
        self.assertEqual(str(self.tree_soft.positions), '{1: (-2, 0), 2: (-1, 0), 3: (0, 0), 8: (1, 0), 4: (-2, -1), 6: (-1, -1), 5: (0, -1), 9: (1, -1), 7: (0, -2)}')
        self.assertEqual(self.tree_soft.positions, {self.item1: (-2, 0), self.item2: (-1, 0), self.item3: (0, 0), self.item8: (1, 0), self.item4: (-2, -1), self.item6: (-1, -1), self.item5: (0, -1), self.item9: (1, -1), self.item7: (0, -2)})

    def test_x_offset_calc(self):
        self.assertEqual(self.tree_hard.x_offset_calc(len([1, 2, 3, 4])), -2)
        self.assertEqual(self.tree_hard.x_offset_calc(len([1, 2, 3, 4, 5])), -2)
        self.assertEqual(self.tree_hard.x_offset_calc(len([])), 0)
        
    def test_define_item_position(self):
        self.assertEqual(self.tree_soft.positions, {})
        self.tree_soft.define_item_position([1, 2, 3], 0)
        self.assertEqual(self.tree_soft.positions, {1: (-1, 0), 2: (0, 0), 3: (1, 0)})
        
    def test_fetch_next_layer_list_hard(self):
        self.add_items_by_list(self.tree_hard)
        self.tree_hard.process_connections()
        self.assertEqual(self.tree_hard.fetch_next_layer_list(self.tree_hard.get_roots()), [self.item9])

    def test_fetch_next_layer_list_soft(self):
        self.add_items_by_list(self.tree_soft)
        self.tree_soft.process_connections()
        self.assertEqual(self.tree_soft.fetch_next_layer_list(self.tree_soft.get_roots()), [self.item4, self.item6, self.item5, self.item9])

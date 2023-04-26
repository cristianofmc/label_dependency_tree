import unittest

from source.Item import Item

class TestItem(unittest.TestCase):
    def setUp(self):
        self.item1 = Item(1, ['blue'], [])
        self.item2 = Item(2, ['yellow'], [])
        self.item3 = Item(3, ['red'], [])
        self.item4 = Item(4, ['green'], ['blue', 'yellow'])
        self.item5 = Item(5, ['orange'], ['red', 'yellow'])
        self.item6 = Item(6, ['violet'], ['blue', 'red'])
        self.item7 = Item(7, ['russet'], ['orange', 'violet'])
        self.item8 = Item(8, [], [])
        self.item9 = Item(9, ['one'], ['two'])

    def test_constructor(self):
        self.assertEqual(self.item4.name, 4)
        self.assertEqual(self.item4.labels, ['green'])
        self.assertEqual(self.item4.dependencies, ['blue', 'yellow'])
        self.assertEqual(self.item4.connections, [])

    def test_label_false(self):
        self.assertFalse(['red'] in self.item2.labels)

    def test_dependency_false(self):
        self.assertFalse(['blue'] in self.item5.dependencies)

    def test_add_connection(self):
        self.item1.add_connection(self.item4)
        self.item1.add_connection(self.item6)
        self.assertEqual(self.item1.connections, [self.item4, self.item6])

    if __name__ == '__main__':
        unittest.main()

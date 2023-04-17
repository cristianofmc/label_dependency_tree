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


    def test_has_label_true(self):
        self.assertTrue(self.item1.has_label('blue'))

    def test_has_label_false(self):
        self.assertFalse(self.item2.has_label('red'))

    def test_has_dependency_true(self):
        self.assertTrue(self.item4.has_dependency('blue'))
        self.assertTrue(self.item4.has_dependency('yellow'))

    def test_has_dependency_false(self):
        self.assertFalse(self.item5.has_dependency('blue'))

    if __name__ == '__main__':
        unittest.main()

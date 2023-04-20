from typing import List
from typing import Dict
from Item import Item

class Tree:
    def __init__(self, edge_type: str = 'hard'):
        self.items = []
        self.positions = {}
        self.edge_type = edge_type

    def add_item(self, item: Item):
        self.items.append(item)

    def process_edges(self, edge_type: str = 'hard'):
        for item in self.items:
            item.edges = []
            for depentency_items in self.items:
                if depentency_items.dependencies and item.labels:
                    if self.has_dependency(item.labels, depentency_items.dependencies):
                        item.edges.append(depentency_items)

    def has_dependency(self, labels, dependencies):
        if self.edge_type == 'soft':
            return self.verify_dependency_soft(labels, dependencies)
        else:
            return self.verify_dependency_hard(labels, dependencies)

    def verify_dependency_hard(self, labels, dependencies):
        return set(dependencies).issubset(labels)

    def verify_dependency_soft(self, labels, dependencies):
        return any(set(dependencies).intersection(labels))

    def fetch_item_dependencies_list(self, reference_item: Item):
        item_dependency_list = []
        for item in items:
            if reference_item.dependencies and item.labels:
                if self.has_dependency(item.labels, reference_item.dependencies):
                    item_dependency_list.append(item)
        return item_dependency_list

    def get_roots(self):
        return [item for item in self.items if len(self.fetch_item_dependencies_list(item)) == 0]
        
    def process_items_positions(self):
        self.positions = {}
        self.process_layers(self.get_roots())
    
    def process_layers(self, items, start_point = 0):
        self.define_item_position(items, start_point)
        next_list = self.fetch_next_layer_list(items)
        if next_list: self.process_layers(next_list, start_point + 1)
    
    def define_item_position(self, items:  list, y):
        for index, item in enumerate(items):
            self.positions[item] = (index, y)

    def fetch_next_layer_list(self, current_list: list):
        next_list = []
        for item in current_list:
            for edge in item.edges:
                if edge not in next_list:
                    next_list.append(edge)
        return next_list





tree = Tree('soft')
# tree = Tree()
item1 = Item(1, ['blue'], [])
item2 = Item(2, ['yellow'], [])
item3 = Item(3, ['red'], [])
item4 = Item(4, ['green'], ['blue', 'yellow'])
item5 = Item(5, ['orange'], ['red', 'yellow'])
item6 = Item(6, ['violet'], ['blue', 'red'])
item7 = Item(7, ['russet'], ['orange', 'violet'])
items = [item1,item2,item3,item4,item5,item6,item7]

for item in items:
    tree.add_item(item)

tree.process_edges()
tree.process_items_positions()
print(tree.positions)

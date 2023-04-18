from typing import List
from source.Item import Item

class Tree:
    def __init__(self, edge_type: str = 'hard'):
        self.items = []
        self.edge_type = edge_type

    def add_item(self, item: Item):
        self.items.append(item)

    def process_edges(self, edge_type: str = 'hard'):
        for item in self.items:
            item.edge = []
            for depentency_items in self.items:
                if depentency_items.dependencies and item.labels:
                    if self.has_dependency(item.labels, depentency_items.dependencies):
                        item.edge.append(depentency_items)


    def has_dependency(self, labels, dependencies):
        if self.edge_type == 'soft':
            return self.verify_dependency_soft(labels, dependencies)
        else:
            return self.verify_dependency_hard(labels, dependencies)

    def verify_dependency_hard(self, labels, dependencies):
        return set(dependencies).issubset(labels)

    def verify_dependency_soft(self, labels, dependencies):
        return any(set(dependencies).intersection(labels))
        


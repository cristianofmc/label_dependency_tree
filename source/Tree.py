from typing import List
from typing import Dict
from source.Item import Item

class Tree:
    def __init__(self, connection_type: str = 'hard'):
        self.items = []
        self.positions = {}
        self.connection_type = connection_type

    def add_item(self, item: Item):
        self.items.append(item)

    def process_connections(self):
        for item in self.items:
            item.connections = []
            for depentency_items in self.items:
                if depentency_items.dependencies and item.labels:
                    if self.has_dependency(item.labels, depentency_items.dependencies):
                        item.add_connection(depentency_items)

    def has_dependency(self, labels, dependencies):
        if self.connection_type == 'soft':
            return self.verify_dependency_soft(labels, dependencies)
        else:
            return self.verify_dependency_hard(labels, dependencies)

    def verify_dependency_hard(self, labels, dependencies):
        return set(dependencies).issubset(labels)

    def verify_dependency_soft(self, labels, dependencies):
        return any(set(dependencies).intersection(labels))

    def fetch_item_dependents(self, reference_item: Item):
        direct_item_dependents = []
        all_dependencies_from_item = []
        for item in self.items:
            if reference_item.dependencies and item.labels:
                if self.has_dependency(item.labels, reference_item.dependencies):
                    direct_item_dependents.append(item)
        all_dependencies_from_item = direct_item_dependents
        next_dependents = []
        for item in direct_item_dependents:
            next_dependents = self.fetch_item_dependents(item)
            for next_item in next_dependents:
                if next_item not in all_dependencies_from_item:
                    all_dependencies_from_item.append(next_item)
        return all_dependencies_from_item

    def get_roots(self):
        return [item for item in self.items if len(self.fetch_item_dependents(item)) == 0]
        
    def process_items_positions(self):
        self.positions = {}
        self.process_layers(self.get_roots())
    
    def process_layers(self, items: List, start_point = 0):
        self.define_item_position(items, start_point)
        next_list = self.fetch_next_layer_list(items)
        if next_list: self.process_layers(next_list, start_point - 1)
    
    def x_offset_calc(self, len):
        return int(len / 2) *-1
    
    def define_item_position(self, items:  list, y):
        x_offset = self.x_offset_calc(len(items))
        for index, item in enumerate(items):
            self.positions[item] = (index + x_offset, y)

    def fetch_next_layer_list(self, current_list: list):
        next_list = []
        for item in current_list:
            for connection in item.connections:
                if connection not in next_list:
                    next_list.append(connection)
        return next_list
 
from typing import List

class Item:
    def __init__(self, name: str, labels: List[str], dependencies: List[str]):
        self.name = name
        self.labels = labels
        self.dependencies = dependencies
        self.connections = []

    def add_connection(self, item):
        self.connections.append(item)

    def __repr__(self):
        return str(self.name)

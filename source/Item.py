from typing import List

class Item:
    def __init__(self, name: str, labels: List[str], dependencies: List[str]):
        self.name = name
        self.labels = labels
        self.dependencies = dependencies
        self.edges = []

    def add_edge(self, item):
        self.edges.append(item)

    def __repr__(self):
        return str(self.name)

    def has_label(self, label):
        return label in self.labels

    def has_dependency(self, label):
        return any(label in dependency for dependency in self.dependencies)

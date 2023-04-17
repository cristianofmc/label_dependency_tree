import networkx as nx
import matplotlib.pyplot as plt
from typing import List
from source.Item import Item

class DependencyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.node_positions = {}


    def add_items(self, items: List[Item], edge_type: str = 'hard'):
        for item in items:
            self.graph.add_node(item.name)

        if edge_type == 'soft':
            self.soft_edge_dependencies(items)
        else:
            self.hard_edge_dependencies(items)

    def soft_edge_dependencies(self, items):
        for item in items:
            for depentency_items in items:
                if depentency_items.dependencies and item.labels:
                    common_labels = set(depentency_items.dependencies).intersection(item.labels)
                    if common_labels:
                        self.graph.add_edge(depentency_items.name, item.name)

    def hard_edge_dependencies(self, items):
        for item in items:
            for depentency_items in items:
                if depentency_items.dependencies and item.labels:
                    if set(depentency_items.dependencies).issubset(item.labels):
                        self.graph.add_edge(depentency_items.name, item.name)

    def count_edges_from_node(self, node):
        count = 0
        for _ in self.graph.out_edges(node):
            count += 1
        return count

    def count_edges_to_node(self, node):
        count = 0
        for _ in self.graph.in_edges(node):
            count += 1
        return count

    def get_roots(self):
        roots = []
        for node in self.graph.nodes():
            if self.count_edges_from_node(node) == 0:
                roots.append(node)
        return roots

    def set_node_position(self, current_list, y):
        next_list = []      
        try:
            for current in current_list:
                next_list = list(set(next_list).union(set(self.graph.predecessors(current))))
        except:
            pass

        if next_list:
            y -= 1
            for i, next_node in enumerate(next_list):
                x = self.x_offset_calc(len(next_list))
                self.node_positions[next_node] = (x + i , y)
            self.set_node_position(next_list, y)

    def x_offset_calc(self, len):
        return int(len / 2) *-1

    def generate_tree(self):
        y = 0
        roots = self.get_roots()
        x_offset = self.x_offset_calc(len(roots))
        for i, root in enumerate(roots):
            self.node_positions[root] = (x_offset + i, y)

        self.set_node_position(roots, y)       

    def draw(self, file_name):
        nx.draw_networkx_nodes(self.graph, self.node_positions, node_color='lightblue', node_size=1000)
        nx.draw_networkx_edges(self.graph, self.node_positions, arrows=True)
        nx.draw_networkx_labels(self.graph, self.node_positions)

        plt.savefig(file_name+'.png')
        plt.show()

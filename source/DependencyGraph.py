import networkx
from matplotlib import pyplot
from typing import List
from source.Tree import Tree

class DependencyGraph:
    def __init__(self, tree: Tree):
        self.graph = networkx.DiGraph()
        self.tree = tree
        self.node_positions = {}

    def process_tree(self):
        self.graph.clear()
        self.tree.process_connections()
        self.tree.process_items_positions()
        self.create_nodes_by_tree_items()
        self.create_edges_by_items()
        self.node_positions = self.process_positions()

    def process_positions(self):
        return self.tree.positions

    def create_nodes_by_tree_items(self):
        self.graph.add_nodes_from(self.tree.items)
    
    def create_edges_by_items(self):
        for node in self.graph.nodes():
            for connection in node.connections:
                self.graph.add_edge(node, connection)

    def draw(self, file_name):
        networkx.draw_networkx_nodes(self.graph, self.node_positions, node_color='lightblue', node_size=1000)
        networkx.draw_networkx_edges(self.graph, self.node_positions, arrows=True)
        networkx.draw_networkx_labels(self.graph, self.node_positions)

        pyplot.savefig(file_name+'.png')
        pyplot.clf()
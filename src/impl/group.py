
from .node import Node

# Represents a row, column, or box
class Group:
    def __init__(self, node_list : list[Node]):
        self.nodes = tuple(node_list)
        self.node_set = set(node_list)

        # bit of a hack :)
        for node in self.nodes:
            node.groups.add(self)

    
    def get(self, index):
        return self.nodes[index]
    
    def contains(self, node):
        return self.node_set.contains(node)
    
    def __repr__(self):
        return str(self.nodes)
    
    def __eq__(self, other):
        return self.nodes == other.nodes
    
    def __hash__(self):
        return hash(self.nodes)

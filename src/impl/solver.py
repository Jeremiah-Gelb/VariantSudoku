import itertools

class Node:
    def __init__(self, value_options : set[int] =None, neighbors=None):
        self.value_options = value_options if value_options else {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.neighbors = neighbors if value_options else set()

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)


    # Removes value options based on fully determined neighbors
    # Returns true if this did anything
    def reduce_value_options_based_on_neighbors(self):        
        *_, last = itertools.accumulate(
            map(
                lambda value_options: self.discard_value_option(next(iter(value_options))) if len(value_options) == 1 else False, 
                iter(neighbor.value_options for neighbor in self.neighbors)
            ),
            lambda x, y: x or y,
            initial=False
        )
        
        return last
    
    def __repr__(self):
        return str(self.value_options)
           
    
    def discard_value_option(self, option):
        len_before = len(self.value_options)
        self.value_options.discard(option)
        return len_before != len(self.value_options)

def iteravely_reduce_value_options(nodes):
    work_set = set(nodes)

    while work_set:
        node = work_set.pop()
        if (node.reduce_value_options_based_on_neighbors()):
            work_set.update(node.neighbors)



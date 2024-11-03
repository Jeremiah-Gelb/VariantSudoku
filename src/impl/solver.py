import itertools

def solve(puzzle):
    work_set = set(itertools.chain.from_iterable([group.nodes for group in puzzle.rows]))

    while work_set:
        node = work_set.pop()
        print("processing node", node)
        # Handle a node having exactly one value
        if (node.value is not None):
            for group in node.groups:
                for neighbor in group.nodes:
                    if (neighbor == node): 
                        continue

                    if neighbor.discard_value_option(node.value) and neighbor.value is not None:
                        print("did something to that neighbor", neighbor)
                        work_set.update(set(itertools.chain.from_iterable([group.nodes for group in neighbor.groups])))

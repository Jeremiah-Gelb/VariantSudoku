import itertools
from .puzzle import Puzzle

def solve(puzzle):
    did_something = True
    while(did_something):
        did_something = False
        if (eval_naked_singles(puzzle)):
            did_something = True
            # No need to reset loop after this
        if (eval_hidden_singles(puzzle)):
            did_something = True
            continue
        

def eval_naked_singles(puzzle):
    work_set = set(itertools.chain.from_iterable([group.nodes for group in puzzle.rows]))
    did_something = False
    while work_set:
        node = work_set.pop()
        print("processing node", node)
        # Handle a node having exactly one value
        if (node.value is not None):
            for group in node.groups:
                for neighbor in group.nodes:
                    if (neighbor == node): 
                        continue

                    if neighbor.discard_value_option(node.value):
                        # did remove at least one option
                        did_something = True
                        if neighbor.value is not None:
                            # if we removed an option, and now it has a determined value, now we check the other neighbors!
                            work_set.update(set(itertools.chain.from_iterable([group.nodes for group in neighbor.groups])))
    return did_something

def eval_hidden_singles(puzzle: Puzzle):
    did_something = False

    for group in puzzle.rows + puzzle.boxes + puzzle.columns:
        possible_cell_indcides_by_value = {}
        for index, node in enumerate(group.nodes):
            if not node.value:
                for value in node.value_options:
                    if value not in possible_cell_indcides_by_value.keys():
                        possible_cell_indcides_by_value[value] = set()
                    possible_cell_indcides_by_value[value].add(index)
        for value in possible_cell_indcides_by_value.keys():
            indices = possible_cell_indcides_by_value[value]
            if len(indices) == 1:
                did_something = True
                for index in indices:
                    group.nodes[index].set_value(value)
    return did_something

def eval_intersections(puzzle: Puzzle):
    did_something = False

    # If all of the candidates cells for a certain value within a group also all reside in a second group, then all the other
    # candidates in the second group for that value may be eliminated

    # Ex 1 (Pointing): if all of the 1s within box 2 lie in row 3, then we may eliminate all of the 1s in row 3 not in box 2
    # Ex 2 (Claiming): if all of the 1s within row 2 lie in box 3, then we may eliminate all of the 1s in box 3 not in row 2

    for group in puzzle.rows:
        pass
    return did_something


import itertools
from .puzzle import Puzzle
from .house import House
from .cell import Cell
from collections import deque


def solve(puzzle):
    did_something = True
    while(did_something):
        did_something = False
        
        print("1")
        if (eval_all_naked_subsets(puzzle, 1, False, True)):
            did_something = True
            # No need to reset loop after this

        if not puzzle.undetermined_cells: 
            return

        print("2")
        if (eval_all_naked_subsets(puzzle, 2, False, True)):
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        print("3")
        if (eval_all_naked_subsets(puzzle, 3, True, False)):
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        print("4")
        if (eval_all_naked_subsets(puzzle, 4, True, False)):
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        

def eval_all_naked_subsets(puzzle: Puzzle, n: int, stop_early=True, requeue=False):
    queue = deque(puzzle.houses) # might be better to randomize the order ?
    did_something = False
    while queue:
        house = queue.popleft()
        affected_cells = eval_naked_subsets(house, n)

        if (affected_cells):
            did_something = True

            if (stop_early):
                return did_something
            
            if (requeue):
                cell: Cell
                for cell in affected_cells:
                    for affected_house in cell.houses:
                        if affected_house != house:
                            queue.append(affected_house)

    return did_something

def eval_naked_subsets(house: House, cells: int):
    affected_cells = []
    combinations = list(itertools.combinations(house.cells, cells)) 

    for combination in combinations:
        # For each unique combination of n cells

        unique_candidates = set(itertools.chain.from_iterable(cell.candidates for cell in combination))

        if len(unique_candidates) <= cells:
            # we identified a cet of n cells that contains n candidates
            for cell in house.cells:
                if cell not in combination: # Slightly inefficient: combination is a tuple. Set might be faster?
                    for candidate in unique_candidates:
                        if cell.remove_candidate(candidate):
                            affected_cells.append(cell)
    return affected_cells


def eval_hidden_singles(puzzle: Puzzle):
    did_something = False
    return did_something

def eval_intersections(puzzle: Puzzle):
    did_something = False

    # If all of the candidates cells for a certain value within a group also all reside in a second group, then all the other
    # candidates in the second group for that value may be eliminated

    # Ex 1 (Pointing): if all of the 1s within box 2 lie in row 3, then we may eliminate all of the 1s in row 3 not in box 2
    # Ex 2 (Claiming): if all of the 1s within row 2 lie in box 3, then we may eliminate all of the 1s in box 3 not in row 2
    return did_something


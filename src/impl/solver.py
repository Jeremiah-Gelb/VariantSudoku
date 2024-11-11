import itertools
from .puzzle import Puzzle
from .house import House
from .cell import Cell
from collections import deque


def solve(puzzle):
    did_something = True
    while(did_something):
        did_something = False
        
        print("\nSize 1 Naked Subsets")
        if (eval_all_naked_subsets(puzzle, 1, False, True)):
            did_something = True
            # No need to reset loop after this

        if not puzzle.undetermined_cells: 
            return
        
        print("\nSize 1 Hidden Subsets")
        if (eval_all_hidden_subsets(puzzle, 1, False, True)):
            did_something = True
            # No need to reset loop after this

        if not puzzle.undetermined_cells: 
            return

        print("\nSize 2 Naked Subsets")
        if (eval_all_naked_subsets(puzzle, 2, False, True)):
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        print("\nSize 2 Hidden Subsets")
        if (eval_all_hidden_subsets(puzzle, 2, False, True)):
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        print("\nSize 3 Naked Subsets")
        if (eval_all_naked_subsets(puzzle, 3, True, False)):
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        print("\nSize 3 Hidden Subsets")
        if (eval_all_hidden_subsets(puzzle, 3, True, False)):
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        print("\nSize 4 Naked Subsets")
        if (eval_all_naked_subsets(puzzle, 4, True, False)):
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        print("\nSize 4 Hidden Subsets")
        if (eval_all_hidden_subsets(puzzle, 4, True, False)):
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


def eval_all_hidden_subsets(puzzle: Puzzle, n: int, stop_early=True, requeue=False):
    queue = deque(puzzle.houses) # might be better to randomize the order ?
    did_something = False
    while queue:
        house = queue.popleft()
        affected_cells = eval_hidden_subsets(house, n)

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


def eval_hidden_subsets(house: House, values: int):
    affected_cells = []
    combinations = list(itertools.combinations([1, 2, 3, 4, 5, 6, 7, 8, 9], values)) 

    for combination in combinations:
        # For each unique combination of n values

        unique_cells = set(itertools.chain.from_iterable(house.candidate_to_cell_map[value] for value in combination))

        if len(unique_cells) <= values:
            # we identified that the n values are only contained in n cells.
            # so we can remove all other candidates from those cells
            for cell in unique_cells:
                for candidate in list(cell.candidates): # slight hack, make a copy to avoid removing from the list where we are iterating
                    if candidate not in combination: # Slightly inefficient: combination is a tuple. Set might be faster?
                        if cell.remove_candidate(candidate):
                            affected_cells.append(cell)
    return affected_cells

def eval_intersections(puzzle: Puzzle):
    did_something = False

    # If all of the candidates cells for a certain value within a group also all reside in a second group, then all the other
    # candidates in the second group for that value may be eliminated

    # Ex 1 (Pointing): if all of the 1s within box 2 lie in row 3, then we may eliminate all of the 1s in row 3 not in box 2
    # Ex 2 (Claiming): if all of the 1s within row 2 lie in box 3, then we may eliminate all of the 1s in box 3 not in row 2
    return did_something


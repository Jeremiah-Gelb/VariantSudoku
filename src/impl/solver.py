import itertools
from .puzzle import Puzzle
from .house import House
from .cell import Cell
from collections import deque


def solve(puzzle, debug=False):
    did_something = True
    while(did_something):
        did_something = False
        
        log(debug, "Trying Size 1 Naked Subsets")
        affected_cells = eval_first_naked_subsets(puzzle, 1)
        if (affected_cells):
            log(debug, "Found Size 1 Naked Subsets", affected_cells)
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        log(debug, "Trying Size 1 Hidden Subsets")
        affected_cells = eval_first_hidden_subsets(puzzle, 1)
        if (affected_cells):
            log(debug, "Found Size 1 Hidden Subsets", affected_cells)
            did_something = True
            continue
            # No need to reset loop after this

        if not puzzle.undetermined_cells: 
            return

        affected_cells = eval_first_naked_subsets(puzzle, 2)
        if (affected_cells):
            log(debug, "Found Size 2 Naked Subsets", affected_cells)
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        log(debug, "Trying Size 2 Hidden Subsets")
        affected_cells = eval_first_hidden_subsets(puzzle, 2)
        if (affected_cells):
            log(debug, "Found Size 2 Hidden Subsets", affected_cells)
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        log(debug, "Trying Intersections")
        affected_cells = eval_first_intersection(puzzle)
        if affected_cells:
            log(debug, "Found Intersections", affected_cells)
            did_something = True
            continue
        if not puzzle.undetermined_cells: 
            return
        
        log(debug, "Size 3 Naked Subsets")
        affected_cells = eval_first_naked_subsets(puzzle, 3)
        if (affected_cells):
            log(debug, "Found Size 3 Naked Subsets", affected_cells)
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        log(debug, "Trying Size 3 Hidden Subsets")
        affected_cells = eval_first_hidden_subsets(puzzle, 3)
        if (affected_cells):
            log(debug, "Found Size 3 Hidden Subsets", affected_cells)
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        log(debug, "Trying Size 4 Naked Subsets")
        affected_cells = eval_first_naked_subsets(puzzle, 4)
        if (affected_cells):
            log(debug, "Found Size 4 Naked Subsets", affected_cells)
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
        
        log(debug, "Size 4 Hidden Subsets")
        affected_cells = eval_first_hidden_subsets(puzzle, 4)
        if (affected_cells):
            log(debug, "Found Size 4 Hidden Subsets", affected_cells)
            did_something = True
            continue

        if not puzzle.undetermined_cells: 
            return
def log(debug, *args):
    if (debug):
        print(args)
        

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

def eval_first_naked_subsets(puzzle: Puzzle, n: int):
    queue = deque(puzzle.houses) # might be better to randomize the order ?
    affected_cells = set()
    while queue:
        house = queue.popleft()
        affected_cells = eval_naked_subsets(house, n)

        if (affected_cells):
            return affected_cells

    return affected_cells

def eval_naked_subsets(house: House, cells: int):
    affected_cells = set()
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
                            affected_cells.add(cell)
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

def eval_first_hidden_subsets(puzzle: Puzzle, n: int):
    queue = deque(puzzle.houses) # might be better to randomize the order ?
    affected_cells = set()
    while queue:
        house = queue.popleft()
        affected_cells = eval_hidden_subsets(house, n)

        if (affected_cells):
            return affected_cells

    return affected_cells


def eval_hidden_subsets(house: House, values: int):
    affected_cells = set()
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
                            affected_cells.add(cell)
    return affected_cells

# Should rewrite this to handle n houses
def eval_first_intersection(puzzle: Puzzle):
    combinations = list(itertools.combinations(puzzle.houses, 2))
    affected_cells = set()

    for combination in combinations:
        affected_cells = eval_intersections(combination[0], combination[1])
        if affected_cells:
            return affected_cells

    return affected_cells


# Should rewrite this to handle n houses
def eval_intersections(house1: House, house2: House):
    affected_cells = set()

    if house2 not in house1.intersecting_houses:
        return affected_cells
    
    for candidate in [1, 2, 3, 4, 5, 6, 7, 9]:
        # we make a copy here because we mutate it during remove_candidate call
        # other option is to iterate through house1.cells That might be better
        # because iterating through 9 cells is likely faster than making a set but idk
        house_1_candidate_cells = set(house1.candidate_to_cell_map[candidate])
        house_2_candidate_cells = set(house2.candidate_to_cell_map[candidate])



        if house_1_candidate_cells.issubset(house2.cells):
            # all the cells for a given candidate in house 1 are also in house 2. 
            # That means that in house 2, the only place for those candidates is also in house 1
            # so all other places in house 2 
            for cell in house_2_candidate_cells:
                if cell not in house_1_candidate_cells:
                    if cell.remove_candidate(candidate):
                        affected_cells.add(cell)

        if house_2_candidate_cells.issubset(house1.cells):
            for cell in house_1_candidate_cells:
                if cell not in house_2_candidate_cells:
                    if cell.remove_candidate(candidate):
                        affected_cells.add(cell)
        
        # early stop (rather than looking through other candidate values)
        if affected_cells:
            return affected_cells

    
    return affected_cells

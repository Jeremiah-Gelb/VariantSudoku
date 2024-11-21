import itertools
from .puzzle import Puzzle
from .puzzle import Constraint
from .house import House
from .cell import Cell
from collections import deque
from enum import Enum

class SolveTechnique(Enum):
    NAKED_SUBSETS_1 = 1
    NAKED_SUBSETS_2 = 2
    NAKED_SUBSETS_3 = 3
    NAKED_SUBSETS_4 = 4
    HIDDEN_SUBSETS_1 = 5
    HIDDEN_SUBSETS_2 = 6
    HIDDEN_SUBSETS_3 = 7
    HIDDEN_SUBSETS_4 = 8
    INTERSECTIONS = 9

default = set(s for s in SolveTechnique)

def solve(puzzle, debug=False, solve_techniques: set[SolveTechnique] = default):
    solve_logical(puzzle, debug, solve_techniques)

def solve_logical(puzzle, debug=False, solve_techniques: set[SolveTechnique] = set()):
    did_something = True
    while(did_something):
        did_something = False
        
        if Constraint.RCV in puzzle.constraints:
            log(debug, "Trying RCV")
            affected_cells = propagate_rcv_constraint(puzzle)
            if affected_cells:
                did_something = True
                log(debug, "Eliminated Candidates using rcv", affected_cells)
                continue
            if not puzzle.undetermined_cells: 
                return


        if SolveTechnique.NAKED_SUBSETS_1 in solve_techniques:
            log(debug, "Trying Size 1 Naked Subsets")
            affected_cells = eval_first_naked_subsets(puzzle, 1)
            if (affected_cells):
                log(debug, "Found Size 1 Naked Subsets", affected_cells)
                did_something = True
                continue

            if not puzzle.undetermined_cells: 
                return
        
        if SolveTechnique.HIDDEN_SUBSETS_1 in solve_techniques:
            log(debug, "Trying Size 1 Hidden Subsets")
            affected_cells = eval_first_hidden_subsets(puzzle, 1)
            if (affected_cells):
                log(debug, "Found Size 1 Hidden Subsets", affected_cells)
                did_something = True
                continue
                # No need to reset loop after this

            if not puzzle.undetermined_cells: 
                return

        if SolveTechnique.NAKED_SUBSETS_2 in solve_techniques:
            affected_cells = eval_first_naked_subsets(puzzle, 2)
            if (affected_cells):
                log(debug, "Found Size 2 Naked Subsets", affected_cells)
                did_something = True
                continue

            if not puzzle.undetermined_cells: 
                return
        
        if SolveTechnique.HIDDEN_SUBSETS_2 in solve_techniques:
            log(debug, "Trying Size 2 Hidden Subsets")
            affected_cells = eval_first_hidden_subsets(puzzle, 2)
            if (affected_cells):
                log(debug, "Found Size 2 Hidden Subsets", affected_cells)
                did_something = True
                continue

            if not puzzle.undetermined_cells: 
                return
        
        if SolveTechnique.INTERSECTIONS in solve_techniques:
            log(debug, "Trying Intersections")
            affected_cells = eval_first_intersection(puzzle)
            if affected_cells:
                log(debug, "Found Intersections", affected_cells)
                did_something = True
                continue
            if not puzzle.undetermined_cells: 
                return
        
        if SolveTechnique.NAKED_SUBSETS_3 in solve_techniques:
            log(debug, "Size 3 Naked Subsets")
            affected_cells = eval_first_naked_subsets(puzzle, 3)
            if (affected_cells):
                log(debug, "Found Size 3 Naked Subsets", affected_cells)
                did_something = True
                continue

            if not puzzle.undetermined_cells: 
                return
        
        if SolveTechnique.HIDDEN_SUBSETS_3 in solve_techniques:
            log(debug, "Trying Size 3 Hidden Subsets")
            affected_cells = eval_first_hidden_subsets(puzzle, 3)
            if (affected_cells):
                log(debug, "Found Size 3 Hidden Subsets", affected_cells)
                did_something = True
                continue

            if not puzzle.undetermined_cells: 
                return
        
        if SolveTechnique.NAKED_SUBSETS_4 in solve_techniques:
            log(debug, "Trying Size 4 Naked Subsets")
            affected_cells = eval_first_naked_subsets(puzzle, 4)
            if (affected_cells):
                log(debug, "Found Size 4 Naked Subsets", affected_cells)
                did_something = True
                continue

            if not puzzle.undetermined_cells: 
                return
        
        if SolveTechnique.HIDDEN_SUBSETS_4 in solve_techniques:
            log(debug, "Tring Size 4 Hidden Subsets")
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


def propagate_rcv_constraint(puzzle: Puzzle):
    # For each Row = R, Column = C, Value = V
    # That implies the existance of another cell
    # Where Row = V, Column = R, and Value = C
    # (r, c, v) => (v, r, c) => (c, v, r) => (r, c, v)
    # Also don't forget that we index arrays at 0, but rcv is notated starting at 1

    # Now say you are looking at a cell with unknown value (r, c, x)
    # Well, that must be pointed at by the cell (c, x, r)
    # So the question of "What is the value x at Row = r, Column = c"
    # Is the same as saying in Row = c, what is the column where the Value = r lies

    affected_cells = set()

    for row_index, row in enumerate(puzzle.rows):
        for col_index, cell in enumerate(row):
            target_value = row_index + 1
            target_row: list[Cell] = puzzle.rows[col_index]
            candidate_values = set(i + 1 for i in range(0,9) if target_value in target_row[i].candidates)
            intersect = cell.candidates.intersection(candidate_values)
            if len(intersect) < len(cell.candidates):
                copy = set(cell.candidates)
                for c in copy:
                    if c not in intersect:
                        affected_cells.add(cell)
                        cell.remove_candidate(c)
    return affected_cells
     
def right_shift_rotate_tuple(tuple):
    x, y, z = tuple
    return (z, x, y)

def left_shift_rotate_tuple(tuple):
    x, y, z = tuple
    return (y, z, x)

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

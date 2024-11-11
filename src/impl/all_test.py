import math
from .cell import Cell
from .puzzle import Puzzle
from .solver import *

def test_discard_value_option():
   node = Cell(row_column=(1,1))
   node.candidates={1, 2, 3}
   
   assert node.value is None
   assert node.candidates == {1, 2, 3}

   node.remove_candidate(1)
   assert node.value is None
   assert node.candidates == {2, 3}

   node.remove_candidate(2)
   assert node.value == 3
   assert node.candidates ==  {3}


def test_construct():
   values = [
      [1, 1, 1, 1, 1, 1, 1, 1, 1],
      [2, 2, 2, 2, 2, 2, 2, 2, 2],
      [3, 3, 3, 3, 3, 3, 3, 3, 3],
      [4, 4, 4, 4, 4, 4, 4, 4, 4],
      [5, 5, 5, 5, 5, 5, 5, 5, 5],
      [6, 6, 6, 6, 6, 6, 6, 6, 6],
      [7, 7, 7, 7, 7, 7, 7, 7, 7],
      [8, 8, 8, 8, 8, 8, 8, 8, 8],
      [9, 9, 9, 9, 9, 9, 9, 9, 9]
   ]

   p = Puzzle(values)

def test_eval_naked_subsets_singles():
   cell_list = [
      Cell(row_column=(0,0), value=1),
      Cell(row_column=(0,1)),
      Cell(row_column=(0,2)),
      Cell(row_column=(0,3)),
      Cell(row_column=(0,4)),
      Cell(row_column=(0,5)),
      Cell(row_column=(0,6)),
      Cell(row_column=(0,7)),
      Cell(row_column=(0,8))
   ]

   house = House(set(cell_list))
   eval_naked_subsets(house, 1)

   expected_cell_list = [
      Cell(row_column=(0,0), value=1),
      Cell(row_column=(0,1), candidates={2, 3, 4, 5, 6, 7, 8, 9}),
      Cell(row_column=(0,2), candidates={2, 3, 4, 5, 6, 7, 8, 9}),
      Cell(row_column=(0,3), candidates={2, 3, 4, 5, 6, 7, 8, 9}),
      Cell(row_column=(0,4), candidates={2, 3, 4, 5, 6, 7, 8, 9}),
      Cell(row_column=(0,5), candidates={2, 3, 4, 5, 6, 7, 8, 9}),
      Cell(row_column=(0,6), candidates={2, 3, 4, 5, 6, 7, 8, 9}),
      Cell(row_column=(0,7), candidates={2, 3, 4, 5, 6, 7, 8, 9}),
      Cell(row_column=(0,8), candidates={2, 3, 4, 5, 6, 7, 8, 9})
   ]

   for index, cell in enumerate(cell_list):
      assert cell.equivalent(expected_cell_list[index])

def test_eval_naked_subsets_quads():
   cell_list = [
      Cell(row_column=(0,0), candidates={1, 2, 3}),
      Cell(row_column=(0,1), candidates={1, 2, 4}),
      Cell(row_column=(0,2), candidates={1, 3, 4}),
      Cell(row_column=(0,3), candidates={2, 3, 4}),
      Cell(row_column=(0,4)),
      Cell(row_column=(0,5)),
      Cell(row_column=(0,6)),
      Cell(row_column=(0,7)),
      Cell(row_column=(0,8))
   ]

   house = House(set(cell_list))
   eval_naked_subsets(house, 4)

   expected_cell_list = [
      Cell(row_column=(0,0), candidates={1, 2, 3}),
      Cell(row_column=(0,1), candidates={1, 2, 4}),
      Cell(row_column=(0,2), candidates={1, 3, 4}),
      Cell(row_column=(0,3), candidates={2, 3, 4}),
      Cell(row_column=(0,4), candidates={5, 6, 7, 8, 9}),
      Cell(row_column=(0,5), candidates={5, 6, 7, 8, 9}),
      Cell(row_column=(0,6), candidates={5, 6, 7, 8, 9}),
      Cell(row_column=(0,7), candidates={5, 6, 7, 8, 9}),
      Cell(row_column=(0,8), candidates={5, 6, 7, 8, 9})
   ]

   for index, cell in enumerate(cell_list):
      assert cell.equivalent(expected_cell_list[index])

def test_eval_hidden_subsets_quads():
   cell_list = [
      Cell(row_column=(0,0), candidates={2, 4, 5, 6, 7, 8, 9}), # 2, 4, 5, 9
      Cell(row_column=(0,1), candidates={2, 3, 4, 5, 6, 7}), # 2, 4, 5
      Cell(row_column=(0,2), candidates={2, 3, 5, 7, 9}), # 2, 5, 9
      Cell(row_column=(0,3), candidates={1, 8, 3}),
      Cell(row_column=(0,4), candidates={1, 7, 6}),
      Cell(row_column=(0,5), candidates={3, 6, 7, 8}),
      Cell(row_column=(0,6), candidates={3, 8}),
      Cell(row_column=(0,7), candidates={2, 3, 5, 6, 8}), # 2, 5
      Cell(row_column=(0,8), candidates={3, 6, 8})
   ]

   house = House(set(cell_list))
   eval_hidden_subsets(house, 4)

   expected_cell_list = [
      Cell(row_column=(0,0), candidates={2, 4, 5, 9}),
      Cell(row_column=(0,1), candidates={2, 4, 5}),
      Cell(row_column=(0,2), candidates={2, 5, 9}),
      Cell(row_column=(0,3), candidates={1, 8, 3}),
      Cell(row_column=(0,4), candidates={1, 7, 6}),
      Cell(row_column=(0,5), candidates={3, 6, 7, 8}),
      Cell(row_column=(0,6), candidates={3, 8}),
      Cell(row_column=(0,7), candidates={2, 5}),
      Cell(row_column=(0,8), candidates={3, 6, 8})
   ]

   for index, cell in enumerate(cell_list):
      assert cell.equivalent(expected_cell_list[index])

def test_eval_all_naked_subsets():
   n = None
   unsolved_values = [
      [n, n, n, 6, 7, 8, 9, 1, 2],
      [n, n, n, 1, 9, 5, 3, 4, 8],
      [n, n, n, 3, 4, 2, 5, 6, 7],
      [8, 5, 9, n, n, n, 4, 2, 3],
      [4, 2, 6, n, n, n, 7, 9, 1],
      [7, 1, 3, n, n, n, 8, 5, 6],
      [9, 6, 1, 5, 3, 7, n, n, n],
      [2, 8, 7, 4, 1, 9, n, n, n],
      [3, 4, 5, 2, 8, 6, n, n, n]
   ]

   puzzle_to_solve = Puzzle(unsolved_values)

   eval_all_naked_subsets(puzzle_to_solve, 1, False, True)

   solved_values = [
      [5, 3, 4, 6, 7, 8, 9, 1, 2],
      [6, 7, 2, 1, 9, 5, 3, 4, 8],
      [1, 9, 8, 3, 4, 2, 5, 6, 7],
      [8, 5, 9, 7, 6, 1, 4, 2, 3],
      [4, 2, 6, 8, 5, 3, 7, 9, 1],
      [7, 1, 3, 9, 2, 4, 8, 5, 6],
      [9, 6, 1, 5, 3, 7, 2, 8, 4],
      [2, 8, 7, 4, 1, 9, 6, 3, 5],
      [3, 4, 5, 2, 8, 6, 1, 7, 9]
   ]

   solution = Puzzle(solved_values)

   assert puzzle_to_solve.equivalent(solution)

def test_eval_all_hidden_subsets():
   n = None
   solved_values = [
      [n, n, n, n, n, n, n, n, 1],
      [n, n, n, n, n, 1, n, n, n],
      [n, n, 1, n, n, n, n, n, n],
      [n, n, n, n, n, n, n, 1, n],
      [n, n, n, n, 1, n, n, n, n],
      [n, 1, n, n, n, n, n, n, n],
      [n, n, n, n, n, n, 1, n, n],
      [n, n, n, 1, n, n, n, n, n],
      [1, n, n, n, n, n, n, n, n],
   ]

   solution = Puzzle(solved_values)

   unsolved_values = [
      [n, n, n, n, n, n, n, n, n],
      [n, n, n, n, n, 1, n, n, n],
      [n, n, 1, n, n, n, n, n, n],
      [n, n, n, n, n, n, n, 1, n],
      [n, n, n, n, 1, n, n, n, n],
      [n, 1, n, n, n, n, n, n, n],
      [n, n, n, n, n, n, 1, n, n],
      [n, n, n, 1, n, n, n, n, n],
      [1, n, n, n, n, n, n, n, n],
   ]

   puzzle_to_solve = Puzzle(unsolved_values)

   eval_all_naked_subsets(puzzle_to_solve, 1, False, True) # need to run this first to remove candidates
   eval_all_hidden_subsets(puzzle_to_solve, 1, False, True)

   assert puzzle_to_solve.equivalent(solution)

def test_solve_easy():
   n = None
   unsolved_values = [
      [1, 4, 3, n, 5, 2, n, n, n],
      [9, n, n, 4, n, 7, n, 2, n],
      [7, 5, n, 3, n, n, 9, n, 1],
      [n, n, 7, n, n, n, 3, n, n],
      [4, 3, 5, n, n, n, 1, 7, 6],
      [n, n, 9, n, n, n, 8, n, n],
      [3, n, 4, n, n, 5, n, 1, 8],
      [n, 8, n, 2, n, 3, n, n, 9],
      [n, n, n, 1, 8, n, 7, 3, 5]
   ]

   puzzle_to_solve = Puzzle(unsolved_values)

   solve(puzzle_to_solve)

   solved_values = [
      [1, 4, 3, 9, 5, 2, 6, 8, 7],
      [9, 6, 8, 4, 1, 7, 5, 2, 3],
      [7, 5, 2, 3, 6, 8, 9, 4, 1],
      [8, 1, 7, 5, 4, 6, 3, 9, 2],
      [4, 3, 5, 8, 2, 9, 1, 7, 6],
      [6, 2, 9, 7, 3, 1, 8, 5, 4],
      [3, 7, 4, 6, 9, 5, 2, 1, 8],
      [5, 8, 1, 2, 7, 3, 4, 6, 9],
      [2, 9, 6, 1, 8, 4, 7, 3, 5]
   ]

   solution = Puzzle(solved_values)

   assert puzzle_to_solve.equivalent(solution)

def test_solve_medium():
   n = None
   unsolved_values = [
      [4, n, n, 8, n, 1, n, n, n],
      [n, n, n, n, n, 3, n, 5, n],
      [n, 5, n, n, n, n, 2, 1, n],
      [2, n, n, n, 8, 9, n, 6, n],
      [n, n, n, n, 1, n, n, n, n],
      [n, 9, n, 6, 3, n, n, n, 7],
      [n, 4, 9, n, n, n, n, 7, n],
      [n, 1, n, 3, n, n, n, n, n],
      [n, n, n, 2, n, 8, n, n, 4]
   ]

   puzzle_to_solve = Puzzle(unsolved_values)

   solve(puzzle_to_solve)

   solved_values = [
      [4, 2, 6, 8, 5, 1, 7, 3, 9],
      [1, 7, 8, 9, 2, 3, 4, 5, 6],
      [9, 5, 3, 7, 4, 6, 2, 1, 8],
      [2, 3, 7, 4, 8, 9, 5, 6, 1],
      [6, 8, 4, 5, 1, 7, 9, 2, 3],
      [5, 9, 1, 6, 3, 2, 8, 4, 7],
      [8, 4, 9, 1, 6, 5, 3, 7, 2],
      [7, 1, 2, 3, 9, 4, 6, 8, 5],
      [3, 6, 5, 2, 7, 8, 1, 9, 4]
   ]

   solution = Puzzle(solved_values)

   assert puzzle_to_solve.equivalent(solution)

def test_solve_hard():
   print("Test Solve Hard Start")
   n = None
   unsolved_values = [
      [2, 4, n, n, n, n, n, 8, 6],
      [n, n, 3, n, n, n, n, n, n],
      [1, n, n, n, n, 2, 5, n, n],
      [5, 9, n, n, 1, n, n, n, 2],
      [n, n, 7, n, n, n, 3, n, n],
      [8, n, n, n, 4, n, n, 9, 7],
      [n, n, 5, 8, n, n, n, n, 3],
      [n, n, n, n, n, n, 6, n, n],
      [3, 2, n, n, n, n, n, 1, 9]
   ]

   puzzle_to_solve = Puzzle(unsolved_values)

   solve(puzzle_to_solve)

   solved_values = [
      [2, 4, 9, 1, 3, 5, 7, 8, 6],
      [7, 5, 3, 4, 6, 8, 9, 2, 1],
      [1, 8, 6, 9, 7, 2, 5, 3, 4],
      [5, 9, 4, 7, 1, 3, 8, 6, 2],
      [6, 1, 7, 2, 8, 9, 3, 4, 5],
      [8, 3, 2, 5, 4, 6, 1, 9, 7],
      [4, 6, 5, 8, 9, 1, 2, 7, 3],
      [9, 7, 1, 3, 2, 4, 6, 5, 8],
      [3, 2, 8, 6, 5, 7, 4, 1, 9]
   ]

   solution = Puzzle(solved_values)

   print("Test Solve Hard End")
   assert puzzle_to_solve.equivalent(solution)
import math
from .node import Node
from .puzzle import Puzzle
from .solver import *

def test_discard_value_option():
   node = Node(row_column=(1,1))
   node.value_options={1, 2, 3}
   
   assert node.value is None
   assert node.value_options == {1, 2, 3}

   node.discard_value_option(1)
   assert node.value is None
   assert node.value_options == {2, 3}

   node.discard_value_option(2)
   assert node.value == 3
   assert node.value_options ==  {3}

   node.discard_value_option(3)
   assert node.value is None
   assert node.value_options == set()


def test_naked_singles():
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
   print("unsolved")
   print(puzzle_to_solve)

   eval_naked_singles(puzzle_to_solve)
   print("solved")
   print(puzzle_to_solve)

   assert puzzle_to_solve == solution

def test_hidden_singles():
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
   print("unsolved")
   print(puzzle_to_solve)

   eval_naked_singles(puzzle_to_solve)
   eval_hidden_singles(puzzle_to_solve)
   
   print("solved")
   print(puzzle_to_solve)

   assert puzzle_to_solve == solution


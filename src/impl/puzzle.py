from .cell import Cell
from .house import House
from enum import Enum

class Constraint(Enum):
    RCV = 1
    NEGATIVE_DIAGONAL = 2

class Puzzle:

    # assuming n by n for now. 
    def __init__(self, row_values : list[list[int]], constraints: set[Constraint] = set()):
        self.rows: list[list[Cell]] = []
        self.houses: list[House] = []
        self.undetermined_cells = set()
        self.constraints = constraints

        # build rows
        for row_index, row in enumerate(row_values):
            cells = set()
            cell_list = []
            for column_index, value in enumerate(row):
                row_column = (row_index, column_index)
                cell = Cell(value, row_column, puzzle=self) if value else Cell(row_column=row_column, puzzle=self)

                if not cell.value:
                    self.undetermined_cells.add(cell)

                cell_list.append(cell)
                cells.add(cell)

            self.houses.append(House(cells))
            self.rows.append(cell_list)

        # build columns
        size = len(self.rows[0]) 
        for row_index in range(size):
            cells = set()
            for column_index in range(size):
                cells.add(self.rows[column_index][row_index])
            self.houses.append(House(cells))

        # build boxes

        # row_start, row_end, column_start, column end. This also assumes 9x9 for now
        box_boundaries = [
            [0, 2, 0, 2], # 1
            [3, 5, 0, 2], # 2
            [6, 8, 0, 2], # 3
            [0, 2, 3, 5], # 4
            [3, 5, 3, 5], # 5
            [6, 8, 3, 5], # 6
            [0, 2, 6, 8], # 7
            [3, 5, 6, 8], # 8
            [6, 8, 6, 8], # 9
        ]

        for box_boundary in box_boundaries:
            cells = set()
            for column_index in range(box_boundary[2], box_boundary[3] + 1):
                for row_index in range(box_boundary[0], box_boundary[1] + 1):
                    cells.add(self.rows[column_index][row_index])
            self.houses.append(House(cells))

        if Constraint.NEGATIVE_DIAGONAL in self.constraints:
            cells = set()
            for i in range(size):
                cells.add(self.rows[i][i])
            self.houses.append(House(cells))

    def __repr__(self):
        string = ""
        for row in self.rows:
            string += str(row) + "\n"

        return string
    
    def equivalent(self, other):
        # only used for testing
        if (len(self.rows) != len(other.rows)):
            raise Exception("Puzzle mismatch number of rows")
        
        for row_index, row in enumerate(self.rows):
            other_row = other.rows[row_index]
            if len(row) != len(other_row):
                raise Exception("Puzzle mismatch row length")

            for cell_index, cell in enumerate(row):
                if cell.value != other_row[cell_index].value:
                    raise Exception("Puzzle mismatching VALUE", row_index, cell_index, cell.value, other_row[cell_index].value)

        return True
    
    def copy(self):
        # Generate a new puzzle
        row_values : list[list[int]] = []
        for row in self.rows:
            values = []
            for cell in row:
                values.append(cell.value)
            row_values.append(values)

        cp = Puzzle(row_values, self.constraints)

        # copy the solve state
        for row_index, row in enumerate(self.rows):
            for cell_index, cell in enumerate(row):
                copy_cell = cp.rows[row_index][cell_index]
                copy_cell.candidates = set(cell.candidates)
                copy_cell.value = int(cell.value)









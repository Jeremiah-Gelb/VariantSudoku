
from .cell import Cell

# Represents a row, column, or box
class House:
    def __init__(self, cells: set[Cell]):
        self.cells = cells
        self.intersecting_houses: set[House] = set()

        # need to fix to support non 9x9
        self.candidate_to_cell_map = {
            1: set(),
            2: set(),
            3: set(),
            4: set(),
            5: set(),
            6: set(),
            7: set(),
            8: set(),
            9: set()
        }

        for cell in cells:
            for candidate in cell.candidates:
                self.candidate_to_cell_map[candidate].add(cell)

        # bit of a hack :) Link the cell to this house, and link this house to other houses touching that cell
        for node in self.cells:
            for house in node.houses:
                if self != house:
                    self.intersecting_houses.add(house)
                    house.intersecting_houses.add(self)
            
            node.houses.add(self)

    
    def get_intersecting_cells(self, other):
        return self.cells.intersection(other.cells)
    
    def __repr__(self):
        return str(sorted(self.cells, key=lambda c: c.row_column))
    
def get_intersecting_cells(a: House, b: House):
    return a.cells.intersection(b.cells)

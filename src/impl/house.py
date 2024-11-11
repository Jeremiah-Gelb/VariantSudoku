
from .cell import Cell

# Represents a row, column, or box
class House:
    def __init__(self, cells: set[Cell]):
        self.cells = cells

        # bit of a hack :)
        for node in self.cells:
            node.houses.add(self)
    
    def get_intersecting_cells(self, other):
        return self.cells.intersection(other.cells)
    
    def __repr__(self):
        return str(sorted(self.cells, key=lambda c: c.row_column))
    
def get_intersecting_cells(a: House, b: House):
    return a.cells.intersection(b.cells)

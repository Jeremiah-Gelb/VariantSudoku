class Cell:
    def __init__(self, value=None, row_column: tuple =None, candidates = None, puzzle=None):
        self.value = value
        self.puzzle = puzzle
        if candidates:
            self.candidates = candidates
        elif value:
            self.candidates = {value}
        else:
            self.candidates = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        self.houses = set()
        self.row_column = row_column
    
    def __repr__(self):
        row, column = self.row_column
        return str([row, column, self.value, sorted(self.candidates)])
        #return str(self.value) if self.value else 'n'

    def remove_candidate(self, option):
        len_before = len(self.candidates)
        self.candidates.discard(option)
        len_after = len(self.candidates)

        if (len_before != len_after and len_after == 1):
            self.value = next(iter(self.candidates))
            if self.puzzle:
                self.puzzle.undetermined_cells.remove(self)

        if (len_before != len_after and len_after == 0):
            self.value = None

        return len_before != len_after
    
    def set_value(self, value):
        self.value = value
        self.candidates = {value}
        if self.puzzle:
            self.puzzle.undetermined_cells.remove(self)
    
    def get_intersecting_groups(self, other):
        return self.houses.intersection(other.groups)
    
    def equivalent(self, other):
        # used for testing. By default, we want to compare pointers for hash, eq, etc
        return self.value == other.value and self.candidates == other.candidates

    
def get_intersecting_groups(a, b):
    return a.groups.intersection(b.groups)
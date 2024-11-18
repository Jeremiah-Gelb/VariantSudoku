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
        #return str([row, column, self.value, sorted(self.candidates)])
        return str(self.value) if self.value else 'n'
        #return str(sorted(self.candidates))

    def remove_candidate(self, candidate):
        len_before = len(self.candidates)
        self.candidates.discard(candidate)
        len_after = len(self.candidates)

        if (len_before != len_after):
            if len_after == 1:
                # Cell value is determined
                self.value = next(iter(self.candidates))
                if self.puzzle:
                    self.puzzle.undetermined_cells.remove(self)
            
            if len_after == 0:
                raise Exception("No options for cell")
            
            for house in self.houses:
                house.candidate_to_cell_map[candidate].discard(self)

        return len_before != len_after
    
    def get_intersecting_groups(self, other):
        return self.houses.intersection(other.groups)
    
    def equivalent(self, other):
        # used for testing. By default, we want to compare pointers for hash, eq, etc
        if self.value != other.value or self.candidates != other.candidates:
            raise Exception("Cell mismatch\n" + str(self) + "\n" + str(other))
        return True
    
def get_intersecting_groups(a, b):
    return a.groups.intersection(b.groups)
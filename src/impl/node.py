class Node:
    def __init__(self, value=None, row_column=None):
        self.value = value
        self.value_options = {value} if value else {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.groups = set()
        self.row_column = row_column
    
    def __repr__(self):
        row, column = self.row_column
        return str([row, column, self.value])

    def discard_value_option(self, option):
        len_before = len(self.value_options)
        self.value_options.discard(option)
        len_after = len(self.value_options)

        if (len_before != len_after and len_after == 1):
            self.value = next(iter(self.value_options))

        if (len_before != len_after and len_after == 0):
            print("none", str(self))
            self.value = None

        return len_before != len_after
    
    def __eq__(self, other):
        return other is not None and self.row_column == other.row_column and self.value is other.value
    
    def __hash__(self):
        return hash(self.row_column)
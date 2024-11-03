from .node import Node
from .group import Group
class Puzzle:

    # assuming n by n for now. 
    def __init__(self, row_values : list[list[int]]):
        self.rows = []
        self.columns = []
        self.boxes = []

        # build rows
        for row_index, row in enumerate(row_values):
            node_list = []
            for column_index, value in enumerate(row):
                row_column = (row_index + 1, column_index + 1)
                node = Node(value, row_column) if value else Node(row_column=row_column)
                node_list.append(node)
            self.rows.append(Group(node_list))

        # build columns   
        for row_index in range(len(row_values[0])):
            node_list = []
            for column_index in range(len(row_values[0])):
                node_list.append(self.rows[column_index].nodes[row_index])
            self.columns.append(Group(node_list))

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
            node_list = []
            for column_index in range(box_boundary[2], box_boundary[3] + 1):
                for row_index in range(box_boundary[0], box_boundary[1] + 1):
                    node_list.append(self.rows[column_index].nodes[row_index])
            self.boxes.append(Group(node_list))

    def __repr__(self):
        string = "Rows: \n"
        for row in self.rows:
            string += str(row) + "\n"
        
        #string += "Columns: \n"
        #for column in self.columns:
        #    string += str(column) + "\n"
        
        #string += "Boxes: \n"
        #for box in self.boxes:
        #    string += str(box) + "\n"

        return string
    
    def __eq__(self, other):
        return self.rows == other.rows


        








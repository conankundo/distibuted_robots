import os
import csv
class moveRule:
    def __init__(self, filename):
        self.filename = filename
        self.map_matrix = self.read_csv_algo()
        self.adj_list = self.matrix_to_adjacency_list()

    def read_csv_algo(self):
        map_data = []
        with open(self.filename, "r") as data:
            data = csv.reader(data, delimiter=",")
            for row in data:
                # map_data.append(list(row))
                result_list = [item for item in row if item != '']
                map_data.append(list(result_list))
        return map_data
    
    def matrix_to_adjacency_list(self):
        rows, cols = len(self.map_matrix), len(self.map_matrix[0])
        adjacency_list = {}
        def index(row, col):
            return row * cols + col
        for row in range(rows):
            for col in range(cols):
                directions = self.map_matrix[row][col]
                current_index = index(row, col)
                adjacency_list[current_index] = []
                if 'u' in directions and row > 0:
                    adjacency_list[current_index].append((index(row - 1, col), 1))
                if 'd' in directions and row < rows - 1:
                    adjacency_list[current_index].append((index(row + 1, col), 1))
                if 'l' in directions and col > 0:
                    adjacency_list[current_index].append((index(row, col - 1), 1))
                if 'r' in directions and col < cols - 1:
                    adjacency_list[current_index].append((index(row, col + 1), 1))
        return adjacency_list
    

if __name__ == "__main__":
    filename = "map_test.csv"
    move = moveRule(filename)
    print(move.matrix_to_adjacency_list())
    # print(move.read_csv_algo())
    # print(move.read_csv_algo())
    # print(move.matrix_to_adjacency_list())
    # print(move.matrix_to_adjacency())
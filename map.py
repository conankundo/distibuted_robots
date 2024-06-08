import csv
import os

class GRAPH:
    def __init__(self, filename):
        self.filename = filename
        self.map_matrix = self.read_csv(filename)
        self.adj_list = self.create_weighted_adj_list()
        # self.map_matrix_moveRule = self.matrix_to_adjacency()
        # self.adj_list_moveRule = self.matrix_to_adjacency_list()
        
    def create_weighted_adj_list(self):
        rows, cols = len(self.map_matrix), len(self.map_matrix[0])
        adj_list = {}

        def index(row, col):
            return row * cols + col

        for row in range(rows):
            for col in range(cols):
                # weight = self.map_matrix[row][col]
                current_index = index(row, col)
                adj_list[current_index] = []
                if row > 0 and self.map_matrix[row - 1][col] < 9:
                    adj_list[current_index].append((index(row - 1, col), self.map_matrix[row-1][col]))  # Weight is 1 for adjacent nodes
                if row < rows - 1 and self.map_matrix[row + 1][col] < 9:
                    adj_list[current_index].append((index(row + 1, col), self.map_matrix[row+1][col]))
                if col > 0 and self.map_matrix[row][col - 1] < 9:
                    adj_list[current_index].append((index(row, col - 1), self.map_matrix[row][col-1]))
                if col < cols - 1 and self.map_matrix[row][col + 1] < 9:
                    adj_list[current_index].append((index(row, col + 1), self.map_matrix[row][col+1]))

                # if weight != 0:
                #     if row > 0 and self.map_matrix[row - 1][col] == 0:
                #         adj_list[current_index].append((index(row - 1, col), 1))  # Weight is 1 for adjacent nodes
                #     if row < rows - 1 and self.map_matrix[row + 1][col] == 0:
                #         adj_list[current_index].append((index(row + 1, col), 1))
                #     if col > 0 and self.map_matrix[row][col - 1] == 0:
                #         adj_list[current_index].append((index(row, col - 1), 1))
                #     if col < cols - 1 and self.map_matrix[row][col + 1] == 0:
                #         adj_list[current_index].append((index(row, col + 1), 1))
                # if weight == 2:
                #     if row > 0 and self.map_matrix[row - 1][col] == 2:
                #         adj_list[current_index].append((index(row - 1, col), 2))  # Weight is 1 for adjacent nodes
                #     if row < rows - 1 and self.map_matrix[row + 1][col] == 2:
                #         adj_list[current_index].append((index(row + 1, col), 2))
                #     if col > 0 and self.map_matrix[row][col - 1] == 2:
                #         adj_list[current_index].append((index(row, col - 1), 2))
                #     if col < cols - 1 and self.map_matrix[row][col + 1] == 2:
                #         adj_list[current_index].append((index(row, col + 1), 2))
                #     if row > 0 and self.map_matrix[row - 1][col] == 0:
                #         adj_list[current_index].append((index(row - 1, col), 1))  # Weight is 1 for adjacent nodes
                #     if row < rows - 1 and self.map_matrix[row + 1][col] == 0:
                #         adj_list[current_index].append((index(row + 1, col), 1))
                #     if col > 0 and self.map_matrix[row][col - 1] == 0:
                #         adj_list[current_index].append((index(row, col - 1), 1))
                #     if col < cols - 1 and self.map_matrix[row][col + 1] == 0:
                #         adj_list[current_index].append((index(row, col + 1), 1))
        # print(adj_list)
        return adj_list
    
    def read_csv(self,filename):
        map_data = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=",")
            for row in data:
                result_list = [int(item) if item != '' else 0 for item in row]
                # print(result_list)
                map_data.append(list(result_list))
        # print(map_data)
        return map_data

    def matrix_to_adjacency(self):
        rows, cols = len(self.map_matrix), len(self.map_matrix[0])
        adjacency_matrix = [[0] * (rows * cols) for _ in range(rows * cols)]

        def index(row, col):
            return row * cols + col

        for row in range(rows):
            for col in range(cols):
                directions = self.map_matrix[row][col]
                current_index = index(row, col)

                if 'u' in directions and row > 0:
                    adjacency_matrix[current_index][index(row - 1, col)] = 1
                    
                if 'd' in directions and row < rows - 1:
                    adjacency_matrix[current_index][index(row + 1, col)] = 1
                    
                if 'l' in directions and col > 0:
                    adjacency_matrix[current_index][index(row, col - 1)] = 1
                
                if 'r' in directions and col < cols - 1:
                    adjacency_matrix[current_index][index(row, col + 1)] = 1
                
        return adjacency_matrix

    def matrix_to_adjacency_list(self):
        adjacency_list = {}

        for i in range(len(self.map_matrix_moveRule)):
            neighbors = []
            for j in range(len(self.map_matrix_moveRule[i])):
                if self.map_matrix_moveRule[i][j] > 0:
                    neighbors.append((j, self.map_matrix_moveRule[i][j]))
            adjacency_list[i] = neighbors

        return adjacency_list

if __name__ == "__main__":
    graph = GRAPH("map2_unmark.csv")
    # print(graph.map_matrix)
    print(graph.adj_list)
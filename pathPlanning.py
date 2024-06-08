from heapq import *
from collections import deque
from draw import *

class Algorithm:
    def __init__(self, adjacency_list,map_matrix):
        self.adjacency_list = adjacency_list
        self.map_matrix = map_matrix
        

    def getCoordinate(self, index):
        rows, cols = len(self.map_matrix), len(self.map_matrix[0])
        row = index // cols
        col = index % cols  
        return row, col
    
    def heuristic_manhattan(self, node, end_node):
        # Hàm heuristic Mahattan cho A*
        x1, y1 = self.getCoordinate(node)
        x2, y2 = self.getCoordinate(end_node)
        return abs(x1 - x2) + abs(y1 - y2)

    def Astar(self, start, end):
        inf = float('inf')
        # draw = DRAW(self.map_matrix)
        # Khởi tạo mảng khoảng cách và đỉnh cha
        dist = {vertex: inf for vertex in self.adjacency_list}
        parent = {vertex: None for vertex in self.adjacency_list}

        # Đỉnh xuất phát có khoảng cách là 0
        dist[start] = 0

        # Hàng đợi ưu tiên để lựa chọn đỉnh có khoảng cách ngắn nhất
        priority_queue = [(0, start)]

        while priority_queue:
            # draw.draw_finding_path(priority_queue)
            # print(priority_queue)

            # Lấy đỉnh u có khoảng cách ngắn nhất
            cur_dist, u = heappop(priority_queue)

            # Duyệt qua các đỉnh kề của u
            for v, edge_weight in self.adjacency_list[u]:
                new_dist = cur_dist + edge_weight

                # Cập nhật khoảng cách và đỉnh cha nếu có đường đi ngắn hơn
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    parent[v] = u
                    # print(parent[v])
                    # Sử dụng hàm heuristic Mahattan để tối ưu hóa A*
                    priority = new_dist + 0.1*self.heuristic_manhattan(v, end)
                    heappush(priority_queue, (priority, v))
                    # heappush(priority_queue, (new_dist, v))

        # Truy vết đường đi ngắn nhất từ end về start
        path = []
        # print(dist[end])
        cost = dist[end]
        cur_node = end
        while cur_node is not None:
            path.insert(0, cur_node)
            cur_node = parent[cur_node]
            # print(parent) 

        return path
    


# if __name__ == "__main":

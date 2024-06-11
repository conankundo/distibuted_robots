import pygame
import numpy as np
from robot import *
from map import *
import math
import random
from pathPlanning import *
import time
from moveRule import *

class DRAW:
    def __init__(self,map_matrix):
        
        self.tile_size = 30
        self.length_x = 20
        self.length_y = 25
        self.width = self.tile_size * self.length_x
        self.height = self.tile_size * self.length_y
        pygame.init() 
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Path Planning")
        # self.num_robots = num_robots
        self.map_matrix = map_matrix
        self.centers = self.getPosition()
        self.pos_posible = []
        self.order0 = []
        self.order1 = []
    def get_rect(self,x, y):
        return x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size
    
    def getCoordinate(self, index):
        rows, cols = len(self.map_matrix), len(self.map_matrix[0])
        row = index // cols
        col = index % cols  
        return row, col
    
    def getPosition(self):
        centers = []
        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[0])):
                rect1 = pygame.Rect(self.get_rect(j,i))
                centers.append(rect1.center)  
        # center = matrix_to_array(center)
        # print(center[1])

        return centers


    def draw_robot(self,robot):
        # pygame.draw.circle(self.screen, robot.color, (int(robot.current_pos[0]), int(robot.current_pos[1])), 15)

        pygame.draw.circle(self.screen, pygame.Color("brown"), robot.current_pos, self.tile_size/3.5,10)
        font = pygame.font.Font(None, 24)
        text = font.render(str(robot.robot_id), True, pygame.Color("black"))
        self.screen.blit(text, robot.current_pos)
        # print(robot.current_pos)
        # for i in range(len(robot.trace)):
        #     pygame.draw.circle(self.screen, (255,215,0), (int(robot.trace[i][0]), int(robot.trace[i][1])), 2)
        #     if i > 0:
        #         pygame.draw.line(self.screen, (255,215,0), (int(robot.trace[i][0]), int(robot.trace[i][1])), (int(robot.trace[i-1][0]), int(robot.trace[i-1][1])), 2)
    def draw_target(self, target_pos): 
        pygame.draw.circle(self.screen, pygame.Color("red"), target_pos, self.tile_size/5, 10)

    def draw_map(self):
        rows, cols = len(self.map_matrix), len(self.map_matrix[0])
        for row in range(rows):
            for col in range(cols):
                if self.map_matrix[row][col] == 1:
                    pygame.draw.rect(self.screen, pygame.Color("white"), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                    # self.pos_posible.append(self.get_index(row, col))
                elif self.map_matrix[row][col] == 2:
                    pygame.draw.rect(self.screen, (255,0,0), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                elif self.map_matrix[row][col] == 3:
                    self.order0.append(self.get_index(row, col))
                    pygame.draw.rect(self.screen, pygame.Color("green"), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                elif self.map_matrix[row][col] == 4:
                    self.pos_posible.append(self.get_index(row, col))
                    pygame.draw.rect(self.screen, pygame.Color("white"), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                elif self.map_matrix[row][col] == 5:
                    self.order1.append(self.get_index(row, col))
                    pygame.draw.rect(self.screen, (89,140,40), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                elif self.map_matrix[row][col] == 6:
                    pygame.draw.rect(self.screen, (13,100,150), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                elif self.map_matrix[row][col] == 7:
                    pygame.draw.rect(self.screen, (78,40,150), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))        
                elif self.map_matrix[row][col] == 8:
                    pygame.draw.rect(self.screen, (0,30,50), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                elif self.map_matrix[row][col] == 9:
                    pygame.draw.rect(self.screen, pygame.Color("purple"), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))

    def drawMove(self,path,robot):
        for point in path:
            pygame.draw.circle(self.screen, pygame.Color('blue'), self.centers[point], 5)
        if(len(path) > 0):
            pygame.draw.circle(self.screen, pygame.Color('darkorange'), self.centers[path[- 1]], 10,3)
            if((path[-1] in self.order0)) or (path[-1] in self.order1):
                self.draw_target(self.centers[path[len(path) - 1]])
            else:
                pygame.draw.circle(self.screen, pygame.Color('darkorange'), self.centers[path[len(path) - 1]], 10,3)
            # pygame.draw.rect(self.screen, pygame.Color('darkorange'), self.get_rect(self.getCoordinate(path[len(path) - 1])[1], self.getCoordinate(path[len(path) - 1])[0]), 3)
            # font = pygame.font.Font(None, 24)
            # text = font.render(str(robot.robot_id), True, pygame.Color("black"))
            # self.screen.blit(text, self.centers[path[-1]])
        # for point in path:
        #     pygame.draw.circle(self.screen, pygame.Color('blue'), self.centers[point], 5)

    def get_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        row = mouse_pos[1] // self.tile_size
        col = mouse_pos[0] // self.tile_size
        return self.get_index(row, col)
    def get_robot_pos(self, pos):
        mouse_pos = pos
        row = mouse_pos[1] // self.tile_size
        col = mouse_pos[0] // self.tile_size
        return self.get_index(row, col)
    
    def get_index(self, row, col):
        return row * self.length_x + col
    
    def plot(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        
        # số hàng đã chuyển
        goods = 0
        # số lần va chạm
        collided = 0
        #469
        init_point = 13
        target_point = 17
        init_pos = self.centers[init_point]
        target_pos = self.centers[target_point]
        
        # #điểm khởi tạo
        # init_points = [301, 304, 307, 310, 313, 316]
        init_points = [6, 5, 8, 15, 25, 13, 16,18,22, 387, 384, 385, 386, 390, 388, 389, 392, 393, 394, 395, 396]
        # #điểm đích
        target_points = [226,224,229,112,178,352,115,113,110, 167, 223, 221, 286, 175, 235, 295, 43,46,49,52,55 ]
    
            
        
        init_poses = [self.centers[point] for point in init_points]
        # target_poses = [self.centers[point] for point in target_points]
        
        robots = [ROBOT(init_pos) for init_pos in init_poses]
        paths = [astar.Astar(init_point, target_point) for init_point, target_point in zip(init_points, target_points)]
        # # print(paths)
        
        for i in range(len(robots)):
            robots[i].robot_id = i
            robots[i].status = 1
            robots[i].path = paths[i]
            robots[i].centers = self.centers
            
    
        robot = ROBOT(init_pos)
        # self.map_matrix = map.map_matrix
        
        path = astar.Astar(init_point, target_point)
        print(path)
        robot.path = path
        robot.centers = self.centers
        # robot.prev_goal = path[0] - 15
        
        # Create a map
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            self.screen.fill(WHITE)
            self.draw_map()
            pygame.draw.rect(self.screen, pygame.Color('gray'),[140,630,120,60])
            font = pygame.font.Font(None, 24)
            text = font.render(f'transfered {goods}', True, pygame.Color("black"))
            self.screen.blit(text, [150,650])

            pygame.draw.rect(self.screen, pygame.Color('gray'),[360,630,120,60])
            font = pygame.font.Font(None, 24)
            text = font.render(f'collided {collided}', True, pygame.Color("black"))
            self.screen.blit(text, [380,650])
            
            # self.drawMove(path)
            position = self.get_mouse_pos()
            print(position)
            # robot.followPath(path)
            # self.draw_robot(robot)
            
            for robot in robots:
                # targett = self.pos_posible[random.randint(0, len(self.pos_posible)-1)]
                if (robot.status == 0 and robot.path == []):
                    targett = self.pos_posible[random.randint(0, len(self.pos_posible)-1)]
                    robot.path = astar.Astar(self.get_robot_pos(robot.current_pos), targett)
                    robot.status = 1
                    goods += 1
                    continue
                if (robot.status == 1 and robot.path == []):
                    # if robot.prev_order == 0:
                    #     targett = self.order1[random.randint(0, len(self.order1)-1)]
                    #     # robot.prev_order = 1
                    # else:
                    targett = self.order0[random.randint(0, len(self.order0)-1)]
                    robot.path = astar.Astar(self.get_robot_pos(robot.current_pos), targett)
                    robot.status = 0

                if (robot.status == 3):
                    # robot.trace = robot.path.copy()
                    # robot.path = []
                    robot.velocity = 0
                    # print(robot.path)
                if (robot.status == 4):
                    # robot.path = robot.path
                    robot.velocity = robot.velocity
                    if robot.path == []:
                        robot.status = 0
                    # print(robot.path)
                for other_robot in robots:
                    if robot != other_robot:
                        
                        if len(other_robot.path) > 1 and len(robot.path) > 1 and robot.path[1] == other_robot.path[1]:
                            robot.status = 3
                            robot.path_wait = robot.path
                            robot.path = []
                            other_robot.status = 3
                            other_robot.path_wait = other_robot.path
                            other_robot.path = []
                            collided +=  1
                            print(robot.robot_id, " -+-", other_robot.robot_id)
                            if other_robot.prev_goal in robot.path_wait:
                                other_robot.status = 4
                                other_robot.path = other_robot.path_wait
                                # other_robot.path_wait = []
                            elif robot.prev_goal in other_robot.path_wait:
                                robot.status = 4
                                robot.path = robot.path_wait
              
            # for robot in robots:
            #     flag = 0
            #     if robot.status == 4 and len(robot.path) > 2 or robot.status == 1 and len(robot.path) > 2:
            #         for other in robots:
            #             if other != robot:
            #                 if other.status == 3 and robot.path[0] == other.prev_goal :
            #                     flag += 1
            #                 elif other.status != 3 and len(other.path) > 2 and robot.path[0] != other.path[0]:
            #                     flag += 1
            #                 elif other.status == 0 or len(other.path) < 2:
            #                     flag += 1
            #                 else:
            #                     flag = flag
            #         if flag == (len(robots)-1):
            #             robot.status = robot.status
            #         else:
            #             robot.status = 3
            #             robot.path_wait = robot.path
            #             robot.path = []

            #     elif robot.status == 3 and len(robot.path_wait) > 2:
            #         for other in robots:
            #             if other != robot:
            #                 if other.status == 3 and robot.path_wait[0] != other.prev_goal :
            #                     flag += 1
            #                 elif other.status != 3 and len(other.path) > 2 and robot.path_wait[0] != other.path[0]:
            #                     flag += 1
            #                 elif other.status == 0 or len(other.path) < 2:
            #                     flag += 1
            #                 else:
            #                     flag = flag
            #         if flag == (len(robots) - 1):
            #             robot.status = 4
            #             robot.path = robot.path_wait
            #             robot.path_wait = []
            #         else:
            #             robot.status = robot.status
            
            for robot in robots:
                robot.followPath(robot.path)
                
                self.draw_robot(robot)
                # self.drawMove(robot.path, robot)
                # status += f"{len(robots)} ||"
                
            # print(status)
            # status = ""
            # for i in range(len(robots)):
            #     status += f"r{i}: {robots[i].status}; "
            # # print(status)
            #     print(i,"pre_goal ",robots[i].prev_goal,": path: ", robots[i].path," path_wait", robots[i].path_wait)

            # print("path: ",robots[12].path)
            # print("prev_goal",robots[12].prev_goal)
            # print(robots[0].path)
            pygame.display.flip()
            self.clock.tick(100)
            
        pygame.quit()

    

    def draw_finding_path(self, queue):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill((255, 255, 255))

            for _, xy in queue:
                # pygame.draw.rect(self.screen, pygame.Color('darkslategray'), self.get_rect(self.getCoordinate(self.centers[queue[0][1]])), 1)
                # print("canh ke")
                # print(queue[0][1])
                col = self.getCoordinate(xy)[1]
                row = self.getCoordinate(xy)[0]
                pygame.draw.rect(self.screen, pygame.Color('darkslategray'), self.get_rect(col, row), 3)
                print("end phase")        
            pygame.display.flip()
            self.clock.tick(60)
            


if __name__ == "__main__":
    
    map = moveRule("map2.csv")

    astar = Algorithm(map.adj_list, map.map_matrix)
    print(map.map_matrix)

    grid = GRAPH("map2_unmark.csv")
    draw = DRAW(grid.map_matrix)
    # path = astar.Astar(0, 115)
    # print(draw.map_matrix)

    draw.plot()
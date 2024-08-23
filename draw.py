import pygame
import numpy as np
from robot import *
from map import *
import math
import random
from pathPlanning import *
import time
from moveRule import *
from datetime import datetime


class DRAW:
    def __init__(self,map_matrix):
        self.tile_size = 700//len(map_matrix)
        self.length_x = len(map_matrix)
        self.length_y = len(map_matrix) + 10
        # self.tile_size = 19  #30 20
        # self.length_x = 38   #20 38
        # self.length_y = 43   #25 40
        self.width = self.tile_size * self.length_x
        self.height = self.tile_size * self.length_y
        self.error = []
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
        self.occupied_waypoints = []
        self.move_robot = 0
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
        if(robot.task == 0):
            pygame.draw.circle(self.screen, pygame.Color("brown"), robot.current_pos, self.tile_size/4,10)
            font = pygame.font.Font(None, 24)
            text = font.render(str(robot.robot_id), True, pygame.Color("black"))
            self.screen.blit(text, robot.current_pos)
        if(robot.task == 1):
            pygame.draw.circle(self.screen, pygame.Color("blue"), robot.current_pos, self.tile_size/4,10)
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

    def get_pos_posible(self):
        rows, cols = len(self.map_matrix), len(self.map_matrix[0])
        for row in range(rows):
            for col in range(cols):
                if self.map_matrix[row][col] == 4:
                    self.pos_posible.append(self.get_index(row, col))
    
    def get_order0(self):
        rows, cols = len(self.map_matrix), len(self.map_matrix[0])
        for row in range(rows):
            for col in range(cols):
                if self.map_matrix[row][col] == 3:
                    self.order0.append(self.get_index(row, col))

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
                    # self.order0.append(self.get_index(row, col))
                    pygame.draw.rect(self.screen, pygame.Color("green"), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                elif self.map_matrix[row][col] == 4:
                    # self.pos_posible.append(self.get_index(row, col))
                    pygame.draw.rect(self.screen, pygame.Color("white"), (col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size))
                elif self.map_matrix[row][col] == 5:
                    # self.order1.append(self.get_index(row, col))
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
        # for point in path:
        #     pygame.draw.circle(self.screen, pygame.Color('blue'), self.centers[point], 5)
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
    def get_init_and_target(self,num_robot):
        init = []
        target = []
        point = self.pos_posible.copy()
        while len(init) < num_robot:
            init.append(random.choice(point))
            point.remove(init[-1])
        point = self.pos_posible.copy()
        while len(target) < num_robot:
            ran = random.choice(point)
            if ran not in init:
                target.append(ran)
                point.remove(ran)
        return init, target

    def plot(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)

        goods = 0
        
        robots_temp = []
        self.get_pos_posible()
        self.get_order0()
        # print("length of self.pos_posible:",len(self.pos_posible))
        ## map lớn

        init_points, target_points = self.get_init_and_target(num_robot)

        ## map bé
        # all_init_points = [41, 43, 44, 46, 47, 49, 50, 52, 53, 55, 56, 58, 101, 103, 104, 106, 107, 109, 110, 112, 113, 115, 116, 118, 161, 163, 164, 166, 167, 169, 170, 172, 173, 175, 176, 178, 221, 223, 224, 226, 227, 229, 230, 232, 233, 235, 236, 238, 281, 283, 284, 286, 287, 289, 290, 292, 293, 295, 296, 298, 341, 343, 344, 346, 347, 349, 350, 352, 353, 355, 356, 358]
        # #điểm đích
        # all_target_points = [358, 356, 355, 353, 352, 350, 349, 347, 346, 344, 343, 341, 298, 296, 295, 293, 292, 290, 289, 287, 286, 284, 283, 281, 238, 236, 235, 233, 232, 230, 229, 227, 226, 224, 223, 221, 178, 176, 175, 173, 172, 170, 169, 167, 166, 164, 163, 161, 118, 116, 115, 113, 112, 110, 109, 107, 106, 104, 103, 101, 58, 56, 55, 53, 52, 50, 49, 47, 46, 44, 43, 41]
        
        

        
        

        init_poses = [self.centers[point] for point in init_points]
        robots = [ROBOT(init_pos) for init_pos in init_poses]
        paths = [astar.Astar(init_point, target_point) for init_point, target_point in zip(init_points, target_points)]
        
        ## Kiểm tra a* có chạy không
        # print("path:",paths)
        
        for i in range(len(robots)):
            robots[i].robot_id = i  
            # robots[i].prev_goal = init_points[i]
            robots[i].status = 1
            robots[i].path = paths[i]
            robots[i].centers = self.centers
        
        
        ##--------------------- Create a map
        frame =  0
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            f_report = True
            self.screen.fill(WHITE)
            self.draw_map()
            self.move_robot = 0

            robots_temp = robots.copy()
            self.occupied_waypoints = []
            
            for i,robots in enumerate(robots_temp):
                self.occupied_waypoints.append(self.get_robot_pos(robots.current_pos))
            # print(self.occupied_waypoints)

            for robot in robots_temp:
                if robot.task == 0 and robot.path == []:
                    targett = self.order0[random.randint(0, len(self.order0)-1)]
                    robot.path = astar.Astar(self.get_robot_pos(robot.current_pos), targett)
                    robot.task = 1
                    goods += 1
                elif robot.task == 1 and robot.path == []:
                    targett = self.pos_posible[random.randint(0, len(self.pos_posible)-1)]
                    robot.path = astar.Astar(self.get_robot_pos(robot.current_pos), targett)
                    robot.task = 0

            for robot in robots_temp:
                if robot.status == 3:
                    can_continue = True
                    for other_robot in robots_temp:
                        if robot.robot_id != other_robot.robot_id and robot.get_next_waypoint() == other_robot.get_next_waypoint():
                            if(np.linalg.norm(np.array(robot.current_pos) - np.array(other_robot.current_pos)) <  self.tile_size/2):
                                can_continue = False
                                # print(robot.get_next_waypoint())
                                # break
                    if can_continue:
                        robot.status = 1

            for i, robot in enumerate(robots_temp):
                for j, other_robot in enumerate(robots_temp):
                    if i != j and robot.get_next_waypoint() == other_robot.get_next_waypoint():
                        if random.randint(0,1) == 1:
                            other_robot.status = 3
                        else:
                            robot.status = 3

            for i,robot in enumerate(robots_temp):
                for j, point in enumerate(self.occupied_waypoints):
                    if i!=j and robot.get_next_waypoint() == point:
                        robot.status = 3
                        # break 

            robots = robots_temp.copy()
            robots_temp = []

            for robot in robots:
                if robot.status != 3:
                    robot.followPath(robot.path, self.occupied_waypoints, len(self.map_matrix))  # map = square --> length == width
                    self.move_robot += 1
                # self.draw_robot(robot)
                # self.drawMove(robot.path, robot)
            

            map2checkInside = pygame.Rect(0, 0, self.width, self.height)
            for robot in robots:
                robot2check = pygame.Rect(robot.current_pos[0], robot.current_pos[1], 2,2)
                # pos = pygame.mouse.get_pos()
                # robot2check = pygame.Rect(pos[0], pos[1], 2,2)
                if not map2checkInside.contains(robot2check) and not robot.robot_id in self.error:
                    self.error.append(robot.robot_id)
                    

                # if robot.get_next_waypoint() is not None:
                #     self.draw_target(self.centers[robot.get_next_waypoint()])
            

            

            #-------------------------------
            # pos = pygame.mouse.get_pos()
            # print(self.get_robot_pos(pos))
            ##-------------------------------
            panel_pos = [self.width*0.1,self.height*0.9]  
            panel_size = [120,30]
            # panel_pos = [140,630] #map bé
            ##------------------------------## Draw transfer table noti
            pygame.draw.rect(self.screen, pygame.Color('gray'),[panel_pos[0],panel_pos[1],panel_size[0], panel_size[1]])
            
            font = pygame.font.Font(None, 18)
            frame 
            frame += 1
            # timer = frame // 120
            c = datetime.now()
            
            output_text = (c.strftime('%H:%M:%S') +
                           f'||Sec counter: {frame//120}' +
                           f'||Transfered: {goods}' +
                           f'||NumRobot: {len(robots)}' + 
                           f'||Input-Output: {len(self.order0)}-{len(self.pos_posible)}' + 
                           f'||Moving: {self.move_robot}'+
                           f'||Error: {self.error}')
            text = font.render(output_text,True, pygame.Color("black"))
            self.screen.blit(text, [panel_pos[0]+10,panel_pos[1]+10])
            
            ##------------------------------
            # if (timer % 120 == 0 and timer > 120) :
            if (frame >=2*120 and frame % (9*120) == 0 and f_report) :
                print(output_text)
                f = open("report.txt","a")
                f.write(output_text + '\n')
                f.close()
                f_report = False
            
            pygame.display.flip()
            self.clock.tick(120)
            # print("robots[0].target_pos:",robots[0].target_pos)    # đoạn này in ra để check thông số xem có gì lỗi ko
            # print("robots[0].current_pos:",robots[0].current_pos) 
            # print("robots[0].veloc:",robots[0].velocity)   
        pygame.quit()

    

    
            


if __name__ == "__main__":
    num_robot = 150
    head = "map4"
    map = moveRule(head + ".csv")
    astar = Algorithm(map.adj_list, map.map_matrix)
    grid = GRAPH(head +"_unmark.csv")
    draw = DRAW(grid.map_matrix)
    # path_test = astar.Astar(0, 115)
    # print("path_test 0-->115:",path_test)
    # print(draw.map_matrix)
    f = open("report.txt","a")
    f.write('\n' + 
            '------------------------------' +
            f'{datetime.now().strftime('%Y-%m-%d | %H:%M:%S')}'+
            '-----------------------------' '\n')
    f.close()
    draw.plot()
    

    
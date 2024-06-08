import numpy as np
import pygame
from map import *

class ROBOT:
    def __init__(self,initial_pos):
        self.robot_id = 0
        self.target_pos = np.array([0,0])
        self.current_pos = initial_pos
        self.velocity = np.zeros(2).astype(int)
        self.color = (200, 0, 0)
        self.trace = []    ## vết đường đã đi
        self.path = []      ## đường đi
        self.path_wait = []
        self.centers = []
        self.prev_goal = 0
        self.status = 0
        self.prev_order = 0
        # self.map = map
    
    def updatePose(self):
        if np.linalg.norm(self.current_pos - self.target_pos) < 0.01:
            self.velocity = np.zeros(2)
        else:
            self.current_pos = self.current_pos + self.velocity
            self.trace.append(self.current_pos)

    def movetoGoal(self,goal, pre_goal):
        if (goal - pre_goal) == 1:
            self.velocity = np.array([1,0])
        elif (goal - pre_goal) == -1:
            self.velocity = np.array([-1,0])
        elif (goal - pre_goal) == 20:
            self.velocity = np.array([0,1])
        elif (goal - pre_goal) == -20:
            self.velocity = np.array([0,-1])
        # else:
        #     self.velocity = np.array([0,-1])
    
    def followPath(self, path):
        if path != []:
            self.movetoGoal(path[0], self.prev_goal)
            # self.movetoGoal(path[1], path[0] )
            self.target_pos = np.array(self.centers[path[0]])
            self.updatePose()
            # print(np.linalg.norm(self.current_pos - np.array(self.centers[path[0]])))
            if np.linalg.norm(self.current_pos - np.array(self.centers[path[0]])) < 1.5:
                self.prev_goal = path[0]
                path.pop(0)
                # print(path[0], init_point)
            if path == []:
                # break
                pass
        return self.current_pos
    
    def check_range(self, robots):
        for robot in robots:
            if robot != self:
                print(np.linalg.norm(np.array(self.current_pos) - np.array(robot.current_pos)))
                if np.linalg.norm(np.array(self.current_pos) - np.array(robot.current_pos)) < 250:
                    if np.linalg.norm(np.array(self.target_pos) - np.array(self.current_pos)) < np.linalg.norm(np.array(robot.target_pos) - np.array(robot.current_pos)):
                        self.velocity = np.zeros(2)
                    
        

    
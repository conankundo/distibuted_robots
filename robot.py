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
        self.trace = []
        self.path = []
        self.centers = []
        self.prev_goal = 0
        self.status = 0
        self.prev_order = 0
        self.next_goal = 0
        self.prev_status = 0
        self.task = 0
        # self.map = map
    
    def updatePose(self):
        if np.linalg.norm(self.current_pos - self.target_pos) < 0.01:
            self.velocity = np.zeros(2)
        else:
            self.current_pos = self.current_pos + self.velocity
            # self.trace.append(self.current_pos)

    def movetoGoal(self,goal, pre_goal, range_y):
        if (goal - pre_goal) == 1:
            self.velocity = np.array([2,0])
        elif (goal - pre_goal) == -1:
            self.velocity = np.array([-2,0])
        elif (goal - pre_goal) == range_y:
            self.velocity = np.array([0,2])
        elif (goal - pre_goal) == -range_y:
            self.velocity = np.array([0,-2])
        # else:
        #     self.velocity = np.array([0,-1])
    
    def followPath(self, path, occupied, range_y):
        if path != []:
            # for i, waypoint in enumerate(occupied):
            #     if self.robot_id != i and path[0] == waypoint:
            #         self.velocity = np.zeros(2)
            #         break

            self.movetoGoal(path[0], self.prev_goal, range_y)
            # if len(path) > 1:
            #     self.next_goal = path[1]
                
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
                    
        

    def get_next_waypoint(self):
        if self.path:
            return self.path[0]
        return None

    def is_colliding(self, other_robot):
        next_waypoint = self.get_next_waypoint()
        other_next_waypoint = other_robot.get_next_waypoint()
        if next_waypoint and other_next_waypoint:
            if next_waypoint == other_next_waypoint:
                return True
        return False
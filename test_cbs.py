import numpy as np
import pygame
import heapq

class ROBOT:
    def __init__(self, robot_id, initial_pos, color):
        self.robot_id = robot_id
        self.target_pos = np.array([0,0])
        self.current_pos = np.array(initial_pos)
        self.velocity = np.zeros(2).astype(int)
        self.color = color
        self.trace = []
        self.path = []
        self.centers = []
        self.prev_goal = initial_pos

    def updatePose(self):
        if np.linalg.norm(self.current_pos - self.target_pos) < 0.01:
            self.velocity = np.zeros(2)
        else:
            self.current_pos = self.current_pos + self.velocity
            self.trace.append(self.current_pos)

    def movetoGoal(self, goal, pre_goal):
        if (goal - pre_goal)[0] == 1:
            self.velocity = np.array([1, 0])
        elif (goal - pre_goal)[0] == -1:
            self.velocity = np.array([-1, 0])
        elif (goal - pre_goal)[1] == 1:
            self.velocity = np.array([0, 1])
        elif (goal - pre_goal)[1] == -1:
            self.velocity = np.array([0, -1])

    def followPath(self):
        if self.path:
            self.movetoGoal(self.path[0], self.prev_goal)
            self.target_pos = np.array(self.centers[self.path[0]])
            self.updatePose()
            if np.linalg.norm(self.current_pos - np.array(self.centers[self.path[0]])) < 1.5:
                self.prev_goal = self.path[0]
                self.path.pop(0)
        return self.current_pos

    def setPath(self, path, centers):
        self.path = path
        self.centers = centers

def draw_grid():
    for x in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_SIZE))
    for y in range(0, SCREEN_SIZE, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_SIZE, y))

def draw_robot(robot):
    pygame.draw.circle(screen, robot.color, (robot.current_pos[0] * CELL_SIZE + CELL_SIZE // 2, robot.current_pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

# A* algorithm
def a_star(start, goal, constraints):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            tentative_g_score = g_score[current] + 1

            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                if (neighbor, tentative_g_score) in constraints:
                    continue

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None

# Find conflicts
def find_conflict(paths):
    max_length = max(len(path) for path in paths)
    for t in range(max_length):
        positions = {}
        for i, path in enumerate(paths):
            pos = path[min(t, len(path) - 1)]
            if pos in positions:
                return (positions[pos], i, pos, t)
            positions[pos] = i
    return None

# CBS algorithm
def cbs(start_positions, goal_positions):
    class Node:
        def __init__(self, constraints, paths):
            self.constraints = constraints
            self.paths = paths
            self.cost = sum(len(path) for path in paths)
        def __lt__(self, other):
            return self.cost < other.cost

    def low_level_search(agent, constraints):
        return a_star(start_positions[agent], goal_positions[agent], constraints)

    root = Node(constraints=[], paths=[])
    for i in range(len(start_positions)):
        path = low_level_search(i, root.constraints)
        if path is None:
            return None
        root.paths.append(path)

    open_list = []
    heapq.heappush(open_list, root)

    while open_list:
        node = heapq.heappop(open_list)
        conflict = find_conflict(node.paths)
        if conflict is None:
            return node.paths

        agent1, agent2, position, time = conflict
        for agent in [agent1, agent2]:
            new_constraints = node.constraints.copy()
            new_constraints.append((position, time))

            new_paths = node.paths.copy()
            new_paths[agent] = low_level_search(agent, new_constraints)
            if new_paths[agent] is not None:
                new_node = Node(new_constraints, new_paths)
                heapq.heappush(open_list, new_node)

    return None

# Constants
SCREEN_SIZE = 600
GRID_SIZE = 10
CELL_SIZE = SCREEN_SIZE // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Start and goal positions for two robots
start_positions = [(0, 0), (9, 9)]
goal_positions = [(9, 0), (0, 9)]

# Create pygame window
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("CBS Pathfinding")

# Run CBS to find paths
paths = cbs(start_positions, goal_positions)

# Create robots
robot1 = ROBOT(1, start_positions[0], BLUE)
robot2 = ROBOT(2, start_positions[1], RED)
robots = [robot1, robot2]

# Set paths for robots
if paths:
    robot1.setPath(paths[0], {i: pos for i, pos in enumerate(paths[0])})
    robot2.setPath(paths[1], {i: pos for i, pos in enumerate(paths[1])})

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    draw_grid()

    # Update and draw robots
    for robot in robots:
        robot.followPath()
        draw_robot(robot)

    pygame.display.flip()

pygame.quit()

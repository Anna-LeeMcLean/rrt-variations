import math
import random

# 3rd party dependencies
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RRT():
    start: tuple
    goal: tuple
    tree: list[tuple] = []
    step_size_mm: float
    goal_range: float
    workspace_length_mm : int = 500
    workspace_height_mm : int = 500
    _success: bool = False

    def __init__(self, start:tuple, goal:tuple, step_size_mm: float = 20.0) -> None:
        self.start = start
        self.goal = goal
        self.step_size_mm = step_size_mm

        # add start point to tree
        self.tree.append(self.start)
        plt.figure()

        # visulize start and end nodes
        plt.plot(self.start[0], self.start[1], "go")
        plt.plot(self.goal[0], self.goal[1], "ro")

    def create(self):
        if not self._success:
            new_sample = self._sample_space()
            nearest_neighbour = self._find_nearest_neighbour(new_sample)
            print("adding to tree")
            new_node = self._add_node_to_tree(new_sample, nearest_neighbour)
            plt.plot(new_node[0], new_node[1], "bo", linewidth=0.5)
            self._connect_to_parent(new_node, nearest_neighbour)
            self._check_if_at_goal(new_node)
    
    def _sample_space(self) -> tuple:
        sample_x = random.uniform(0, self.workspace_length_mm)
        sample_y = random.uniform(0, self.workspace_height_mm)

        return (sample_x, sample_y)
    
    def _find_nearest_neighbour(self, sample: tuple) -> tuple:

        min_distance = math.inf
        nearest_neighbour = None

        for node in self.tree:
            distance = math.dist(node, sample)
            if distance < min_distance:
                min_distance = distance
                nearest_neighbour = node

        return nearest_neighbour
    
    def _add_node_to_tree(self, sample: tuple, nearest_neighbour: tuple) -> tuple:

        x_diff = (sample[0] - nearest_neighbour[0])/self.step_size_mm
        y_diff = (sample[1] - nearest_neighbour[1])/self.step_size_mm

        new_node_x = nearest_neighbour[0] + x_diff
        new_node_y = nearest_neighbour[1] + y_diff

        new_node = (new_node_x, new_node_y)
        self.tree.append(new_node)

        return new_node
    
    def _connect_to_parent(self, new_node: tuple, nearest_neighbour: tuple) -> None:

        x = [nearest_neighbour[0], new_node[0]]
        y = [nearest_neighbour[1], new_node[1]]
        plt.plot(x, y, 'gray', linestyle='--')
    
    def _check_if_at_goal(self, new_node: tuple) -> None:
        # TODO: can make the process faster if you don't do this after every sample created. 
        # Maybe after every 5 samples? Maybe a function of the size of the workspace.

        if math.dist(self.goal, new_node) <= self.step_size_mm:
            # add goal node to tree
            self.tree.append(self.goal)
            self._connect_to_parent(new_node, self.goal)
            self._success = True


start1 = (10.0, 10.0)
end1 = (100.0, 100.0)
rrt = RRT(start=start1, goal=end1)
def func(frames):
    rrt.create()

# initialize animation for visualization
animation = FuncAnimation(plt.gcf(), func)
plt.show()
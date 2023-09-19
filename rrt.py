# Python imports
import math
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Anna-Lee's imports
from node import Node

class RRT():
    start: Node
    goal: Node
    tree: list[Node] = []
    step_size_mm: float
    goal_range: float
    workspace_length_mm : int = 500
    workspace_height_mm : int = 500
    _success: bool = False

    def __init__(self, start:Node, goal:Node, step_size_mm: float = 20.0) -> None:
        self.start = start
        self.goal = goal
        self.step_size_mm = step_size_mm

        # add start point to tree
        self.tree.append(self.start)
        plt.figure()

        # visulize start and end nodes
        plt.plot(self.start.x, self.start.y, "go")
        plt.plot(self.goal.x, self.goal.y, "ro")

    def create(self):
        if not self._success:
            new_sample = self._sample_space()
            nearest_neighbour = self._find_nearest_neighbour(new_sample)
            print("adding to tree")
            new_node = self._add_node_to_tree(new_sample, nearest_neighbour)
            plt.plot(new_node.x, new_node.y, "bo", linewidth=0.5)
            self._connect_to_parent(new_node)
            at_goal = self._check_if_at_goal(new_node)

            if at_goal:
                self._return_path()
    
    def _sample_space(self) -> Node:
        sample_x = random.uniform(0, self.workspace_length_mm)
        sample_y = random.uniform(0, self.workspace_height_mm)
        sample = Node(x=sample_x, y=sample_y)

        return sample
    
    def _find_nearest_neighbour(self, sample: Node) -> Node:

        min_distance = math.inf
        nearest_neighbour = None

        for node in self.tree:
            distance = node.euclidean_dist(sample)
            if distance < min_distance:
                min_distance = distance
                nearest_neighbour = node

        return nearest_neighbour
    
    def _add_node_to_tree(self, sample: Node, nearest_neighbour: Node) -> Node:

        distance = sample.euclidean_dist(nearest_neighbour)
        scale_factor = distance/self.step_size_mm

        x_diff = (sample.x - nearest_neighbour.x)/scale_factor
        y_diff = (sample.y - nearest_neighbour.y)/scale_factor

        new_node_x = nearest_neighbour.x + x_diff
        new_node_y = nearest_neighbour.y + y_diff

        new_node = Node(x=new_node_x, y=new_node_y)
        self.tree.append(new_node)
        new_node.parent = nearest_neighbour
        nearest_neighbour.child = new_node

        return new_node
    
    def _connect_to_parent(self, new_node: Node) -> None:

        x = [new_node.parent.x, new_node.x]
        y = [new_node.parent.y, new_node.y]
        plt.plot(x, y, 'gray', linestyle='--')
    
    def _check_if_at_goal(self, new_node: Node) -> bool:
        # TODO: can make the process faster if you don't do this after every sample created. 
        # Maybe after every 5 samples? Maybe a function of the size of the workspace.

        if self.goal.euclidean_dist(new_node) <= self.step_size_mm:
            # add goal node to tree
            self.tree.append(self.goal)
            self.goal.parent = new_node
            new_node.child = self.goal
            self._connect_to_parent(self.goal)
            self._success = True
            print("Found path to goal!")

            return True
        
        return False
    
    def _return_path(self):

        current_node = self.goal
        path = [current_node]

        while current_node.parent != None:
            path.append(current_node.parent)
            current_node = current_node.parent

        path_x = [node.x for node in path]
        path_y = [node.y for node in path]

        plt.plot(path_x, path_y, 'yellow')


start1 = Node(x=10.0, y=10.0)
end1 = Node(x=100.0, y=100.0)
rrt = RRT(start=start1, goal=end1)
def func(frames):
    rrt.create()

# initialize animation for visualization
animation = FuncAnimation(plt.gcf(), func)
plt.show()
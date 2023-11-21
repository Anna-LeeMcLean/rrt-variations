import math
import matplotlib.pyplot as plt

class Node():

    def __init__(self, x: float, y: float, parent = None, child = None) -> None:
        self.x = x
        self.y = y
        self.parent = parent
        self.child = child
        self.cost = 0.0                     # total cost from start node to this node
    
    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}"

    def euclidean_dist(self, other_node) -> float:
        node_tuple = (self.x, self.y)
        other_node_tuple = (other_node.x, other_node.y)
        
        return math.dist(node_tuple, other_node_tuple)


class RewireNode(Node):


    def __init__(self, x: float, y: float, parent=None, child=None) -> None:
        super().__init__(x, y, parent, child)

        self._cost_difference = 0.0          # difference in cost between neighbour node in path 

    @property
    def cost_difference(self):
        return self._cost_difference
    
    @cost_difference.setter
    def cost_difference(self, value: float):
        self._cost_difference = value


class Path():

    def __init__(self) -> None:
        self.nodes : list[Node] = []
        self.line : list = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def plot(self):
        path_x = [node.x for node in self.nodes]
        path_y = [node.y for node in self.nodes]

        if self.line:
            l = self.line.pop(0)
            l.remove()

        self.line = plt.plot(path_x, path_y, 'yellow')
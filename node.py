import math

class Node():

    def __init__(self, x: float, y: float, parent = None, child = None) -> None:
        self.x = x
        self.y = y
        self.parent = parent
        self.child = child
        self.cost = 0.0

    def euclidean_dist(self, other_node) -> float:
        node_tuple = (self.x, self.y)
        other_node_tuple = (other_node.x, other_node.y)
        
        return math.dist(node_tuple, other_node_tuple)

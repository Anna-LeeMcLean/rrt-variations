from utils.node import Node
import matplotlib.pyplot as plt

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

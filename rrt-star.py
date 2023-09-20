from node import Node
from rrt import RRT

class RRTStar(RRT):

    def __init__(self, start: Node, goal: Node, step_size_mm: float = 20, neighbours: int = 5) -> None:
        super().__init__(start, goal, step_size_mm)

        self.neighbours = neighbours

    def rewire_path(self):
        '''
        This function tries to shorten the overall distance from the start node to the goal node 
        by rewiring the path edges.

        1. add sample to workspace
              - choose random node in the path and add random x,y values to the node's coords. 
                random value will be +/- step_size
        2. get self.neighbours closest neighbours
        3. for each neighbour, if the cost to the neighbour's parent is less through the 
           random sample than it currently is, rewire the path. 
        4. rewire the path
              - set the neighbours child and parent nodes to the sample's child and parent nodes

        5. remove previous two edges and redraw new edges to child/parent

        Number of samples to add = Number of nodes in path * 10?
        '''


        pass

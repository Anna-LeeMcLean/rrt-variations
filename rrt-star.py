# Python native dependencies
import copy
import math
import random

# Anna-Lee's imports
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

        1. create a random sample in the workspace that is close to a node in the path
              - choose random node in the path and add random x,y values to the node's coords. 
                random value will be +/- step_size

        Let self.neighbours = n

        2. get n closest neighbours
        3. for each neighbour, if the cost to the neighbour's parent is less through the 
           random sample than it currently is, rewire the path. 
        4. rewire the path
              - set the neighbours child and parent nodes to the sample's child and parent nodes

        5. remove previous two edges and redraw new edges to child/parent

        Number of samples to add = Number of nodes in path * 100?
        '''

        number_of_nodes_to_add = len(self.path_to_goal) * 100
        count = 0

        path = self.path_to_goal[1:-1]      # remove start and goal nodes from path

        while count != number_of_nodes_to_add:
            # Step 1: create a random sample in the workspace that is close to a node in the path
            node = random.choice(path)       # choose a random node in the path (excluding the start and goal nodes)

            random_x = random.uniform(-self.step_size_mm, self.step_size_mm)
            random_y = random.uniform(-self.step_size_mm, self.step_size_mm)

            random_node = Node(x=node.x + random_x, y=node.y + random_y)

            # Step 2: get n closest neighbours to the random node

            # Initialize a list which will hold the n smallest distances between the random sample and neighbour nodes
            distances = [math.inf for _ in range(self.neighbours)]   
            # Initalize a list which will hold the nearest neighbours   
            nodes = [None for _ in range(self.neighbours)]

            for path_node in path:
                # check distance between path_node and random node
                dist = random_node.euclidean_dist(path_node)
                max_dist = max(distances)                   # get the current largest distances in the distances list

                if dist < max_dist:
                    index_of_max_distance = distances.index(max_dist)
                    distances[index_of_max_distance] = dist     # replace current largest distance with new distance
                    nodes[index_of_max_distance] = path_node    # replace corresponding node with new node

            # The nodes list now holds the n closest path nodes to our random sample. These are the random samples neighbours.
            # The distances list holds the corresponding n smallest distances.

            # Step 3: for each neighbour, if the cost to the neighbour's parent is less through the 
            # random sample than it currently is, rewire the path.
            random_nodes = [copy.copy(random_node) for _ in range(self.neighbours)]     # every neighbour has their own copy of the random node
            cost_differences = [math.inf]*self.neighbours

            for neighbour in nodes:
                index_of_neighbour = nodes.index(neighbour)
                _node = random_nodes[index_of_neighbour]        # get copy of random sample at the same index as the neighboure node
                original_child_cost = neighbour.child.cost

                _node.parent = neighbour.parent
                _node.child = neighbour.child
                _node.cost = _node.parent.cost + _node.euclidean_dist(_node.parent)
                new_child_cost = _node.cost + _node.euclidean_dist(_node.child)

                if new_child_cost < original_child_cost:
                    cost_differences[index_of_neighbour] = original_child_cost - new_child_cost

            # find the samllest cost_difference and get corresponding neighbour
            smallest_diff = min(cost_differences)
            idx = cost_differences.index(smallest_diff)
            best_neighbour = nodes.index(idx)


            # Step 5: Create new path
                


                    

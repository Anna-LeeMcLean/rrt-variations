# Python native dependencies
import copy
import math
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Anna-Lee's imports
from node import Node, RewireNode
from rrt import RRT

class RRTStar():

    _success: bool = False

    def __init__(self, start: Node, goal: Node, step_size_mm: float = 20, neighbours: int = 3) -> None:
        self.rrt = RRT(start, goal, step_size_mm)

        self.neighbours = neighbours
        

    def create(self):
        if not self._success:
            self.rrt.create()

            if self.rrt._success:
                print("rewiring")
                self.rewire_path()
                self._success = True

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
        5. replace current node in path with random sample

        6. remove previous two edges and redraw new edges to child/parent

        Number of samples to add = Number of nodes in path * 100?
        '''

        number_of_nodes_to_add = len(self.rrt.path_to_goal)
        # number_of_nodes_to_add = 2
        count = 0

        path = self.rrt.path_to_goal[1:-1]      # remove start and goal nodes from path

        while count != number_of_nodes_to_add:
            # Step 1: create a random sample in the workspace that is close to a node in the path
            node = random.choice(path)       # choose a node in the path (excluding the start and goal nodes)

            random_x = random.uniform(-self.rrt.step_size_mm, self.rrt.step_size_mm)
            random_y = random.uniform(-self.rrt.step_size_mm, self.rrt.step_size_mm)

            rewire_node = RewireNode(x=node.x + random_x, y=node.y + random_y)
            plt.plot(rewire_node.x, rewire_node.y, "rx")
            # Step 2: get n closest neighbours to the random node

            # Initialize a list which will hold the n smallest distances between the random sample and neighbour nodes
            distances = [math.inf for _ in range(self.neighbours)]   
            # Initalize a list which will hold the nearest neighbours   
            neighbour_nodes = [None for _ in range(self.neighbours)]

            for path_node in path:
                # check distance between path_node and random node
                dist = rewire_node.euclidean_dist(path_node)
                max_dist = max(distances)                   # get the current largest distances in the distances list

                if dist < max_dist:
                    index_of_max_distance = distances.index(max_dist)
                    distances[index_of_max_distance] = dist     # replace current largest distance with new distance
                    neighbour_nodes[index_of_max_distance] = path_node    # replace corresponding node with new node

            # The nodes list now holds the n closest path nodes to our random sample. These are the random samples neighbours.
            # The distances list holds the corresponding n smallest distances.

            # Step 3: for each neighbour, if the cost to the neighbour's parent is less through the 
            # random sample than it currently is, rewire the path.
            largest_cost_difference = -math.inf
            best_rewire_node = None
            corresponding_neighbour_node = None

            for neighbour in neighbour_nodes:
                rewire_node_copy = copy.copy(rewire_node)
                original_child_cost = neighbour.child.cost

                rewire_node_copy.parent = neighbour.parent
                rewire_node_copy.child = neighbour.child
                rewire_node_copy.cost = rewire_node_copy.parent.cost + rewire_node_copy.euclidean_dist(rewire_node_copy.parent)
                new_child_cost = rewire_node_copy.cost + rewire_node_copy.euclidean_dist(rewire_node_copy.child)

                if new_child_cost < original_child_cost:
                    rewire_node_copy.cost_difference = original_child_cost - new_child_cost

                    if rewire_node_copy.cost_difference > largest_cost_difference:     
                        largest_cost_difference = rewire_node_copy.cost_difference
                        best_rewire_node = rewire_node_copy
                        corresponding_neighbour_node = neighbour

            if best_rewire_node is not None:
                # Step 5: replace neighbour with random sample.
                best_rewire_node.child.parent = best_rewire_node
                best_rewire_node.parent.child = best_rewire_node
                best_rewire_node.child.cost = new_child_cost
                
                for path_node in path:
                    if path_node == corresponding_neighbour_node:
                        path_node_idx = path.index(path_node)
                        path[path_node_idx] = best_rewire_node

                # Step 6: Create new path
                self.rrt._connect_to_parent(best_rewire_node, 'red')
                self.rrt._connect_to_parent(best_rewire_node.child, 'red')

            count+=1


start1 = Node(x=10.0, y=10.0)
end1 = Node(x=100.0, y=100.0)
rrt_star = RRTStar(start=start1, goal=end1)
def func(frames):
    rrt_star.create()

# initialize animation for visualization
animation = FuncAnimation(plt.gcf(), func)
plt.show()
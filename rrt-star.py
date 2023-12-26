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

    def __init__(self, start: Node, goal: Node, step_size_mm: float = 20, 
                 neighbours: int = 3, number_of_added_nodes = 50) -> None:
        
        self.rrt = RRT(start, goal, step_size_mm)

        self.neighbours = neighbours
        self.number_of_added_nodes = number_of_added_nodes
        

    def create(self):
        if not self._success:
            self.rrt.create()

            if self.rrt.success:
                print("rewiring")
                self.rewire_path()
                self._success = True

    def visualize(self):
        def func(frames):
            self.create()

        # initialize animation for visualization
        animation = FuncAnimation(plt.gcf(), func)
        plt.show()

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

        '''

        count = 0

        while count != self.number_of_added_nodes:

            path = self.rrt.path_to_goal.nodes[1:-1]      # remove start and goal nodes from path
            node = random.choice(path)       # choose a node in the path (excluding the start and goal nodes)

            # Step 1: create a random sample in the workspace that is close to a node in the path
            rewire_node = self.sample_space(node=node)

            # Step 2: get n closest neighbours to the random node
            neighbour_nodes = self.find_n_nearest_neighbours(rewire_node, path)
            
            # Step 3: for each neighbour, if the cost to the neighbour's parent is less through the 
            # random sample than it currently is, rewire the path.
            updated_rewire_node, best_neighbour_option, new_child_cost = self.find_best_rewire_option(neighbour_nodes, rewire_node)

            if updated_rewire_node is not None:
                # Step 5: replace neighbour with random sample.
                updated_rewire_node.child.parent = updated_rewire_node
                updated_rewire_node.parent.child = updated_rewire_node
                self.update_child_costs(updated_rewire_node, new_child_cost)
                rrt_path = self.rrt.path_to_goal.nodes

                for path_node in rrt_path:
                    if path_node == best_neighbour_option:
                        path_node_idx = rrt_path.index(path_node)
                        rrt_path[path_node_idx] = updated_rewire_node
                        break

                # Step 6: Create new path
                self.rrt.path_to_goal.plot()

            count+=1

    def sample_space(self, node) -> Node:

        random_x = random.uniform(-self.rrt.step_size_mm, self.rrt.step_size_mm)
        random_y = random.uniform(-self.rrt.step_size_mm, self.rrt.step_size_mm)

        rewire_node = RewireNode(x=node.x + random_x, y=node.y + random_y)
        plt.plot(rewire_node.x, rewire_node.y, "rx")

        return rewire_node

    def find_n_nearest_neighbours(self, rewire_node: Node, path: list[Node]) -> list[Node]:
            
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
        
        return neighbour_nodes
    
    def find_best_rewire_option(self, neighbour_nodes: list[Node], rewire_node):
        largest_cost_difference = -math.inf
        best_rewire_node = None
        corresponding_neighbour_node = None

        for neighbour in neighbour_nodes:
            rewire_node_copy = copy.copy(rewire_node)
            original_child_cost = neighbour.child.cost

            rewire_node_copy.parent = neighbour.parent
            rewire_node_copy.child = neighbour.child
            rewire_node_copy_cost = rewire_node_copy.parent.cost + rewire_node_copy.euclidean_dist(rewire_node_copy.parent)
            rewire_node_copy.cost = rewire_node_copy_cost
            new_child_cost = rewire_node_copy.cost + rewire_node_copy.euclidean_dist(rewire_node_copy.child)

            if new_child_cost < original_child_cost:
                rewire_node_copy.cost_difference = original_child_cost - new_child_cost

                if rewire_node_copy.cost_difference > largest_cost_difference:     
                    largest_cost_difference = rewire_node_copy.cost_difference
                    best_rewire_node = rewire_node_copy
                    corresponding_neighbour_node = neighbour

        return best_rewire_node, corresponding_neighbour_node, new_child_cost
    
    def update_child_costs(self, rewire_node: Node, new_child_cost: float) -> None:

        current_child = rewire_node.child

        while True:
            current_child.cost = new_child_cost
            if current_child.child != None:
                new_child_cost += current_child.euclidean_dist(current_child.child)
                current_child = current_child.child
            else:
                break


start1 = Node(x=10.0, y=10.0)
end1 = Node(x=100.0, y=100.0)
rrt_star = RRTStar(start=start1, goal=end1, neighbours=4, number_of_added_nodes=200)
rrt_star.visualize()

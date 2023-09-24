# rrt-variations

TODO:

1. Make NeghbourNode class that inherits from Node class. This class will store the distance to another node, the cost difference and the instance of the other node?

2. Make an edge attribute for the Node class. An edge is a line between the node and its parent. Only the start node doesn't have an edge.

3. Make animation a function of the class so I don't need to comment out code in the rrt.py file to run the rrt_star.py file.

4. Make __eq__ function for the Node class (or just use a dataclass)

5. Doc strings for all methods

6. Break up rewire method into saller methods.
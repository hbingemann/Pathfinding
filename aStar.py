# to calculate distance:
# -- 1.4 (sqrt of 2) for diagonal, 1 for straight

# g cost = distance from start node through all previously explored nodes
# h cost = distance from end node
# f cost = g cost + h cost

# look for lowest f cost of all surrounding nodes
# if equal f cost look for lowest h cost
# if equal h cost pick a random one of them at random

# -------------------------------------------------------------
# pseudo-code:

# open list (nodes to be evaluated (green nodes)), we will call this green nodes
# closed list (nodes already evaluated (red nodes)), we will call this red nodes
# add the starting node to open list

# while loop
#
#   current = node from green nodes with lowest f_cost (or h_cost if f_cost is equal)
#   remove current from green nodes
#   add current to red nodes
#
#   if current is the end node:
#       return (leave the loop)
#
#   for each neighbour of the current node
#
#       if neighbour is not traversable OR neighbor is in red nodes
#           go to next neighbor (continue)
#
#       if new path to neighbour is shorter OR neighbour is not in green nodes
#           set f_cost of neighbour
#           set parent of neighbour to current
#           if neighbour is not in green nodes
#               add neighbour to green nodes
#
#
# now loop through closed list from ending node
# the path is that nodes parent
# that parents parent ...
# until hit start

class Node:
    def __init__(self, x, y, is_obstacle):
        self.parent = None
        self.x = x
        self.y = y
        self.h_cost = None
        self.g_cost = None
        self.f_cost = None
        self.is_obstacle = is_obstacle

    def update_costs(self):
        self.update_g_cost()
        self.update_f_cost()
        self.update_h_cost()

    def update_f_cost(self):  # g_cost + h_cost
        pass

    def update_g_cost(self):  # distance from start node through red nodes
        pass

    def update_h_cost(self):  # distance from end node
        pass


class Grid:
    def __init__(self, start_pos, end_pos, size, obstacles):
        self.start_node = None
        self.start_pos = start_pos
        self.end_node = None
        self.end_pos = end_pos
        self.size = size
        self.x_size, self.y_size = size
        self.obstacles = obstacles
        self.nodes = []
        self.node_matrix = [[] for i in range(self.y_size)]
        self.create_nodes()

    def create_nodes(self):
        for y in range(self.y_size):
            for x in range(self.x_size):

                # check if its an obstacle
                if (x, y) in self.obstacles:
                    is_obstacle = True
                else:
                    is_obstacle = False

                # get the node
                node = Node(x, y, is_obstacle)

                # see if its the start or end node
                if (x, y) == self.start_pos:
                    self.start_node = node
                elif (x, y) == self.end_node:
                    self.end_node = node

                # add to node list and matrix
                self.node_matrix[y].append(node)
                self.nodes.append(node)

    def node_at(self, x, y):
        return self.node_matrix[y][x]

    def find_path(self):
        # this is the MAIN LOOP
        # return a path with all coordinates
        green_nodes = []  # all neighboring nodes to be explored
        red_nodes = []  # all nodes already explored
        green_nodes.append(self.start_node)

        while len(green_nodes) > 0:

            # get the lowest cost node
            # will optimize later
            lowest_f_cost = min([node.f_cost for node in green_nodes])
            valid_nodes = [node for node in green_nodes if node.f_cost == lowest_f_cost]
            lowest_h_cost = min([node.h_cost for node in valid_nodes])
            lowest_cost_nodes = [node for node in valid_nodes if node.h_cost == lowest_h_cost]
            current = lowest_cost_nodes[0]

            # remove the node from green nodes and add it to red nodes
            green_nodes.remove(current)
            red_nodes.append(current)

            # check if we reached the end
            if current == self.end_node:
                break

            # check all neighboring nodes
            for neighbour in self.get_neighbors(current):

                # check if valid node
                if neighbour.is_obstacle or neighbour in red_nodes:
                    continue

                # tbc


    def get_neighbors(self, node):

        # keep track of neighbors
        neighbors = []

        # look at all 8 positions around node
        for x in range(-1, 2):
            for y in range(-1, 2):

                # make sure not looking at self position
                if x == 0 and y == 0:
                    continue

                # within bounds?
                if 0 <= node.x + x <= self.x_size and 0 <= node.y + y <= self.y_size:

                    # add neighbor to neighbors
                    neighbor = self.node_at(node.x + x, node.y + y)
                    neighbors.append(neighbor)

        return neighbors

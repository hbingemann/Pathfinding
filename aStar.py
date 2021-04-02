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
# for-result ---------------------------------
# now loop through closed list from ending node
# the path is that nodes parent
# that parents parent ...
# until hit start

class _Node:
    def __init__(self, x, y, is_obstacle):
        self.parent = None
        self.x = x
        self.y = y
        self.h_cost = None  # distance from end
        self.g_cost = None  # distance from start
        self.is_obstacle = is_obstacle

        @property
        def f_cost(self):
            return self.g_cost + self.h_cost


class Grid:
    def __init__(self, start_pos, end_pos, size, obstacles=()):
        self.start_node = None
        self.start_pos = start_pos
        self.end_node = None
        self.end_pos = end_pos
        self.size = size
        self.x_size, self.y_size = size
        self.obstacles = obstacles
        self.nodes = []
        self.node_matrix = [[] for i in range(self.y_size)]
        self.path = []
        self._create_nodes()

    def _create_nodes(self):
        for y in range(self.y_size):
            for x in range(self.x_size):

                # check if its an obstacle
                if (x, y) in self.obstacles:
                    is_obstacle = True
                else:
                    is_obstacle = False

                # get the node
                node = _Node(x, y, is_obstacle)

                # see if its the start or end node
                if (x, y) == self.start_pos:
                    self.start_node = node
                elif (x, y) == self.end_node:
                    self.end_node = node

                # add to node list and matrix
                self.node_matrix[y].append(node)
                self.nodes.append(node)

        # set the values for starting node
        self.start_node.h_cost = self._get_distance(self.start_node, self.end_node)
        self.start_node.g_cost = 0

    def _node_at(self, x, y):
        return self.node_matrix[y][x]

    def find_path(self, delay: float) -> list:
        # this is the MAIN LOOP
        # return a list path with all coordinates in the path
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
                return self.retrace_path()

            # check all neighboring nodes
            for neighbor in self._get_neighbors(current):

                # check if valid node
                if neighbor.is_obstacle or neighbor in red_nodes:
                    continue

                # see what to do with the neighbor
                new_neighbor_g_cost = current.g_cost + self._get_distance(current, neighbor)

                if neighbor not in green_nodes or new_neighbor_g_cost < neighbor.g_cost:
                    neighbor.g_cost = new_neighbor_g_cost
                    neighbor.h_cost = self._get_distance(neighbor, self.end_node)
                    neighbor.parent = current

                    if neighbor not in green_nodes:
                        green_nodes.append(neighbor)

    def _get_retraced_path(self):
        path = []
        current = self.end_node

        # go through all parents to until found start node
        while current != self.start_node:
            path.append((current.x, current.y))
            current = current.parent

        # reverse the path to have it in the proper direction
        path.reverse()

        return path

    def _get_distance(self, node1, node2):

        # get distances
        x_distance = abs(node1.x - node2.x)
        y_distance = abs(node1.y - node2.y)

        # return distance value with diagonal
        if x_distance > y_distance:
            return 14 * y_distance + 10 * (x_distance - y_distance)
        return 14 * x_distance + 10 * (y_distance - x_distance)

    def _get_neighbors(self, node):

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
                    neighbor = self._node_at(node.x + x, node.y + y)
                    neighbors.append(neighbor)

        return neighbors

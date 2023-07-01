from Maze import Maze

class Node:
    """
    This class represents a node in a search tree.
    """
    def __init__(self, state, parent):
        """
        Initializes a new Node object with the given state and parent.
        
        :param state: The state of the node.
        :param parent: The parent of the node.
        """
        self.state = state
        self.parent = parent
        try:
            self.action = parent.action + 1
        except AttributeError:
            self.action = 0


class StackFrontier:
    """
    This class represents a stack-based frontier for use in depth-first search.
    """
    def __init__(self):
        """
        Initializes a new StackFrontier object.
        """
        self.frontier = []

    def add(self, node):
        """
        Adds a new node to the frontier.
        
        :param node: The node to add to the frontier.
        """
        self.frontier.append(node)

    def is_empty(self):
        """
        Returns True if the frontier is empty, False otherwise.
        
        :return: A boolean indicating whether the frontier is empty.
        """
        return len(self.frontier) == 0


    def remove(self):
        """
        Removes and returns the next node from the frontier.
        
        :return: The next node from the frontier.
        :raises Exception: If the frontier is empty.
        """
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop()
            return node
    
    def contains(self, state):
        """
        Returns True if the frontier contains a node with the given state, False otherwise.
        
        :param state: The state to check for in the frontier.
        :return: A boolean indicating whether the frontier contains a node with the given state.
        """
        return any(node.state == state for node in self.frontier)
    

class QueueFrontier(StackFrontier):
    """
    This class represents a queue-based frontier for use in breadth-first search. It inherits from StackFrontier and overrides the remove method to implement a queue instead of a stack.
    """
    def remove(self):
        """
        Removes and returns the next node from the frontier. Overrides the remove method from StackFrontier to implement a queue instead of a stack.
        
        :return: The next node from the frontier.
        :raises Exception: If the frontier is empty.
        """
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop(0)
            return node
        
class GeedyFrontier(QueueFrontier):
    """
    This class represents a greedy best-first search frontier. It inherits from QueueFrontier and overrides the add method to implement a priority queue based on distance to the goal.
    """
    def __init__(self, end_point):
        """
        Initializes a new GeedyFrontier object with the given end point.
        
        :param end_point: The end point of the search.
        """
        super().__init__()
        self.end_point = end_point

    def add(self, node: Node):
        """
       Adds a new node to the frontier based on its distance to the goal. Overrides the add method from QueueFrontier to implement a priority queue based on distance to the goal.

       :param node: The node to add to the frontier.
       """
        for i, fornter_node in enumerate(self.frontier):
            if self.get_distance(fornter_node) > self.get_distance(node):
                self.frontier.insert(i, node)
                return
            
        self.frontier.append(node)

    def get_distance(self, node: Node):
        """
       Returns the distance between the given node and the end point.

       :param node: The node to calculate distance for.
       :return: The distance between the given node and the end point.
       """
        return abs(node.state[0] - self.end_point[0]) + abs(node.state[1] - self.end_point[1])
    
class AstarFrontier(GeedyFrontier):
    """
   This class represents an A* search frontier. It inherits from GeedyFrontier and overrides get_distance method to include both distance to goal and cost so far in its calculation of priority.
   """
    def get_distance(self, node: Node):
        """
      Returns an estimate of total cost from start through this given node to reach goal. Overrides get_distance method from GeedyFrontier.

      :param node: The node to calculate total cost for
      :return: An estimate of total cost from start through this given node to reach goal
      """
        return super().get_distance(node) + node.action


class Search:
    """
    This class represents a generic search algorithm for solving mazes.
    """
    def __init__(self, maze: Maze):
        """
        Initializes a new Search object with the given maze.
        
        :param maze: The maze to solve.
        """
        self.maze = maze
        self.start_position = self.maze.starting_point
        self.start_node = Node(self.start_position, None)
        self.end_position = self.maze.ending_point

    def neighphors(self, state):
        """
        Returns the neighbors of the given state in the maze.
        
        :param state: The state to find neighbors for.
        :return: A list of neighboring states.
        """
        maze = self.maze
        neighbors = []
        x, y = state

        if x > 0 and maze.maze[x-1][y] != 1:
            neighbors.append((x-1, y))
        if x < maze.width-1 and maze.maze[x+1][y] != 1:
            neighbors.append((x+1, y))
        if y > 0 and maze.maze[x][y-1] != 1:
            neighbors.append((x, y-1))
        if y < maze.height-1 and maze.maze[x][y+1] != 1:
            neighbors.append((x, y+1))

        return neighbors
    
    def search_solve(self):
        """
       Solves the maze using the search algorithm defined by the frontier.

       :return: A tuple containing the solution path and the list of visited states.
       """
        frontier = self.frontier
        source_node = self.start_node


        frontier.add(source_node)

        visited = []

        while(not frontier.is_empty()):

            node = frontier.remove()
            visited.append(node.state)
            if node.state == self.end_position:
                goal = node
                break

            neighbors = self.neighphors(node.state)
            for neighbor in neighbors:
                neighbor
                if neighbor not in visited and not frontier.contains(neighbor):
                    new_node = Node(neighbor, node)
                    frontier.add(new_node)


        else:
            return (None, visited)
        
        path = []
        while goal.parent is not None:
            path.append(goal.state)

            goal = goal.parent


        return (path[::-1], visited)
    
class BFSearch(Search):
    """
   This class represents a breadth-first search algorithm for solving mazes. It inherits from Search and sets the frontier to a QueueFrontier.
   """
    def __init__(self, maze: Maze):
        """
      Initializes a new BFSearch object with the given maze.

      :param maze: The maze to solve.
      """
        super().__init__(maze)
        self.frontier = QueueFrontier()

class DFSearch(Search):
    """
   This class represents a depth-first search algorithm for solving mazes. It inherits from Search and sets the frontier to a StackFrontier.
   """
    def __init__(self, maze: Maze):
        """
      Initializes a new DFSearch object with the given maze.

      :param maze: The maze to solve.
      """
        super().__init__(maze)
        self.frontier = StackFrontier()

class GBFSearch(Search):
    """
   This class represents a greedy best-first search algorithm for solving mazes. It inherits from Search and sets the frontier to a GeedyFrontier.
   """
    def __init__(self, maze: Maze):
        """
      Initializes a new GBFSearch object with the given maze.

      :param maze: The maze to solve.
      """
        super().__init__(maze)
        self.frontier = GeedyFrontier(maze.ending_point)

class AstarSearch(Search):
    """
   This class represents an A* search algorithm for solving mazes. It inherits from Search and sets the frontier to an AstarFrontier.
   """
    def __init__(self, maze: Maze):
        """
      Initializes a new AstarSearch object with the given maze.

      :param maze: The maze to solve.
      """
        super().__init__(maze)
        self.frontier = AstarFrontier(maze.ending_point)

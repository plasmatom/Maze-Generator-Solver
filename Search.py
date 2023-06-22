from Maze import Maze

class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        try:
            self.action = parent.action + 1
        except AttributeError:
            self.action = 0


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def is_empty(self):
        return len(self.frontier) == 0


    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop()
            return node
    
    def contains(self, state):
        return any(node.state == state for node in self.frontier)
    

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier.pop(0)
            return node
        
class GeedyFrontier(QueueFrontier):
    def __init__(self, end_point):
        super().__init__()
        self.end_point = end_point

    def add(self, node: Node):
        for i, fornter_node in enumerate(self.frontier):
            if self.get_distance(fornter_node) > self.get_distance(node):
                self.frontier.insert(i, node)
                return
            
        self.frontier.append(node)

    def get_distance(self, node: Node):
        return abs(node.state[0] - self.end_point[0]) + abs(node.state[1] - self.end_point[1])
    
class AstarFrontier(GeedyFrontier):
    def get_distance(self, node: Node):
        return super().get_distance(node) + node.action


class Search:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.start_position = self.maze.starting_point
        self.start_node = Node(self.start_position, None)
        self.end_position = self.maze.ending_point

    def neighphors(self, state):
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
    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.frontier = QueueFrontier()

class DFSearch(Search):
    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.frontier = StackFrontier()

class GBFSearch(Search):
    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.frontier = GeedyFrontier(maze.ending_point)

class AstarSearch(Search):
    def __init__(self, maze: Maze):
        super().__init__(maze)
        self.frontier = AstarFrontier(maze.ending_point)

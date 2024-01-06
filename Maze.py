import random
import time

class Maze:
    """
    Class for generating a maze and managing the starting, ending points, and path display within the maze.
    .............
    Methods:
        __init__: Initializes the maze with given size, coverage, and aspect ratio.
        generate_maze: Generates a maze based on specified coverage.
        set_point: Sets a point in the maze based on a given value.
        set_starting_point: Sets the starting point in the maze.
        set_ending_point: Sets the ending point in the maze.
        update_maze: Updates the maze based on a given position.
        display_path: Displays a given path in the maze.
    """
    def __init__(self, size: int, coverage: float, aspect_ratio: float):
        """
        Initializes the maze with given size, coverage, and aspect ratio.
        .............
        Input:
            size: Size of the maze
            coverage: Coverage ratio for maze generation
            aspect_ratio: Aspect ratio for maze dimensions
        """
        self.aspect_ratio = aspect_ratio
        self.height = size
        self.width = int(size * self.aspect_ratio)
        self.coverage = coverage
        self.maze = self.generate_maze()
        self.starting_point = self.set_starting_point()
        self.ending_point = self.set_ending_point()

    def generate_maze(self):
        """
        Generates a maze based on the specified coverage.
        .............
        Output:
            Generated maze
        """
        maze = [[0 for _ in range(self.height)] for _ in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                if random.random() > self.coverage:
                    maze[i][j] = 1

        return maze
    
    def set_point(self, value):
        """
        Sets a point in the maze based on a given value.
        .............
        Input:
            value: Value to set in the maze
        Output:
            Point position
        """
        if value == 2:
            random.seed(int(time.time()))
    
        x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)

        while(self.maze[x][y] == 0):
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
        else:
            self.maze[x][y] = value
            point = (x, y)
        
        return point
    
    def set_starting_point(self):
        """
        Sets the starting point in the maze.
        .............
        Output:
            Starting point position
        """
        return self.set_point(2)

    def set_ending_point(self):
        """
        Sets the ending point in the maze.
        .............
        Output:
            Ending point position
        """
        return self.set_point(3)
    
    def update_maze(self, postion):
        """
        Updates the maze based on a given position.
        .............
        Input:
            position: Position to be updated
        """
        x = postion[0]
        y = postion[1]

        if postion == self.starting_point:
            self.maze[x][y] = 2
        
        elif postion == self.ending_point:
            self.maze[x][y] = 3

        else:
            self.maze[x][y] = 5
            
        

    def display_path(self, path):
        """
        Displays a given path in the maze.
        .............
        Input:
            path: Path to be displayed
        """
        try:
            for x, y in path:
                self.maze[x][y] = 4
            self.maze[self.starting_point[0]][self.starting_point[1]] = 2
            self.maze[self.ending_point[0]][self.ending_point[1]] = 3
        except:
            return None

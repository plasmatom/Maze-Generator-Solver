import random
import time

class Maze:
    def __init__(self, size: int, coverage: float, aspect_ratio: float):
        self.aspect_ratio = aspect_ratio
        self.height = size
        self.width = int(size * self.aspect_ratio)
        self.coverage = coverage
        self.maze = self.generate_maze()
        self.starting_point = self.set_starting_point()
        self.ending_point = self.set_ending_point()

    def generate_maze(self):
        maze = [[0 for _ in range(self.height)] for _ in range(self.width)]
        for i in range(self.width):
            for j in range(self.height):
                if random.random() > self.coverage:
                    maze[i][j] = 1

        return maze
    
    def set_point(self, value):
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
        return self.set_point(2)

    def set_ending_point(self):
        return self.set_point(3)
    
    def update_maze(self, postion):
        x = postion[0]
        y = postion[1]

        if postion == self.starting_point:
            self.maze[x][y] = 2
        
        elif postion == self.ending_point:
            self.maze[x][y] = 3

        else:
            self.maze[x][y] = 5
            
        

    def display_path(self, path):
        try:
            for x, y in path:
                self.maze[x][y] = 4
            self.maze[self.starting_point[0]][self.starting_point[1]] = 2
            self.maze[self.ending_point[0]][self.ending_point[1]] = 3
        except:
            return None
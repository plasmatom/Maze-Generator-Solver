from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer
from Search import DFSearch, BFSearch, GBFSearch, AstarSearch
from Maze import Maze
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
import copy


def draw_maze(maze: Maze, image_size: tuple[int]):
    """
    Generates a pixrl map for display
    INPUT:
        maze: Maze
            Maze object that will be displayed
        image_size: tuple[int]
            conisists of the hight and width of the pixel map (width , hight)
    OUTPUT:
        img: Image
            the pixel map
    """
    width, height = image_size
    cell_size = min(width // maze.height, height // maze.width)

    img = Image.new("RGB", (height, width), "white")
    draw = ImageDraw.Draw(img)

    for i in range(maze.width):
        for j in range(maze.height):
            x0 = i * cell_size
            y0 = j * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
        
            if maze.maze[i][j] == 1:
                draw.rectangle([x0, y0, x1, y1], fill="#261420")
            if maze.maze[i][j] == 2:
                draw.rectangle([x0, y0, x1, y1], fill="#33FF99")
            if maze.maze[i][j] == 3:
                draw.rectangle([x0, y0, x1, y1], fill="#FC630A")
            if maze.maze[i][j] == 4:
                draw.rectangle([x0, y0, x1, y1], fill="#E6DB15")
            if maze.maze[i][j] == 5:
                draw.rectangle([x0, y0, x1, y1], fill="#6AAED9")
            if maze.maze[i][j] == 0:
                draw.rectangle([x0, y0, x1, y1], fill="#8FA1A6")

    for i in range(maze.width):
        for j in range(maze.height):
            x0 = i * cell_size
            y0 = j * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            if j == 0 or maze.maze[i][j-1] != maze.maze[i][j]:
                draw.line((x0,y0,x1,y0), fill="black")

            if j == maze.height-1 or maze.maze[i][j+1] != maze.maze[i][j]:
                draw.line((x0,y1,x1,y1), fill="black")

            if i == 0 or maze.maze[i-1][j] != maze.maze[i][j]:
                draw.line((x0,y0,x0,y1), fill="black")

            if i == maze.width-1 or maze.maze[i+1][j] != maze.maze[i][j]:
                draw.line((x1,y0,x1,y1), fill="black")

    return img

class MazeWidget(QWidget):
    """
    Object to render and control the maze image
    Attributes:
        dimenions: tuble
        maze: Maze
        unsearched_maze: Maze
        label: Qlabel
    Methods:
        get_path(method='reg'):
        draw_maze():
        update_maze():
    """
    def __init__(self, maze: Maze, dimensions: tuple):
        """
        the function initilizes the MazeWidget object and controls the apearnce of the maze through class methods
        INPUT:
            maze: Maze
                Maze object which will be displayed
            dimensions: tuple
                contains the image dimentions to be displayed
        OUTPUT:
            ...
        """
        super().__init__()
        self.dimensions = dimensions
        self.maze = maze
        self.unsearched_maze = copy.deepcopy(self.maze)
        self.get_path()

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.draw_maze()

    def get_path(self, method="reg"):
        if method == "reg":
            self.solution = []
            self.steps = []
        elif method == "DFS":
            self.search = DFSearch(self.maze)
            self.solution, self.steps = self.search.search_solve()
        elif method =="BFS":
            self.search = BFSearch(self.maze)
            self.solution, self.steps = self.search.search_solve()
        elif method == "GBFS":
            self.search = GBFSearch(self.maze)
            self.solution, self.steps = self.search.search_solve()
        elif method == "A*":
            self.search = AstarSearch(self.maze)
            self.solution, self.steps = self.search.search_solve()

        
        if self.solution == None:
            self.solution = []

    def draw_maze(self):
        """
        draws the initial image in the widget
        INPUT:
            ....
        OUTPUT:
            ....
        """
        img = draw_maze(self.maze, image_size=self.dimensions)

        qimg = ImageQt(img)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_maze)
        self.timer.start(0)

    def update_maze(self):
        """
        Updates the maze image in the widget
        INPUT:
            ....
        OUTPUT:
            ....
        """
        try:
            position = self.steps.pop(0)
            self.maze.update_maze(position)
        except IndexError:
            self.maze.display_path(self.solution)


        img = draw_maze(self.maze, image_size=self.dimensions)

        qimg = ImageQt(img)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)
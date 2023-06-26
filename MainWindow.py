from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QToolBar, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from MazePlot import MazeWidget
from Maze import Maze
import copy

class MainPanel(QWidget):
    """
    Class to display the maze in the screen
    Attributes:
        main_layout: QHBoxLayout
            the layout to put the image
        height: int
            hieght of the maze that will be displayed
        width:  int
            width of the maze that will be displayed
        maze: list[list]
            the maze that will be generated and then displayed    
        maze_widget: MazeWidget
            the widget that fully contains the maze and it is responsible for updating the maze
    Metheods:
        display_maze(clicked: str):
            Resets the maze to the original maze and generates a new path
        regenerate_maze(clicked: str):
            generates a new empty maze
    """
    def __init__(self):
        """
        Constructs all neccessary attributes for the MainPanel object
        INPUT:
            ....
        OUTPUT:
            ....
        """
        super().__init__()
        self.main_layout = QHBoxLayout()
        size = self.size()
        self.height = size.height()
        self.width = size.width()
        self.maze = Maze(30, 0.7, self.width/self.height)
        self.maze_widget = MazeWidget(self.maze, (self.height, self.width))
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.maze_widget)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)



    def display_maze(self, clicked: str):
        """
        resets the maze and generates a new path pased on the clicked algorithem
        INPUT:
            clicked: str
                represents the algorithem that has been clicked
        OUTPUT:
            ....
        """
        self.maze_widget.maze = copy.deepcopy(self.maze_widget.unsearched_maze)
        self.maze_widget.get_path(method=clicked)
    
    def regenerate_maze(self, clicked='reg'):
        """
        genertes a new empty maze and removes the previews maze
        INPUT:
            clicked: str
                takes a 'reg' string
        OUTPUT:
            ....
        """
        new_maze = Maze(self.maze_widget.maze.height, self.maze_widget.maze.coverage, self.maze_widget.maze.aspect_ratio)
        new_maze_widget = MazeWidget(new_maze, (self.height, self.width))
        index = self.main_layout.indexOf(self.maze_widget)
        self.main_layout.removeWidget(self.maze_widget)
        self.maze_widget.deleteLater()
        self.maze_widget = new_maze_widget
        self.main_layout.insertWidget(index, self.maze_widget)
        self.maze_widget.get_path(method=clicked)




class mainWindow(QMainWindow):
    """
    mainWindow class for main window of the GUI
    """
    def __init__(self):
        super().__init__()
        self.main_panel = MainPanel()
        self.setCentralWidget(self.main_panel)
        tool_bar = QToolBar()
        tool_bar.setMovable(False)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tool_bar.addWidget(spacer)

        tool_bar.addSeparator()
        action_1 = tool_bar.addAction('depth_first Search'.title())
        action_1.triggered.connect(lambda : self.checked('DFS'))
        action_1.setIcon(QIcon("Icons/stack.png"))
        action_1.setIconText('depth-first Search'.title())
        tool_bar.addSeparator()

        action_2 = tool_bar.addAction('bredth_first Search'.title())
        action_2.triggered.connect(lambda : self.checked('BFS'))
        action_2.setIcon(QIcon("Icons/queue.png"))
        action_2.setIconText('bredth-first Search'.title())
        tool_bar.addSeparator()

        action_3 = tool_bar.addAction('Gready best-first search'.title())
        action_3.triggered.connect(lambda : self.checked('GBFS'))
        action_3.setIcon(QIcon("Icons/greedy.png"))
        action_3.setIconText('Greedy best-first search'.title())
        tool_bar.addSeparator()

        action_4 = tool_bar.addAction('A*'.title())
        action_4.triggered.connect(lambda : self.checked('A*'))
        action_4.setIcon(QIcon("Icons/A.png"))
        action_4.setIconText('A*'.title())
        tool_bar.addSeparator()

        action_5 = tool_bar.addAction('regenerate'.title())
        action_5.triggered.connect(lambda : self.checked('reg'))
        action_5.setIcon(QIcon("Icons/regenerate.png"))
        action_5.setIconText('regenerate'.title())
        tool_bar.addSeparator()

        spacer_end = QWidget()
        spacer_end.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tool_bar.addWidget(spacer_end)

        self.addToolBar(Qt.LeftToolBarArea, tool_bar)

        self.setWindowTitle('Maze Generator')

        spacing = 20
        tool_bar.setStyleSheet(f"QToolBar {{spacing: {spacing}px;}}")
        tool_bar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.move(400, 130)



    def checked(self, action):
        if action == 'reg':
            self.main_panel.regenerate_maze(action)
        else:
            self.main_panel.display_maze(action)
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from MainWindow import mainWindow
import sys


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('Icons/maze.png'))
    window = mainWindow()
    window.show()
    sys.exit(app.exec())



if __name__ == '__main__':
    main()
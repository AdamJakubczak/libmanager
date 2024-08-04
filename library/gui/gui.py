from PySide6.QtCore import QSize
from PySide6.QtWidgets import QTabWidget, QMainWindow, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Library management system')
        self.setMinimumSize(QSize(1000,600))
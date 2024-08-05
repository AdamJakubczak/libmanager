from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QToolBar
from library.gui.gui_models import TabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window settings

        self.setWindowTitle('Library management system')
        self.setMinimumSize(QSize(1000,600))

        # Toolbar settings
        
        self.addToolBar(QToolBar())

        # Central Tab Widget settings

        main_tab_widget = TabWidget()
        self.setCentralWidget(main_tab_widget)
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QTabWidget, QHBoxLayout, QVBoxLayout


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self.tab_one = TabOne()
        self.tab_two = TabTwo()

        self.addTab(self.tab_one, 'Tab 1')
        self.addTab(self.tab_two, 'Tab 2')

        ...

class TabOne(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        ...

class TabTwo(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        ...
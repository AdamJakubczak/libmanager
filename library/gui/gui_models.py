from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QHeaderView


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

        self.book_table = BooksTable()
        main_layout.addWidget(self.book_table)

        self.setLayout(main_layout)
        
        ...

class TabTwo(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        ...

class BooksTable(QTableWidget):
    def __init__(self):
        super().__init__()

        horizontal_headers = ['Id', 'Title', 'Author Name', 'Author Last Name', 'Isbn']

        self.setColumnCount(len(horizontal_headers))
        self.setHorizontalHeaderLabels(horizontal_headers)

        header = self.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
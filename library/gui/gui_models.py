from cgitb import text
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QHeaderView, QTableWidgetItem, QFormLayout
from PySide6.QtCore import QSize
from library.db.connection import DataAcessObject


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self.tab_one = TabOne()
        self.tab_two = TabTwo()

        self.addTab(self.tab_one, 'Books')
        self.addTab(self.tab_two, 'Tab 2')

        ...

class TabOne(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        self.book_table = BooksTable()
        main_layout.addWidget(self.book_table)

        self.tab_one_buttons = TabOneButtons(self.book_table)
        main_layout.addWidget(self.tab_one_buttons)

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

        self.load_data()
    
    
    def load_data(self):

        self.setRowCount(0) #Clears existing data

        table_data = DataAcessObject.select_all_books()

        for pos, row in enumerate(table_data):
            self.insertRow(pos)
            self.setItem(pos, 0, QTableWidgetItem(str(row.book_id)))
            self.setItem(pos, 1, QTableWidgetItem(row.book_title))
            self.setItem(pos, 2, QTableWidgetItem(row.book_author_name))
            self.setItem(pos, 3, QTableWidgetItem(row.book_author_last_name))
            self.setItem(pos, 4, QTableWidgetItem(str(row.book_isbn)))


class TabOneButtons(QWidget):
    def __init__(self, book_table):
        super().__init__()

        self.book_table = book_table

        main_layout = QHBoxLayout()

        self.button1 = QPushButton('Add book')
        self.button1.clicked.connect(self.add_book)
        main_layout.addWidget(self.button1)
        
        self.setLayout(main_layout)

        self.add_book_window = None
    
    def add_book(self):

        if self.add_book_window is None:
            self.add_book_window = AddBookWindow(self.book_table)
        
        self.add_book_window.show()

class AddBookWindow(QWidget):
    def __init__(self, book_table : BooksTable):
        super().__init__()

        self.book_table = book_table

        self.setWindowTitle('Add new book')
        self.setFixedSize(QSize(600,200))

        main_layout = QVBoxLayout()

        self.form = BookWindowForm()
        main_layout.addWidget(self.form)

        self.add_book_button = QPushButton('Add book')
        self.add_book_button.clicked.connect(self.add_book)

        main_layout.addWidget(self.add_book_button)

        self.setLayout(main_layout)
    
    def add_book(self):
        db = DataAcessObject()
        db.open_connection()

        book_title = self.form.book_title.text()
        book_author_name = self.form.book_author_name.text()
        book_author_last_name = self.form.book_author_last_name.text()
        book_isbn = int(self.form.book_isbn.text())

        # print(book_title, book_author_name, book_author_last_name, book_isbn)

        db.add_book(book_title, book_isbn, book_author_name, book_author_last_name)
        self.book_table.load_data()

class BookWindowForm(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QFormLayout()

        self.book_title = QLineEdit()
        self.book_author_name = QLineEdit()
        self.book_author_last_name = QLineEdit()
        self.book_isbn = QLineEdit()

        main_layout.addRow(QLabel('Book title'), self.book_title)
        main_layout.addRow(QLabel('Author name'), self.book_author_name)
        main_layout.addRow(QLabel('Author last name'), self.book_author_last_name)
        main_layout.addRow(QLabel('Book ISBN'), self.book_isbn)

        self.setLayout(main_layout)
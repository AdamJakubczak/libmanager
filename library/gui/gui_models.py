# Standard and third-party library imports
from ast import Add, main
from http import server
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QLineEdit, QTableWidget, 
    QTabWidget, QHBoxLayout, QVBoxLayout, QHeaderView, 
    QTableWidgetItem, QFormLayout, QMessageBox, QAbstractItemView
)
# Local application imports
from library.db.connection import DataAcessObject


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()

        self.tab_one = TabOne()
        self.tab_two = TabTwo()

        self.addTab(self.tab_one, 'Books')
        self.addTab(self.tab_two, 'Users')


class TabOne(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search for books')
        self.search_bar.textChanged.connect(self.search)
        main_layout.addWidget(self.search_bar)

        self.book_table = BooksTable()
        main_layout.addWidget(self.book_table)

        self.tab_one_buttons = TabOneButtons(self.book_table)
        main_layout.addWidget(self.tab_one_buttons)

        self.setLayout(main_layout)

    def search(self):
        search_term = self.search_bar.text().lower()
        self.book_table.filter_data(search_term)


class BooksTable(QTableWidget):
    def __init__(self):
        super().__init__()

        horizontal_headers = ['Id', 'Title', 'Author Name', 'Author Last Name', 'Isbn', 'Quantity']

        self.setColumnCount(len(horizontal_headers))
        self.setHorizontalHeaderLabels(horizontal_headers)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) #Brak możliwości edycji tabeli

        header = self.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)

        self.table_data = []
        self.load_data()

        self.cellClicked.connect(self.retrieve_book_id) #Podczas kliknięcia w komórkę, zwraca ID książki
        self.table_book_id = ''
   
    def load_data(self):
        self.table_data = DataAcessObject.select_all_books()
        self.filter_data('')
    
    def filter_data(self, search_term):

        self.setRowCount(0)
        current_row = 0

        for row in self.table_data:
            if (search_term in row.book_title.lower() or
                search_term in row.book_author_name.lower() or
                search_term in row.book_author_last_name.lower() or
                search_term in str(row.book_isbn)):

                self.insertRow(current_row)
                self.setItem(current_row, 0, QTableWidgetItem(str(row.book_id)))
                self.setItem(current_row, 1, QTableWidgetItem(row.book_title))
                self.setItem(current_row, 2, QTableWidgetItem(row.book_author_name))
                self.setItem(current_row, 3, QTableWidgetItem(row.book_author_last_name))
                self.setItem(current_row, 4, QTableWidgetItem(str(row.book_isbn)))
                self.setItem(current_row, 5, QTableWidgetItem(str(row.book_count)))

                current_row += 1
    
    def retrieve_book_id(self, row, column):
        self.table_book_id = self.item(row, 0).text()
        print(self.table_book_id)


class TabOneButtons(QWidget):
    def __init__(self, book_table):
        super().__init__()

        self.book_table = book_table

        main_layout = QHBoxLayout()

        self.button1 = QPushButton('Add book')
        self.button1.clicked.connect(self.add_book)
        main_layout.addWidget(self.button1)

        self.button2 = QPushButton('Rent book')
        self.button2.clicked.connect(self.rent_book)
        main_layout.addWidget(self.button2)
        
        self.setLayout(main_layout)

        self.add_book_window = None
        self.rent_book_window = None
    
    def add_book(self):

        if self.add_book_window is None:
            self.add_book_window = AddBookWindow(self.book_table)
        
        self.add_book_window.show()
    
    def rent_book(self):
        if not self.book_table.table_book_id:
            error_msg = QMessageBox()
            error_msg.setText('No book was selected!')
            error_msg.setWindowTitle('Error')
            error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.exec()

        elif self.rent_book_window is None:
            self.rent_book_window = RentBookWindow(self.book_table)
        
            self.rent_book_window.show()


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
        
        book_title = self.form.book_title.text()
        book_author_name = self.form.book_author_name.text()
        book_author_last_name = self.form.book_author_last_name.text()
        book_isbn = self.form.book_isbn.text()

        try:
            self.validate_inputs(book_title, book_author_name, book_author_last_name, book_isbn)
            db = DataAcessObject()
            db.add_book(book_title, int(book_isbn), book_author_name, book_author_last_name)
            self.book_table.load_data()
        
        except ValueError as ve:

            error_msg = QMessageBox()
            error_msg.setText(str(ve))
            error_msg.setWindowTitle('Error')
            error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.exec()
    
    def validate_inputs(self, book_title, book_author_name, book_author_last_name, book_isbn):
        if not book_title:
            raise ValueError('Book title must not be empty')
        if not book_author_name:
            raise ValueError('Author name must not be empty')
        if not book_author_last_name:
            raise ValueError('Author last name must not be empty')
        if not book_isbn:
            raise ValueError('Book isbn must not be empty')
        if not str(book_isbn).isdigit() or not 10 < len(book_isbn) < 13:
            raise ValueError('ISBN not a number, or too long, or maybe too short')

        
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

class RentBookWindow(QWidget):
    def __init__(self, books_table):
        super().__init__()

        self.books_table = books_table

        self.setFixedSize(QSize(800,600))
        self.setWindowTitle('Rent a book')

        main_layout = QVBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search user')
        main_layout.addWidget(self.search_bar)        

        self.rent_users_table = UsersTable()
        main_layout.addWidget(self.rent_users_table)

        self.rent_button = QPushButton('Rent book')
        self.rent_button.clicked.connect(self.rent_book)
        main_layout.addWidget(self.rent_button)

        self.setLayout(main_layout)
    
    def rent_book(self):
        print('Renting in progress')

class TabTwo(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        self.user_table = UsersTable()
        main_layout.addWidget(self.user_table)

        self.buttons_layout = TabTwoButtons(self.user_table)
        main_layout.addWidget(self.buttons_layout)

        self.setLayout(main_layout)

class UsersTable(QTableWidget):
    def __init__(self):
        super().__init__()

        horizontal_headers = ['Id', 'Name', 'Last name', 'Card no.']

        self.setColumnCount(len(horizontal_headers))
        self.setHorizontalHeaderLabels(horizontal_headers)

        header = self.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.load_data()
    
    def load_data(self):

        self.setRowCount(0) #Clears existing data

        table_data = DataAcessObject.select_all_users()

        for pos, row in enumerate(table_data):
            self.insertRow(pos)
            self.setItem(pos, 0, QTableWidgetItem(str(row.user_id)))
            self.setItem(pos, 1, QTableWidgetItem(row.user_name))
            self.setItem(pos, 2, QTableWidgetItem(row.user_last_name))
            self.setItem(pos, 3, QTableWidgetItem(str(row.user_card_number)))


class TabTwoButtons(QWidget):
    def __init__(self, user_table):
        super().__init__()

        self.user_table = user_table

        main_layout = QHBoxLayout()

        self.add_user_button = QPushButton('Add user')
        self.add_user_button.clicked.connect(self.add_user)
        
        main_layout.addWidget(self.add_user_button)

        self.setLayout(main_layout)
        self.add_user_window = None
    
    def add_user(self):

        if self.add_user_window is None:
            self.add_user_window = AddUserWindow(self.user_table)
        
        self.add_user_window.show()


class AddUserWindow(QWidget):
    def __init__(self, user_table : UsersTable):
        super().__init__()

        self.user_table = user_table
        
        self.setWindowTitle('Add user')
        self.setFixedSize(QSize(600,150))

        main_layout = QVBoxLayout()

        self.add_user_form = AddUserForm()
        main_layout.addWidget(self.add_user_form)

        self.add_user_button = QPushButton('Add user')
        self.add_user_button.clicked.connect(self.add_user)
        main_layout.addWidget(self.add_user_button)

        self.setLayout(main_layout)

    def add_user(self):

        user_name = self.add_user_form.user_name.text()
        user_last_name = self.add_user_form.user_last_name.text()
        user_card_numer = self.add_user_form.user_card_number.text()

        try:
            self.validate_inputs(user_name, user_last_name, user_card_numer)
            db = DataAcessObject()
            db.add_user(user_name, user_last_name, int(user_card_numer))
            self.user_table.load_data()
            
        except ValueError as ve:
            error_msg = QMessageBox()
            error_msg.setText(str(ve))
            error_msg.setWindowTitle('Error')
            error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.exec()
    
    def validate_inputs(self, user_name, user_last_name, user_card_number):

        if not user_name:
            raise ValueError('User name must not be empty')
        if not user_last_name:
            raise ValueError('User last name must not be empty')
        if not user_card_number:
            raise ValueError('User card number must not empty')
        if not str(user_card_number).isdigit():
            raise ValueError('User card number must be a number')


class AddUserForm(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QFormLayout()

        self.user_name = QLineEdit()
        self.user_last_name = QLineEdit()
        self.user_card_number = QLineEdit()

        main_layout.addRow(QLabel('User name'), self.user_name)
        main_layout.addRow(QLabel('User name'), self.user_last_name)
        main_layout.addRow(QLabel('User card number'), self.user_card_number)

        self.setLayout(main_layout)

        
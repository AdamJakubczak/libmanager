import sqlite3
import json

from datetime import datetime
from library.models.models import Book, User

class DataAcessObject:
    def __init__(self):
        
        with open ('library\\db\\config.json', 'r') as file:
            config_file = json.load(file)
            self.db_path = config_file['db_path']
        
        self.connection : sqlite3.Connection
        self.cursor : sqlite3.Cursor
    
    def open_connection(self) -> None:
        
        self.connection = sqlite3.Connection(self.db_path)
        self.cursor = self.connection.cursor()
        print('Connection established')

    def close_connection(self) -> None:

        self.cursor.close()
        self.connection.close()
        print('Connection terminated')

    def check_if_author_exist(self, author_name : str, author_last_name : str) -> int:

        db = DataAcessObject()
        db.open_connection()

        execute_querry = '''
        SELECT author_id
        FROM Authors
        WHERE author_name = ?
        AND author_last_name = ?
        ''' 

        db.cursor.execute(execute_querry, (author_name.strip().capitalize(), author_last_name.strip().capitalize()))
        data = db.cursor.fetchone()
        db.close_connection()
        if data:
            print(f'Author was found Returned Id = {data[0]}')
            return data[0]
        else:
            return False
        
    def add_author(self, author_name : str, author_last_name : str) -> None:

        db = DataAcessObject()
        db.open_connection()

        execute_querry = '''
        INSERT INTO Authors (author_name, author_last_name)
        VALUES (?, ?)
        '''
        db.cursor.execute(execute_querry, (author_name.strip().capitalize(), author_last_name.strip().capitalize()))
        db.connection.commit()
        print(f'Added new author {author_name.capitalize()}, {author_last_name.capitalize()}')
        db.close_connection()

    def check_if_book_exist(self, book_title : str, book_isbn : int) -> int | None:

        db = DataAcessObject()
        db.open_connection()
        print(f'checking book id')

        execute_querry = '''
        SELECT book_id
        FROM Books
        WHERE book_title = ?
        AND book_isbn = ?
        '''

        db.cursor.execute(execute_querry, (book_title, book_isbn))
        data = db.cursor.fetchone()
        db.close_connection()
        if data:
            print(f'Book was found Returned Id = {data[0]}')
            return data[0]
        else:
            return False

    def add_book(self, book_title: str, book_isbn : int, author_name : str, author_last_name : str) -> None:

        book_id = self.check_if_book_exist(book_title, book_isbn)
        author_id = self.check_if_author_exist(author_name, author_last_name)

        if not author_id:
            self.add_author(author_name, author_last_name)
            author_id = self.check_if_author_exist(author_name, author_last_name)

        if not book_id:
            db = DataAcessObject()
            db.open_connection()

            execute_querry = '''
            INSERT INTO Books (book_title, book_isbn, book_author_id)
            VALUES (?, ?, ?)
            '''

            db.cursor.execute(execute_querry, (book_title, book_isbn, author_id))
            print(f'Added new book to library {book_title} by {author_name} {author_last_name}')
            db.connection.commit()
            db.close_connection()
            
        else:
            print('Book already exists')

    def add_user(self, user_name : str, user_last_name : str, user_card_number : int) -> None:

        db = DataAcessObject()
        db.open_connection()

        execute_querry = '''
        INSERT INTO Users (user_name, user_last_name, user_card_number)
        VALUES (?, ?, ?)
        '''

        db.cursor.execute(execute_querry, (user_name, user_last_name, user_card_number))
        db.connection.commit()
        print(f'Added new user: {user_name} {user_last_name}')

    def check_if_user_exist(self, user_name : str, user_last_name : str, user_card_number : int) -> bool:

        db = DataAcessObject()
        db.open_connection()

        execute_querry = '''
        SELECT user_id
        FROM Users
        WHERE user_name = ?
        AND user_last_name = ?
        AND user_card_number = ?
        '''

        db.cursor.execute(execute_querry, (user_name, user_last_name, user_card_number))
        data = db.cursor.fetchone()
        db.close_connection()
        if data:
            print(f'User exists with Id {data[0]}')
            return data[0]
        else:
            return False
    
    def check_book_amount(self, book_id : int) -> int:
        
        db = DataAcessObject()
        db.open_connection()

        execute_querry = '''
        SELECT book_count
        FROM Books
        WHERE book_id = ?'''
        ...

        db.cursor.execute(execute_querry, (book_id, ))
        data = db.cursor.fetchone()[0]
        db.close_connection()

        if data:
            print(f'Available amount for book {book_id} = {data}')
            return data
        else:
            return 0
    
    def reduce_book_amount(self, book_id):
        
        db = DataAcessObject()
        db.open_connection()

        execute_querry = '''
        UPDATE Books
        SET book_count = book_count - 1
        WHERE book_id = ?'''

        db.cursor.execute(execute_querry, (book_id, ))
        db.connection.commit()
        db.close_connection()
                    
    def rent_book(self, user_id : int, book_id : int) -> None:

        time_stamp = datetime.now().timestamp()
        
        if self.check_book_amount(book_id) > 0:
            db = DataAcessObject()
            db.open_connection()

            execute_querry = '''
            INSERT INTO Transactions (transaction_user_id, transaction_book_id, transaction_borrow_date)
            VALUES (?, ?, ?)'''

            db.cursor.execute(execute_querry, (user_id, book_id, time_stamp))
            db.connection.commit()
            db.close_connection()

            db.reduce_book_amount(book_id)

            print(f'User {user_id} borrowed {book_id} on {time_stamp}')
        else:
            raise Exception('No books available to rent')
    
    @classmethod
    def select_all_books(cls) -> list:

        books = []
        
        db = DataAcessObject()
        db.open_connection()

        execute_querry = '''
        SELECT book_id, book_title, author_name, author_last_name, book_isbn, book_count
        FROM Books
        JOIN Authors ON book_author_id = author_id
        '''

        db.cursor.execute(execute_querry)
        data = db.cursor.fetchall()

        for row in data:
            book = Book()
            book.book_id = row[0]
            book.book_title = row[1]
            book.book_author_name = row[2]
            book.book_author_last_name = row[3]
            book.book_isbn = row[4]
            book.book_count = row[5]
            books.append(book)
        
        db.close_connection()
                
        return books
    
    @classmethod
    def select_all_users(cls):

        users = []

        db = DataAcessObject()
        db.open_connection()

        execute_querry = '''
        SELECT *
        FROM Users'''

        db.cursor.execute(execute_querry)
        data = db.cursor.fetchall()

        for row in data:
            user = User()
            user.user_id = row[0]
            user.user_name = row[1]
            user.user_last_name = row[2]
            user.user_card_number = row[3]
            users.append(user)
        
        db.close_connection()

        return users
    
    @classmethod
    def retrieve_what_user_got(cls, user_id):

        borrowed_books = []

        db = DataAcessObject()
        db.open_connection()

        execute_querry = '''
        SELECT book_id, book_title, author_name, author_last_name, book_isbn
        FROM Books
        JOIN Transactions ON transaction_book_id = book_id
        JOIN Users ON transaction_user_id = user_id
        JOIN Authors ON book_author_id = author_id
        WHERE user_id = ?
        '''

        db.cursor.execute(execute_querry, (user_id,))
        data = db.cursor.fetchall()
        db.close_connection()

        for row in data:
            book = Book()
            book.book_id = row[0]
            book.book_title = row[1]
            book.book_author_name = row[2]
            book.book_author_last_name= row[3]
            book.book_isbn = row[4]
            borrowed_books.append(book)
        
        return borrowed_books

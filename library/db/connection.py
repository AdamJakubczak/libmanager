import sqlite3
import json
from datetime import datetime

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
        db.cursor.execute('SELECT author_id FROM Authors WHERE author_name = ? AND author_last_name = ?', (author_name.strip().capitalize(), author_last_name.strip().capitalize()))
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
        db.cursor.execute('INSERT INTO Authors (author_name, author_last_name) VALUES (?, ?)', (author_name.strip().capitalize(), author_last_name.strip().capitalize()))
        db.connection.commit()
        print(f'Added new author {author_name.capitalize()}, {author_last_name.capitalize()}')
        db.close_connection()

    
    def check_if_book_exist(self, book_title : str, book_isbn : int) -> int | None:

        db = DataAcessObject()
        db.open_connection()
        db.cursor.execute('SELECT book_id FROM Books WHERE book_title = ? AND book_isbn = ?', (book_title, book_isbn))
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
        elif not book_id:
            db = DataAcessObject()
            db.open_connection()
            db.cursor.execute('INSERT INTO Books (book_title, book_isbn, book_author_id) VALUES (?, ?, ?)', (book_title, book_isbn, author_id))
            print(f'Added new book to library {book_title} by {author_name} {author_last_name}')
            db.connection.commit()
            db.close_connection()
        else:
            print('Book already exists')

    def add_user(self, user_name : str, user_last_name : str, user_card_number : int) -> None:

        db = DataAcessObject()
        db.open_connection()
        db.cursor.execute('INSERT INTO Users (user_name, user_last_name, user_card_number) VALUES (?, ?, ?)', (user_name, user_last_name, user_card_number))
        db.connection.commit()
        print(f'Added new user: {user_name} {user_last_name}')

    def check_if_user_exist(self, user_name : str, user_last_name : str, user_card_number : int) -> bool:

        db = DataAcessObject()
        db.open_connection()
        db.cursor.execute('SELECT user_id FROM Users where user_name = ? AND user_last_name = ? AND user_card_number = ?', (user_name, user_last_name, user_card_number))
        data = db.cursor.fetchone()
        if data:
            print(f'User exists with Id {data[0]}')
            return data[0]
        else:
            return False
    
    def borrow_book(self, user_id : int, book_id : int) -> None:
        ...
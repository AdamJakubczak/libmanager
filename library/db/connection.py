import sqlite3
import json

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

        author_checker =  self.check_if_author_exist(author_name, author_last_name)
        if author_checker:
            pass
        else:
            db = DataAcessObject()
            db.open_connection()
            db.cursor.execute('INSERT INTO Authors (author_name, author_last_name) VALUES (?, ?)', (author_name.strip().capitalize(), author_last_name.strip().capitalize()))
            db.connection.commit()
            print(f'Added new author {author_name.capitalize()}, {author_last_name.capitalize()}')
            db.close_connection()
    
    def check_if_book_exist(self, book_title : str, book_isbn : int):

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

    def add_book(self, book_title, book_isbn):
        ...
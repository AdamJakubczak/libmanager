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
        if data:
            print(f'Author was found Returned Id = {data[0]}')
            print(type(data[0]))
            return data[0]
    
    def add_author(self, author_name : str, author_last_name : str) -> None:
        db = DataAcessObject()
        db.open_connection()
        db.cursor.execute('INSERT INTO Authors (author_name, author_last_name) VALUES (?, ?)', (author_name.strip().capitalize(), author_last_name.strip().capitalize()))
        db.connection.commit()
        print(f'Added new author {author_name}, {author_last_name}')
        db.close_connection()

    def add_book(self, book_title, book_isbn, author_name, author_last_name):
        ...
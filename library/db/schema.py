from library.db.connection import DataAcessObject

def create_user_table():
    db = DataAcessObject()
    db.open_connection()
    db.cursor.execute('CREATE TABLE Users (user_id INT PRIMARY KEY AUTOINCREMENT, user_name TEXT NOT NULL, user_last_name TEXT NOT NULL, user_card_number INT NOT NULL)')
    db.connection.commit()
    db.close_connection()

def create_authors_table():
    db = DataAcessObject()
    db.open_connection()
    db.cursor.execute('CREATE TABLE Authors (author_id INT PRIMARY KEY AUTOINCREMENT, author_name TEXT NOT NULL, author_last_name TEXT NOT NULL)')
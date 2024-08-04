from library.db.connection import DataAcessObject

def create_user_table():
    db = DataAcessObject()
    db.open_connection()

    execute_querry = '''
    CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_last_name TEXT NOT NULL,
    user_card_number INTEGER NOT NULL
    )
    '''

    db.cursor.execute(execute_querry)
    db.connection.commit()
    db.close_connection()

def create_authors_table():
    db = DataAcessObject()
    db.open_connection()

    execute_querry = '''
    CREATE TABLE Authors (
    author_id INTEGER PRIMARY KEY,
    author_name TEXT NOT NULL,
    author_last_name TEXT NOT NULL
    )
    '''

    db.cursor.execute(execute_querry)
    db.connection.commit()
    db.close_connection()

def create_books_table():
    db = DataAcessObject()
    db.open_connection()

    execute_querry = '''
    CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY,
    book_title TEXT NOT NULL,
    book_author_id INTEGER NOT NULL,
    book_isbn INTEGER (13) NOT NULL,
    book_count INTEGER,
    FOREIGN KEY (book_author_id) REFERENCES Authors(author_id)
    )
    '''
    db.cursor.execute(execute_querry)
    db.connection.commit()
    db.close_connection()

def create_transactions_table():
    db = DataAcessObject()
    db.open_connection()

    execute_querry = '''
    CREATE TABLE Transactions (
    transaction_id INTEGER PRIMARY KEY,
    transaction_user_id INTEGER NOT NULL,
    transaction_book_id INTEGER NOT NULL,
    transaction_borrow_date INTEGER NOT NULL,
    transaction_return_date INTEGER,
    FOREIGN KEY (transaction_user_id) REFERENCES Users(user_id)
    FOREIGN KEY (transaction_book_id) REFRENCES Books(book_id)
    )
    '''
    db.cursor.execute(execute_querry)
    db.connection.commit()
    db.close_connection()
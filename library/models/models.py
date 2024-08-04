class Book:
    def __init__(self):
        
        self.book_id : int
        self.book_title : str
        self.book_author_name : str
        self.book_author_last_name : str
        self.book_isbn : int
    
    def __repr__(self):
        return f'Book Id: {self.book_id}'

class User:
    def __init__(self):

        self.user_id : int
        self.user_name : str
        self.user_last_name : str
        self.user_card_number : int

    def __repr__(self):
        return f'User id: {self.user_id}'


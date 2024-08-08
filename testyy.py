def validate_inputs(self, book_title, book_author_name, book_author_last_name, book_isbn):
        if not book_title:
            raise ValueError('Book title must not be empty')
        if not book_author_name:
            raise ValueError('Author name must not be empty')
        if not book_author_last_name:
            raise ValueError('Author last name must not be empty')
        if not book_isbn:
            raise ValueError('Book isbn must not be empty')
        if not book_isbn.isdigit() or not 10 < len(book_isbn) > 13:
            raise ValueError('ISBN not a number, or too long, or maybe too short')
        
book_title = ''
book_author_name = 'Stephen'
book_author_last_name = 'King'
book_isbn = 1231231231
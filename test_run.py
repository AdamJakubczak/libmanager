from library.db.connection import DataAcessObject
from datetime import datetime

db = DataAcessObject()
db.borrow_book(1,1)
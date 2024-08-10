import library
from library.db.connection import DataAcessObject
from datetime import datetime
from library.main import main
import csv
from random import randint

db = DataAcessObject()


with open ('library\\db\\book_records.csv', 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        db.add_book(row['book_title'], randint(9000000000, 9999999999), row['book_author_name'], row['book_author_last_name'])
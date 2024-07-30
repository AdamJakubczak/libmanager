from library.db.connection import DataAcessObject

db = DataAcessObject()
db.open_connection()
db.close_connection()
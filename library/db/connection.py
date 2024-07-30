import sqlite3
import json

class DataAcessObject:
    def __init__(self):
        
        with open ('library\\db\\config.json', 'r') as file:
            config_file = json.load(file)
            self.db_path = config_file['db_path']
        
        self.connection : sqlite3.Connection
        self.cursor : sqlite3.Cursor
    
    def open_connection(self):
        
        self.connection = sqlite3.Connection(self.db_path)
        self.cursor = self.connection.cursor()
        print('Connection established')

    def close_connection(self):

        self.cursor.close()
        self.connection.close()
        print('Connection terminated')
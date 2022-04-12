import sqlite3
import json


class Database:
    def __init__(self, filename: str):
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()
    
    def get_module(self, class_id: str, module: str, id: str) -> list:
        table = 'sb_' + str(class_id)
        data = self.cur.execute(f'''SELECT words FROM {table} WHERE module="{module+id}"''')
        data = json.loads(data.fetchall()[0][0])
        return data


if __name__ == "__main__":
    db = Database('Dictations.db')
    print(db.get_module('7', '2', 'a'))
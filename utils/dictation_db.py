import sqlite3
import json


class DictationDatabase:
    '''Реализует удобное взаимодействие с бд диктантов'''
    def __init__(self, filename: str):
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()
    
    def get_module(self, class_id: str, module: str, id: str) -> list:
        table = 'sb_' + str(class_id)
        data = self.cur.execute(f'''SELECT words FROM {table} WHERE module="{module+id}"''')
        data = json.loads(data.fetchall()[0][0])
        return data

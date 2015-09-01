__author__ = 'PapEr'

import sqlite3
import logging


class db:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def create_table(self, name):
        self.table_name = name
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ''' + self.table_name + ''' (
        id 		INTEGER PRIMARY KEY,
        title		TEXT,
        description	TEXT,
        href		TEXT,
        tag		TEXT,
        premium		INTEGER
        )
        ''')
        self.conn.commit()
        logging.debug("table created!")

    def insert_problems(self, problems, pages=None):
        data = []
        if pages:
            for prob, page in zip(problems, pages):
                data.append(
                    (int(prob['id']), page['title'], page['description'],
                     prob['href'], prob['tag'], 1))
        else:
            for prob in problems:
                data.append((int(prob['id']), '', '', prob['href'],
                             prob['tag'], 0))

        self.cursor.executemany('''
        INSERT or REPLACE INTO ''' + self.table_name + ' ' + '''
        VALUES ((select id from ''' + self.table_name + ''' where id = ?),
        (?, ?, ?, ?, ?, ?))''', (data[0], data))
        self.conn.commit()
        logging.debug('table inserted!')

    def __del__(self):
        self.cursor.close()
        self.conn.close()

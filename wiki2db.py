#!/usr/bin/env python3

import os
import re
import sqlite3
import xml.etree.ElementTree as ET
#import sqlalchemy as sa

class Wiki2db:

    ns = dict(mw="http://www.mediawiki.org/xml/export-0.10")

    # One Source of Truth for both XML and SQL schema for pages
    page_schema = """
    title:TEXT
    id:INT
    ns:INT
    revision/id:INT:PRIMARY:KEY
    revision/parentid:INT
    revision/timestamp:TEXT
    revision/contributor/username:TEXT
    revision/contributor/id:INT
    revision/contributor/ip:TEXT
    revision/comment:TEXT
    revision/text:TEXT
    """.split('\n')[1:-1]

    PAGE_ON = re.compile(r'<page>')
    PAGE_OFF = re.compile(r'</page>')

    def __init__(self, db_file, verbose=True):
        self.db = sqlite3.connect(db_file)
        self.db.row_factory = sqlite3.Row
        self.verbose = verbose
        self.sql = {}
        self.xpaths = None
        self.fields = None
        self.generate_schema()
        self.create_tables()

    def __del__(self):
        self.db.close()

    def generate_schema(self):
        self.fields = [re.sub(r'/', '_', item.strip()) for item in self.page_schema]
        self.fields = [re.sub(r':', ' ', field) for field in self.fields]
        self.xpaths = [re.sub(r':.+', '', item.strip()) for item in self.page_schema]
        self.sql['create_table_page'] = "CREATE TABLE IF NOT EXISTS page (src_file_id INT, {})".format(', '.join(self.fields))
        self.sql['insert_row_page'] = "INSERT INTO page VALUES(?, {})".format(', '.join(['?' for _ in self.fields]))
        self.sql['create_table_file'] = "CREATE TABLE IF NOT EXISTS file " \
                                        "(file_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                                        "file_path TEXT NOT NULL UNIQUE, imported INT NOT NULL)"
        self.sql['insert_row_file'] = "INSERT INTO file (file_path, imported) VALUES (?,?)"
        self.sql['select_row_file'] = "SELECT file_id FROM file WHERE file_path = ?"
        self.sql['select_new_files'] = "SELECT file_id, file_path FROM file WHERE imported = 0"
        self.sql['update_row_file'] = "UPDATE file SET imported = ? WHERE file_id = ?"

    def create_tables(self):
        self.db.execute(self.sql['create_table_page'])
        self.db.execute(self.sql['create_table_file'])
        self.db.commit()

    def add_files(self, files, imported=0):
        rows = [(file, imported) for file in files]
        for row in rows:
            try:
                self.db.execute(self.sql['insert_row_file'], row)
                self.db.commit()
            except sqlite3.IntegrityError:
                print("File '{}' exists in db".format(row[0]))
                pass

    def get_files(self):
        sql = "SELECT file_id, file_name, imported FROM file"
        return self.db.execute(sql).fetchall()

    def check_file_import_status(self, file_id):
        sql = "SELECT imported FROM file WHERE file_id = ?"
        return self.db.execute(sql, (file_id,)).fetchone()[0]

    def parse_page(self, page, src_file_id):
        values = [src_file_id]
        root = ET.fromstring(page)
        for xpath in self.xpaths:
            try:
                val = "".join(root.find(xpath).itertext())
            except AttributeError:
                val = ''
            values.append(val)
        try:
            self.db.execute(self.sql['insert_row_page'], values)
        except sqlite3.IntegrityError:
            pass

    def import_xml_files(self):
        cur = self.db.cursor()
        cur.execute(self.sql['select_new_files'])
        src_files = [(row['file_id'], row['file_path']) for row in cur.fetchall()]
        for src_file in src_files:
            self.import_xml(src_file[1], src_file[0], self.parse_page)
            cur.execute(self.sql['update_row_file'], (1, src_file[0]))
            self.db.commit()

    def import_xml(self, src_file_path, src_file_id, node_handler):
        with open(src_file_path, 'r') as src:
            switch = page_n = 0
            lines = []
            for line in src.readlines():
                if self.PAGE_ON.search(line):
                    switch = 1
                    page_n += 1
                    if self.verbose and page_n % 1000 == 0:
                        print(page_n)
                elif self.PAGE_OFF.search(line):
                    switch = 0
                    lines.append(line)
                    page = ''.join(lines)
                    node_handler(page, src_file_id)
                    lines = []
                if switch:
                    lines.append(line)


if __name__ == '__main__':

    # Do something like this:

    db_file = 'test.db'
    src_file = 'pages-articles-sample.xml'

    w2b = Wiki2db(db_file, verbose=True)
    w2b.add_files([src_file])
    w2b.import_xml_files()

    #from sqlalchemy import create_engine
    #e1 = create_engine('sqlite://test.db')

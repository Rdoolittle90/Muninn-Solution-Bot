import random
import json
import mysql.connector


from os import getenv
from dotenv import load_dotenv
from settings import SC_URL

load_dotenv()

class DBConnect():
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = getenv("SQL_HOST"),
            user = getenv("SQL_USER"),
            passwd = getenv("SQL_PASSWORD"),
            database = getenv("SQL_DB")
            )
        self.c = self.conn.cursor()

    def close(self):
        self.c.close()
        self.conn.close()

    def execute(self, sql, vars):
        self.c.execute(sql, vars)
        return self.c.fetchall()

    def commit(self):
        self.conn.commit()

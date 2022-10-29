import random
import sqlite3

from os import getenv
from dotenv import load_dotenv
load_dotenv()



class DBConnect():
    def __init__(self, db_name: str = "sc_db.db"):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def insert_member(self, org, member_info):
        sql_insert = """
            INSERT INTO members
            (Org, Display, Handle, Image, Rank, Stars)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.c.execute(sql_insert, (org, member_info['display'], member_info['handle'], member_info['image'], member_info['rank'], member_info['stars']))

    def insert_member_default(self, member):
        sql_insert = """
            INSERT INTO members
            (Org, PID, Display, Handle, Image, Rank, Stars)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        default_img = "https://robertsspaceindustries.com/rsi/static/images/account/avatar_default_big.jpg"

        self.c.execute(sql_insert, ("Unregistered", member.id, member.name, member.name, default_img, "Unregistered", 0))

    def insert_org(self, details):
        sql_insert = """
            INSERT INTO orgs
            (SID, Name, Headline, MemberCount, Logo, URL)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.c.execute(sql_insert, (details['sid'], details['name'], details['headline']['plaintext'], details['members'], details['logo'], details['url']))


    def select_versions(self):
        sql = "SELECT * FROM versions"
        self.c.execute(sql)

        return self.c.fetchall()


    def select_categories(self):
        sql = "SELECT * FROM categories"
        self.c.execute(sql)

        return self.c.fetchall()


    def select_muninn_ranks(self):
        sql = "SELECT DISTINCT Rank FROM members WHERE Org = ?"
        self.c.execute(sql, (getenv("HOME_ORG_SID"), ))

        return [i[0] for i in self.c.fetchall()]


    def select_org(self, SID: int):
        sql = "SELECT * FROM orgs WHERE SID = ?"
        self.c.execute(sql, (SID, ))

        return self.c.fetchone()

    def select_muninn_members(self, rank:str = "all"):
        if rank == "all":
            sql = "SELECT * FROM members WHERE Org = ? ORDER BY Stars DESC, Handle ASC"
            self.c.execute(sql, (getenv("HOME_ORG_SID"), ))
        else:
            sql = "SELECT * FROM members WHERE Org = ? AND Rank = ? ORDER BY Stars DESC, Handle ASC"
            print(rank)
            self.c.execute(sql, (getenv("HOME_ORG_SID"), rank))
        members = self.c.fetchall()
        
        return members

    def select_org_members(self):
        sql = "SELECT * FROM members"
        self.c.execute(sql)

        return self.c.fetchall()

    def select_member_by_Handle(self, handle:str):
        sql = "SELECT * FROM members WHERE Handle = ?"
        self.c.execute(sql, (handle, ))

        return self.c.fetchone()

    def select_pid(self, PID):
        sql_check = "SELECT Handle FROM members WHERE PID = ?"
        self.c.execute(sql_check, (PID, ))
        
        return self.c.fetchall()

    def select_handle_name(self, pid) -> str:
        sql = "SELECT Handle FROM members WHERE Org = ? AND PID = ?"
        self.c.execute(sql, (getenv("HOME_ORG_SID"), pid))
        return self.c.fetchone()[0]

    def select_registered(self) -> list[str]:
        sql = "SELECT Handle FROM members WHERE Org = ? AND PID != ?"
        self.c.execute(sql, (getenv("HOME_ORG_SID"), "NULL"))

        return [i[0].lower() for i in self.c.fetchall()]

    def select_registered_ids(self):
        sql = "SELECT PID FROM members WHERE Org = ? AND PID != ?"
        self.c.execute(sql, (getenv("HOME_ORG_SID"), "NULL"))

        return [i[0] for i in self.c.fetchall()]

    def update_member_all(self, handle, member):
        sql = "UPDATE members Set Display = ?, Image = ?, Rank = ?, Stars = ? WHERE Handle = ?"
        self.c.execute(sql, (member['display'], member['image'], member['rank'], member['stars'], handle))


    def update_member(self, k, v):
        sql = "UPDATE members Set PID = ? WHERE Handle = ?"
        self.c.execute(sql, (v, k))

    def update_versions(self, new_versions):
        sql_delete = "DELETE FROM versions"
        self.c.execute(sql_delete)

        sql_insert = "INSERT INTO versions (Version) VALUES (?)"
        for version in new_versions:
            self.c.execute(sql_insert, (version, ))

    def update_org(self, org: dict, name: str = getenv("HOME_ORG_SID")):
        sql = "UPDATE orgs Set Headline = ?, MemberCount = ?, Logo = ?, URL = ? WHERE SID = ?"
        self.c.execute(sql, (org['headline']['plaintext'], org['members'], org['logo'], org['url'], name))

    def update_categories(self, new_categories):
        sql_delete = "DELETE FROM categories"
        self.c.execute(sql_delete)

        sql_insert = "INSERT INTO categories (Category) VALUES (?)"
        for category in new_categories:
            self.c.execute(sql_insert, (category, ))



# ================================================================================================================================



class extraDBConnect():
    def __init__(self, db_name: str = "extras.db"):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def insert_poems(self, title, author, poem):
        sql = "INSERT INTO poems (Title, Author, Poem) VALUES (?, ?, ?)"
        self.c.execute(sql, (title, author, poem))

    def select_poems(self):
        sql = "SELECT * FROM poems"
        self.c.execute(sql)
        return self.c.fetchall()
import psycopg2
from api import app
import os


class Config:
    def __init__(self):
        if app.config['TESTING'] is not True:
            DATABASE_URL = os.environ['DATABASE_URL']
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cur = self.conn.cursor()
            sql_create_tables_users = """ CREATE  TABLE IF NOT EXISTS users(user_no SERIAL NOT NULL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL , user_name VARCHAR(255) NOT NULL, user_password text NOT NULL);"""

            sql_create_tables_entries = """ CREATE TABLE IF NOT EXISTS entries(entry_id SERIAL NOT NULL  PRIMARY KEY ,
              entry_date VARCHAR(255) NOT NULL , entry_title VARCHAR(255) NOT NULL , entry_description text NOT NULL,
              author_id VARCHAR(255) NOT NULL);"""

            self.cur.execute(sql_create_tables_users)
            self.cur.execute(sql_create_tables_entries)
            self.conn.commit()

        else:
            self.conn = psycopg2.connect(host='localhost', user='postgres',
                                         password='root', dbname='test_db')
            self.cur = self.conn.cursor()
            sql_create_tables_users = """ CREATE  TABLE IF NOT EXISTS users(user_no SERIAL NOT NULL PRIMARY KEY,
               user_id VARCHAR(255) NOT NULL , user_name VARCHAR(255) NOT NULL, user_password text NOT NULL);"""

            sql_create_tables_entries = """ CREATE TABLE IF NOT EXISTS entries(entry_id SERIAL NOT NULL  PRIMARY KEY ,
                 entry_date VARCHAR(255) NOT NULL , entry_title VARCHAR(255) NOT NULL , entry_description text NOT NULL,
                 author_id VARCHAR(255) NOT NULL);"""
            sql = """INSERT INTO entries(entry_date,entry_title,entry_description, author_id)
            VALUES('1-08-18','Alice in never land','Alice:How long is forever? White Rabbit:Sometimes,
            just one second.', '9d3f8598-3be5-493c-b993-107486ef8844');"""

            self.cur.execute(sql_create_tables_users)
            self.cur.execute(sql_create_tables_entries)
            self.cur.execute(sql)
            self.conn.commit()

    def drop_users(self):
        sql = """drop table users;"""
        self.cur.execute(sql)
        self.conn.commit()

    def drop_entries(self):
        sql = """drop table entries"""
        self.cur.execute(sql)
        self.conn.commit()


class Entries(Config):
    def __init__(self):
        Config.__init__(self)

    def insert_new_entry(self, new_date, title, description, author_id):
        """A function to create a new user to the database"""
        sql = """INSERT INTO entries(entry_date,
            entry_title,entry_description, author_id) VALUES(%s,%s,%s,%s);"""
        # make the query
        self.cur.execute(sql, (new_date, title, description, author_id))
        # commit the changes to the database
        self.conn.commit()

    def get_all_entries(self):
        """A function to get a single user from the database"""
        sql = """SELECT * FROM entries;"""
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def get_all_entries_by_id(self, author_id):
        """A function to get a single user from the database"""
        sql = """SELECT * FROM entries where author_id=%s;"""
        self.cur.execute(sql, (author_id,))
        result = self.cur.fetchall()
        return result

    def get_single_entry(self, entry_id):
        """A function to get a single entry from the database"""
        sql = """SELECT * FROM entries where entry_id= %s;"""
        self.cur.execute(sql, (entry_id,))
        result = self.cur.fetchall()
        return result

    def update_single_data(self, title, description, entry_id):
        """  this is for updating a data entry"""
        sql = """UPDATE entries SET entry_title = %s, entry_description= %s WHERE entry_id = %s;"""
        self.cur.execute(sql, (title, description, entry_id,))
        self.conn.commit()


class Users(Config):
    def __init__(self):
        Config.__init__(self)

    def get_all_user(self):
        """A function to get a single user from the database"""
        sql = """SELECT * FROM users;"""
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def insert_new_user(self, u_id, name, password):
        """A function to create a new user to the database"""
        sql = """INSERT INTO users(user_id, user_name,user_password)VALUES(%s,%s,%s);"""
        # make the query
        self.cur.execute(sql, (u_id, name, password))
        self.conn.commit()
        return "new data has been inserted"

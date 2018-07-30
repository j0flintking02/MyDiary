from config import db_connection as conn


class Entries:
    def __init__(self):
        self.conn = conn
        self.cur = self.conn.cursor()

    def insert_new_entry(self, new_date, title, description, author_id):
        """A function to create a new user to the database"""
        sql = """INSERT INTO my_diary.public.entries(entry_date,
        entry_title,entry_description, author_id) VALUES(%s,%s,%s,%s);"""
        # make the query
        self.cur.execute(sql, (new_date, title, description, author_id))
        # commit the changes to the database
        self.conn.commit()
        # close communication with the database
        # self.cur.close()
        # close the connection

    def get_all_entries(self, author_id):
        """A function to get a single user from the database"""
        sql = """SELECT * FROM my_diary.public.entries where author_id=%s;"""
        self.cur.execute(sql, (author_id,))
        result = self.cur.fetchall()
        # close communication with the database
        # self.cur.close()
        # close the connection
        return result

    def get_single_entry(self, entry_id):
        """A function to get a single entry from the database"""
        sql = """SELECT * FROM my_diary.public.entries where entry_id= %s;"""
        self.cur.execute(sql, (entry_id,))
        result = self.cur.fetchall()
        # close communication with the database
        # self.cur.close()
        # close the connection
        return result

    def update_single_data(self, title, description, entry_id):
        """  this is for updating a data entry"""
        sql = """UPDATE entries SET entry_title = %s, entry_description= %s WHERE entry_id = %s;"""
        self.cur.execute(sql, (title, description, entry_id,))
        self.conn.commit()
        # self.cur.close()


class Users:
    def __init__(self):
        self.conn = conn
        self.cur = self.conn.cursor()

    def get_all_user(self):
        """A function to get a single user from the database"""
        sql = """SELECT * FROM my_diary.public.users;"""
        self.cur.execute(sql)
        result = self.cur.fetchall()
        # close communication with the database
        # self.conn.close()
        # close the connection
        return result

    def insert_new_user(self, u_id, name, password):
        """A function to create a new user to the database"""
        sql = """INSERT INTO my_diary.public.users(user_id, user_name,user_password)VALUES(%s,%s,%s);"""
        # make the query
        self.cur.execute(sql, (u_id, name, password))
        self.conn.commit()
        # close communication with the database
        # self.cur.close()
        # close the connection
        return "new data has been inserted"



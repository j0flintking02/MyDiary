def insert_new_user(conn, u_id, name, password):
    """A function to create a new user to the database"""
    sql = """INSERT INTO my_diary.public.users(user_id, user_name,user_password)VALUES(%s,%s,%s);"""
    cur = conn.cursor()
    # make the query
    cur.execute(sql, (u_id, name, password))
    # u_id = cur.fetchone()[0]
    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()
    # close the connection


def get_all_user(conn):
    """A function to get a single user from the database"""
    sql = """SELECT * FROM my_diary.public.users;"""
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    # close communication with the database
    cur.close()
    # close the connection
    return result


def insert_new_entry(conn, new_date, title, description, author_id):
    """A function to create a new user to the database"""
    sql = """INSERT INTO my_diary.public.entries(entry_date, entry_title,entry_description, author_id)
          VALUES(%s,%s,%s,%s);"""

    cur = conn.cursor()
    # make the query
    cur.execute(sql, (new_date, title, description, author_id))

    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()
    # close the connection


def get_all_entries(conn, author_id):
    """A function to get a single user from the database"""
    sql = """SELECT * FROM my_diary.public.entries where author_id=%s;"""
    cur = conn.cursor()
    cur.execute(sql,(author_id,))
    result = cur.fetchall()
    # close communication with the database
    cur.close()
    # close the connection
    return result


def get_single_entry(conn, entry_id):
    """A function to get a single entry from the database"""
    sql = """SELECT * FROM my_diary.public.entries where entry_id= %s;"""
    cur = conn.cursor()
    cur.execute(sql, (entry_id,))
    result = cur.fetchall()
    # close communication with the database
    cur.close()
    # close the connection
    return result


def update_single_data(conn, title, description, entry_id):
    sql = """UPDATE entries SET entry_title = %s, entry_description= %s WHERE entry_id = %s;"""
    cur = conn.cursor()
    cur.execute(sql, (title, description, entry_id,))
    conn.commit()
    cur.close()

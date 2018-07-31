import psycopg2
from api import app

if not app.config['TESTING']:
    db_connection = psycopg2.connect(host='localhost', user='postgres',
                                     password='root', dbname='my_diary')
    cur = db_connection.cursor()
    sql_create_tables_users = """ CREATE  TABLE IF NOT EXISTS users(user_no SERIAL NOT NULL PRIMARY KEY, 
    user_id VARCHAR(255) NOT NULL , user_name VARCHAR(255) NOT NULL, user_password text NOT NULL);"""

    sql_create_tables_entries = """ CREATE TABLE IF NOT EXISTS entries(entry_id SERIAL NOT NULL  PRIMARY KEY , 
      entry_date VARCHAR(255) NOT NULL , entry_title VARCHAR(255) NOT NULL , entry_description text NOT NULL,
      author_id VARCHAR(255) NOT NULL);"""
    cur.execute(sql_create_tables_users)
    cur.execute(sql_create_tables_entries)
    db_connection.commit()

else:
    db_connection = psycopg2.connect(host='localhost', user='postgres',
                                     password='root', dbname='test_db')
    cur = db_connection.cursor()
    sql_create_tables_users = """ CREATE  TABLE IF NOT EXISTS users(user_no SERIAL NOT NULL PRIMARY KEY, 
       user_id VARCHAR(255) NOT NULL , user_name VARCHAR(255) NOT NULL, user_password text NOT NULL);"""

    sql_create_tables_entries = """ CREATE TABLE IF NOT EXISTS entries(entry_id SERIAL NOT NULL  PRIMARY KEY , 
         entry_date VARCHAR(255) NOT NULL , entry_title VARCHAR(255) NOT NULL , entry_description text NOT NULL,
         author_id VARCHAR(255) NOT NULL);"""
    cur.execute(sql_create_tables_users)
    cur.execute(sql_create_tables_entries)
    db_connection.commit()

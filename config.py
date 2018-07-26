import psycopg2

hostname = 'localhost'
username = 'postgres'
password = 'root'
database = 'my_diary'

db_connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

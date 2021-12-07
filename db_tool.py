import json
import os
import sqlite3


sql_create_author_table = """CREATE TABLE IF NOT EXISTS author (
                        id integer PRIMARY KEY AUTOINCREMENT, 
                        author_name text NOT NULL, 
                        author_email text NOT NULL, 
                        author_github text NOT NULL
                    );"""

sql_create_comments_table = """CREATE TABLE IF NOT EXISTS comments (
                id integer PRIMARY KEY AUTOINCREMENT,
                comments text NOT NULL
                );"""

sql_create_device_table = """CREATE TABLE IF NOT EXISTS device (
                id integer PRIMARY KEY AUTOINCREMENT,
                device_type text NOT NULL,
                device_vendor text NOT NULL,
                device_url text NOT NULL
                );"""

sql_create_os_table = """CREATE TABLE IF NOT EXISTS os (
            id integer PRIMARY KEY AUTOINCREMENT,
            os_name text NOT NULL,
            os_version text NOT NULL,
            os_class text NOT NULL,
            os_vendor text NOT NULL,
            os_url text NOT NULL
            );"""

sql_create_version_table = """CREATE TABLE IF NOT EXISTS version (
                id integer PRIMARY KEY AUTOINCREMENT,
                version_rev	integer NOT NULL,
                version_date text NOT NULL
                );"""

sql_create_signature_table = """CREATE TABLE IF NOT EXISTS "signature" (
                id integer PRIMARY KEY AUTOINCREMENT,
                acid text NOT NULL,
                tcp_flag text NOT NULL,
                tcp_sig	text NOT NULL,
                sig_os integer NOT NULL,
                sig_version	integer NOT NULL,
                sig_author	integer NOT NULL,
                sig_name text NOT NULL,
                sig_comments integer NOT NULL,
                FOREIGN KEY("sig_os") REFERENCES "os"("id"),
                FOREIGN KEY("sig_version") REFERENCES "version"("id"),
                FOREIGN KEY("sig_comments") REFERENCES "comments"("id")
                );"""




db_name = "signatures.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn



def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)




def main():
    conn = create_connection(db_name)
    if conn is not None:
        # create author table
        create_table(conn, sql_create_author_table)
        create_table(conn, sql_create_comments_table)
        create_table(conn, sql_create_device_table)
        create_table(conn, sql_create_os_table)
        create_table(conn, sql_create_version_table)
        create_table(conn, sql_create_signature_table)
        





if __name__ == "__main__":
    main()


'''
P
f = open('signature.json')
data = json.load(f)

for i in data['signature_list']:
    print(i)

f.close()

'''
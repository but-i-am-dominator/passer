import json
import os
import sqlite3


sql_create_author_table = """CREATE TABLE IF NOT EXISTS author (
                        id integer PRIMARY KEY AUTOINCREMENT, 
                        author_name text NOT NULL, 
                        author_email text NOT NULL, 
                        author_github text NOT NULL
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
                version_date text NOT NULL,
                version_name text NOT NULL
                );"""

sql_create_signature_table = """CREATE TABLE IF NOT EXISTS "signature" (
                id integer PRIMARY KEY AUTOINCREMENT,
                sig_name text NOT NULL,
                acid text NOT NULL,
                tcp_flag text NOT NULL,
                tcp_sig	text NOT NULL,
                sig_os integer NOT NULL,
                sig_version	integer NOT NULL,
                sig_author	integer NOT NULL,
                sig_device integer NOT NULL,
                sig_comments text NOT NULL,
                FOREIGN KEY("sig_os") REFERENCES "os"("id"),
                FOREIGN KEY("sig_version") REFERENCES "version"("id"),
                FOREIGN KEY("sig_author") REFERENCES "author"("id"),
                FOREIGN KEY("sig_device") REFERENCES "device"("id")
                );"""

sql_insert_author = "INSERT INTO author (author_name, author_email, author_github) values (?, ?, ?)"
sql_insert_os = "INSERT INTO os (os_name, os_version, os_class, os_vendor, os_url) values (?, ?, ?, ?, ?)"
sql_insert_device = "INSERT INTO device (device_type, device_vendor, device_url) values (?, ?, ?)"
sql_insert_version = "INSERT INTO version (version_rev, version_date, version_name) values (?, ?, ?)"
sql_insert_signature = "INSERT INTO signature (acid, tcp_flag, tcp_sig, sig_os, sig_version, sig_author, sig_device, sig_name, sig_comments) values (?, ?, ?, ?, ?, ?, ?, ?, ?)"

sql_select_acid = "SELECT id FROM signature WHERE acid=?;"
sql_select_author = "SELECT id FROM author WHERE author_name=? AND author_email=?;"
sql_select_os = "SELECT id FROM os WHERE os_name=? AND os_version=?;"
sql_select_device = "SELECT id FROM device WHERE device_type=? AND device_vendor=?;"
sql_select_version = "SELECT id FROM version WHERE version_name=?;"



db_name = "signatures.db"
json_file = "signature.json"


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
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return: True
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)
    return True


def read_json(json_file):
    """ reads a json file
    :param json_file: string name of local json file
    :return: list of dictionary objects created from json file
    """
    f = open(json_file)
    data = json.load(f)
    f.close()
    return data['signature_list']


def insert_signature(db_file, sig_obj):
    """ inserts dictionary object into database
    :param db_file: string name of sqlite3 db file
    :param sig_obj: signature object - dictionary of values 
    :return: True
    """
    conn = sqlite3.connect(db_file)
    conn.execute("BEGIN TRANSACTION")
    for i in sig_obj['signatures']:
        acid = conn.execute(sql_select_acid, (i['acid'],)).fetchall()
        version = conn.execute(sql_select_version, (sig_obj['version']['name'],)).fetchall()
        
        # If signature exists
        if len(acid) == 1 and len(version) == 1:
            pass
        else:
            author = conn.execute(sql_select_author, (sig_obj['author']['name'], sig_obj['author']['email'],)).fetchall()
            os = conn.execute(sql_select_os, (sig_obj['os']['name'], sig_obj['os']['version'],)).fetchall()
            device = conn.execute(sql_select_device, (sig_obj['device']['type'], sig_obj['device']['vendor'],)).fetchall()
            
            if (len(author) == 0):
                author_insert = conn.execute(sql_insert_author,(sig_obj['author']['name'], sig_obj['author']['email'], sig_obj['author']['github']))
                conn.commit()
                # lastrow id  .lastrowid
 
            if (len(os) == 0):
                os_insert = conn.execute(sql_insert_os, (sig_obj['os']['name'], sig_obj['os']['version'], sig_obj['os']['class'], sig_obj['os']['vendor'], sig_obj['os']['url']))
                conn.commit()

            if (len(device) == 0):
                device_insert = conn.execute(sql_insert_device, (sig_obj['device']['type'], sig_obj['device']['vendor'], sig_obj['device']['url']))
                conn.commit()

            if (len(version) == 0):
                version_insert = conn.execute(sql_insert_version, (sig_obj['version']['rev'], sig_obj['version']['date'], sig_obj['version']['name']))
                conn.commit()

            conn.execute(sql_insert_signature, (i['acid'], i['tcp_flag'], i['tcp_sig'], os_insert.lastrowid, version_insert.lastrowid, author_insert.lastrowid, device_insert.lastrowid, sig_obj['version']['name'], i['comments']))
            conn.commit()
    conn.close()
    return True


def main():
    """ Main Function"""
    conn = create_connection(db_name)
    if conn is not None:
        create_table(conn, sql_create_author_table)       # create author table
        create_table(conn, sql_create_device_table)       # create device table
        create_table(conn, sql_create_os_table)           # create os table
        create_table(conn, sql_create_version_table)      # create version table
        create_table(conn, sql_create_signature_table)    # create signature table
        
    data = read_json(json_file)                           # reads json file into a dictionary
    
    for i in data:
        insert_signature(db_name, i)                      # moves dictionary into sqlite3 db
    

if __name__ == "__main__":
    main()
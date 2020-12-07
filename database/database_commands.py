import sqlite3
import datetime as dt
import re

DATABASE_PATH = 'database/local_database.db' #localmente
#Database functions:
def connect_to_user_database():
     con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
     con.close()

def create_user_database():
     con = sqlite3.connect(DATABASE_PATH)
     con.close()

def create_tables():
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    with open('database/database_schema.sql') as f:
        script = f.read()
        cur = con.cursor()
        cur.executescript(script)
    con.close()

#Modify user:

def get_user():
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    cur = con.cursor()
    cur.execute('''
    SELECT * FROM user
    ''')
    result = cur.fetchall()
    con.close()
    return result

def add_user(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO user(name, birth_date) VALUES (?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

def edit_user(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        UPDATE user SET name = ?, birth_date = ?
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

#Modify Tasks:
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_tasks():
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    con.row_factory = dict_factory
    cur = con.cursor()
    cur.execute('''
    SELECT task_id, creation_date, difficulty, description, name, importance, total_hours, deadline, daily_hours FROM task WHERE is_finished = 0
    ''')
    result = cur.fetchall()
    con.close()
    return result

def add_normal_task(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO task (name, description, deadline, 
        importance, daily_hours, frequency) VALUES (?, ?, ?, ?, ?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

def add_book(task_value, book_value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO task (name, description, deadline, 
        importance, daily_hours, frequency) VALUES (?, ?, ?, ?, ?, ?)
        ''', task_value)
        con.commit()
        cur.execute('''
        SELECT last_insert_rowid();
        ''')
        task_id = cur.fetchall()
        cur.execute('''
        INSERT INTO task_book (task_id, book_name, publisher, total_pages, edition, volume, author) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', task_id[0] + book_value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

def finish_task(task_id):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        UPDATE task SET is_finished = ? WHERE task_id = ?
        ''', (1, task_id))
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

#Modify Sessions:
def add_session(value):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO session (user_id, task_id, start_time, end_time) VALUES (?, ?, ?, ?)
        ''', value)
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()

def add_task_time(task_id, total_hours):
    con = sqlite3.connect('file:' + DATABASE_PATH + '?mode=rw', uri=True)
    try:
        cur = con.cursor()
        cur.execute('''
        UPDATE task SET total_hours = total_hours + ? WHERE task_id = ? 
        ''', (total_hours, task_id))
        con.commit()
    except:
        print("Operation failed.")
        con.rollback()
    finally:
        con.close()



#Auxiliary functions:

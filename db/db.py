# file contains db connection and operations

import sqlite3
from config import *
from datetime import datetime, timedelta

DATABASE = os.path.join(PROJECT_ROOT, 'db', 'mydb')

# Create a database in RAM
# db = sqlite3.connect(':memory:') # we did not use this as this only stores temporary data

# Creates or opens a file called mydb with a SQLite3 DB
db = sqlite3.connect(DATABASE)
try:
    cursor = db.cursor()
    cursor.execute('''
                   create table if not exists users(id INTEGER PRIMARY KEY, name TEXT,
                   phone TEXT, email TEXT unique, password TEXT);
                   ''')
    cursor.execute('''
                   create table if not exists notifications(id INTEGER PRIMARY KEY, name TEXT unique,
                   email TEXT, userId integer, created_at datetime, scheduled_at datetime,status varchar, foreign key(userId) references users(id));
                   ''')
    # cursor.execute('''
    # delete from users;
    # ''')
    # cursor.execute('''
    # delete from notifications;
    # ''')
    # cursor.execute('''
    # alter table notifications add created_at datetime;
    # ''')
    # cursor.execute('''
    #     alter table notifications add scheduled_at datetime;
    #     ''')
    # cursor.execute('''
    #         alter table notifications add status varchar;
    #     ''')

    db.commit()
except Exception as e:
    print("exception occurred", e)
    db.rollback()
    print("rollback successfully")
    raise e
finally:
    db.close()


def get_record(sql_query, user=None):
    record_exists = False
    try:
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        print(user.email)
        if user is not None:
            cursor.execute(sql_query, (user.email,))
        else:
            cursor.execute(sql_query)
        record = cursor.fetchone()
        print(record)
        if record is not None:
            record_exists = True
    except Exception as e:
        print("exception occurred", e)
        db.rollback()
        print("rollback successfully")
        raise e
    finally:
        db.close()
        return record_exists, record


def create_user_record(sql_query, user):
    record_created = False
    try:
        print("email is - ", user.email)
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.execute(sql_query, {'name': user.name, 'phone': '', 'email':user.email, 'password':user.password})
        cursor.execute('''select email from users where email=?''', (user.email,))
        record = cursor.fetchone()
        print(record)
        if record is not None:
            record_created = True
            db.commit()
    except Exception as e:
        print("exception occurred", e)
        db.rollback()
        print("rollback successfully")
        raise e
    finally:
        db.close()
        return record_created


def login(sql_query, user):
    record_exists = False
    try:
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        print(user.email)
        cursor.execute(sql_query, (user.email, user.password))
        record = cursor.fetchone()
        print(record)
        if record is not None:
            record_exists = True
    except Exception as e:
        print("exception occurred", e)
        db.rollback()
        print("rollback successfully")
        raise e
    finally:
        db.close()
        return record_exists


def create_notification_record(sql_query, notify, user):
    record_created = False
    try:
        print("email id is - ", notify.user_id)
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        notify_name = str(notify.user_id) + str(datetime.now())
        cursor.execute(sql_query, {'name': notify_name, 'email':user.email, 'created_at': datetime.now(),
                                   'scheduled_at': datetime.now() + timedelta(seconds=notify.duration),
                                   'userId': notify.user_id, 'status': notify.status})
        print("Executed notify record")
        cursor.execute('''select name from notifications where name=?''', (notify_name,))
        record = cursor.fetchone()
        print(record)
        if record is not None:
            record_created = True
            db.commit()
    except Exception as e:
        print("exception occurred", e)
        db.rollback()
        print("rollback successfully")
        raise e
    finally:
        db.close()
        return record_created, record

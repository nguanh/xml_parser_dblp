import mysql.connector
from mysql.connector import errorcode


#TODO das ganze als Klasse verpacken

def create_database(cursor,name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def connect(database = None):
    if(database is None):
        return mysql.connector.connect(user='root', password='master',
                                        host='127.0.0.1')
    return mysql.connector.connect(user='root', password='master',
                                   host='127.0.0.1', database=database)

def createDB(connector,cursor,name):
    # try to change to DB  DB_NAME
    try:
        connector.database = name
    except mysql.connector.Error as err:
        # if there is no such db, create DB and change afterwards
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, name)
            connector.database = name
        else:
            print(err)
            exit(1)


def createTable(name,cursor,query):

        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
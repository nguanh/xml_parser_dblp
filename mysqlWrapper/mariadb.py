import mysql.connector
from mysql.connector import errorcode



class MariaDb:
    #TODO test

    def __init__(self, credentials):
        self.query = None
        if "database" in credentials:
            self.current_database = credentials["database"]
        else:
            self.current_database = None

        try:
            self.connector = mysql.connector.connect(**credentials)
        except mysql.connector.Error as err:
            raise Exception("MariaDB connection error: {}".format(err))

        if self.connector is not None:
            self.cursor = self.connector.cursor()

    def create_database(self, name):
        try:
            self.cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

    def create_db(self, name):

        # try to change to DB  DB_NAME
        try:
            self.connector.database = name
            self.current_database = name
        except mysql.connector.Error as err:
        # if there is no such db, create DB and change afterwards
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(name)
                self.connector.database = name
            else:
                print(err)

    def createTable(self, name, query):

        try:
            print("Creating table {}: ".format(name), end='')
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
                return True
            else:
                return False
        else:
            return True

    def set_query(self, query):
        self.query = query

    def execute(self,tup):
        if self.query is None:
            raise Exception("query not set")
        try:
            self.cursor.execute(self.query, tup)
            self.connector.commit()
        except mysql.connector.Error as err:
            raise Exception("MariaDB query error: {} File not added".format(err))

    def close_connection(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connector is not None:
            self.connector.close()
        print("Connection closed")

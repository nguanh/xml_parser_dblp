from mysqlWrapper.mariadb import MariaDb
from conf.config import get_config
import datetime
from pub_storage.setup_database import setup_database
import csv


def get_table_data(table,database, null_dates = True):
    credentials = dict(get_config("MARIADB"))
    # connect to database
    connector = MariaDb(credentials)
    connector.connector.database = database
    # fetch everything
    query = "SELECT * FROM {}".format(table)
    connector.cursor.execute(query)
    result = []
    for dataset in connector.cursor:
        tmp = []
        for element in dataset:
            # overwrite timestamps with generic date for easier testing
            if null_dates and isinstance(element,datetime.datetime):
                tmp.append(datetime.datetime(1990,1,1,1,1,1))
            else:
                tmp.append(element)
        result.append(tmp)
    return result


def compare_tables(self, comp_object,database):
    for key,value in comp_object.items():
        self.assertEqual(get_table_data(key, database), value)


def delete_database(database):
    credentials = dict(get_config("MARIADB"))
    # connect to database
    connector = MariaDb(credentials)
    connector.connector.database = database
    connector.execute_ex("DROP DATABASE {}".format(database))


def setup_tables(filename, database, table_query, insert_query):
    # load testconfig
    credentials = dict(get_config("MARIADB"))
    # setup database
    connector = MariaDb(credentials)
    connector.create_db(database)
    connector.connector.database = database
    connector.createTable("test dblp table", table_query)

    # setup test ingester database
    setup_database(database)
    # import records from csv
    with open(filename, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        do_once = False
        for row in spamreader:
            # remove last updated and harvest date
            del row[-2:]
            # skip first line
            if do_once is True:
                tup = tuple(map(lambda x: x if x != "" else None, row))
                connector.execute_ex(insert_query, tup)
            else:
                do_once = True
    connector.close_connection()


from mysqlWrapper.mariadb import MariaDb
from conf.config import get_config
import datetime

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
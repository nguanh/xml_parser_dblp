from dblp.queries import DBLP_ARTICLE
from mysqlWrapper.mariadb import MariaDb

DB_NAME = 'dblp'
credentials = {
    'user': 'root',
    'password': 'master',
    'host': '127.0.0.1',
}

try:
    database = MariaDb(credentials)
except Exception as err:
    print(err)
else:
    database.create_db(DB_NAME)
    database.createTable("article", DBLP_ARTICLE)
    database.close_connection()







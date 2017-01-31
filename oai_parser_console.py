from mysqlWrapper.mariadb import MariaDb
from oai.oaimph_parser import harvestOAI
credentials = {
    'user': 'root',
    'password': 'master',
    'host': '127.0.0.1',
    'database': 'oaimph',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}
link ='http://citeseerx.ist.psu.edu/oai2'

try:
    database = MariaDb(credentials)
except Exception as err:
    print(err)
else:
    x = harvestOAI(link, database)


'''
citeseerx hat publikationen ohne autoren

'''
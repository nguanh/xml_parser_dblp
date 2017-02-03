from mysqlWrapper.mariadb import MariaDb
from oai.oaimph_parser import harvestOAI
from oai.arxiv_handler import parse_arxiv
credentials = {
    'user': 'root',
    'password': 'master',
    'host': '127.0.0.1',
    'database': 'oaimph',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}
link ='http://citeseerx.ist.psu.edu/oai2'
link2 = 'http://export.arxiv.org/oai2'
link3 = 'http://elis.da.ulcc.ac.uk/cgi/oai2'

try:
    database = MariaDb(credentials)
except Exception as err:
    print(err)
else:
    x = harvestOAI(link2, database, processing_function=parse_arxiv, format="arXiv")


'''
citeseerx hat publikationen ohne autoren

'''
from mysqlWrapper.mariadb import MariaDb
from oai.oaimph_parser import harvestOAI
from oai.arxiv_handler import parse_arxiv,ArXivRecord
from oai.queries import ARXIV_ARTICLE,ADD_ARXIV
credentials = {
    'user': 'root',
    'password': 'master',
    'host': '127.0.0.1',
    'database': 'harvester',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}
link ='http://citeseerx.ist.psu.edu/oai2'
link2 = 'http://export.arxiv.org/oai2'
link3 = 'http://elis.da.ulcc.ac.uk/cgi/oai2'

try:
    database = MariaDb(credentials)
    database.createTable("arxiv_articles",ARXIV_ARTICLE)
except Exception as err:
    print(err)
else:
    x = harvestOAI(link2, database, processing_function=parse_arxiv, parsing_class=ArXivRecord, xml_format="arXiv", query=ADD_ARXIV)


'''
citeseerx hat publikationen ohne autoren

'''
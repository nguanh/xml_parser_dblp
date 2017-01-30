from dblp.xml_parser import parse_xml
from mysqlWrapper.mariadb import  MariaDb


xml_path = "/home/nguyen/raw_file/dblp.xml"
xml_path = "dblp.xml"
#xml_path = 'tests/files/valid-title4.xml'
dtd_path ="/home/nguyen/raw_file/dblp.dtd"
dtd_path = "dblp.dtd"

credentials = {
    'user': 'root',
    'password': 'master',
    'host': '127.0.0.1',
    'database': 'dblp',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

try:
    database = MariaDb(credentials)
except Exception as err:
    print(err)
else:
    x=parse_xml(xml_path,dtd_path,database,("article","inproceedings"))


    # articles count 40841 ?
    # 5422465
    # TODO proceedings sind nur die konferenzen und brauchen nicht übernommen zu werden?
    # TODO www enthalten autoren websites

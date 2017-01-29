from dblp.xml_parser import parse_xml
from mysqlWrapper.mariadb import  MariaDb




xml_path = "dblp.xml"
dtd_path ="dblp.dtd"
credentials = {
    'user': 'root',
    'password': 'master',
    'host': '127.0.0.1',
    'database': 'dblp',
}

try:
    database = MariaDb(credentials)
except Exception as err:
    print(err)
else:
    x=parse_xml(xml_path,dtd_path,database,"article", "01-01-1991","01-01-1991")


    # articles count 40841 ?
    # 5422465
    # TODO proceedings sind nur die konferenzen und brauchen nicht übernommen zu werden?
    # TODO www enthalten autoren websites

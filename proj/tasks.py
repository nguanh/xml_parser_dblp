from __future__ import absolute_import, unicode_literals
from .celery import app
from dblp.xml_parser import parse_xml
from mysqlWrapper.mariadb import  MariaDb



@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task
def hello_world(x):
    print(x)


@app.task
def test(arg):
    print("FANKAR")
    with open('workfile.txt', 'a') as f:
        f.write(arg)
    return "GRAMMAR"

@app.task
def parse_dblp():
    xml_path = "/home/nguyen/raw_file/dblp.xml"
    dtd_path ="/home/nguyen/raw_file/dblp.dtd"
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
        x = parse_xml(xml_path, dtd_path, database, ("article", "inproceedings"))
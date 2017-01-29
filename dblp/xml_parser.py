from lxml import etree
from mysqlWrapper.mariadb import MariaDb
import os
from queries import ADD_DBLP_ARTICLE
from .helper import parse_mdate, parse_year, dict_to_tuple
import datetime

COMPLETE_TAG_LIST = (
"article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person",
"data")


def parse_xml(xmlPath, dtdPath, sql_connector, tagList=COMPLETE_TAG_LIST, startDate=None, endDate=None):
    # validate parameters
    if isinstance(tagList, (str, tuple)) is False:
        print("Error: Invalid tagList")
        return False
    try:
        datetime.datetime.strptime(startDate, '%d-%m-%Y')
    except ValueError:
        if isinstance(startDate, datetime) is False:
            print("Error: Invalid start date")
            return False

    try:
        datetime.datetime.strptime(endDate, '%d-%m-%Y')
    except ValueError:
        if isinstance(endDate, datetime) is False:
            print("Error: Invalid start date")
            return False

    if os.path.isfile(xmlPath) is False:
        print("Error: invalid xml path")
        return False
    if os.path.isfile(dtdPath) is False:
        print("Error: invalid dtd path")
        return False
    if isinstance(sql_connector, MariaDb) is False:
        print("Error: Invalid sql_connector instance")
        return False

    # init values
    count = 0
    etree.DTD(file=dtdPath)

    # iterate through XML
    for event, element in etree.iterparse(xmlPath, tag=tagList, load_dtd=True):

        count += 1
        dataset = {
            'key': element.get('key'),
            'mdate': parse_mdate(element.get('mdate')),
            'title': ''
        }
        author_csv_list = ''
        #TODO include start and enddate
        # iterate through elements of block
        for child in element:
            if child.tag == 'author':
                # stores authors as csv
                author_csv_list += child.text + ";"
            elif child.tag == 'year':
                dataset[child.tag] = parse_year(child.text)
            elif child.tag == 'title' and child.text is None:
                for x in child:
                    dataset[child.tag] += x.text.strip() + " " + x.tail.strip()
            else:
                dataset[child.tag] = str(child.text).strip()

        dataset['author'] = author_csv_list
        tup = dict_to_tuple(dataset)

        print(count, ":", element.get('key'), end=' ')
        if sql_connector.execute(ADD_DBLP_ARTICLE, tup):
            print(' added')
        element.clear()

    print("Final Count :", count)
    sql_connector.close_connection()
    return True

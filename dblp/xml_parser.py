import datetime
import os

from lxml import etree

from dblp.queries import ADD_DBLP_ARTICLE
from mysqlWrapper.mariadb import MariaDb
from .helper import parse_mdate, parse_year, dict_to_tuple

COMPLETE_TAG_LIST = (
"article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person",
"data")

#TODO create tables?
#TODO include more types like inproceedings
def parse_xml(xmlPath, dtdPath, sql_connector, tagList=COMPLETE_TAG_LIST, startDate=None, endDate=None):
    # validate parameters
    if isinstance(tagList, (str, tuple)) is False:
        print("Error: Invalid tagList")
        return False,0
    if startDate is not None:
        try:
            datetime.datetime.strptime(startDate, '%Y-%m-%d')
            start = parse_mdate(startDate)
        except:
            if isinstance(startDate, datetime.datetime) is False:
                print("Error: Invalid start date")
                return False,0
            else:
                start = startDate
    if endDate is not None:
        try:
            datetime.datetime.strptime(endDate, '%Y-%m-%d')
            end = parse_mdate(endDate)
        except:
            if isinstance(endDate, datetime.datetime) is False:
                print("Error: Invalid end date")
                return False, 0
            else:
                end = endDate

    if os.path.isfile(xmlPath) is False:
        print("Error: invalid xml path")
        return False, 0
    if os.path.isfile(dtdPath) is False:
        print("Error: invalid dtd path")
        return False, 0
    if isinstance(sql_connector, MariaDb) is False:
        print("Error: Invalid sql_connector instance")
        return False, 0

    # init values
    success_count = 0
    overall_count = 0
    etree.DTD(file=dtdPath)

    time_range = startDate is not None and endDate is not None



    # iterate through XML
    for event, element in etree.iterparse(xmlPath, tag=tagList, load_dtd=True):

        overall_count += 1
        # print(element.tag)
        dataset = {
            'key': element.get('key'),
            'mdate': parse_mdate(element.get('mdate')),
            'title': ''
        }

        # check date range
        if time_range:
            if (start <= dataset["mdate"] <= end) is False:
                continue

        author_csv_list = ''
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

        print(success_count, ":", element.get('key'), end=' ')
        if sql_connector.execute(ADD_DBLP_ARTICLE, tup):
            success_count += 1
            print(' added')
        element.clear()

    print("Final Count :", success_count)
    sql_connector.close_connection()
    return True,success_count

from lxml import etree
from lxml.etree import XMLSyntaxError
import sys
from queries import ADD_DBLP_ARTICLE
from mariadb_common import connect
from datetime import date, datetime, timedelta

source = sys.argv[1]
dtd = etree.DTD(file=sys.argv[2])
count = 0

# mariaDB  connection
cnx = connect('dblp')
# cursor is used to pass SQL queries
cursor = cnx.cursor()

tagList = ("article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data")
# article = inproceedings = phdthesis = masterthesis
'''
JOIN
www
proceedings ignore

'''

#TODO
def parse_mdate(obj):
    """
    :param obj:
    :return:
    """
    return date(1977, 6, 14)


#TODO
def parse_year(obj):
    """

    :param obj:
    :return:
    """
    return date(1977, 6, 14)


def dict_to_tuple(obj):
    """
    TODO validate dict
    TODO handling verschiedener parameter
    :param obj:
    :return:
    """

    if 'ee' not in obj:
        obj['ee'] = ''
        print(obj)
    if 'number' not in obj:
        obj['number'] = 0
    result = (obj['key'],obj['mdate'], obj['author'], obj['title'], obj['pages'],obj['year'],obj['volume'], obj['journal'],obj['number'], obj['ee'], obj['url'])
    return result





for event, element in etree.iterparse(source, tag='article', load_dtd=True):

    count += 1

    dataset ={
        'key'   :    element.get('key'),
        'mdate' :    parse_mdate(element.get('mdate')),
    }
    for child in element:
        if child.tag == 'author':
            dataset[child.tag] = 'TODO'
        elif child.tag =='year':
            dataset[child.tag] = parse_year(child.text)
        else:
            dataset[child.tag] = child.text
    tup = dict_to_tuple(dataset)
    print(count, end=' : ')
    print(element.get('key'))
    cursor.execute(ADD_DBLP_ARTICLE, tup)
    print(' added')
    cnx.commit()
    element.clear()

print("Final Count :", count)
cursor.close()
cnx.close()
#articles count 40841 ?
#5422465
#TODO proceedings sind nur die konferenzen und brauchen nicht übernommen zu werden?
#TODO www enthalten autoren websites



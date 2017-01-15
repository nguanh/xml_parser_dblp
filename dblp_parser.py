from lxml import etree
from lxml.etree import XMLSyntaxError
import sys
from queries import ADD_DBLP_ARTICLE
from mariadb_common import connect
from dblp_config import Dblp_Parsing_Exception
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

def parse_mdate(obj):
    """
    :param obj: string in format YYYY-MM-DD
    :return: datetime
    """
    try:
        return datetime.strptime(obj, "%Y-%m-%d")
    except ValueError:
        raise Dblp_Parsing_Exception('mdate','Invalid mdate')


def parse_year(obj):
    """
    :param obj: number containing publication year
    :return: date object, with month and day set to 1, as they are not further specified
    """
    try:
        year = int(obj)
        return date(year,1,1)
    except TypeError:
        raise Dblp_Parsing_Exception('year','Invalid year')
    except ValueError:
        raise Dblp_Parsing_Exception('year', 'Year is out of range')


def dict_to_tuple(obj):
    """
    attribute überprüfen, die zusätzlich existieren
    :param obj:
    :return:
    """
    all_attributes ={'key','mdate','author','title','ee','url','journal','number','volume','pages','year'}
    optional_attributes= ['ee','url','journal','number','volume','pages']

    #check for outlier keys
    key_list = set(obj.keys())
    diff = key_list-all_attributes
    if len(diff)> 0:
        print(obj['key'],":",diff)



    # set missing attributes as None
    for attr in optional_attributes:
        if attr not in obj:
            obj[attr] = None

    if obj['title'] is None:
        print("title missing in", obj['key'])
        obj['title'] = "Test"


    result = (obj['key'],obj['mdate'], obj['author'], obj['title'], obj['pages'],obj['year'],obj['volume'], obj['journal'],obj['number'], obj['ee'], obj['url'])
    return result





for event, element in etree.iterparse(source, tag='article', load_dtd=True):

    count += 1

    dataset ={
        'key'   :    element.get('key'),
        'mdate' :    parse_mdate(element.get('mdate')),
        'title' :    ''
    }
    author_csv_list = '';
    for child in element:
        if child.tag == 'author':
            #stores authors as csv
            dataset[child.tag] = 'TODO'
            author_csv_list += child.text + ";"
        elif child.tag =='year':
            dataset[child.tag] = parse_year(child.text)
        elif(child.tag == 'title' and child.text is None):
            for x in child:
                dataset[child.tag] += x.text.strip() + " "+x.tail.strip()
        else:
            dataset[child.tag] = str(child.text).strip()



    dataset['author']= author_csv_list
    tup = dict_to_tuple(dataset)

    print(count, end=' : ')
    print(element.get('key') ,end=' ')
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



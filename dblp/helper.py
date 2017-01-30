from datetime import date, datetime, timedelta
from .exception import Dblp_Parsing_Exception

def parse_mdate(obj):
    """
    :param obj: string in format YYYY-MM-DD
    :return: datetime
    """
    try:
        return datetime.strptime(obj, "%Y-%m-%d")
    except:
        raise Dblp_Parsing_Exception('Invalid mdate')


def parse_year(obj):
    """
    :param obj: number containing publication year
    :return: date object, with month and day set to 1, as they are not further specified
    """
    try:
        year = int(obj)
        return datetime(year,1,1)
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
    all_attributes ={'key','mdate','author','title','ee','url','journal','number','volume','pages','year',"cite", "crossref","booktitle"}
    optional_attributes= ['ee','url','journal','number','volume','pages',"cite", "crossref","booktitle"]

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


    result = (obj['key'],obj['mdate'], obj['author'], obj['title'], obj['pages'],
              obj['year'],obj['volume'], obj['journal'],obj['number'], obj['ee'],
              obj['url'], obj['cite'],obj['crossref'], obj['booktitle'])
    return result
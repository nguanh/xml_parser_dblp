import datetime
import os

from lxml import etree

from dblp.queries import ADD_DBLP_ARTICLE
from mysqlWrapper.mariadb import MariaDb
from .helper import parse_mdate, parse_year, dict_to_tuple, parse_title
from harvester.exception import IHarvest_Exception

COMPLETE_TAG_LIST = ("article", "inproceedings", "proceedings", "book", "incollection",
                     "phdthesis", "mastersthesis", "www", "person", "data")

#TODO limit einführen
#TODO handle dblp parsing exception
def parse_xml(xmlPath, dtdPath, sql_connector,logger, tagList=COMPLETE_TAG_LIST, startDate=None, endDate=None):
    """

    :param xmlPath: path to dblp.xml file
    :param dtdPath: path to dblp.dtd file
    :param sql_connector:
    :param tagList: tuple of tags we want to parse (inproceeedings,article,...) see DTD file
    :param startDate: include all records with mdate >= startDate
    :param endDate: include all records with mdate <= endDate
    :return: number of succesfully added records
    """
    # validate parameters
    if isinstance(tagList, (str, tuple)) is False:
        raise IHarvest_Exception("Invalid tagList")
    if startDate is not None:
        try:
            datetime.datetime.strptime(startDate, '%Y-%m-%d')
            start = parse_mdate(startDate)
        except:
            if isinstance(startDate, datetime.datetime) is False:
                raise IHarvest_Exception("Invalid start Date")
            else:
                start = startDate
    if endDate is not None:
        try:
            datetime.datetime.strptime(endDate, '%Y-%m-%d')
            end = parse_mdate(endDate)
        except:
            if isinstance(endDate, datetime.datetime) is False:
                raise IHarvest_Exception("Invalid end Date")
            else:
                end = endDate

    if os.path.isfile(xmlPath) is False:
        raise IHarvest_Exception("Invalid XML path")
    if os.path.isfile(dtdPath) is False:
        raise IHarvest_Exception("Invalid DTD path")
    if isinstance(sql_connector, MariaDb) is False:
        raise IHarvest_Exception("Invalid sql_connector instance")

    # init values
    success_count = 0
    overall_count = 0
    etree.DTD(file=dtdPath)

    time_range = startDate is not None and endDate is not None
    sql_connector.set_query(ADD_DBLP_ARTICLE)


    # iterate through XML
    for event, element in etree.iterparse(xmlPath, tag=tagList, load_dtd=True):

        overall_count += 1
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
            elif child.tag == 'title':
                title = parse_title(child).replace('\n', '')
                dataset[child.tag] = title
            else:
                dataset[child.tag] = str(child.text).strip()

        dataset['author'] = author_csv_list
        tup = dict_to_tuple(dataset)

        try:
            sql_connector.execute(tup)
        except Exception as e:
            logger.error("MariaDB error: %s", e)
        else:
            success_count += 1
            logger.debug("%s: %s",success_count,element.get('key'))
        element.clear()

        if overall_count > 100:
            return 101


    logger.info("Final Count %s/%s", success_count, overall_count)
    sql_connector.close_connection()
    return success_count

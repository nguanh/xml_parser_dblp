from sickle import Sickle
from sickle import oaiexceptions
from requests import exceptions
from mysqlWrapper.mariadb import MariaDb
from .helper import parse_metadata_default
from .queries import ADD_OAI_DEFAULT
from .exception import Oai_Parsing_Exception
import logging
from celery.utils.log import get_task_logger

'''
TODO
resumption token in case of emergency stop

'''


def harvestOAI(link, sql_connector, query=ADD_OAI_DEFAULT,
               processing_function=parse_metadata_default, startDate=None, endDate=None, format="oai_dc", celery=False):
    """

    :param link: link to resource
    :param sql_connector: handle sql queries
    :param query:  query for inserting data
    :param processing_function: function to parse metadata for given link
    :param startDate: harvest data from given date
    :param endDate:  harvest data to given date
    :return:
    """

    if isinstance(sql_connector, MariaDb) is False:
        raise Oai_Parsing_Exception("Error: Invalid sql_connector instance")

    # init connection to OAI provider
    sickle = Sickle(link)
    sql_connector.set_query(query)
    success_count = 0
    overall_count = 0

    # for every of the OAI verbs (ListRecords, GetRecord, Identify, ListSets, ListMetadataFormats, ListIdentifiers)
    # there is a separate sickle method
    try:
        records = sickle.ListRecords(**{'metadataPrefix': format, 'from': startDate, 'until': endDate})
    except oaiexceptions.NoRecordsMatch:
        raise Oai_Parsing_Exception("No Records found for the the given criteria")
    except exceptions.MissingSchema:
        raise Oai_Parsing_Exception("Error: Link", link, "is not a valid link")
    except exceptions.ConnectionError:
        raise Oai_Parsing_Exception("Error: Link", link, "cannot be connected")
    except oaiexceptions.BadArgument:
        raise Oai_Parsing_Exception("Error: Invalid Parameters")

    #init
    #set logger
    if celery:
        logger = get_task_logger(__name__)
    else:
        logger = logging.getLogger(__name__)


    for record in records:
            # header is xml
            # header = record.header
            # metadata is a dict
            overall_count += 1
            metadata = record.metadata
            met_tuple = processing_function(metadata)
            try:
                sql_connector.execute(met_tuple)
                success_count += 1
                logger.info("%s: %s", success_count, metadata['identifier'])
            except Exception as e:
                logger.error("MariaDB error: %s", e)
                for key, value in metadata.items():
                    logger.debug("%s : %s",key, value)
            #TEST
            if success_count > 100:
                return 100
    return success_count
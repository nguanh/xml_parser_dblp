from sickle import Sickle
from sickle import oaiexceptions
from requests import exceptions
from mysqlWrapper.mariadb import MariaDb
from .helper import parse_metadata_default
from .queries import ADD_OAI_DEFAULT
'''
OAI LINKS
http://citeseerx.ist.psu.edu/oai2
http://export.arxiv.org/oai2

TODO
how to process records?
resumption token in case of emergency stop

'''


def harvestOAI(link, sql_connector, query=ADD_OAI_DEFAULT,
               processing_function=parse_metadata_default, startDate=None, endDate=None):
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
        print("Error: Invalid sql_connector instance")
        return False, 0

    # init connection to OAI provider
    sickle = Sickle(link)
    sql_connector.set_query(query)
    success_count = 0
    overall_count = 0

    # for every of the OAI verbs (ListRecords, GetRecord, Identify, ListSets, ListMetadataFormats, ListIdentifiers)
    # there is a separate sickle method
    try:
        records = sickle.ListRecords(**{'metadataPrefix': 'oai_dc', 'from': startDate, 'until': endDate})
    except oaiexceptions.NoRecordsMatch:
        print("No Records found for the the given criteria")
        return False, 0
    except exceptions.MissingSchema:
        print("Error: Link", link, "is not a valid link")
        return False, 0
    except exceptions.ConnectionError:
        print("Error: Link", link, "cannot be connected")
        return False, 0
    except oaiexceptions.BadArgument:
        print("Error: Invalid Parameters")
        return False, 0

    for record in records:
            # header is xml
            # header = record.header
            # metadata is a dict
            overall_count += 1
            metadata = record.metadata
            met_tuple = processing_function(metadata)
            if sql_connector.execute(met_tuple):
                success_count += 1
                # print(metadata['identifier'], "added")
            else:
                for key, value in metadata.items():
                    pass
                        #print(key, ":", value)

    return True, success_count
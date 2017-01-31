from sickle import Sickle
from sickle import oaiexceptions
from requests import exceptions
from mysqlWrapper.mariadb import MariaDb
from .helper import parse_metadata
'''
OAI LINKS
http://citeseerx.ist.psu.edu/oai2
http://export.arxiv.org/oai2

TODO
how to process records?
resumption token in case of emergency stop

'''

def harvestOAI(link, sql_connector,startDate=None, endDate=None):

    '''
    harvest Records from given repository
    :param processingFunction: function to process the header and metadata
    :param link: Link to OAI-MPH repository
    :param startDate: search for records from given Date
    :param endDate:  search for records until given Date
    :return:
    '''
    if isinstance(sql_connector, MariaDb) is False:
        print("Error: Invalid sql_connector instance")
        return False, 0

    # init connection to OAI provider
    sickle = Sickle(link)

    # for every of the OAI verbs (ListRecords, GetRecord, Idenitfy, ListSets, ListMetadataFormats, ListIdentifiers)
    # there is a separate sickle method
    try:
        records = sickle.ListRecords(**{'metadataPrefix': 'oai_dc', 'from': startDate, 'until': endDate})
    except oaiexceptions.NoRecordsMatch:
        print("No Records found for the the given criteria")
        return False, 0
    except exceptions.MissingSchema:
        print("Link", link, "is not a valid link")
        return False, 0
    except exceptions.ConnectionError:
        print("Link", link, "cannot be connected")
        return False, 0
    except oaiexceptions.BadArgument:
        print("Invalid Parameters")
        return False, 0

    for record in records:
            # header is xml
            #header = record.header
            # metadata is a dict
            metadata = record.metadata
            met_tuple = parse_metadata(metadata)

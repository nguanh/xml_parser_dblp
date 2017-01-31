from sickle import Sickle
from sickle import oaiexceptions
from requests import exceptions
from mysqlWrapper.mariadb import MariaDb
from .helper import parse_metadata
from .queries import ADD_OAI_DATASET
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
    sql_connector.set_query(ADD_OAI_DATASET)
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
            # header = record.header
            # metadata is a dict
            overall_count += 1
            metadata = record.metadata
            met_tuple = parse_metadata(metadata)
            if sql_connector.execute(met_tuple):
                success_count += 1
                #print(metadata['identifier'], "added")
            else:
                for key,value in metadata.items():
                        print(key ,":",value)

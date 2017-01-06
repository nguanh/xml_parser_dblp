from sickle import Sickle
from sickle import oaiexceptions
from requests import exceptions
'''
OAI LINKS
http://citeseerx.ist.psu.edu/oai2
http://export.arxiv.org/oai2

TODO
how to process records?

'''
def harvestOAI(link,startDate=None, endDate=None):

    '''
    harvest Records from given repository
    :param link: Link to OAI-MPH repository
    :param startDate: search for records from given Date
    :param endDate:  search for records until given Date
    :return:
    '''

    # init connection to OAI provider
    sickle = Sickle(link)

    # for every of the OAI verbs (ListRecords, GetRecord, Idenitfy, ListSets, ListMetadataFormats, ListIdentifiers)
    # there is a separate sickle method
    try:
        records = sickle.ListRecords(**{'metadataPrefix': 'oai_dc', 'from': startDate, 'until': endDate})
    except oaiexceptions.NoRecordsMatch:
        print("No Records found for the the given criteria")
    except exceptions.MissingSchema:
        print("Link", link, "is not a valid link")
    except exceptions.ConnectionError:
        print("Link", link, "cannot be connected")
    except oaiexceptions.BadArgument:
        print("Invalid Parameters")
    else:
        for record in records:
            print(record)

link1 = 'http://citeseerx.ist.psu.edu/oai2'
link2 = 'http://export.arxiv.org/oai2'
link3 = 'http://elis.da.ulcc.ac.uk/cgi/oai2'

startDate = '2016-01-10'
endDate = '2017-01-06'
link = link1

harvestOAI(link,endDate=endDate)
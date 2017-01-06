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

link1 = 'http://citeseerx.ist.psu.edu/oai2'
link2 = 'http://export.arxiv.org/oai2'
link3 = 'http://elis.da.ulcc.ac.uk/cgi/oai2'

startDate = '2016-01-10'
endDate = '2017-01-06'

#init connection to OAI provider
link = link1

sickle = Sickle(link)

# for every of the OAI verbs (ListRecords, GetRecord, Idenitfy, ListSets, ListMetadataFormats, ListIdentifiers)
# there is a separate sickle method
exception = False


try:
    records = sickle.ListRecords(**{'metadataPrefix': 'oai_dc', 'from': startDate, 'until': endDate })
except oaiexceptions.NoRecordsMatch:
    print("No Records found for the the given criteria")
    exception = True
except exceptions.MissingSchema:
    print("Link", link, "is not a valid link")
    exception = True
except exceptions.ConnectionError:
    print("Link", link, "cannot be connected")
    exception = True
except oaiexceptions.BadArgument:
    print("Invalid Parameters")
    exception = True

if exception is False:
    for record in records:
        print(record)


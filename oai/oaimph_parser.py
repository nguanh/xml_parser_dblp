from sickle import Sickle
from sickle import oaiexceptions
from requests import exceptions
from mysqlWrapper.mariadb import MariaDb
from .helper import parse_metadata_default
from .queries import ADD_OAI_DEFAULT

from harvester.exception import IHarvest_Exception
from sickle.models import Record

'''
TODO
resumption token in case of emergency stop

'''


def harvestOAI(link, sql_connector, logger,
               query=ADD_OAI_DEFAULT,
               processing_function=parse_metadata_default,
               parsing_class= None,
               xml_format="oai_dc",
               startDate=None, endDate=None, limit=None):

    if isinstance(sql_connector, MariaDb) is False:
        raise IHarvest_Exception("Error: Invalid sql_connector instance")

    # init
    sql_connector.set_query(query)
    success_count = 0
    overall_count = 0
    # init connection to OAI provider
    sickle = Sickle(link)
    # set record parser
    if xml_format is not None and xml_format != "oai_dc":
        if issubclass(parsing_class, Record) is False:
            raise IHarvest_Exception("Invalid parsing class")
        sickle.class_mapping['ListRecords'] = parsing_class
        sickle.class_mapping['GetRecord'] = parsing_class
        pass

    # for every of the OAI verbs (ListRecords, GetRecord, Identify, ListSets, ListMetadataFormats, ListIdentifiers)
    # there is a separate sickle method
    try:
        records = sickle.ListRecords(**{'metadataPrefix': xml_format, 'from': startDate, 'until': endDate})
    except oaiexceptions.NoRecordsMatch:
        return 0
    except exceptions.MissingSchema:
        raise IHarvest_Exception("Error: Link", link, "is not a valid link")
    except exceptions.ConnectionError:
        raise IHarvest_Exception("Error: Link", link, "cannot be connected")
    except oaiexceptions.BadArgument:
        raise IHarvest_Exception("Error: Invalid Parameters")

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
                logger.error("MariaDB error %s: %s", metadata['identifier'], e)

            if limit is not None and overall_count >= limit:
                break
    return success_count

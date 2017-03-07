
from pub_storage.setup_database import setup_database
from pub_storage.constants import DATABASE_NAME
from pub_storage.ingester import ingest_data2
from dblp.dblpingester import DblpIngester

setup_database(DATABASE_NAME)
ingester = DblpIngester(DATABASE_NAME,"harvester")

ingest_data2(ingester, DATABASE_NAME)

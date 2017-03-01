
from pub_storage.setup_database import setup_database
from pub_storage.constants import *
from pub_storage.init_dblp import init_dblp
from pub_storage.ingester import ingest_data
from dblp.queries import INGESTION
from dblp.ingestion import map_to_dict

setup_database(DATABASE_NAME)
dblp_data = init_dblp()

ingest_data(dblp_data, INGESTION.format("storage.dblp_article"), map_to_dict, DATABASE_NAME)

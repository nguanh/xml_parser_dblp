from mysqlWrapper.mariadb import MariaDb
from pub_storage.constants import *
from pub_storage.queries import *
from conf.config import get_config
from pub_storage.helper import *
from .difference_storage import *


def match_author(authors, database= "storage"):
    connector = MariaDb(dict(get_config("MARIADB")))
    connector.connector.database = database
    results = []
    # iterate through all authors
    for author_index, author_dict in enumerate(authors):
        name_block = get_name_block(author_dict["parsed_name"])
        # find matching existing author with name block
        author_block_match = connector.fetch_one((name_block,), COUNT_AUTHORS)

        # case 0 matching name blocks: create new  publication author
        if author_block_match == 0:
            results.append({
                "status": Status.SAFE,
                "match": Match.NO_MATCH,
                "id": None,
                "reason": None,
            })
        # case 1 matching name blocks: include author names as possible alias
        elif author_block_match == 1:
            # get authors id
            author_id = connector.fetch_one((name_block,), CHECK_AUTHORS)
            results.append({
                "status": Status.SAFE,
                "match": Match.SINGLE_MATCH,
                "id": author_id,
                "reason": None,
            })
        # case more than 1 matching name blocks:  match by alias
        else:
            # count possible matching name blocks by matching alias
            alias_count_match = connector.fetch_one((name_block, author_dict["original_name"]),
                                                    COUNT_MATCH_AUTHOR_BY_ALIAS)
            if alias_count_match == 1:
                author_id = connector.fetch_one((name_block, author_dict["original_name"]),
                                                MATCH_AUTHOR_BY_ALIAS)
                results.append({
                    "status": Status.SAFE,
                    "match": Match.MULTI_MATCH,
                    "id": author_id,
                    "reason": None
                })
            else:
                results.append({
                    "status": Status.LIMBO,
                    "match": Match.MULTI_MATCH,
                    "id": None,
                    "reason": Reason.AMB_ALIAS
                })
    connector.close_connection()
    return results


def match_title(title, database= "storage"):
    connector = MariaDb(dict(get_config("MARIADB")))
    connector.connector.database = database
    # iterate through all authors
    cluster_name = normalize_title(title)
    # check for matching cluster (so far ONLY COMPLETE MATCH) TODO levenshtein distance
    connector.cursor.execute(CHECK_CLUSTER, (cluster_name,))
    cluster_matches = []
    for match in connector.cursor:
        cluster_matches.append(match[0])

    if len(cluster_matches) == 0:
        result={
            "status": Status.SAFE,
            "match": Match.NO_MATCH,
            "id": None,
            "reason": None,
        }
    elif len(cluster_matches) == 1:
        idx = connector.fetch_one((cluster_name,),CHECK_CLUSTER)
        count_pub = connector.fetch_one((idx,),COUNT_PUBLICATION)
        if count_pub== 1 :
            result = {
                "status": Status.SAFE,
                "match": Match.SINGLE_MATCH,
                "id": idx,
                "reason": None,
            }
        else:
            result = {
                "status": Status.LIMBO,
                "match": Match.SINGLE_MATCH,
                "id": None,
                "reason": Reason.AMB_PUB
            }

    else:
        result ={
            "status": Status.LIMBO,
            "match": Match.MULTI_MATCH,
            "id": None,
            "reason": Reason.AMB_CLUSTER
        }
    connector.close_connection()
    return result


def ingest_data(harvester_data, query, mapping_function, database=DATABASE_NAME):
    credentials = dict(get_config("MARIADB"))
    # establish mariadb connections, one for reading from harvester, one for writing in ingester
    read_connector = MariaDb(credentials)
    write_connector = MariaDb(credentials)
    write_connector.connector.database = database
    read_connector.cursor.execute(query)

    for query_dataset in read_connector.cursor:
        mapping = mapping_function(query_dataset)

        # ------------------------- LOCAL_URL --------------------------------------------------------------------------
        # check for duplicates by looking up the local URL
        duplicate_id = write_connector.fetch_one((mapping["local_url"], harvester_data['global_url']), CHECK_LOCAL_URL)
        if duplicate_id is not None:
            # TODO duplicate skip
            continue
        # insert local url
        local_url_id = write_connector.execute_ex(INSERT_LOCAL_URL, (mapping["local_url"], harvester_data['global_url']))
        #TODO create separate local url for default

        # ------------------------- CLUSTER ----------------------------------------------------------------------------
        cluster_name = normalize_title(mapping["publication"]["title"])
        # check for matching cluster (so far ONLY COMPLETE MATCH) TODO levenshtein distance
        write_connector.cursor.execute(CHECK_CLUSTER, (cluster_name,))
        cluster_matches = []

        for match in write_connector.cursor:
            cluster_matches.append(match[0])

        if len(cluster_matches) == 0:
            print("Creating new Cluster")
            # create new cluster
            cluster_id = write_connector.execute_ex(INSERT_CLUSTER, (cluster_name,))
            mapping['publication']['cluster_id'] = cluster_id
            # create default url
            # TODO generate url for own publications
            identifier = write_connector.execute_ex(INSERT_LOCAL_URL,
                                                    ("Platzhalter", 1))

        elif len(cluster_matches) == 1:
            print("Appending cluster")
            # find cluster id
            # get matching publications
            #TODO add to difference table
        else:
            print("ambiguous matches, move dataset to other database  ")
            #TODO

        # ------------------------- AUTHORS ----------------------------------------------------------------------------
        for author_index,author_dict in enumerate(mapping["authors"]):
            name_block = get_name_block(author_dict["parsed_name"])
            # find matching existing author with name block
            author_block_match = write_connector.fetch_one((name_block,), COUNT_AUTHORS)

            # case 0 matching name blocks: create new  publication author
            if author_block_match == 0:
                author_dict["block_name"] = name_block
                author_id = write_connector.execute_ex(INSERT_AUTHORS, author_dict)
            # case 1 matching name blocks: include author names as possible alias
            elif author_block_match == 1:
                # get authors id
                author_id = write_connector.fetch_one((name_block,), CHECK_AUTHORS)
            # case more than 1 matching name blocks:  match by alias
            else:
                # count possible matching name blocks by matching alias
                alias_count_match = write_connector.fetch_one((name_block, author_dict["original_name"]),
                                                              COUNT_MATCH_AUTHOR_BY_ALIAS)
                if alias_count_match == 1:
                    author_id = write_connector.fetch_one((name_block, author_dict["original_name"]),
                                                          MATCH_AUTHOR_BY_ALIAS)
                else:
                    print("trolololo")
                    # TODO rollback
            # add original name as alias
            write_connector.execute_ex(INSERT_ALIAS, (author_id, author_dict["original_name"]))
            write_connector.execute_ex(SELECT_ALIAS, (author_id, author_dict["original_name"]))
            write_connector.execute_ex(INSERT_ALIAS_SOURCE, (identifier,))
            # add parsed name as alias, if it's = original name, skip
            write_connector.execute_ex(INSERT_ALIAS, (author_id, author_dict["parsed_name"]))
            write_connector.execute_ex(SELECT_ALIAS, (author_id, author_dict["parsed_name"]))
            write_connector.execute_ex(INSERT_ALIAS_SOURCE, (identifier,))
            # add to publication authors
            write_connector.execute_ex(INSERT_PUBLICATION_AUTHORS, (identifier, author_id, author_index))

        # ------------------------- DEFAULT/DIFFERENCE TABLE -----------------------------------------------------------

        mapping['publication']['url_id'] = identifier
        print()

        # new cluster, insert into default table
        if len(cluster_matches) <= 1:
            write_connector.execute_ex(INSERT_PUBLICATION, mapping["publication"])
        else:
            # TODO
            pass
    write_connector.close_connection()
    read_connector.close_connection()








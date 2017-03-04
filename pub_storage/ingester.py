from mysqlWrapper.mariadb import MariaDb
from pub_storage.constants import *
from pub_storage.queries import *
from conf.config import get_config
from pub_storage.helper import *
from .difference_storage import *


def match_author(authors, database= DATABASE_NAME):
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


def match_title(title, database=DATABASE_NAME):
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
        if count_pub == 1:
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


#TODO
def match_keywords():
    return None

def match_pub_source():
    return None

def push_limbo(mapping):
    pass


def create_authors(matching_list, author_list, local_url, database=DATABASE_NAME):
    connector = MariaDb(dict(get_config("MARIADB")))
    connector.connector.database = database
    result = []
    priority = 0
    for match, author in zip(matching_list,author_list):
        name_block = get_name_block(author["parsed_name"])
        # create author record first depending on matching status
        if match["match"] == Match.NO_MATCH:
            # NOMATCH: create new  publication author
            author["block_name"] = name_block
            author_id = connector.execute_ex(INSERT_AUTHORS, author)
        else:
            # SINGLE MATCH:
            # MULTIMATCH:  author id is already included
            author_id = match["id"]

        # add ALIASES and alias SOURCES
        # add original name as alias
        connector.execute_ex(INSERT_ALIAS, (author_id, author["original_name"]))
        connector.execute_ex(SELECT_ALIAS, (author_id, author["original_name"]))
        connector.execute_ex(INSERT_ALIAS_SOURCE, (local_url,))
        # add parsed name as alias, if it's = original name, skip
        connector.execute_ex(INSERT_ALIAS, (author_id, author["parsed_name"]))
        connector.execute_ex(SELECT_ALIAS, (author_id, author["parsed_name"]))
        connector.execute_ex(INSERT_ALIAS_SOURCE, (local_url,))
        # add to publication authors
        connector.execute_ex(INSERT_PUBLICATION_AUTHORS, (local_url, author_id, priority))
        # store author id for each author
        result.append(author_id)
        priority += 1
    connector.close_connection()
    return result


def create_title(matching, cluster_name, database=DATABASE_NAME):
    connector = MariaDb(dict(get_config("MARIADB")))
    connector.connector.database = database
    if matching["match"] == Match.NO_MATCH:
        cluster_id = connector.execute_ex(INSERT_CLUSTER, (cluster_name,))
    else:
        cluster_id = matching["id"]
    connector.close_connection()
    return cluster_id


def create_publication(cluster_id, author_ids, database= DATABASE_NAME):
    connector = MariaDb(dict(get_config("MARIADB")))
    connector.connector.database = database
    # find publication associated with cluster_id
    publication_data = connector.fetch_one((cluster_id,),CHECK_PUBLICATION,ret_tup=True)
    # publication_data is tuple with (id,url_id)
    if publication_data is None:
        # create local url and default publication
        url_id = connector.execute_ex(INSERT_LOCAL_URL, ("TODO PLATZHALTER", 1))
        pub_id = connector.execute_ex(INSERT_DEFAULT_PUBLICATION, (url_id, cluster_id))
    else:
        url_id = publication_data[1]
        pub_id = publication_data[0]

    # add authors to default pub
    for priority, idx in enumerate(author_ids):
        connector.execute_ex(INSERT_PUBLICATION_AUTHORS, (url_id, idx, priority))
    connector.close_connection()
    # get return publication_id
    return pub_id


def update_diff_tree(pub_id, pub_dict, author_ids, database=DATABASE_NAME):
    connector = MariaDb(dict(get_config("MARIADB")))
    connector.connector.database = database
    diff_tree = connector.fetch_one((pub_id,), CHECK_DIFF_TREE)
    if diff_tree is None:
        # create diff tree
        diff_tree = generate_diff_store(pub_dict)
    else:
        # de serialize first
        diff_tree = deserialize_diff_store(diff_tree)
        insert_diff_store(pub_dict, diff_tree)
    # insert each author
    for author in author_ids:
        # create pub_dict for insertion
        author_dict = {
            "url_id": pub_dict["url_id"],
            "author_ids": author
        }
        #TODO fehler hier
        insert_diff_store(author_dict, diff_tree)

    connector.close_connection()
    return diff_tree


def ingest_data2(harvester_data, query, mapping_function, database=DATABASE_NAME):
    credentials = dict(get_config("MARIADB"))
    # establish mariadb connections, one for reading from harvester, one for writing in ingester
    read_connector = MariaDb(credentials)
    write_connector = MariaDb(credentials)
    write_connector.connector.database = database
    read_connector.cursor.execute(query)

    for query_dataset in read_connector.cursor:
        # 1. get Harvester specific record and parse to common-form dict
        mapping = mapping_function(query_dataset)
        # ------------------------- LOCAL_URL --------------------------------------------------------------------------
        # check for duplicates by looking up the local URL
        duplicate_id = write_connector.fetch_one((mapping["local_url"], harvester_data['global_url']), CHECK_LOCAL_URL)
        if duplicate_id is not None:
            # TODO duplicate skip
            continue
        # 2. create local url entry for record
        local_url_id = write_connector.execute_ex(INSERT_LOCAL_URL, (mapping["local_url"], harvester_data['global_url']))

        # ------------------------- MATCHINGS --------------------------------------------------------------------------
        # 3. find matching cluster for title and matching existing authors
        title_match = match_title(mapping["publication"]["title"])
        author_matches = match_author(mapping["authors"])

        author_valid = True
        for author in author_matches:
            if author["status"] == Status.LIMBO:
                author_valid = False
                break

        # 4. If title or author cannot be matched due to ambiguos matching, push into limbo and delete local url record
        if title_match["status"] == Status.LIMBO or author_valid is False:
            write_connector.execute_ex(DELETE_LOCAL_URL, (local_url_id,))
            push_limbo(mapping)
            continue
        # ------------------------ CREATION ----------------------------------------------------------------------------
        cluster_name = normalize_title(mapping["publication"]["title"])
        author_ids = create_authors(author_matches, mapping["authors"], local_url_id)
        cluster_id = create_title(title_match, cluster_name)
        # create default publication / or find existing one and link with authors and cluster
        def_pub_id = create_publication(cluster_id, author_ids)
        # get /create diff tree
        mapping['publication']['url_id'] = local_url_id
    write_connector.close_connection()
    read_connector.close_connection()


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








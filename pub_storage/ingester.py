from mysqlWrapper.mariadb import MariaDb
from pub_storage.constants import *
from pub_storage.queries import *
from pub_storage.helper import *
from .difference_storage import *


def match_author(authors, database= DATABASE_NAME):
    connector = MariaDb(db = database)
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
    connector = MariaDb(db=database)
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
    connector = MariaDb(db=database)
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
    connector = MariaDb(db=database)
    if matching["match"] == Match.NO_MATCH:
        cluster_id = connector.execute_ex(INSERT_CLUSTER, (cluster_name,))
    else:
        cluster_id = matching["id"]
    connector.close_connection()
    return cluster_id


def create_publication(cluster_id, author_ids, database= DATABASE_NAME):
    connector = MariaDb(db=database)
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
    return [pub_id,url_id]


def update_diff_tree(pub_id, pub_dict, author_ids, database=DATABASE_NAME):
    connector = MariaDb(db=database)
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
        insert_diff_store(author_dict, diff_tree)

    connector.close_connection()
    return diff_tree


def ingest_data2(harvester_data, query, mapping_function, database=DATABASE_NAME):
    # establish mariadb connections, one for reading from harvester, one for writing in ingester
    read_connector = MariaDb()
    write_connector = MariaDb(db = database)
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
        title_match = match_title(mapping["publication"]["title"], database=database)
        author_matches = match_author(mapping["authors"], database=database)

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
        author_ids = create_authors(author_matches, mapping["authors"], local_url_id, database=database)
        cluster_id = create_title(title_match, cluster_name, database=database)
        # 5.create default publication / or find existing one and link with authors and cluster
        def_pub_id, def_url_id = create_publication(cluster_id, author_ids, database=database)
        # 6.get /create diff tree
        mapping['publication']['url_id'] = def_url_id
        diff_tree = update_diff_tree(def_pub_id, mapping['publication'], author_ids, database=database)
        # 7.get default values from diff tree and re-serialize tree
        publication_values = get_default_values(diff_tree)
        serialized_tree = serialize_diff_store(diff_tree)
        # set missing values that are not default
        publication_values["differences"] = serialized_tree
        publication_values["cluster_id"] = cluster_id
        publication_values["url_id"] = def_url_id
        publication_values["date_added"] = None
        publication_values["id"] = def_pub_id
        # 8.store publication
        write_connector.execute_ex(UPDATE_PUBLICATION, publication_values)
        # 9.set publication as harvested
    write_connector.close_connection()
    read_connector.close_connection()

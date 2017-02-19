INSERT_LOCAL_URL = "INSERT INTO local_url(url,global_url_id) VALUES (%s, %s)"
CHECK_LOCAL_URL = "SELECT id FROM local_url WHERE url = %s AND global_url_id = %s"

INSERT_CLUSTER = "INSERT INTO cluster(cluster_name) VALUES (%s)"
CHECK_CLUSTER = "SELECT id FROM cluster WHERE cluster_name = %s"

INSERT_PUBLICATION_AUTHORS = ("INSERT INTO authors(main_name, block_name, website, contact, about, orcid_id) "
                              "VALUES (%s,%s,%s,%s,%s,%s)")
COUNT_PUBLICATION_AUTHORS = "SELECT COUNT(*) FROM authors WHERE block_name = %s"
CHECK_PUBLICATION_AUTHORS = "SELECT COUNT(*) FROM authors WHERE block_name = %s"


INSERT_ALIAS = ("INSERT IGNORE INTO name_alias(authors_id, local_url_id, alias) "
                "VALUES (%s, %s,%s)")
INSERT_LOCAL_URL = "INSERT INTO local_url(url,global_url_id) VALUES (%s, %s)"
CHECK_LOCAL_URL = "SELECT id FROM local_url WHERE url = %s AND global_url_id = %s"

INSERT_CLUSTER = "INSERT INTO cluster(cluster_name) VALUES (%s)"
CHECK_CLUSTER = "SELECT id FROM cluster WHERE cluster_name = %s"

INSERT_PUBLICATION_AUTHORS = ("INSERT INTO authors(main_name, block_name, website, contact, about, orcid_id) "
                              "VALUES (%s,%s,%s,%s,%s,%s)")
COUNT_PUBLICATION_AUTHORS = "SELECT COUNT(*) FROM authors WHERE block_name = %s"
CHECK_PUBLICATION_AUTHORS = "SELECT COUNT(*) FROM authors WHERE block_name = %s"


INSERT_ALIAS = "INSERT IGNORE INTO name_alias(authors_id, alias) VALUES (%s, %s)"
#INSERT_ALIAS = "INSERT INTO name_alias(authors_id, alias) VALUES (%s, %s) "
SELECT_ALIAS = "SELECT id FROM name_alias WHERE authors_id = %s AND alias = %s INTO @id"
INSERT_ALIAS_SOURCE = "INSERT IGNORE INTO alias_source(alias_id,url_id) VALUES (@id,%s)"

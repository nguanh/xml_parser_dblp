INSERT_LOCAL_URL = "INSERT INTO local_url(url,global_url_id,type_id) VALUES (%s, %s,%s)"
CHECK_LOCAL_URL = "SELECT id FROM local_url WHERE url = %s AND global_url_id = %s"
DELETE_LOCAL_URL = "DELETE FROM local_url WHERE id=%s"

INSERT_CLUSTER = "INSERT INTO cluster(cluster_name) VALUES (%s)"
CHECK_CLUSTER = "SELECT id FROM cluster WHERE cluster_name = %s"

COUNT_PUBLICATION = "SELECT COUNT(*) FROM publication WHERE cluster_id = %s "
CHECK_PUBLICATION = "SELECT id,url_id FROM publication WHERE cluster_id = %s"
CHECK_DIFF_TREE = "SELECT differences FROM publication WHERE id = %s"

INSERT_AUTHORS = ("INSERT INTO authors(main_name, block_name, website, contact, about, orcid_id) "
                              "VALUES (%(parsed_name)s,%(block_name)s,%(website)s,%(contact)s,%(about)s,%(orcid_id)s)")
COUNT_AUTHORS = "SELECT COUNT(*) FROM authors WHERE block_name = %s"
CHECK_AUTHORS = "SELECT id FROM authors WHERE block_name = %s"


COUNT_MATCH_AUTHOR_BY_ALIAS = ("SELECT COUNT(*)"
                               "FROM name_alias, authors "
                               "WHERE authors.id = name_alias.authors_id "
                               "AND authors.block_name = %s "
                               "AND alias= %s")
MATCH_AUTHOR_BY_ALIAS = ("SELECT authors.id "
                         "FROM name_alias, authors "
                         "WHERE authors.id = name_alias.authors_id "
                         "AND authors.block_name = %s "
                         "AND alias= %s")

CHECK_PUB_SOURCE = "SELECT id FROM authors WHERE block_name = %s"



INSERT_ALIAS = "INSERT IGNORE INTO name_alias(authors_id, alias) VALUES (%s, %s)"
SELECT_ALIAS = "SELECT id FROM name_alias WHERE authors_id = %s AND alias = %s INTO @id"
INSERT_ALIAS_SOURCE = "INSERT IGNORE INTO alias_source(alias_id,url_id) VALUES (@id,%s)"

CHECK_TYPE = "SELECT id FROM types WHERE name = %s"

INSERT_PUBLICATION_AUTHORS = ("INSERT INTO publication_authors(url_id, author_id, priority) VALUES (%s, %s, %s)")

UPDATE_PUBLICATION=   ("UPDATE publication "
                       "SET   url_id = %(url_id)s, "
                       "      cluster_id =  %(cluster_id)s,"
                       "      differences =  %(differences)s,"
                       "      title=  %(title)s,"
                       "      pages=  %(pages)s, "
                       "      note=  %(note)s,"
                       "      doi=  %(doi)s,"
                       "      abstract=  %(abstract)s,"
                       "      copyright=  %(copyright)s,"
                       "      date_added=  %(date_added)s,"
                       "      date_published=  %(date_published)s,"
                       "      volume=  %(volume)s,"
                       "      number=  %(number)s"
                       " WHERE id = %(id)s"
                       "      ")

INSERT_DEFAULT_PUBLICATION = ("INSERT INTO publication(url_id,cluster_id) VALUES(%s,%s)")


INSERT_LIMBO_PUB= ("INSERT INTO limbo_publication"
                       "       (title_reason,"
                       "        local_url, "
                       "        title, "
                       "        pages, "
                       "        note,"
                       "        doi,"
                       "        abstract,"
                       "        copyright,"
                       "        date_added,"
                       "        date_published,"
                       "        volume,"
                       "        number,"
                       "        series,"
                       "        edition,"
                       "        location,"
                       "        publisher,"
                       "        institution,"
                       "        school,"
                       "        address,"
                       "        isbn,"
                       "        howpublished,"
                       "        book_title,"
                       "        journal) "
                       "VALUES (%(title_reason)s,"
                       "        %(local_url)s, "
                       "        %(title)s, "
                       "        %(pages)s, "
                       "        %(note)s,"
                       "        %(doi)s,"
                       "        %(abstract)s,"
                       "        %(copyright)s,"
                       "        %(date_added)s,"
                       "        %(date_published)s,"
                       "        %(volume)s,"
                       "        %(number)s,"
                       "        %(series)s,"
                       "        %(edition)s,"
                       "        %(location)s,"
                       "        %(publisher)s,"
                       "        %(institution)s,"
                       "        %(school)s,"
                       "        %(address)s,"
                       "        %(isbn)s,"
                       "        %(howpublished)s,"
                       "        %(book_title)s,"
                       "        %(journal)s"
                       "       )")



INSERT_LIMBO_AUTHORS= ("INSERT INTO limbo_authors"
                       "       (author_reason,"
                       "        pub_id,"
                       "        name, "
                       "        priority)"
                       "VALUES (%s,"
                       "        %s,"
                       "        %s, "
                       "        %s"
                       "       )")





# ===========================================URL========================================================================
# TODO extend
LOCAL_URL_FK = ("ALTER TABLE `local_url` "
                 "ADD CONSTRAINT `FK_global_url` "
                 "FOREIGN KEY (`global_url_id`) REFERENCES "
                 "global_url(id) ON UPDATE CASCADE ON DELETE CASCADE")
# ===========================================AUTHORS====================================================================

PUBLICATIONS_AUTHORS_FK = ("ALTER TABLE `publication_authors` "
                           "   ADD CONSTRAINT `FK_local_url` "
                           "     FOREIGN KEY (`url_id`) REFERENCES "
                           "     local_url(id) ON UPDATE CASCADE ON DELETE CASCADE,"
                           "   ADD CONSTRAINT `FK_authors` "
                           "     FOREIGN KEY (`author_id`) REFERENCES "
                           "     authors(id) ON UPDATE CASCADE ON DELETE CASCADE")

NAME_ALIAS_FK = ("ALTER TABLE `name_alias` "
                 "   ADD CONSTRAINT `FK_authors` "
                 "     FOREIGN KEY (`authors_id`) REFERENCES "
                 "     authors(id) ON UPDATE CASCADE ON DELETE CASCADE")

ALIAS_SOURCE_FK = ("ALTER TABLE `alias_source` "
                   "   ADD CONSTRAINT `FK_local_url` "
                   "     FOREIGN KEY (`url_id`) REFERENCES "
                   "     local_url(id) ON UPDATE CASCADE ON DELETE CASCADE,"
                   "   ADD CONSTRAINT `FK_alias` "
                   "     FOREIGN KEY (`alias_id`) REFERENCES "
                   "     name_alias(id) ON UPDATE CASCADE ON DELETE CASCADE"
                   )
# ===========================================PUBLICATIONS===============================================================
PUBLICATION_FK = ("ALTER TABLE `publication` "
                           "   ADD CONSTRAINT `FK_local_url` "
                           "     FOREIGN KEY (`url_id`) REFERENCES "
                           "     local_url(id) ON UPDATE CASCADE ON DELETE CASCADE,"
                           "   ADD CONSTRAINT `FK_cluster` "
                           "     FOREIGN KEY (`cluster_id`) REFERENCES "
                           "     cluster(id) ON UPDATE CASCADE ON DELETE CASCADE"
                  )


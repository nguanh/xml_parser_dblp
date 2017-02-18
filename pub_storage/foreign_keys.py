
LOCAL_URL_FK  = ("ALTER TABLE `local_url` "
                 "ADD CONSTRAINT `FK_global_url` "
                 "FOREIGN KEY (`global_url_id`) REFERENCES "
                 "global_url(id) ON UPDATE CASCADE ON DELETE CASCADE")

NAME_ALIAS_FK = ("ALTER TABLE `name_alias` "
                 "   ADD CONSTRAINT `FK_authors` "
                 "     FOREIGN KEY (`authors_id`) REFERENCES "
                 "     authors(id) ON UPDATE CASCADE ON DELETE CASCADE,"
                 "   ADD CONSTRAINT `FK_local_url` "
                 "     FOREIGN KEY (`local_url_id`) REFERENCES "
                 "     local_url(id) ON UPDATE CASCADE ON DELETE CASCADE")

PUBLICATIONS_AUTHORS_FK = ("ALTER TABLE `publication_authors` "
                           "   ADD CONSTRAINT `FK_authors_group` "
                           "     FOREIGN KEY (`url_id`) REFERENCES "
                           "     local_url(id) ON UPDATE CASCADE ON DELETE CASCADE,"
                           "   ADD CONSTRAINT `FK_authors` "
                           "     FOREIGN KEY (`author_id`) REFERENCES "
                           "     authors(id) ON UPDATE CASCADE ON DELETE CASCADE")


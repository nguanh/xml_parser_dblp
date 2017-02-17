
GLOBAL_URL_LOCAL_URL_FK = ("ALTER TABLE `local_url` "
                           "ADD CONSTRAINT `FK_global_url` "
                           "FOREIGN KEY (`global_url_id`) REFERENCES "
                           "global_url(id) ON UPDATE CASCADE ON DELETE CASCADE")
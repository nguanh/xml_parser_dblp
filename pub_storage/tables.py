

PUBLICATION = (
    "CREATE TABLE `publication` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `default_table_id` INT NOT NULL,"
    "  `difference_table_id` INT NOT NULL,"
    "  `cluster_id` INT NOT NULL,"
    "  PRIMARY KEY (`id`),"
    " FOREIGN KEY (`cluster_id`) REFERENCES cluster(id)"
    "        ON DELETE CASCADE"
    ") ENGINE={} CHARSET=utf8mb4")


CLUSTER = (
    "CREATE TABLE `cluster` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `cluster_name` TEXT,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

GLOBAL_URL = (
    "CREATE TABLE `global_url` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `domain` TEXT NOT NULL ,"
    "  `url` TEXT NOT NULL ,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

LOCAL_URL = (
    "CREATE TABLE `local_url` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `global_url_id` INT NOT NULL ,"
    "  `url` TEXT NOT NULL ,"
    "  `last_updated` TIMESTAMP NOT NULL ,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")


KEYWORDS = (
    "CREATE TABLE `keywords` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `name` TEXT NOT NULL ,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

PUBLICATION_KEYWORDS = (
    "CREATE TABLE `keywords` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `url_id` INT NOT NULL,"
    "  `keyword_id` INT NOT NULL,"
    "  `source` MEDIUMTEXT,"
    "  `last_update` TIMESTAMP,"
    "  `is_default` BOOL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")


TYPES = (
    "CREATE TABLE `types` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `name` VARCHAR(45) NOT NULL ,"
    "  `description` TEXT,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")


STUDYFIELDS = (
    "CREATE TABLE `study_fields` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `name` VARCHAR(45) NOT NULL ,"
    "  `description` TEXT,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")


NAMEALIAS = (
    "CREATE TABLE `name_alias` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `authors_id` INT NOT NULL,"
    "  `local_url_id` INT NOT NULL ,"
    "  `alias` VARCHAR(150) NOT NULL ,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")


AUTHORS = (
    "CREATE TABLE `authors` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `main_name` VARCHAR(100)NOT NULL ,"
    "  `block_name` VARCHAR(100) NOT NULL ,"
    "  `website` TEXT,"
    "  `contact` TEXT,"
    "  `about` TEXT,"
    "  `modified` TIMESTAMP,"
    "  `orcid_id` VARCHAR(45),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")


PUBLICATION_AUTHORS = (
    "CREATE TABLE `publication_authors` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `url_id` INT NOT NULL ,"
    "  `author_id` INT NOT NULL ,"
    "  `priority` INT,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")


#FILES wird nicht gebraucht

SOURCE_LIST = (
    "CREATE TABLE `source_list` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `url_id` INT NOT NULL ,"
    "  `source_id` INT,"
    "  `publication_id` INT NOT NULL ,"
    "  `bitvector_index` INT,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

REFERENCE = (
    "CREATE TABLE `reference` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `group_id` INT NOT NULL ,"
    "  `cluster_id` INT NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")


DEFAULT_TABLE = (
    "CREATE TABLE `default_table` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `type_id` INT,"
    "  `study_field_id` INT,"
    "  `url_id` INT NOT NULL ,"
    "  `title` TEXT,"
    "  `pages_from` INT,"
    "  `pages_to` INT,"
    "  `series` VARCHAR(100),"
    "  `edition` VARCHAR(100),"
    "  `note` TEXT,"
    "  `location` VARCHAR(100),"
    "  `publisher` VARCHAR(100),"
    "  `institution` VARCHAR(100),"
    "  `school` VARCHAR(100),"
    "  `address` VARCHAR(100),"
    "  `isbn` VARCHAR(100),"
    "  `doi` VARCHAR(100),"
    "  `howpublished` VARCHAR(100),"
    "  `abstract` TEXT,"
    "  `copyright` TEXT,"
    "  `date_added` VARCHAR(100),"
    "  `date_published` VARCHAR(5),"
    "  `book_title` VARCHAR(100),"
    "  `journal` VARCHAR(100),"
    "  `volume` VARCHAR(20),"
    "  `number` VARCHAR(20),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

DIFFERENCE_TABLE = (
    "CREATE TABLE `difference_table` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `type_id` TINYBLOB,"
    "  `study_field_id` TINYBLOB,"
    "  `url_id` TINYBLOB ,"
    "  `title` BLOB,"
    "  `pages_from` TINYBLOB,"
    "  `pages_to` TINYBLOB,"
    "  `series` BLOB,"
    "  `edition` BLOB,"
    "  `note` BLOB,"
    "  `location` BLOB,"
    "  `publisher` BLOB,"
    "  `institution` BLOB,"
    "  `school` BLOB,"
    "  `address` BLOB,"
    "  `isbn` BLOB,"
    "  `doi` BLOB,"
    "  `howpublished` BLOB,"
    "  `abstract` BLOB,"
    "  `copyright` BLOB,"
    "  `date_added` BLOB,"
    "  `date_published` BLOB,"
    "  `book_title` BLOB,"
    "  `journal` BLOB,"
    "  `volume` BLOB,"
    "  `number` BLOB,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

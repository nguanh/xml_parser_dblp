# ===========================================URL========================================================================
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
    "  `type_id` INT ,"
    "  `study_field_id` INT,"
    "  `pub_release_id` INT,"
    "  `url` TEXT NOT NULL ,"
    "  `last_updated` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")
# ===========================================AUTHORS================================================================

# stores, which author belongs to which publication url
PUBLICATION_AUTHORS = (
    "CREATE TABLE `publication_authors` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `url_id` INT NOT NULL ,"
    "  `author_id` INT NOT NULL ,"
    "  `priority` INT NOT NULL ,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

# stores information about an author
AUTHORS = (
    "CREATE TABLE `authors` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `main_name` VARCHAR(100)NOT NULL ,"
    "  `block_name` VARCHAR(100) NOT NULL ,"
    "  `website` TEXT,"
    "  `contact` TEXT,"
    "  `about` TEXT,"
    "  `modified` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
    "  `orcid_id` VARCHAR(45),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

# store alias names of an author, duplicate alias are not stored
NAMEALIAS = (
    "CREATE TABLE `name_alias` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `authors_id` INT NOT NULL,"
    "  `alias` VARCHAR(150) NOT NULL ,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE KEY (`authors_id`,`alias`)"
    ") ENGINE={} CHARSET=utf8mb4")

# stores which alias belongs to which source
ALIASSOURCE = (
    "CREATE TABLE `alias_source` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `url_id` INT NOT NULL,"
    "  `alias_id` INT  NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE KEY (`url_id`,`alias_id`)"
    ") ENGINE={} CHARSET=utf8mb4")


# ===========================================PUBLICATION================================================================
CLUSTER = (
    "CREATE TABLE `cluster` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `cluster_name` TEXT,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

PUBLICATION = (
    "CREATE TABLE `publication` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `url_id` INT NOT NULL ,"
    "  `cluster_id` INT NOT NULL ,"
    "  `differences` BLOB,"
    "  `title` TEXT,"
    "  `pages_from` INT,"
    "  `pages_to` INT,"
    "  `note` TEXT,"
    "  `doi` VARCHAR(100),"
    "  `abstract` TEXT,"
    "  `copyright` TEXT,"
    "  `date_added` VARCHAR(100),"
    "  `date_published` VARCHAR(5),"
    "  `volume` VARCHAR(20),"
    "  `number` VARCHAR(20),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

RELEASE = (
    "CREATE TABLE `pub_release` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `series` VARCHAR(100),"
    "  `edition` VARCHAR(100),"
    "  `location` VARCHAR(100),"
    "  `publisher` VARCHAR(100),"
    "  `institution` VARCHAR(100),"
    "  `school` VARCHAR(100),"
    "  `address` VARCHAR(100),"
    "  `isbn` VARCHAR(100),"
    "  `howpublished` VARCHAR(100),"
    "  `book_title` VARCHAR(100),"
    "  `journal` VARCHAR(100),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")


# ===========================================KEYWORDS===================================================================

# stores, which keyword belongs to which publication url
PUBLICATION_KEYWORDS = (
    "CREATE TABLE `keywords` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `url_id` INT NOT NULL,"
    "  `keyword_id` INT NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

# stores keywords and description
KEYWORDS = (
    "CREATE TABLE `keywords` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `main_name` VARCHAR(150) NOT NULL ,"
    "  `block_name`VARCHAR(150) NOT NULL ,"
    "  `description` TEXT,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")

KEYALIAS = (
    "CREATE TABLE `keyword_alias` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `keyword_id` INT NOT NULL,"
    "  `alias` VARCHAR(150) NOT NULL ,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE KEY (`keyword_id`,`alias`)"
    ") ENGINE={} CHARSET=utf8mb4")

KEYSOURCE = (
    "CREATE TABLE `key_source` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `url_id` INT NOT NULL,"
    "  `alias_id` INT  NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  UNIQUE KEY (`url_id`,`alias_id`)"
    ") ENGINE={} CHARSET=utf8mb4")


# ===========================================NON-HARVEST================================================================
# the values in these tables are not harvested but set by users or admin
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


# ===========================================REFERENCE==================================================================

REFERENCE = (
    "CREATE TABLE `reference` ("
    "  `id` INT NOT NULL AUTO_INCREMENT,"
    "  `url_id` INT NOT NULL ,"
    "  `cluster_id` INT NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE={} CHARSET=utf8mb4")




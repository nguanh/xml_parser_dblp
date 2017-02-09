
OAI_DATASET= (
    "CREATE TABLE `oaipmh_articles` ("
    "  `articleId` int(15) NOT NULL AUTO_INCREMENT,"
    "  `identifier` varchar(200) NOT NULL,"
    "  `author` TEXT NOT NULL," #author =creator(s)
    "  `title` TEXT NOT NULL,"
    "  `description` TEXT,"
    "  `contributor` VARCHAR(200),"
    "  `coverage` varchar(200),"
    "  `dates` TEXT NOT NULL ," #array
    "  `formats` varchar(200),"
    "  `languages` varchar(50),"
    "  `publisher` varchar(200),"
    "  `relation` varchar(200),"
    "  `rights` TEXT,"
    "  `sources` varchar(200),"
    "  `subjects` TEXT,"
    "  `type` varchar(200),"
    "  PRIMARY KEY (`articleId`)"
    #") ENGINE=TokuDB CHARSET=utf8mb4")
    ") ENGINE=InnoDB CHARSET=utf8mb4")

ADD_OAI_DEFAULT = ("INSERT INTO oaipmh_articles"
                    " (identifier,author, title,description,contributor,coverage,dates,"
                    "formats,languages,publisher,relation,rights,sources,subjects,type) "
                    "VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s )")


ARXIV_ARTICLE = (
    "CREATE TABLE `arxiv_articles` ("
    "  `articleId` int(15) NOT NULL AUTO_INCREMENT,"
    "  `identifier` varchar(50) NOT NULL,"
    "  `created` DATE,"
    "  `updated` DATE,"
    "  `author` TEXT NOT NULL,"
    "  `title` TEXT NOT NULL,"
    "  `mscclass` varchar(200),"
    "  `acmclass` varchar(200),"
    "  `reportno` varchar(200),"
    "  `journalref` varchar(200),"
    "  `comments` TEXT,"
    "  `description` TEXT,"
    "  `categories` VARCHAR(200),"
    "  `doi` varchar(200),"
    "  PRIMARY KEY (`articleId`)"
    # ") ENGINE=TokuDB CHARSET=utf8mb4")
    ") ENGINE=InnoDB CHARSET=utf8mb4")


ADD_ARXIV = ("INSERT INTO arxiv_articles"
                    " (identifier,created, updated,author,title,mscclass,acmclass,"
                    "reportno,journalref,comments,description,categories,doi) "
                    "VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )")

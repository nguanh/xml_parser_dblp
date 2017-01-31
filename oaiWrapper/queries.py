
OAI_DATASET= (
    "CREATE TABLE `oai` ("
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
    "  `subjects` varchar(200),"
    "  `type` varchar(200),"
    "  PRIMARY KEY (`articleId`)"
    #") ENGINE=TokuDB CHARSET=utf8mb4")
    ") ENGINE=InnoDB CHARSET=utf8mb4")

ADD_OAI_DATASET = ("INSERT INTO oai"
                    " (identifier,author, title,description,contributor,coverage,dates,"
                    "formats,languages,publisher,relation,rights,sources,subjects,type) "
                    "VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s )")





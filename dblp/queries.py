
DBLP_ARTICLE= (
    "CREATE TABLE `article` ("
    "  `articleId` int(15) NOT NULL AUTO_INCREMENT,"
    "  `dblp_key` varchar(200) NOT NULL,"
    "  `mdate` date NOT NULL,"
    "  `author` TEXT NOT NULL,"
    "  `title` TEXT NOT NULL,"
    "  `pages` varchar(20),"
    "  `pub_year` date,"
    "  `volume` varchar(20),"
    "  `journal` varchar(100),"
    "  `journal_number` varchar(20),"
    "  `ee` varchar(200),"
    "  `url` varchar(200),"
    "  `cite` varchar(200),"
    "  `crossref` varchar(200),"
    "  `booktitle` varchar(200),"
    "  PRIMARY KEY (`articleId`)"
    ") ENGINE=TokuDB")
    #") ENGINE=InnoDB CHARSET=utf8 COLLATE utf8_unicode_ci")

ADD_DBLP_ARTICLE = ("INSERT INTO article"
                    " (dblp_key,mdate, author,title,pages,pub_year,volume,journal,journal_number,ee,url,cite,crossref,booktitle) "
                    "VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )")





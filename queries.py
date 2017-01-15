
DBLP_ARTICLE= (
    "CREATE TABLE `article` ("
    "  `articleId` int(15) NOT NULL AUTO_INCREMENT,"
    "  `dblp_key` varchar(200) NOT NULL,"
    "  `mdate` date NOT NULL,"
    "  `author` varchar(100) NOT NULL,"
    "  `title` varchar(200) NOT NULL,"
    "  `pages` varchar(10),"
    "  `pub_year` date,"
    "  `volume` int(4),"
    "  `journal` varchar(100),"
    "  `journal_number` int(4),"
    "  `ee` varchar(200),"
    "  `url` varchar(200),"
    "  PRIMARY KEY (`articleId`)"
    ") ENGINE=TokuDB")

ADD_DBLP_ARTICLE = ("INSERT INTO article"
                    " (dblp_key,mdate, author,title,pages,pub_year,volume,journal,journal_number,ee,url) "
                    "VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )")





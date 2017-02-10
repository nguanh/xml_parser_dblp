
DBLP_ARTICLE3= (
    "CREATE TABLE `dblp_article` ("
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
    #") ENGINE=TokuDB CHARSET=utf8mb4")
    ") ENGINE=InnoDB CHARSET=utf8mb4")

ADD_DBLP_ARTICLE3 = ("INSERT INTO dblp_article"
                    " (dblp_key,mdate, author,title,pages,pub_year,volume,journal,journal_number,ee,url,cite,crossref,booktitle) "
                    "VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )")

'''
INSERT INTO upsert (id, updated_on, value) VALUES (1, CURRENT_TIMESTAMP, 'abc')
ON DUPLICATE KEY UPDATE updated_on = VALUES(updated_on), value = VALUES(value);

'''

#dblp key is primary key
# added fields for date of last update
# and date of last harvest date
DBLP_ARTICLE = (
    "CREATE TABLE `dblp_article` ("
    "  `dblp_key` varchar(100) NOT NULL,"
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
    "  `last_updated` TIMESTAMP,"
    "  `last_harvested` TIMESTAMP,"
    "  PRIMARY KEY (`dblp_key`)"
    #") ENGINE=TokuDB CHARSET=utf8mb4")
    ") ENGINE=InnoDB CHARSET=utf8mb4")

ADD_DBLP_ARTICLE = ("INSERT INTO dblp_article"
                    " (dblp_key,mdate, author,title,pages,pub_year,volume,journal,journal_number,"
                    "ee,url,cite,crossref,booktitle,last_updated,last_harvested) "
                    "VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, CURRENT_TIMESTAMP, 0 )"
                    "ON DUPLICATE KEY UPDATE last_updated= CURRENT_TIMESTAMP,"
                    "mdate =VALUES(mdate),"
                    "author =VALUES(author),"
                    "title =VALUES(title),"
                    "pages =VALUES(pages),"
                    "pub_year =VALUES(pub_year),"
                    "volume =VALUES(volume),"
                    "journal =VALUES(journal_number),"
                    "ee =VALUES(ee),"
                    "url =VALUES(url),"
                    "cite =VALUES(cite),"
                    "crossref =VALUES(crossref),"
                    "booktitle =VALUES(booktitle)"
                     )




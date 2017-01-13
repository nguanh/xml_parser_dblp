from queries import DBLP_ARTICLE
from mariadb_common import create_database, connect, createDB,createTable
import mysql.connector

DB_NAME = 'dblp'


cnx = connect()

#cursor is used to pass SQL queries
cursor = cnx.cursor()

createDB(cnx,cursor,DB_NAME)
createTable("article",cursor,DBLP_ARTICLE)


cursor.close()
cnx.close
from lxml import etree
from lxml.etree import XMLSyntaxError
from dblp_config import checkMainFolder,createFolder
import configparser
import sys
import os

source = sys.argv[1]
dtd = etree.DTD(file=sys.argv[2])
count = 0
main_path= checkMainFolder()

tagList = ("article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data")
#article = inproceedings = phdthesis = masterthesis
'''
JOIN
www
proceedings ignore

'''
for event, element in etree.iterparse(source, tag=tagList, load_dtd=True):
    count += 1
    config = configparser.ConfigParser()
    element_date = element.get("mdate")
    file_name = element.get("key")
    file_name = file_name.replace("/", "-")
    folder_path = createFolder(main_path, element_date)
    file_path = os.path.join(folder_path, file_name + ".txt")
    config[element.tag] = {}

    for child in element:
        #TODO hier werden die tag und deren inhalte ausgegeben, schreibe die in eine neue datei
        #print(child.tag, child.text)
        try:
            config[element.tag][child.tag] = str(child.text)
        except ValueError:
            newText = str(child.text).replace("%", "%%")
            config[element.tag][child.tag]= newText

    with open(file_path, 'a' , encoding='utf-8') as configfile:
        #TODO prüfe ob eintrag bereits existiert
        config.write(configfile)

    element.clear()

print("Final Count :", count)

#articles count 40841 ?
#5422465
#TODO proceedings sind nur die konferenzen und brauchen nicht übernommen zu werden?
#TODO www enthalten autoren websites



from lxml import etree
from lxml.etree import XMLSyntaxError
from dblp_config import checkMainFolder,createFolder
import sys

source = sys.argv[1]
dtd = etree.DTD(file=sys.argv[2])
count = 0
main_path= checkMainFolder()

tagList = ("article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data")
for event, element in etree.iterparse(source, tag=tagList, load_dtd=True):
    count += 1
    element_date = element.get("mdate")
    file_name = element.get("key")
    file_name = file_name.replace("/", "-")
    createFolder(main_path, element_date)

    '''
    for child in element:
        #TODO hier werden die tag und deren inhalte ausgegeben, schreibe die in eine neue datei
        print(child.tag, child.text)
    '''
    element.clear()

print("Final Count :", count)

#articles count 40841 ?
#5422465
#TODO proceedings sind nur die konferenzen und brauchen nicht übernommen zu werden?
#TODO www enthalten autoren websites



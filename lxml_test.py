from lxml import etree
from lxml.etree import XMLSyntaxError
import sys

source = sys.argv[1]
dtd = etree.DTD(file=sys.argv[2])
count = 0

tagList = ("article", "inproceedings", "proceedings", "book", "incollection", "phdthesis", "mastersthesis", "www", "person", "data")
try:
    for event, element in etree.iterparse(source, tag=tagList, load_dtd=True):
        count += 1
        print(element.tag)
        for child in element:
            #TODO hier werden die tag und deren inhalte ausgegeben, schreibe die in eine neue datei
            print(child.tag, child.text)
        element.clear()
except XMLSyntaxError:
    count += 1
    print("fuck")
    #keine fehler mit dtd validation

print("Final Count :", count)

#articles count 40841 ?
#5422465




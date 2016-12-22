import sys
from xml.etree.ElementTree import iterparse,ParseError
import xml.etree.ElementTree as ET


source = sys.argv[1]
parser = ET.XMLParser()
parser.entity['&ouml;'] = "u"
# get an iterable
context = iterparse(source, events=("start", "end"),parser=parser)
# man kann bei iterparse schauen, dass man einen eigenen parser nimmt

# turn it into an iterator
context = iter(context)

# get the root element
event, root = context.__next__()
print("===============Reading new Stuff=============================")
for event, elem in context:

    if event == "start" and elem.tag == "article":
        print("found new article")
        print(elem.attrib)
    elif event == "end" and elem.tag == "article":
        root.clear()
        #TODO es wird erstmal nur ein einzelner artikel eingelesen, um zu schauen, wie das alles funktioniert
        #exit()
    elif event == "start":
        #TODO hier müssen wir checken, ob die texte umlaute und ähnliches haben und das abfangen
        try:
            print(elem.tag + ":" + elem.text)
        except ParseError:
            print("Parse Error")
        except TypeError:
            print("Type Error")
            print(elem.tag)
        except:
            print("Stuff");


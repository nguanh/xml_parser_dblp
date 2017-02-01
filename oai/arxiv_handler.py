from .helper import ATTRIBUTE_ORDER, parse_entry
from sickle.models import Record

class ArXivRecord(Record):

    def __init__(self,record_element, strip_ns=True):
        self.record = record_element
        self.ns = strip_ns

    def __iter__(self):
        pass


def parse_arxiv(metadata):
    tup = ()
    print(metadata)
    for attribute in ATTRIBUTE_ORDER:
        if attribute not in metadata:
            tup += (None,)
        elif attribute == "identifier":
            blob = metadata[attribute]
            identifier = blob[0]
            if(len(blob) ==2):
                print("HHHHHHH", identifier)
            if isinstance(blob,list) and len(blob) > 2:
                doi = blob[2]
                print(doi)
            print(identifier)


        else:
            # default handling
            tup += (parse_entry(metadata[attribute]),)

    return tup

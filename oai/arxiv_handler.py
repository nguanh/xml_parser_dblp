from .helper import ATTRIBUTE_ORDER, parse_entry


def parse_arxiv(metadata):
    tup = ()
    print("ARXIV")
    for attribute in ATTRIBUTE_ORDER:
        if attribute not in metadata:
            tup += (None,)
        elif attribute == "identifier":
            blob = metadata[attribute]
            identifier = blob[0]
            if isinstance(blob,list) and len(blob) > 2:
                doi = blob[2]
                print(doi)
            print(identifier)


        else:
            # default handling
            tup += (parse_entry(metadata[attribute]),)

    return tup

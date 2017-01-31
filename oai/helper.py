
ATTRIBUTE_ORDER = ["identifier", "author","title", "description",
                   "contributor","coverage", "dates","formats","languages",
                   "publisher","relation", "rights","sources", "subjects","type"]


def parse_metadata(metadata):

    tup = ()
    for attribute in ATTRIBUTE_ORDER:
        if attribute not in metadata:
            tup += (None,)
        else:
            tup += (parse_entry(metadata[attribute]),)
    return tup


def parse_entry(obj):

    result = ""
    if isinstance(obj,list) is False:
        return obj
    else:
        for entry in obj:
            result += entry+ " "
    return result.trim()
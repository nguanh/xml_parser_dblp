URL_LIST_MAX =128

#TODO pages erstmal überspringen, es macht vom schema her keinen sinn, beides getrennt zu speichern
# viel mehr sollten sie ein mal validiert und dann immer zusammen als string gespeichert werden
def generate_node(value, index =0):
    if value is None:
        return None
    return {
        "value": value,
        "votes": 0,
        "bitvector": 1<< index,
    }

def append_node(value,index, store):
    has_changed = False
    for i in range(len(store)):
        if store[i]["value"] == value:
            has_changed = True
            #value already exists in tree --> set bitvector
            store[i]["bitvector"] |= 1 << index
    if has_changed is False:
        store.append(generate_node(value, index))

def get_default_values(store):
    pass

def vote(store,attribute,value,vote_count = 1):
    pass

def un_vote(store,attribute,value,vote_count = 1):
    pass

def generate_diff_store(pub_dict):
    object = {
        "url_id" : [], #url list for bitvector
        "title": [],
        "pages":[], #pages from-to are always stored together
        "note":[],
        "doi":[],
        "abstract":[],
        "copyright":[],
        "date_published":[],
        "volume":[],
        "number":[],
    }
    for key in object.keys():
        if key == "url_id":
            object["url_id"].append((pub_dict["url_id"]))
        else:
            node = generate_node(pub_dict[key])
            if node is not None:
                object[key].append(node)
    return object



def insert_diff_store(pub_dict, diff_store):
    # get bitvector index first
    try:
        idx = diff_store["url_id"].index(pub_dict["url_id"])
    except ValueError:
        diff_store["url_id"].append(pub_dict["url_id"])
        # TODO check if limit is reached
        idx = len(diff_store["url_id"]) - 1

    for key in diff_store.keys():
        if key == "url_id":
            continue
        else:
            # insert value into tree
            # skip empty values
            if pub_dict[key] is None:
                continue
            append_node(pub_dict[key], idx ,diff_store[key])

    pass



def serialize_diff_store(store):
    pass


def deserialize_diff_store(store):
    pass
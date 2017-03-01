from unittest import TestCase
from pub_storage.difference_storage import *

import datetime


def get_pub_dict(url_id=None, title=None, pages=None, note=None, doi=None, abstract= None, copyright = None,
                 date_published=None, volume= None, number = None):
    return{
        "url_id": url_id,
        "title":title,
        "pages": pages,
        "note": note,
        "doi": doi,
        "abstract": abstract,
        "copyright": copyright,
        "date_published": date_published,
        "volume": volume,
        "number": number,
    }


class TestDifferenceStorage(TestCase):

    def test_generate_node1(self):
        self.assertIsNone(generate_node(None))

    def test_generate_node2(self):
        self.assertEqual(generate_node("hello"), {"value": "hello", "votes": 0, "bitvector": 1})

    def test_generate_node3(self):
        self.assertEqual(generate_node("hello",4), {"value": "hello", "votes": 0, "bitvector": 16})

    def test_generate_diff_store(self):
        result = generate_diff_store(get_pub_dict(url_id=5,title="Hello World",
                                                  date_published=datetime.datetime(1990,1,1,1,1,1)))
        self.assertEqual(result["url_id"],[5])
        self.assertEqual(result["title"],[ {"value": "Hello World","votes": 0, "bitvector": 1}])
        self.assertEqual(result["date_published"], [{"value": datetime.datetime(1990,1,1,1,1,1), "votes": 0, "bitvector": 1}])
        self.assertEqual(result["abstract"],[])

    def test_insert_diff_store(self):
        result = generate_diff_store(get_pub_dict(url_id=5,title="Hello World",
                                                  date_published=datetime.datetime(1990,1,1,1,1,1)))
        added_values = get_pub_dict(url_id=2,title="Hello World", date_published=datetime.datetime(1990,2,2,2,2,2),
                                    abstract="Test Text")
        insert_diff_store(added_values,result)
        self.assertEqual(result["url_id"], [5,2])
        self.assertEqual(result["title"], [{"value": "Hello World", "votes": 0, "bitvector": 3}])
        self.assertEqual(result["date_published"],
                         [{"value": datetime.datetime(1990, 1, 1, 1, 1, 1), "votes": 0, "bitvector": 1},
                          {"value": datetime.datetime(1990, 2, 2, 2, 2, 2), "votes": 0, "bitvector": 2}
                          ])
        self.assertEqual(result["abstract"], [{"value": "Test Text", "votes": 0, "bitvector": 2}])
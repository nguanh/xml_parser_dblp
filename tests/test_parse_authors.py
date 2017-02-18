from unittest import TestCase
from pub_storage.helper import parse_authors

class TestParse_authors(TestCase):
    def test_parse_authors1(self):
        name = parse_authors("Walter Vogler;")[0]
        self.assertEqual(name['original'], "Walter Vogler")
        self.assertEqual(name['real'], "Walter Vogler")
        self.assertEqual(name['block'], "vogler,w")

    def test_parse_authors2(self):
        name = parse_authors("Richard Müller 0001;")[0]
        self.assertEqual(name['original'], "Richard Müller 0001")
        self.assertEqual(name['real'], "Richard Müller")
        self.assertEqual(name['block'], "muller,r")

    def test_parse_authors3(self):
        name = parse_authors("Alexander S. szalay 0501;")[0]
        self.assertEqual(name['original'], "Alexander S. szalay 0501")
        self.assertEqual(name['real'], "Alexander S. szalay")
        self.assertEqual(name['block'], "szalay,a")

    def test_parse_authors4(self):
        name = parse_authors("luqi;")[0]
        self.assertEqual(name['original'], "luqi")
        self.assertEqual(name['real'], "luqi")
        self.assertEqual(name['block'], "luqi,")

    def test_parse_authors5(self):
        name = parse_authors("Peter van der Stok;")[0]
        self.assertEqual(name['original'], "Peter van der Stok")
        self.assertEqual(name['real'], "Peter van der Stok")
        self.assertEqual(name['block'], "van der stok,p")

    def test_parse_authors6(self):
        name = parse_authors("Yi-Ping Phoebe Chen;")[0]
        self.assertEqual(name['original'], "Yi-Ping Phoebe Chen")
        self.assertEqual(name['real'], "Yi-Ping Phoebe Chen")
        self.assertEqual(name['block'], "chen,y")

    def test_parse_authors7(self):
        name = parse_authors("Jóhanna V. Gísladóttir;")[0]
        self.assertEqual(name['original'], "Jóhanna V. Gísladóttir")
        self.assertEqual(name['real'], "Jóhanna V. Gísladóttir")
        self.assertEqual(name['block'], "gisladottir,j")

    def test_parse_authors8(self):
        name = parse_authors("Andreas Giskeødegård;")[0]
        self.assertEqual(name['original'], "Andreas Giskeødegård")
        self.assertEqual(name['real'], "Andreas Giskeødegård")
        self.assertEqual(name['block'], "giskeodegard,a")

    def test_parse_authors9(self):
        name = parse_authors("Ola R. Snøve Jr;")[0]
        self.assertEqual(name['original'], "Ola R. Snøve Jr")
        self.assertEqual(name['real'], "Ola R. Snøve Jr")
        self.assertEqual(name['block'], "snove,o")

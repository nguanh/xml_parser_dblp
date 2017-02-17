from unittest import TestCase
from pub_storage.helper import normalize_title



class TestNormalize_title(TestCase):
    def test_lower_strip(self):
        title = normalize_title(" ThIs is a TITleß  ")
        self.assertEqual(title, "this is a titless")

    def test_punctuation(self):
        title = normalize_title("O`Really? What's the, iss-ue?  .")
        self.assertEqual(title,"oreally whats the issue")

    def test_whitespace(self):
        title = normalize_title("O`Rea\tlly?\n\n Wha\\t's t\nhe, iss\rue?  .")
        self.assertEqual(title, "oreally whats the issue")

    def test_unicode1(self):
        title = normalize_title("Enhancing Access Privacy of Range Retrievals over (𝔹+)-Trees.")#dblp
        title2 = normalize_title("Enhancing Access Privacy of Range Retrievals Over B+-trees")#citeseer
        self.assertEqual(title, title2)

    def test_unicode2(self):
        title = normalize_title("Enhancing Access Privacy of Range Retrievals over (𝔹+)-Trees.")#dblp
        title2 = normalize_title("Enhancing Access Privacy of Range Retrievals over $({\rm B}^+)$-Trees") #dl.acm
        self.assertEqual(title, title2)




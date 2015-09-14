import unittest
import codecs
import json
import os

from pywikibase import WikibasePage, Claim

try:
    basestring
except NameError:
    basestring = str

class TestWikibasePage(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(os.path.split(__file__)[0], 'data', 'Q7251.wd')) as f:
            self._content = json.load(f)['entities']['Q7251']
        self.wb_page = WikibasePage()
        self.wb_page.get(content=self._content)

    def test_init_wb(self):
        self.assertEqual(self.wb_page.getID(), 'Q7251')

    def test_descriptions(self):
        self.assertEqual(len(self.wb_page.descriptions), 22)
        self.assertIn('fa', self.wb_page.descriptions)
        self.assertIsInstance(self.wb_page.descriptions['en'], basestring)

    def test_labels(self):
        self.assertEqual(len(self.wb_page.labels), 126)
        self.assertIn('uk', self.wb_page.labels)
        self.assertIsInstance(self.wb_page.descriptions['en'], basestring)

    def test_claims(self):
        self.assertEqual(len(self.wb_page.claims), 56)
        self.assertIn('P91', self.wb_page.claims)
        self.assertIsInstance(self.wb_page.claims['P31'], list)
        self.assertTrue(self.wb_page.claims['P27'])
        self.assertIsInstance(self.wb_page.claims['P18'][0], Claim)

    def test_aliases(self):
        self.assertEqual(len(self.wb_page.aliases), 9)
        self.assertIn('en', self.wb_page.aliases)
        self.assertIsInstance(self.wb_page.aliases['en'], list)
        self.assertIsInstance(self.wb_page.aliases['en'][0], basestring)

if __name__ == '__main__':
    unittest.main()
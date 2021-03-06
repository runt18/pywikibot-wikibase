import unittest
import json
import os

from pywikibase import WikibasePage, Claim, ItemPage

try:
    unicode = unicode
except NameError:
    basestring = (str, bytes)


class TestWikibasePage(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(os.path.split(__file__)[0],
                               'data', 'Q7251.wd')) as f:
            self._content = json.load(f)['entities']['Q7251']
        self.wb_page = WikibasePage()
        self.wb_page.get(content=self._content)

    def test_init_wb(self):
        self.assertEqual(self.wb_page.getID(), 'Q7251')
        wb_page = WikibasePage('Q7251')
        self.assertNotEqual(self.wb_page, WikibasePage())
        self.assertEqual(self.wb_page, wb_page)
        wb_page = WikibasePage()
        self.assertRaises(ValueError, wb_page.get)

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

    def test_to_json(self):
        content = self._content
        json_res = self.wb_page.toJSON()
        self.assertEqual(content['labels'], json_res['labels'])
        self.assertEqual(content['descriptions'], json_res['descriptions'])
        self.assertEqual(content['aliases'], json_res['aliases'])
        for p_number in content['claims']:
            self.assertEqual(content['claims'][p_number],
                             json_res['claims'][p_number])

    def test_diffto(self):
        wb_page = self.wb_page
        content = wb_page.toJSON()
        claim_json = wb_page.claims['P31'][0].toJSON()
        wb_page.claims['P31'][0].target = ItemPage('Q6')
        res = wb_page.toJSON(diffto=claim_json)
        self.assertEqual(content['labels'], res['labels'])
        self.assertEqual(content['descriptions'], res['descriptions'])
        self.assertEqual(content['aliases'], res['aliases'])
        for p_number in content['claims']:
            if p_number != 'P31':
                self.assertEqual(content['claims'][p_number],
                                 res['claims'][p_number])
        snak_json = res['claims']['P31'][0]['mainsnak']
        self.assertEqual(snak_json['datavalue']['value']['numeric-id'], 6)


if __name__ == '__main__':
    unittest.main()

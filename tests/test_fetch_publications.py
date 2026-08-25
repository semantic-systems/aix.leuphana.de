import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Add the scripts directory to the python path so we can import the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
import fetch_publications

class TestFetchPublications(unittest.TestCase):
    @patch('fetch_publications.requests.get')
    def test_fetch_dblp_publications(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "hits": {
                    "hit": [
                        {
                            "info": {
                                "key": "conf/test/paper1",
                                "title": "Test Paper",
                                "year": "2026",
                                "venue": "TestConf",
                                "doi": "10.1234/test",
                                "authors": {
                                    "author": [{"text": "Ricardo Usbeck"}, {"text": "John Doe"}]
                                }
                            }
                        }
                    ]
                }
            }
        }
        
        pubs = fetch_publications.fetch_dblp_publications()
        self.assertEqual(len(pubs), 1)
        self.assertEqual(pubs[0]['title'], "Test Paper")
        self.assertEqual(pubs[0]['authors'], ["Ricardo Usbeck", "John Doe"])
        self.assertEqual(pubs[0]['doi'], "10.1234/test")
        
    @patch('fetch_publications.requests.get')
    def test_fetch_abstract(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"abstract": "This is a test abstract."}
        
        abs_text = fetch_publications.fetch_abstract_from_semantic_scholar("10.1234/test")
        self.assertEqual(abs_text, "This is a test abstract.")
        
    def test_slugify(self):
        self.assertEqual(fetch_publications.slugify("Test Title: With, Punctuation!"), "test-title-with-punctuation")
        
    @patch('fetch_publications.fetch_abstract_from_semantic_scholar')
    @patch('fetch_publications.fetch_bibtex_from_dblp')
    def test_generate_markdown(self, mock_bibtex, mock_abstract):
        mock_abstract.return_value = "Test abstract."
        mock_bibtex.return_value = "@inproceedings{test,\n  title={Test}\n}"
        
        pub = {
            "key": "conf/test",
            "title": "My Title",
            "year": "2026",
            "venue": "Conf",
            "doi": "10.1234/567",
            "authors": ["Author A"]
        }
        
        with tempfile.TemporaryDirectory() as tempdir:
            success = fetch_publications.generate_markdown(pub, tempdir)
            self.assertTrue(success)
            files = os.listdir(tempdir)
            self.assertEqual(len(files), 1)
            filepath = os.path.join(tempdir, files[0])
            with open(filepath, 'r') as f:
                content = f.read()
                self.assertIn('title: "My Title"', content)
                self.assertIn('Test abstract.', content)
                self.assertIn('@inproceedings{test,', content)

if __name__ == '__main__':
    unittest.main()

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Add the scripts directory to the python path so we can import the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
import fetch_publications

class TestFetchPublications(unittest.TestCase):
    @patch('fetch_publications.BrowserFetcher')
    def test_fetch_dblp_publications(self, mock_browser_fetcher):
        mock_fetcher = mock_browser_fetcher.get_instance.return_value
        mock_fetcher.get_json.return_value = {
            "result": {
                "hits": {
                    "@total": "1",
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
        
    @patch('fetch_publications.BrowserFetcher')
    def test_fetch_abstract(self, mock_browser_fetcher):
        mock_fetcher = mock_browser_fetcher.get_instance.return_value
        mock_fetcher.get_json.return_value = {"abstract": "This is a test abstract."}
        
        abs_text = fetch_publications.fetch_abstract_semanticscholar("Test Title", "10.1234/test")
        self.assertEqual(abs_text, "This is a test abstract.")
        
    def test_slugify(self):
        self.assertEqual(fetch_publications.sanitize_filename("Test Title: With, Punctuation!"), "test-title-with-punctuation")
        
    def test_generate_markdown(self):
        pub = {
            "key": "conf/test",
            "title": "My Title",
            "year": "2026",
            "venue": "Conf",
            "doi": "10.1234/567",
            "authors": ["Author A"]
        }
        
        with tempfile.TemporaryDirectory() as tempdir:
            filepath = os.path.join(tempdir, "my-title.md")
            fetch_publications.generate_markdown(pub, "@inproceedings{test,\n  title={Test}\n}", filepath, "Test abstract.")
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

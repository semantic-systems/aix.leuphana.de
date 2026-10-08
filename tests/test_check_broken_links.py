"""Focused routing checks; no network access or email delivery."""

import os
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

# Some local preview environments omit PyYAML; these tests mock front matter.
try:
    import yaml  # noqa: F401
except ImportError:
    sys.modules['yaml'] = types.ModuleType('yaml')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
import check_broken_links as checker


class LinkRoutingTests(unittest.TestCase):
    def test_placeholder_contact_is_not_a_recipient(self):
        self.assertFalse(checker.valid_email('first.last@example.org'))
        self.assertFalse(checker.valid_email('not-an-email'))
        self.assertTrue(checker.valid_email('jane.doe@leuphana.de'))

    def test_explicit_owners_not_project_members(self):
        source = '_projects/example.md'
        team = {'jane-doe': {'name': 'Jane Doe', 'email': 'jane@leuphana.de'}}
        with patch.object(checker, 'parse_frontmatter', return_value={
            'project_members': [{'name': 'Jane Doe'}]
        }):
            self.assertEqual(checker.owners_for_source(source, team, {}), ([], 'no owner assigned'))
            owners, reason = checker.owners_for_source(source, team, {source: ['jane-doe']})
        self.assertEqual([owner['email'] for owner in owners], ['jane@leuphana.de'])
        self.assertIsNone(reason)

    def test_team_profile_owns_its_page_and_missing_email_goes_to_admin(self):
        source = '_team/jane-doe.md'
        with patch.object(checker, 'parse_frontmatter', return_value={}):
            owners, reason = checker.owners_for_source(source, {
                'jane-doe': {'name': 'Jane Doe', 'email': 'jane@leuphana.de'}
            }, {})
            missing, missing_reason = checker.owners_for_source(source, {
                'jane-doe': {'name': 'Jane Doe', 'email': None}
            }, {})
        self.assertEqual(owners[0]['email'], 'jane@leuphana.de')
        self.assertIsNone(reason)
        self.assertEqual(missing, [])
        self.assertIn('jane-doe', missing_reason)

    def test_specific_roster_entry_overrides_collection_default(self):
        source = '_publications/special-paper.md'
        team = {
            'jane-doe': {'name': 'Jane Doe', 'email': 'jane@leuphana.de'},
            'alex-example': {'name': 'Alex Example', 'email': 'alex@leuphana.de'},
        }
        roster = {'_publications/*.md': ['jane-doe'], source: ['alex-example']}
        with patch.object(checker, 'parse_frontmatter', return_value={}):
            owners, reason = checker.owners_for_source(source, team, roster)
        self.assertEqual([owner['email'] for owner in owners], ['alex@leuphana.de'])
        self.assertIsNone(reason)

    def test_shared_link_is_not_attributed_to_page_source(self):
        with tempfile.TemporaryDirectory() as temp:
            path = os.path.join(temp, 'example.md')
            with open(path, 'w', encoding='utf-8') as stream:
                stream.write('Read [the paper](https://example.org/paper).')
            self.assertTrue(checker.link_in_source(path, 'https://example.org/paper'))
            self.assertFalse(checker.link_in_source(path, 'https://example.org/shared-navigation'))

    def test_source_index_uses_collection_and_fixed_permalink(self):
        with tempfile.TemporaryDirectory() as temp:
            old = os.getcwd()
            try:
                os.chdir(temp)
                os.makedirs('_projects')
                os.makedirs('_team')
                with open('_projects/example.md', 'w', encoding='utf-8') as stream:
                    stream.write('---\ntitle: Example\n---\n')
                with open('_team/jane-doe.md', 'w', encoding='utf-8') as stream:
                    stream.write('---\nname: Jane Doe\n---\n')
                with patch.object(checker, 'parse_frontmatter', side_effect=lambda path: {
                    'permalink': '/people/jane/' if path.startswith('_team/') else None
                }):
                    index = checker.build_source_index()
            finally:
                os.chdir(old)
        self.assertEqual(index['/projects/example/'], '_projects/example.md')
        self.assertEqual(index['/people/jane/'], '_team/jane-doe.md')


if __name__ == '__main__':
    unittest.main()

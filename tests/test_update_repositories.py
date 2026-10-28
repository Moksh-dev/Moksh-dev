import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('updater',Path(__file__).resolve().parents[1]/'scripts/update_repositories.py')
u=importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)

def repo(name='sample', **extra):
    return dict(name=name, owner={'login':'Moksh-dev'}, private=False, language='Python', **extra)

class UpdaterTests(unittest.TestCase):
    def test_pagination_including_empty_page(self):
        calls=[]
        def fetch(path):
            calls.append(path)
            if '?' not in path:return {'public_repos':101}
            page=int(path.rsplit('=',1)[1])
            return [repo(f'p{i}') for i in range(100)] if page==1 else [repo('last')] if page==2 else []
        self.assertEqual(len(u.discover(fetch)),101)
        self.assertTrue(any('page=3' in p for p in calls))
    def test_incomplete_discovery_rejected(self):
        def fetch(path):
            if '?' not in path:return {'public_repos':2}
            return [repo()] if path.endswith('page=1') else []
        with self.assertRaises(ValueError):u.discover(fetch)
    def test_duplicate_discovery_rejected(self):
        with self.assertRaises(ValueError):u.discover(lambda p:[repo(),repo()] if p.endswith('page=1') else [])
    def test_preserves_curated_text_and_idempotent(self):
        text='hero\n<!-- REPOSITORIES:START -->old<!-- REPOSITORIES:END -->\nmy cards\n<!-- ACTIVITY:START -->old<!-- ACTIVITY:END -->\nfooter'
        updated=u.update(text,[repo()],{})
        self.assertTrue(updated.startswith('hero\n'))
        self.assertIn('\nmy cards\n',updated)
        self.assertTrue(updated.endswith('\nfooter'))
        self.assertEqual(updated,u.update(updated,[repo()],{}))
    def test_missing_duplicate_reversed_markers(self):
        for text in ['', '<!-- X:START --><!-- X:START --><!-- X:END -->', '<!-- X:END --><!-- X:START -->']:
            with self.assertRaises(ValueError):u.region(text,'X','data')
    def test_untrusted_markdown_escaped(self):
        rendered=u.render_index([repo(description='<script>x</script> | [bad](https://bad.test)\nnew')],{})
        self.assertNotIn('<script>',rendered)
        self.assertNotIn('[bad](',rendered)
        self.assertIn('\\|',rendered)
    def test_missing_metadata_and_new_repository(self):
        rendered=u.render_index([repo()],{})
        self.assertIn('Newly discovered',rendered)
        self.assertIn('description not provided',rendered)
        self.assertIn('https://github.com/Moksh-dev/sample',rendered)
    def test_all_repositories_including_profile(self):
        repos=[repo('Moksh-dev'),repo('beginner'),repo('archived',archived=True),repo('forked',fork=True)]
        rendered=u.render_index(repos,{})
        for r in repos:self.assertIn('/'+r['name']+')',rendered)
        self.assertIn('**3 projects**',u.render_activity(repos))
    def test_profile_push_does_not_change_activity(self):
        repos=[repo('Moksh-dev',pushed_at='2099-01-01T00:00:00Z'),repo('project',pushed_at='2026-10-20T00:00:00Z')]
        self.assertIn('2026-10-20',u.render_activity(repos))
        self.assertNotIn('2099',u.render_activity(repos))

if __name__=='__main__':unittest.main()

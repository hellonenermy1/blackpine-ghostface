import csv,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SpecTests(unittest.TestCase):
    def setUp(self): self.s=json.loads((ROOT/'docs/spec.json').read_text())
    def test_input(self): self.assertEqual(self.s['max_input_bytes'],15_000_000)
    def test_deadline(self): self.assertEqual(self.s['warm_deadline_seconds'],60)
    def test_levels(self):
        self.assertEqual([x['name'] for x in self.s['levels']],['Low','Low-Medium','Medium','Medium-High','High','Maximum'])
        self.assertEqual(self.s['default_level'],'Medium')
        self.assertEqual([x['warning'] for x in self.s['levels']],[False]*3+[True]*3)
        self.assertEqual([x['confirmation'] for x in self.s['levels']],[False]*5+[True])
    def test_no_false_claims(self):
        self.assertFalse(self.s['production_ready']); self.assertFalse(any(x['validated'] for x in self.s['levels']))
    def test_privacy(self): self.assertFalse(self.s['backend']);self.assertFalse(self.s['photo_uploads'])
    def test_ledger(self):
        with (ROOT/'docs/requirements.csv').open() as f: rows=list(csv.DictReader(f))
        self.assertEqual([r['id'] for r in rows],[f'R{i:02}' for i in range(1,36)])
        self.assertTrue(all(r['status']=='planned' and not r['evidence'] for r in rows))

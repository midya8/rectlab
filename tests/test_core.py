import unittest,json,copy,itertools,random
from pathlib import Path
from rectlab import solve,verify
from rectlab.schema import validate,loads
from rectlab.verify import reconstruct
ROOT=Path(__file__).resolve().parents[1]
class Core(unittest.TestCase):
 def test_developed(self):
  for x in json.loads((ROOT/'examples.json').read_text()):
   with self.subTest(x=x['id']):self.assertTrue(verify(solve(x['input'])))
 def test_gap(self):
  s=solve(json.loads((ROOT/'examples.json').read_text())[0]['input']);self.assertEqual((s['cover']['size'],s['cover']['count'],s['maximal_cover']['count'],s['maximum_fooling_size']),(4,'68','13',3));self.assertEqual(len(s['rectangles']),41)
 def test_overlap(self):
  s=solve(json.loads((ROOT/'examples.json').read_text())[1]['input']);self.assertEqual((s['cover']['size'],s['partition']['size'],s['real_rank']),(3,4,4));self.assertTrue(s['factors']['cover']['overlap_cells']);self.assertFalse(s['factors']['partition']['overlap_cells'])
 def test_exhaustive_three_by_three(self):
  for mask in range(512):
   x={'matrix':[[mask>>(i*3+j)&1 for j in range(3)]for i in range(3)]};s=solve(x);self.assertEqual(s,reconstruct(x));self.assertLessEqual(s['maximum_fooling_size'],s['cover']['size']);self.assertLessEqual(s['cover']['size'],s['partition']['size']);self.assertEqual(s['factors']['cover']['boolean_product'],x['matrix'])
 def test_transpose(self):
  for x in json.loads((ROOT/'examples.json').read_text()):
   a=x['input']['matrix'];s=solve(x['input']);t=solve({'matrix':[list(z)for z in zip(*a)]})
   for key in ['cover','maximal_cover','partition']:self.assertEqual((s[key]['size'],s[key]['count']),(t[key]['size'],t[key]['count']))
 def test_permutation(self):
  for x in json.loads((ROOT/'examples.json').read_text()):
   s=solve(x['input']);t=solve({'matrix':[r[::-1]for r in x['input']['matrix'][::-1]]})
   for key in ['cover','maximal_cover','partition']:self.assertEqual((s[key]['size'],s[key]['count']),(t[key]['size'],t[key]['count']))
 def test_zero_extension(self):
  for a in [[[1,1],[1,0]],[[0]]]:
   s=solve({'matrix':a});t=solve({'matrix':[r+[0]for r in a]+[[0]*(len(a[0])+1)]})
   self.assertEqual(s['cover'],t['cover']);self.assertEqual(s['partition'],t['partition'])
 def test_empty(self):
  s=solve({'matrix':[[0]*5]*5});self.assertEqual(s['cover'],{'size':0,'count':'1','witness':[]});self.assertEqual(s['maximum_fooling_masks'],[0]);self.assertEqual(s['real_rank'],0);self.assertTrue(verify(s))
 def test_strict_schema(self):
  bad=[{},[],{'matrix':[]},{'matrix':[[True]]},{'matrix':[[1.0]]},{'matrix':[[2]]},{'matrix':[[1],[]]},{'matrix':[[0]*6]},{'matrix':[[0]]*6},{'matrix':[[1]*5]*3},{'matrix':[[1]],'extra':0}]
  for x in bad:
   with self.assertRaises(ValueError):validate(x)
 def test_strict_json(self):
  for s in ['{"matrix":[[0]],"matrix":[[1]]}','{"matrix":[[NaN]]}']:
   with self.assertRaises(ValueError):loads(s)
 def test_shape_tampering(self):
  s=solve({'matrix':[[1,1],[1,0]]})
  for edit in [lambda q:q.update(extra=0),lambda q:q.pop('cover'),lambda q:q['rectangles'].reverse(),lambda q:q['cover'].update(size=True),lambda q:q['input'].update(matrix=[[True,1],[1,0]])]:
   q=copy.deepcopy(s);edit(q)
   with self.assertRaises(ValueError):verify(q)
 def test_checker_is_independent(self):
  import inspect,rectlab.verify as v
  source=(ROOT/'rectlab/verify.py').read_text();self.assertNotIn('from .engine',source);self.assertNotIn('solve(',source)
if __name__=='__main__':unittest.main()

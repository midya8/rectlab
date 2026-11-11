import unittest,itertools,json
from pathlib import Path
from rectlab import solve,verify
from rectlab.families import select_from,rank_from
P=Path(__file__).resolve().parents[1]
FAMILIES=['cover','maximal_cover','partition']
def explicit(s,family):
 ids=[r['id']for r in s['rectangles']if family!='maximal_cover'or r['maximal']];out=[];full=(1<<len(s['cells']))-1
 for chosen in itertools.combinations(ids,s[family]['size']):
  covered=0;okay=True
  for k in chosen:
   m=s['rectangles'][k]['mask']
   if family=='partition'and covered&m:okay=False;break
   covered|=m
  if okay and covered==full:out.append(list(chosen))
 return out
class Families(unittest.TestCase):
 def check_family(self,s,family):
  expected=explicit(s,family);f=s[family];self.assertEqual(str(len(expected)),f['count']);inc=[sum(i in w for w in expected)for i in range(len(s['rectangles']))];self.assertEqual(f['inclusion_counts'],list(map(str,inc)));self.assertEqual(sum(inc),f['size']*len(expected));actual=[]
  for index,ws in enumerate(expected):
   actual.append(select_from(s,family,str(index)));self.assertEqual(actual[-1],ws);self.assertEqual(rank_from(s,family,ws),str(index))
  self.assertEqual(len({tuple(w)for w in actual}),len(expected));self.assertEqual(f['mandatory'],[i for i,c in enumerate(inc)if c==len(expected)])
 def test_exhaustive_three_by_three_families(self):
  for mask in range(512):
   s=solve({'matrix':[[mask>>(i*3+j)&1 for j in range(3)]for i in range(3)]})
   for f in FAMILIES:self.check_family(s,f)
 def test_developed_complete_families(self):
  for x in json.loads((P/'examples.json').read_text()):
   s=solve(x['input'])
   for f in FAMILIES:self.check_family(s,f)
 def test_restriction_changes_membership(self):
  s=solve(json.loads((P/'examples.json').read_text())[0]['input']);self.assertEqual(s['cover']['inclusion_counts'][12],'40');self.assertEqual(s['maximal_cover']['inclusion_counts'][12],'9');self.assertEqual(s['cover']['inclusion_counts'][0],'1');self.assertEqual(s['maximal_cover']['inclusion_counts'][0],'0')
 def test_unique_mandatory(self):
  s=solve(json.loads((P/'examples.json').read_text())[1]['input']);self.assertEqual(s['cover']['mandatory'],s['cover']['witness']);self.assertEqual(s['cover']['optional'],[])
 def test_rank_index_validation(self):
  s=solve({'matrix':[[1,1],[1,0]]})
  for index in [-1,0,True,'-1','01','1.0',' 0',s['cover']['count'],'9'*101]:
   with self.assertRaises(ValueError):select_from(s,'cover',index)
  for f in [None,0,'nope']:
   with self.assertRaises(ValueError):select_from(s,f,'0')
  for ws in [[True],[0,0],[2,1],[-1],[],[99],[0]]:
   with self.assertRaises(ValueError):rank_from(s,'cover',ws)
 def test_membership_forgeries(self):
  import copy
  s=solve({'matrix':[[1,1],[1,0]]})
  for f in FAMILIES:
   for key in ['inclusion_counts','mandatory','optional','never']:
    q=copy.deepcopy(s)
    if q[f][key]:q[f][key][0]='999'if key=='inclusion_counts'else 99
    else:q[f][key].append('0'if key=='inclusion_counts'else 0)
    with self.assertRaises(ValueError):verify(q)
if __name__=='__main__':unittest.main()

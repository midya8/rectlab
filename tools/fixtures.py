import json,random,copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from rectlab import solve,verify
from rectlab.families import select_from
P=Path(__file__).resolve().parents[1]

def fixtures():
 out=[x['input']for x in json.loads((P/'examples.json').read_text())];r=random.Random(9147)
 for t in range(55):
  R=r.randrange(1,6);C=r.randrange(1,6);ones=r.sample(range(R*C),r.randrange(min(12,R*C)+1));out.append({'matrix':[[int(i*C+j in ones)for j in range(C)]for i in range(R)]})
 return out

def paths(x,p=()):
 if type(x)==dict:
  for k,v in x.items():
   if not p and k=='input':continue
   yield from paths(v,p+(k,))
 elif type(x)==list:
  for k,v in enumerate(x):yield from paths(v,p+(k,))
 else:yield p

def mutations(report):
 # Every primitive, noninput field in the small three-positive-cell control; no sampled omissions.
 for p in paths(report):
  q=copy.deepcopy(report);v=q
  for k in p[:-1]:v=v[k]
  old=v[p[-1]];v[p[-1]]=not old if type(old)==bool else old+1 if type(old)==int else old+'x' if type(old)==str else 0
  yield p,q
if __name__=='__main__':
 reports=[solve(x)for x in fixtures()]
 for s in reports:verify(s)
 base=solve({'matrix':[[1,1],[1,0]]})
 for p,q in mutations(base):
  try:verify(q)
  except ValueError:pass
  else:raise AssertionError(p)
 family_witnesses=[{f:[select_from(s,f,str(i))for i in range(int(s[f]['count']))]for f in ['cover','maximal_cover','partition']}for s in reports[:9]]
 payload={'family_witnesses':family_witnesses,'inputs':fixtures(),'reports':reports,'forgery_base':base,'forgery_paths':[list(p)for p in paths(base)]}
 (P/'tests/fixtures.json').write_text(json.dumps(payload,separators=(',',':'))+'\n')
 print(json.dumps({'reports':len(reports),'rectangles':sum(len(s['rectangles'])for s in reports),'subsets':sum(len(s['fooling_subsets'])for s in reports),'forgeries':len(payload['forgery_paths'])}))

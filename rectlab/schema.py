import json

def validate(x):
 if type(x)!=dict or set(x)!={'matrix'} or type(x['matrix'])!=list or not 1<=len(x['matrix'])<=5:raise ValueError('1..5 rows required')
 a=x['matrix'];c=len(a[0]) if type(a[0])==list else 0
 if not 1<=c<=5 or any(type(row)!=list or len(row)!=c or any(type(v)!=int or v not in (0,1) for v in row)for row in a):raise ValueError('rectangular 1..5 columns, integer 0/1 required')
 if sum(map(sum,a))>12:raise ValueError('at most 12 one cells')
 return a

def same(a,b):
 if type(a)!=type(b):return False
 if type(a)==dict:return a.keys()==b.keys() and all(same(a[k],b[k])for k in a)
 if type(a)==list:return len(a)==len(b) and all(same(x,y)for x,y in zip(a,b))
 return a==b

def loads(s):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise ValueError('duplicate key')
   d[k]=v
  return d
 if len(s.encode())>8*1024*1024:raise ValueError('8MiB cap')
 return json.loads(s,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('nonfinite')))

# Independent rectangle discovery from cell subsets. Cover counts use inclusion-
# exclusion, not the producer's skip/take DP. Partitions use first-cell recursion.
import json
from itertools import combinations,permutations
from math import comb
from functools import lru_cache
from .schema import validate,same

def reconstruct(data):
 a=validate(data);R=len(a);C=len(a[0]);cells=[[i,j]for i,row in enumerate(a)for j,v in enumerate(row)if v];n=len(cells);full=(1<<n)-1;found=[]
 for mask in range(1,1<<n):
  subset=[cells[k]for k in range(n)if mask>>k&1];rows=sorted({i for i,j in subset});cols=sorted({j for i,j in subset})
  if len(subset)==len(rows)*len(cols):found.append((sum(1<<i for i in rows),sum(1<<j for j in cols),rows,cols,mask))
 found.sort();rect=[dict(id=i,rows=z[2],columns=z[3],mask=z[4],maximal=not any(z[4]!=s[4] and z[4]&s[4]==z[4]for s in found))for i,z in enumerate(found)]
 def count(ids,need,k):
  # Choose k distinct factors; each forbidden uncovered-cell set excludes every
  # rectangle touching it. Signed subset sum counts exactly full unions.
  if k<0:return 0
  bits=[b for b in range(n)if need>>b&1];ans=0
  for sub in range(1<<len(bits)):
   t=sum(1<<b for j,b in enumerate(bits)if sub>>j&1);m=sum(not(rect[i]['mask']&t)for i in ids)
   if m>=k:ans+=(-1 if sub.bit_count()%2 else 1)*comb(m,k)
  return ans
 def membership(inc,ct):
  return dict(inclusion_counts=list(map(str,inc)),mandatory=[i for i,c in enumerate(inc)if c==ct],optional=[i for i,c in enumerate(inc)if 0<c<ct],never=[i for i,c in enumerate(inc)if c==0])
 def cover(ids):
  k=next(k for k in range(n+1)if count(ids,full,k));ct=count(ids,full,k);chosen=[];need=full;left=k
  for j,rid in enumerate(ids):
   if left and count(ids[j+1:],need&~rect[rid]['mask'],left-1):chosen.append(rid);need&=~rect[rid]['mask'];left-=1
  assert need==0 and left==0
  inc=[count([j for j in ids if j!=rid],full&~rect[rid]['mask'],k-1)if rid in ids else 0 for rid in range(len(rect))]
  return dict(size=k,count=str(ct),witness=chosen,**membership(inc,ct))
 co=cover(list(range(len(rect))));mc=cover([r['id']for r in rect if r['maximal']])
 @lru_cache(None)
 def part(remaining):
  if not remaining:return 0,1,()
  bit=(remaining&-remaining);best=n+1;ct=0;w=()
  for r in rect:
   m=r['mask']
   if not m&bit or m&remaining!=m:continue
   v,c,ws=part(remaining^m);v+=1;ws=tuple(sorted((r['id'],)+ws))
   if v<best:best,ct,w=v,c,ws
   elif v==best:ct+=c;w=min(w,ws)
  return best,ct,w
 size,ct,ws=part(full);inc=[part(full^r['mask'])[1]if part(full^r['mask'])[0]==size-1 else 0 for r in rect];pa=dict(size=size,count=str(ct),witness=list(ws),**membership(inc,ct))
 fs=[];maxsize=0;maxm=[]
 for mask in range(1<<n):
  ids=[i for i in range(n)if mask>>i&1];bad=None
  for u,v in combinations(ids,2):
   # A containing all-one rectangle exists iff both crossed cells exist.
   rs={cells[u][0],cells[v][0]};cs={cells[u][1],cells[v][1]}
   if all(a[i][j]for i in rs for j in cs):bad=[u,v];break
  fs.append(dict(mask=mask,cells=ids,valid=bad is None,obstruction=bad))
  if bad is None:
   if len(ids)>maxsize:maxsize=len(ids);maxm=[mask]
   elif len(ids)==maxsize:maxm.append(mask)
 def det(rows,cols):
  total=0
  for p in permutations(range(len(rows))):
   sign=(-1)**sum(p[i]>p[j]for i in range(len(p))for j in range(i+1,len(p)));v=sign
   for i,j in enumerate(p):v*=a[rows[i]][cols[j]]
   total+=v
  return total
 rank=next((k for k in range(min(R,C),0,-1)if any(det(rs,cs)for rs in combinations(range(R),k)for cs in combinations(range(C),k))),0)
 factors={}
 for name,v in [('cover',co),('maximal_cover',mc),('partition',pa)]:
  ws=v['witness'];B=[[int(i in rect[k]['rows'])for k in ws]for i in range(R)];D=[[int(j in rect[k]['columns'])for j in range(C)]for k in ws];counts=[[sum(int(i in rect[k]['rows'] and j in rect[k]['columns'])for k in ws)for j in range(C)]for i in range(R)]
  factors[name]=dict(left=B,right=D,multiplicities=counts,boolean_product=[[int(v!=0)for v in row]for row in counts],overlap_cells=[[i,j]for i in range(R)for j in range(C)if counts[i][j]>1])
 return dict(schema='rectlab/2',input=data,cells=cells,rectangles=rect,cover=co,maximal_cover=mc,partition=pa,factors=factors,fooling_subsets=fs,maximum_fooling_size=maxsize,maximum_fooling_masks=maxm,real_rank=rank,lower_bound_gap=co['size']-maxsize,partition_gap=pa['size']-co['size'])

@lru_cache(maxsize=128)
def _expected(matrix):
 return json.dumps(reconstruct({'matrix':[list(r)for r in matrix]}))

def verify(report):
 if type(report)!=dict or 'input'not in report:raise ValueError('certificate object required')
 a=validate(report['input'])
 if not same(report,json.loads(_expected(tuple(tuple(r)for r in a)))):raise ValueError('certificate mismatch')
 return True

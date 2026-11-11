from functools import lru_cache
from fractions import Fraction
from itertools import combinations
from .schema import validate
from .families import census

def solve(data):
 a=validate(data);R=len(a);C=len(a[0]);cells=[[i,j]for i in range(R)for j in range(C)if a[i][j]];n=len(cells);full=(1<<n)-1;rect=[]
 for rm in range(1,1<<R):
  for cm in range(1,1<<C):
   rs=[i for i in range(R)if rm>>i&1];cs=[j for j in range(C)if cm>>j&1]
   if all(a[i][j]for i in rs for j in cs):
    mask=sum(1<<k for k,(i,j)in enumerate(cells)if i in rs and j in cs);rect.append(dict(id=len(rect),rows=rs,columns=cs,mask=mask))
 for r in rect:r['maximal']=not any(r['mask']!=s['mask'] and r['mask']&s['mask']==r['mask'] for s in rect)
 def optimize(ids,disjoint=False):return census(rect,n,ids,disjoint)
 cover=optimize(list(range(len(rect))));maxcover=optimize([r['id']for r in rect if r['maximal']]);partition=optimize(list(range(len(rect))),True)
 assert cover['size']==maxcover['size']
 fool=[];maxsize=0;maxids=[]
 for mask in range(1<<n):
  ids=[k for k in range(n)if mask>>k&1];bad=next(([u,v]for u,v in combinations(ids,2)if a[cells[u][0]][cells[v][1]] and a[cells[v][0]][cells[u][1]]),None)
  ok=bad is None
  fool.append(dict(mask=mask,cells=ids,valid=ok,obstruction=bad))
  if ok:
   if len(ids)>maxsize:maxsize=len(ids);maxids=[mask]
   elif len(ids)==maxsize:maxids.append(mask)
 # Exact rational row reduction, arithmetic rank not Boolean factor count.
 b=[list(map(Fraction,row))for row in a];rank=0
 for c in range(C):
  pivot=next((k for k in range(rank,R)if b[k][c]),None)
  if pivot is None:continue
  b[rank],b[pivot]=b[pivot],b[rank];v=b[rank][c];b[rank]=[x/v for x in b[rank]]
  for k in range(R):
   if k!=rank:
    v=b[k][c];b[k]=[x-v*y for x,y in zip(b[k],b[rank])]
  rank+=1
 def factor(ws):
  B=[[int(i in rect[k]['rows'])for k in ws]for i in range(R)];D=[[int(j in rect[k]['columns'])for j in range(C)]for k in ws];counts=[[sum(B[i][k]*D[k][j]for k in range(len(ws)))for j in range(C)]for i in range(R)]
  return dict(left=B,right=D,multiplicities=counts,boolean_product=[[int(v>0)for v in row]for row in counts],overlap_cells=[[i,j]for i in range(R)for j in range(C)if counts[i][j]>1])
 return dict(schema='rectlab/2',input=data,cells=cells,rectangles=rect,cover=cover,maximal_cover=maxcover,partition=partition,factors={name:factor(v['witness'])for name,v in [('cover',cover),('maximal_cover',maxcover),('partition',partition)]},fooling_subsets=fool,maximum_fooling_size=maxsize,maximum_fooling_masks=maxids,real_rank=rank,lower_bound_gap=cover['size']-maxsize,partition_gap=partition['size']-cover['size'])

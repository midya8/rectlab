from functools import lru_cache
import re

def _prepare(rect,n,ids,disjoint):
 full=(1<<n)-1
 @lru_cache(None)
 def dp(i,mask):
  if mask==full:return 0,1,()
  if i==len(ids):return n+1,0,()
  best,count,witness=dp(i+1,mask);rid=ids[i];m=rect[rid]['mask']
  if m&~mask and (not disjoint or not m&mask):
   val,ct,ws=dp(i+1,mask|m);val+=1;ws=(rid,)+ws
   if ct and val<best:best,count,witness=val,ct,ws
   elif ct and val==best:count+=ct;witness=min(witness,ws)
  return best,count,witness
 return dp

def census(rect,n,ids,disjoint=False):
 dp=_prepare(rect,n,ids,disjoint);full=(1<<n)-1
 value,count,ws=dp(0,0);inc=[0]*len(rect);states={0:1}
 for i,rid in enumerate(ids):
  nxt={};m=rect[rid]['mask']
  for mask,prefix in states.items():
   if mask==full:continue
   best=dp(i,mask)[0]
   if dp(i+1,mask)[0]==best:nxt[mask]=nxt.get(mask,0)+prefix
   if m&~mask and(not disjoint or not m&mask):
    v,ct,_=dp(i+1,mask|m)
    if ct and v+1==best:
     inc[rid]+=prefix*ct;nxt[mask|m]=nxt.get(mask|m,0)+prefix
  states=nxt
 return dict(size=value,count=str(count),witness=list(ws),inclusion_counts=list(map(str,inc)),mandatory=[i for i,c in enumerate(inc)if c==count],optional=[i for i,c in enumerate(inc)if 0<c<count],never=[i for i,c in enumerate(inc)if c==0])

def _context(report,family):
 if family not in ('cover','maximal_cover','partition'):raise ValueError('unknown family')
 rect=report['rectangles'];ids=[r['id']for r in rect if family!='maximal_cover'or r['maximal']];n=len(report['cells']);return rect,n,ids,family=='partition'

def select_from(report,family,index):
 if type(index)!=str or not re.fullmatch(r'0|[1-9][0-9]{0,99}',index):raise ValueError('canonical decimal index required, at most 100 digits')
 rank=int(index);rect,n,ids,disjoint=_context(report,family);dp=_prepare(rect,n,ids,disjoint)
 if rank>=dp(0,0)[1]:raise ValueError('index outside optimal family')
 mask=0;chosen=[];full=(1<<n)-1
 for i,rid in enumerate(ids):
  if mask==full:break
  m=rect[rid]['mask'];ct=0
  if m&~mask and(not disjoint or not m&mask):
   v,c,_=dp(i+1,mask|m)
   if v+1==dp(i,mask)[0]:ct=c
  if rank<ct:chosen.append(rid);mask|=m
  else:rank-=ct
 assert mask==full and rank==0
 return chosen

def rank_from(report,family,factors):
 rect,n,ids,disjoint=_context(report,family)
 if type(factors)!=list or any(type(v)!=int for v in factors)or factors!=sorted(set(factors))or any(v not in ids for v in factors):raise ValueError('sorted distinct legal factor ids required')
 dp=_prepare(rect,n,ids,disjoint);mask=0;rank=0;full=(1<<n)-1
 if len(factors)!=dp(0,0)[0]:raise ValueError('not a minimum witness')
 for i,rid in enumerate(ids):
  if mask==full:break
  m=rect[rid]['mask'];ct=0
  if m&~mask and(not disjoint or not m&mask):
   v,c,_=dp(i+1,mask|m)
   if v+1==dp(i,mask)[0]:ct=c
  if rid in factors:
   if not ct:raise ValueError('not an optimal witness')
   mask|=m
  else:rank+=ct
 if mask!=full or select_from(report,family,str(rank))!=factors:raise ValueError('not an optimal witness')
 return str(rank)

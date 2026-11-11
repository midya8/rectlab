export function validate(x){
 if(!x||typeof x!=='object'||Array.isArray(x)||Object.keys(x).sort().join()!=='matrix'||!Array.isArray(x.matrix)||x.matrix.length<1||x.matrix.length>5)throw Error('1..5 rows required');
 const a=x.matrix,c=Array.isArray(a[0])?a[0].length:0;
 if(c<1||c>5||a.some(row=>!Array.isArray(row)||row.length!==c||row.some(v=>!Number.isInteger(v)||(v!==0&&v!==1))))throw Error('rectangular integer 0/1 matrix required');
 if(a.flat().reduce((x,y)=>x+y,0)>12)throw Error('At most 12 one cells');return a;
}
export function solve(data){
 const a=validate(data),R=a.length,C=a[0].length,cells=[];for(let i=0;i<R;i++)for(let j=0;j<C;j++)if(a[i][j])cells.push([i,j]);const n=cells.length,full=(1<<n)-1,rect=[];
 for(let rm=1;rm<(1<<R);rm++)for(let cm=1;cm<(1<<C);cm++){
  const rows=Array.from({length:R},(_,i)=>i).filter(i=>rm>>i&1),columns=Array.from({length:C},(_,j)=>j).filter(j=>cm>>j&1);
  if(rows.every(i=>columns.every(j=>a[i][j])))rect.push({id:rect.length,rows,columns,mask:cells.reduce((m,[i,j],k)=>m|(rows.includes(i)&&columns.includes(j)?1<<k:0),0)});
 }
 for(const r of rect)r.maximal=!rect.some(s=>r.mask!==s.mask&&(r.mask&s.mask)===r.mask);
 const lex=(x,y)=>{for(let i=0;i<Math.min(x.length,y.length);i++)if(x[i]!==y[i])return x[i]-y[i];return x.length-y.length};
 function optimize(ids,disjoint=false){return census(rect,n,ids,disjoint)}
 const ids=rect.map(r=>r.id),cover=optimize(ids),maximal_cover=optimize(ids.filter(i=>rect[i].maximal)),partition=optimize(ids,true),fooling_subsets=[];let maximum_fooling_size=0,maximum_fooling_masks=[];
 for(let mask=0;mask<=full;mask++){
  const cs=cells.map((_,k)=>k).filter(k=>mask>>k&1);let obstruction=null;
  outer:for(let u=0;u<cs.length;u++)for(let v=u+1;v<cs.length;v++)if(a[cells[cs[u]][0]][cells[cs[v]][1]]&&a[cells[cs[v]][0]][cells[cs[u]][1]]){obstruction=[cs[u],cs[v]];break outer}
  const valid=obstruction===null;fooling_subsets.push({mask,cells:cs,valid,obstruction});if(valid){if(cs.length>maximum_fooling_size){maximum_fooling_size=cs.length;maximum_fooling_masks=[mask]}else if(cs.length===maximum_fooling_size)maximum_fooling_masks.push(mask)}
 }
 // Rational Gaussian elimination with integer numerator/denominator pairs.
 const gcd=(a,b)=>b?gcd(b,a%b):(a<0n?-a:a),rat=(p,q=1n)=>{if(q<0n){p=-p;q=-q}const g=gcd(p,q);return[p/g,q/g]},sub=([p,q],[r,s])=>rat(p*s-r*q,q*s),mul=([p,q],[r,s])=>rat(p*r,q*s),div=([p,q],[r,s])=>rat(p*s,q*r);
 const b=a.map(row=>row.map(v=>rat(BigInt(v))));let real_rank=0;
 for(let c=0;c<C;c++){const pivot=b.findIndex((row,k)=>k>=real_rank&&row[c][0]!==0n);if(pivot<0)continue;[b[real_rank],b[pivot]]=[b[pivot],b[real_rank]];const v=b[real_rank][c];b[real_rank]=b[real_rank].map(x=>div(x,v));for(let k=0;k<R;k++)if(k!==real_rank){const z=b[k][c];b[k]=b[k].map((x,j)=>sub(x,mul(z,b[real_rank][j])))}real_rank++}
 function factor(ws){const left=Array.from({length:R},(_,i)=>ws.map(k=>+rect[k].rows.includes(i))),right=ws.map(k=>Array.from({length:C},(_,j)=>+rect[k].columns.includes(j))),multiplicities=Array.from({length:R},(_,i)=>Array.from({length:C},(_,j)=>ws.reduce((v,k,ell)=>v+left[i][ell]*right[ell][j],0))),overlap_cells=[];for(let i=0;i<R;i++)for(let j=0;j<C;j++)if(multiplicities[i][j]>1)overlap_cells.push([i,j]);return{left,right,multiplicities,boolean_product:multiplicities.map(row=>row.map(v=>+(v>0))),overlap_cells}}
 return{schema:'rectlab/2',input:data,cells,rectangles:rect,cover,maximal_cover,partition,factors:{cover:factor(cover.witness),maximal_cover:factor(maximal_cover.witness),partition:factor(partition.witness)},fooling_subsets,maximum_fooling_size,maximum_fooling_masks,real_rank,lower_bound_gap:cover.size-maximum_fooling_size,partition_gap:partition.size-cover.size};
}
function same(a,b){if(typeof a!==typeof b||a===null||b===null)return a===b;if(Array.isArray(a)!==Array.isArray(b))return false;if(typeof a==='object'){const ks=Object.keys(a).sort(),ls=Object.keys(b).sort();return ks.join()===ls.join()&&ks.every(k=>same(a[k],b[k]))}return a===b}
export function replay(report){if(!same(report,solve(report.input)))throw Error('Certificate mismatch');return true}

const lex=(x,y)=>{for(let i=0;i<Math.min(x.length,y.length);i++)if(x[i]!==y[i])return x[i]-y[i];return x.length-y.length};
function prepare(rect,n,ids,disjoint){
 const full=(1<<n)-1,memo=new Map();function dp(i,mask){if(mask===full)return[0,1n,[]];if(i===ids.length)return[n+1,0n,[]];const key=i*4096+mask;if(memo.has(key))return memo.get(key);let[best,count,ws]=dp(i+1,mask);const rid=ids[i],m=rect[rid].mask;
 if((m&~mask)&&(!disjoint||!(m&mask))){let[v,ct,w]=dp(i+1,mask|m);v++;w=[rid,...w];if(ct&&v<best){best=v;count=ct;ws=w}else if(ct&&v===best){count+=ct;if(lex(w,ws)<0)ws=w}}const out=[best,count,ws];memo.set(key,out);return out}return dp;
}
function census(rect,n,ids,disjoint){
 const dp=prepare(rect,n,ids,disjoint),full=(1<<n)-1,[size,count,witness]=dp(0,0),inc=rect.map(()=>0n);let states=new Map([[0,1n]]);
 for(let i=0;i<ids.length;i++){const rid=ids[i],m=rect[rid].mask,nxt=new Map();for(const[mask,prefix]of states){if(mask===full)continue;const best=dp(i,mask)[0];if(dp(i+1,mask)[0]===best)nxt.set(mask,(nxt.get(mask)||0n)+prefix);if((m&~mask)&&(!disjoint||!(m&mask))){const[v,ct]=dp(i+1,mask|m);if(ct&&v+1===best){inc[rid]+=prefix*ct;nxt.set(mask|m,(nxt.get(mask|m)||0n)+prefix)}}}states=nxt}
 return{size,count:String(count),witness,inclusion_counts:inc.map(String),mandatory:rect.filter(r=>inc[r.id]===count).map(r=>r.id),optional:rect.filter(r=>inc[r.id]>0n&&inc[r.id]<count).map(r=>r.id),never:rect.filter(r=>inc[r.id]===0n).map(r=>r.id)};
}
function context(report,family){if(!['cover','maximal_cover','partition'].includes(family))throw Error('Unknown family');const rect=report.rectangles,n=report.cells.length,ids=rect.filter(r=>family!=='maximal_cover'||r.maximal).map(r=>r.id);return{rect,n,ids,disjoint:family==='partition'}}
export function selectFrom(report,family,index){
 if(typeof index!=='string'||!/^(0|[1-9][0-9]{0,99})$/.test(index))throw Error('Canonical decimal index required, at most 100 digits');let rank=BigInt(index);const{rect,n,ids,disjoint}=context(report,family),dp=prepare(rect,n,ids,disjoint),full=(1<<n)-1,chosen=[];if(rank>=dp(0,0)[1])throw Error('Index outside optimal family');let mask=0;
 for(let i=0;i<ids.length&&mask!==full;i++){const rid=ids[i],m=rect[rid].mask;let ct=0n;if((m&~mask)&&(!disjoint||!(m&mask))){const[v,c]=dp(i+1,mask|m);if(v+1===dp(i,mask)[0])ct=c}if(rank<ct){chosen.push(rid);mask|=m}else rank-=ct}if(mask!==full||rank!==0n)throw Error('Internal unrank mismatch');return chosen;
}
export function rankFrom(report,family,factors){
 const{rect,n,ids,disjoint}=context(report,family),dp=prepare(rect,n,ids,disjoint),full=(1<<n)-1;if(!Array.isArray(factors)||factors.some((v,i)=>!Number.isInteger(v)||!ids.includes(v)||(i&&factors[i-1]>=v))||factors.length!==dp(0,0)[0])throw Error('Sorted distinct optimal factors required');let mask=0,rank=0n;
 for(let i=0;i<ids.length&&mask!==full;i++){const rid=ids[i],m=rect[rid].mask;let ct=0n;if((m&~mask)&&(!disjoint||!(m&mask))){const[v,c]=dp(i+1,mask|m);if(v+1===dp(i,mask)[0])ct=c}if(factors.includes(rid)){if(!ct)throw Error('Not an optimal witness');mask|=m}else rank+=ct}if(mask!==full||!same(selectFrom(report,family,String(rank)),factors))throw Error('Not an optimal witness');return String(rank);
}
export function factorFrom(report,ws){const rect=report.rectangles,R=report.input.matrix.length,C=report.input.matrix[0].length,left=Array.from({length:R},(_,i)=>ws.map(k=>+rect[k].rows.includes(i))),right=ws.map(k=>Array.from({length:C},(_,j)=>+rect[k].columns.includes(j))),multiplicities=Array.from({length:R},(_,i)=>Array.from({length:C},(_,j)=>ws.reduce((v,k,ell)=>v+left[i][ell]*right[ell][j],0))),overlap_cells=[];for(let i=0;i<R;i++)for(let j=0;j<C;j++)if(multiplicities[i][j]>1)overlap_cells.push([i,j]);return{left,right,multiplicities,boolean_product:multiplicities.map(row=>row.map(v=>+(v>0))),overlap_cells}}

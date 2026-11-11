# Optional third-party numerical reference. Models are built from raw inputs,
# not RectLab's candidate list. The library uses floating-point tolerances.
import sys,json,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.fixtures import fixtures
from rectlab import solve
import numpy as np,scipy
from scipy.optimize import milp,Bounds,LinearConstraint
models=0
for data in fixtures():
 a=data['matrix'];R=len(a);C=len(a[0]);ones=[(i,j)for i in range(R)for j in range(C)if a[i][j]];n=len(ones);s=solve(data)
 if not n:continue
 rectangles=[]
 for k in range(1,1<<n):
  cells=[ones[z]for z in range(n)if k>>z&1];rs={i for i,j in cells};cs={j for i,j in cells}
  if len(rs)*len(cs)==len(cells):rectangles.append(set(cells))
 incidence=np.array([[int(p in q)for q in rectangles]for p in ones],dtype=float)
 for key,upper in [('cover',np.full(n,np.inf)),('partition',np.ones(n))]:
  res=milp(np.ones(len(rectangles)),integrality=np.ones(len(rectangles)),bounds=Bounds(0,1),constraints=LinearConstraint(incidence,np.ones(n),upper),options={'time_limit':30,'mip_rel_gap':0})
  assert res.success and round(res.fun)==s[key]['size'];chosen=[k for k,v in enumerate(res.x)if v>0.5];assert len(chosen)==s[key]['size'];counts=[sum(p in rectangles[k]for k in chosen)for p in ones];assert all(v==1 if key=='partition'else v>=1 for v in counts);models+=1
 pairs=[(i,j)for i,j in itertools.combinations(range(n),2)if a[ones[i][0]][ones[j][1]]and a[ones[j][0]][ones[i][1]]]
 if pairs:
  B=np.array([[int(k in pair)for k in range(n)]for pair in pairs],dtype=float);constraint=LinearConstraint(B,np.zeros(len(pairs)),np.ones(len(pairs)))
 else:constraint=()
 res=milp(-np.ones(n),integrality=np.ones(n),bounds=Bounds(0,1),constraints=constraint,options={'time_limit':30,'mip_rel_gap':0});assert res.success and round(-res.fun)==s['maximum_fooling_size'];chosen=[i for i,v in enumerate(res.x)if v>0.5];assert all(not(i in chosen and j in chosen)for i,j in pairs);models+=1
print(json.dumps({'scipy':scipy.__version__,'inputs':len(fixtures()),'nonempty_models':models,'objectives':['cover','partition','fooling'],'tolerance':'floating point MILP reference; integer witnesses directly checked; not a proof of exactness or tie counts'}))

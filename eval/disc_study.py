"""If a report is only "somewhere within 20 km of me", how big is the
ambiguity, and how fast does it shrink as towers are added?

Formalised properly: two places are indistinguishable if exactly the same set
of cameras can see both. So the ambiguity region for a fire is the set of
cells sharing its coverage signature. That is the hard floor on disc-only
localisation -- before any weighting.
"""
import numpy as np, math, sys
sys.path.insert(0,"/Users/maximecarriere/src/wild-fire-integrator")
from pyember import GridGeometry
from pyember.geo import ring_network

geo = GridGeometry(cell_size_m=500.0)
gx, gy = geo.cell_centres()
CELL_KM2 = (geo.cell_size_m/1000)**2

print(f"{'towers':>7}{'sees >=1':>10}{'>=2':>8}{'>=3':>8}"
      f"{'median ambiguity':>19}{'equiv radius':>14}")
print("-"*68)
for n in (4, 6, 8, 12, 16, 24, 32):
    cams = ring_network(geo, n, max_range_m=20000.0)
    # binary coverage mask per camera
    cov = np.stack([(np.hypot(gx-c.x_m, gy-c.y_m) <= c.max_range_m) for c in cams])
    ncov = cov.sum(0)
    # signature = which cameras see this cell, packed as an integer
    sig = np.zeros(gx.shape, dtype=np.int64)
    for i in range(n):
        sig |= (cov[i].astype(np.int64) << i)
    # ambiguity: cells sharing a signature, over cells seen by >=2 towers
    interior = ncov >= 2
    vals, counts = np.unique(sig[interior], return_counts=True)
    size_of = dict(zip(vals.tolist(), counts.tolist()))
    amb = np.array([size_of[s] for s in sig[interior].ravel()])
    med = np.median(amb) * CELL_KM2
    print(f"{n:>7}{(ncov>=1).mean()*100:>9.0f}%{(ncov>=2).mean()*100:>7.0f}%"
          f"{(ncov>=3).mean()*100:>7.0f}%{med:>16.1f} km2"
          f"{math.sqrt(med/math.pi)*1000:>11.0f} m")

print()
print("For reference, the simulator's MEASURED disc-only error was ~1,184 m.")
print("The binary floor above is looser than that, because a disc is not flat:")
print("range falloff makes a cell near a camera score higher than one far from")
print("it, so the overlap has a PEAK, not a plateau. That gradient is doing")
print("real work -- it recovers range information the set-intersection throws away.")

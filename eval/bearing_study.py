"""How much is knowing the camera's direction actually worth?

A PTZ tower knows its pan angle, and the plume's pixel position inside the
frame refines it further -- so a bearing is usually available. But it is not
guaranteed: a fixed camera of unknown aim, a gas sensor, a 911 call and a
utility fault sensor all report a PLACE and no direction at all.

So this measures the whole range, from a hairline bearing to none at all.
Each geometry is tuned to its OWN best threshold -- comparing them at one
threshold merely reports which geometry that threshold was tuned for.
"""

import multiprocessing as mp, numpy as np, sys
sys.path.insert(0,"/Users/maximecarriere/src/wild-fire-integrator")
from sim.scenario import make_scenario, DAY_TICKS
from eval.pipeline import run_all

MODES=[(2.0,"precise bearing (+/-2 deg)"),
       (10.0,"camera FOV (+/-10 deg)"),
       (30.0,"coarse sector (+/-30 deg)"),
       (400.0,"NO bearing (GPS only)")]
THETAS=[0.2,0.4,0.8,1.5,3.0,5.0]

def one(job):
    sig, th, seed = job
    scen = make_scenario(n_cams=8, n_days=1.0, n_fires=3, seed=seed)
    r = run_all(scen, DAY_TICKS, proj_sigma=sig, grid_kw={"theta_base":th})
    d = r["ember"].summary(scen)
    return sig, th, d["false_alerts_per_day"], d["detection_rate"], d["median_loc_error_m"]

if __name__=="__main__":
    jobs=[(s,t,seed) for s,_ in MODES for t in THETAS for seed in range(3)]
    with mp.Pool(min(mp.cpu_count(),10)) as pool: rows=pool.map(one,jobs)
    print(f"{'geometry':<28}{'best th':>8}{'FA/day':>9}{'detect':>9}{'loc err':>10}")
    print("-"*66)
    for sig,label in MODES:
        best=None
        for t in THETAS:
            sel=[r for r in rows if r[0]==sig and r[1]==t]
            dr=np.mean([r[3] for r in sel]); fa=np.median([r[2] for r in sel])
            le=[r[4] for r in sel if r[4] is not None]
            if dr>=0.95 and (best is None or fa<best[1]):
                best=(t,fa,dr,np.median(le) if le else None)
        if best is None:   # nothing reached 95% -- report the best detection instead
            cand=max(THETAS,key=lambda t:np.mean([r[3] for r in rows if r[0]==sig and r[1]==t]))
            sel=[r for r in rows if r[0]==sig and r[1]==cand]
            le=[r[4] for r in sel if r[4] is not None]
            best=(cand,np.median([r[2] for r in sel]),np.mean([r[3] for r in sel]),
                  np.median(le) if le else None)
        t,fa,dr,le=best
        print(f"{label:<28}{t:>8.2f}{fa:>9.0f}{dr*100:>8.0f}%"
              f"{(f'{le:.0f} m' if le else '-'):>10}")

import multiprocessing as mp, numpy as np, sys
sys.path.insert(0,"/Users/maximecarriere/src/wild-fire-integrator")
from sim.scenario import make_scenario, DAY_TICKS
from eval.pipeline import run_all
# only the best theta per geometry, but at the SAME 8 seeds as the headline table
BEST=[(2.0,5.0,"bearing +/-2 deg"),(10.0,3.0,"bearing +/-10 deg"),
      (30.0,0.4,"bearing +/-30 deg"),(400.0,0.2,"GPS only (20 km disc)")]
def one(j):
    sig,th,seed=j
    sc=make_scenario(n_cams=8,n_days=1.0,n_fires=3,seed=seed)
    r=run_all(sc,DAY_TICKS,proj_sigma=sig,grid_kw={"theta_base":th})
    d=r["ember"].summary(sc)
    return sig,d["false_alerts_per_day"],d["detection_rate"],d["median_loc_error_m"]
if __name__=="__main__":
    jobs=[(s,t,seed) for s,t,_ in BEST for seed in range(8)]
    with mp.Pool(min(mp.cpu_count(),10)) as p: rows=p.map(one,jobs)
    print(f"{'geometry':<26}{'theta':>6}{'FA/day':>9}{'detect':>9}{'loc err':>10}   (8 seeds)")
    print("-"*64)
    for sig,th,lab in BEST:
        sel=[r for r in rows if r[0]==sig]
        le=[r[3] for r in sel if r[3] is not None]
        print(f"{lab:<26}{th:>6.1f}{np.median([r[1] for r in sel]):>9.0f}"
              f"{np.mean([r[2] for r in sel])*100:>8.0f}%"
              f"{(f'{np.median(le):.0f} m' if le else '-'):>10}")

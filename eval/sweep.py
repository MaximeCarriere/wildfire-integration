"""Sensitivity sweep across seeds -> results/raw/sweep.json.

One scenario proves nothing, so every operating point is run over several
independent scenarios and reported with a spread.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import pathlib
import time

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
METHODS = ("raw", "temporal", "m_of_n", "triangulation", "ember")


def _one(job):
    from eval.pipeline import run_all
    from sim.scenario import DAY_TICKS, make_scenario

    seed, theta, n_cams, n_days, n_fires = job
    scen = make_scenario(n_cams=n_cams, n_days=n_days, n_fires=n_fires, seed=seed)
    res = run_all(scen, int(n_days * DAY_TICKS), grid_kw={"theta_base": theta})
    return {"seed": seed, "theta": theta, "n_cams": n_cams,
            "results": {m: res[m].summary(scen) for m in METHODS}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--cams", type=int, default=8)
    ap.add_argument("--days", type=float, default=1.0)
    ap.add_argument("--fires", type=int, default=3)
    ap.add_argument("--thetas", type=float, nargs="+",
                    default=[2.0, 3.0, 4.0, 5.0, 6.5, 8.0, 10.0, 13.0])
    ap.add_argument("--out", default="results/raw/sweep.json")
    a = ap.parse_args()

    jobs = [(s, th, a.cams, a.days, a.fires)
            for s in range(a.seeds) for th in a.thetas]
    t0 = time.time()
    with mp.Pool(min(mp.cpu_count(), 10)) as pool:
        rows = pool.map(_one, jobs)
    dt = time.time() - t0

    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"config": vars(a), "rows": rows}, indent=1))

    print(f"{len(jobs)} runs in {dt:.0f}s -> {a.out}\n")
    print(f"{'method':<14} {'theta':>6} {'false alerts/day':>18} {'detect':>8} "
          f"{'latency':>9} {'loc err':>9}")
    print("-" * 70)
    for m in METHODS:
        for th in ([None] if m != "ember" else a.thetas):
            sel = [r for r in rows if m != "ember" or r["theta"] == th]
            if m != "ember":
                sel = [r for r in rows if r["theta"] == a.thetas[0]]
            fa = [r["results"][m]["false_alerts_per_day"] for r in sel]
            dr = [r["results"][m]["detection_rate"] for r in sel]
            la = [r["results"][m]["median_latency_min"] for r in sel
                  if r["results"][m]["median_latency_min"] is not None]
            le = [r["results"][m]["median_loc_error_m"] for r in sel
                  if r["results"][m]["median_loc_error_m"] is not None]
            print(f"{m:<14} {('-' if th is None else f'{th:.1f}'):>6} "
                  f"{np.median(fa):>10.1f} ±{np.percentile(fa,75)-np.percentile(fa,25):>5.0f} "
                  f"{np.mean(dr)*100:>7.0f}% "
                  f"{(np.median(la) if la else float('nan')):>7.0f}m "
                  f"{(f'{np.median(le):.0f} m' if le else '-'):>9}")


if __name__ == "__main__":
    main()

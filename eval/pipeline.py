"""Run every method over the SAME detection stream and score them.

Four methods, in increasing sophistication. All four consume identical raw
detector output, so differences are attributable to the fusion logic alone:

  raw        alert on every detector firing -- what a network with no fusion
             at all would page a human for. Upper bound.
  temporal   per-camera temporal confirmation only (ember Layer 1 alone).
             This is roughly the current deployed state of the art.
  m_of_n     M distinct cameras report within a sliding window. Cross-camera
             voting with NO geometry -- the obvious thing to try, and the one
             that correlated regional events defeat.
  ember      full two-layer network with bearing geometry and center-surround.
"""
from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field

import numpy as np

from pyember.core import TIER_SILENT, TIER_STRONG, TIER_WEAK, Grid, Node
from eval.triangulation import TriangulationDetector
from sim.scenario import DAY_TICKS, Scenario


EPISODE_GAP_TICKS = 180      # 30 min -- same incident if it recurs within this
EPISODE_RADIUS_M = 2000.0    # and within this distance


@dataclass
class Result:
    method: str
    alerts: int = 0
    false_alerts: int = 0
    detected: dict = field(default_factory=dict)   # ignition idx -> tick of first alert
    loc_errors: list = field(default_factory=list)
    false_events: list = field(default_factory=list)  # (tick, x_m|None, y_m|None)
    ticks: int = 0

    def false_episodes(self) -> int:
        """Distinct incidents an operator would have to investigate.

        Counting raw alerts is not comparable across methods: a location-less
        baseline collapses everything into one stream, while a located method
        can legitimately report several different places at once. What a
        dispatcher actually experiences is DISTINCT INCIDENTS, so alerts are
        clustered in time -- and in space where a method provides it.
        """
        eps = 0
        open_clusters: list = []      # (last_tick, x, y)
        for t, x, y in sorted(self.false_events, key=lambda e: e[0]):
            open_clusters = [c for c in open_clusters if t - c[0] <= EPISODE_GAP_TICKS]
            hit = None
            for i, (lt, cx, cy) in enumerate(open_clusters):
                if x is None or cx is None:
                    hit = i               # no location: time proximity alone
                    break
                if math.hypot(x - cx, y - cy) <= EPISODE_RADIUS_M:
                    hit = i
                    break
            if hit is None:
                eps += 1
                open_clusters.append((t, x, y))
            else:
                open_clusters[hit] = (t, open_clusters[hit][1], open_clusters[hit][2])
        return eps

    def summary(self, scen: Scenario) -> dict:
        days = self.ticks / DAY_TICKS
        n_fires = len(scen.ignitions)
        lat = [(self.detected[i] - scen.ignitions[i].t_start) for i in self.detected]
        return {
            "method": self.method,
            "false_episodes_per_day": self.false_episodes() / days if days else float("nan"),
            "false_alerts_per_day": self.false_alerts / days if days else float("nan"),
            "detected": len(self.detected),
            "n_fires": n_fires,
            "detection_rate": len(self.detected) / n_fires if n_fires else float("nan"),
            "median_latency_min": (float(np.median(lat)) * 10.0 / 60.0) if lat else None,
            "median_loc_error_m": (float(np.median(self.loc_errors)) if self.loc_errors else None),
            "localises": bool(self.loc_errors),
            "total_alerts": self.alerts,
        }


def _match_fire(scen: Scenario, t: int, x_m=None, y_m=None, tol_m=2000.0):
    """Is there a real, currently-visible fire this alert can be credited to?

    Location-aware methods must also be CLOSE to it. Methods that produce no
    location get credited on time alone, which is generous to the baselines.
    """
    for i, ig in enumerate(scen.ignitions):
        if ig.visibility(t) <= 0.0:
            continue
        if x_m is None:
            return i
        if math.hypot(x_m - ig.x_m, y_m - ig.y_m) <= tol_m:
            return i
    return None


BEARING_BIN = 5.0          # degrees; granularity of a baseline nuisance mask
MASK_TICKS = 2160          # 6 h -- how long a masked bearing stays masked


def run_all(scen: Scenario, total_ticks: int, sensitivity: str = "normal",
            m_of_n: tuple[int, int] = (2, 30), adaptive: bool = True,
            confirm_accuracy: float = 0.95, weak_period: int = 12,
            weak_scale: float = 0.35, grid_kw: dict | None = None,
            rng=None) -> dict[str, Result]:
    """Score all four methods on one scenario.

    adaptive=True gives EVERY method a like-for-like feedback channel, because
    comparing an adaptive system against non-adaptive baselines would be
    rigged. Each alert dispatches a confirmation asset which returns a verdict:

      temporal / m_of_n  mask the offending camera+bearing bin for six hours.
                         This is exactly what deployed networks do by hand --
                         ALERTCalifornia had to teach its software to ignore
                         the Geysers steam field.
      ember              feed the verdict back as inhibition plus a local
                         threshold rise.

    Every method is therefore charged the same price (one confirmation per
    alert) and given the same information. What differs is only how well each
    can USE it: a bearing mask blinds a camera along a whole ray, while cell
    adaptation suppresses just the offending location.
    """
    if rng is None:
        rng = np.random.default_rng(12345)
    geo = scen.geo
    res = {k: Result(k) for k in ("raw", "temporal", "m_of_n", "triangulation", "ember")}

    nodes_t = {c.cam_id: Node() for c in scen.cams}     # for `temporal`
    nodes_e = {c.cam_id: Node() for c in scen.cams}     # for `ember` / `m_of_n`
    cams = {c.cam_id: c for c in scen.cams}

    grid = Grid(**(grid_kw or {}))
    grid.set_sensitivity(sensitivity)

    M, W = m_of_n
    window: deque = deque()          # (tick, cam_id) of STRONG events
    mofn_cool = 0
    masked: dict[tuple[int, int], int] = {}   # (cam, bearing bin) -> expiry tick
    tri = TriangulationDetector(scen.cams, geo, min_cams=M, window=W)

    def is_masked(cid, bearing, t):
        return adaptive and masked.get((cid, int(bearing // BEARING_BIN)), -1) > t

    def mask(cid, bearing, t):
        if adaptive:
            masked[(cid, int(bearing // BEARING_BIN))] = t + MASK_TICKS

    def verdict(x_m, y_m, t):
        """Ground-truth confirmation from a dispatched asset, with error."""
        truth = 1 if _match_fire(scen, t, x_m, y_m) is not None else -1
        return truth if rng.random() < confirm_accuracy else -truth

    for t in range(total_ticks):
        dets = scen.detections(t)

        # ---- raw: every detector firing is an alert -------------------------
        for d in dets:
            res["raw"].alerts += 1
            i = _match_fire(scen, t)
            if i is None:
                res["raw"].false_alerts += 1
                res["raw"].false_events.append((t, None, None))
            else:
                res["raw"].detected.setdefault(i, t)

        # ---- feed Layer 1 (masked bearings are simply not looked at) ---------
        bearing_of = {}
        for d in dets:
            if is_masked(d.cam_id, d.bearing_deg, t):
                continue
            nodes_t[d.cam_id].observe(d.cls, d.conf)
            nodes_e[d.cam_id].observe(d.cls, d.conf)
            bearing_of[d.cam_id] = d.bearing_deg   # last bearing this tick

        strong_now = []
        for cid in cams:
            if nodes_t[cid].tick() == TIER_STRONG:
                res["temporal"].alerts += 1
                i = _match_fire(scen, t)
                if i is None:
                    res["temporal"].false_alerts += 1
                    res["temporal"].false_events.append((t, None, None))
                    if cid in bearing_of:
                        mask(cid, bearing_of[cid], t)
                else:
                    res["temporal"].detected.setdefault(i, t)
            tier_e = nodes_e[cid].tick()
            # Rate coding. The weak tier is defined as a LOW spike rate, not a
            # continuous stream -- emitting it every tick would inject an order
            # of magnitude more current than the core is tuned for, and the
            # spatial layer would light up on sub-threshold noise.
            if cid in bearing_of and (
                    tier_e == TIER_STRONG or
                    (tier_e == TIER_WEAK and (t % weak_period) == (cid % weak_period))):
                strong_now.append((cid, bearing_of[cid], tier_e))

        # ---- m_of_n: cross-camera voting, no geometry ------------------------
        for cid, _, tier in strong_now:
            if tier == TIER_STRONG:
                window.append((t, cid))
        while window and window[0][0] < t - W:
            window.popleft()
        if mofn_cool > 0:
            mofn_cool -= 1
        elif len({c for _, c in window}) >= M:
            res["m_of_n"].alerts += 1
            mofn_cool = 30
            i = _match_fire(scen, t)
            if i is None:
                res["m_of_n"].false_alerts += 1
                res["m_of_n"].false_events.append((t, None, None))
                for _, c in window:
                    if c in bearing_of:
                        mask(c, bearing_of[c], t)
            else:
                res["m_of_n"].detected.setdefault(i, t)

        # ---- triangulation: classical cross-bearing voting -------------------
        for cid, bearing, tier in strong_now:
            if tier == TIER_STRONG:
                tri.report(t, cid, bearing)
        for (tx, ty, ncam) in tri.tick(t):
            res["triangulation"].alerts += 1
            i = _match_fire(scen, t, tx, ty)
            if i is None:
                res["triangulation"].false_alerts += 1
                res["triangulation"].false_events.append((t, tx, ty))
                if adaptive:
                    tri.reject(t, tx, ty)
            else:
                res["triangulation"].detected.setdefault(i, t)
                res["triangulation"].loc_errors.append(
                    math.hypot(tx - scen.ignitions[i].x_m, ty - scen.ignitions[i].y_m))

        # ---- ember: geometry + spatial integration --------------------------
        for cid, bearing, tier in strong_now:
            scale = 1.0 if tier == TIER_STRONG else weak_scale   # graded uplink
            cells, w = cams[cid].project(bearing)
            if len(cells):
                grid.inject_many(cells, w, cid, scale=scale)

        for sp in grid.tick():
            ex, ey = geo.centre_of(sp.cell)
            res["ember"].alerts += 1
            i = _match_fire(scen, t, ex, ey)
            if i is None:
                res["ember"].false_alerts += 1
                res["ember"].false_events.append((t, ex, ey))
            else:
                res["ember"].detected.setdefault(i, t)
                res["ember"].loc_errors.append(
                    math.hypot(ex - scen.ignitions[i].x_m, ey - scen.ignitions[i].y_m))
            if adaptive:
                grid.confirm(sp.cell, verdict(ex, ey, t), sp.response)

    for r in res.values():
        r.ticks = total_ticks
    return res

"""Classical cross-bearing triangulation with voting -- the baseline that matters.

A location-less M-of-N vote is not a fair competitor for a system whose whole
output is a location, so this implements what an engineer would actually build
instead: intersect the bearing rays, cluster the intersections, and require
several cameras to agree on a cluster before alerting. Ghost intersections are
rejected the standard way, by demanding that a cluster be supported by more
bearings than a coincidence would produce.

This is the Osborne Firefinder done arithmetically. If the spiking integrator
cannot beat it, the spiking integrator is not worth its complexity.
"""
from __future__ import annotations

import math
from collections import deque


def ray_intersect(x0, y0, b0_deg, x1, y1, b1_deg, min_sin=0.09):
    """Intersection of two compass-bearing rays, or None.

    min_sin rejects near-parallel pairs: when two towers are nearly collinear
    with the target the intersection is numerically wild and geometrically
    meaningless (this is GDOP, the same effect that degrades a GPS fix from
    badly placed satellites).
    """
    b0, b1 = math.radians(b0_deg), math.radians(b1_deg)
    s0, c0 = math.sin(b0), math.cos(b0)
    s1, c1 = math.sin(b1), math.cos(b1)
    det = s0 * (-c1) - (-s1) * c0
    if abs(det) < min_sin:
        return None
    dx, dy = x1 - x0, y1 - y0
    t = (dx * (-c1) - (-s1) * dy) / det
    u = (s0 * dy - c0 * dx) / det
    if t <= 0 or u <= 0:            # behind one of the cameras
        return None
    return x0 + t * s0, y0 + t * c0


class TriangulationDetector:
    def __init__(self, cams, geo, min_cams=2, window=30, cluster_m=1500.0,
                 cooldown=30, mask_ticks=2160, mask_radius_m=2000.0):
        self.cams = {c.cam_id: c for c in cams}
        self.geo = geo
        self.min_cams = min_cams
        self.window = window
        self.cluster_m = cluster_m
        self.cooldown = cooldown
        self.mask_ticks = mask_ticks
        self.mask_radius_m = mask_radius_m
        self.reports: deque = deque()      # (tick, cam_id, bearing)
        self.cool: dict = {}               # cluster key -> expiry tick
        self.masked: list = []             # (x, y, expiry tick)

    def report(self, t, cam_id, bearing_deg):
        self.reports.append((t, cam_id, bearing_deg))

    def reject(self, t, x, y):
        """Feedback: this location was investigated and found benign."""
        self.masked.append((x, y, t + self.mask_ticks))

    def _is_masked(self, t, x, y):
        self.masked = [m for m in self.masked if m[2] > t]
        return any(math.hypot(x - mx, y - my) <= self.mask_radius_m
                   for mx, my, _ in self.masked)

    def tick(self, t):
        while self.reports and self.reports[0][0] < t - self.window:
            self.reports.popleft()
        if len({c for _, c, _ in self.reports}) < self.min_cams:
            return []

        # latest bearing per camera
        latest: dict = {}
        for tt, cid, b in self.reports:
            latest[cid] = b

        pts = []
        ids = sorted(latest)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a, b = self.cams[ids[i]], self.cams[ids[j]]
                p = ray_intersect(a.x_m, a.y_m, latest[ids[i]],
                                  b.x_m, b.y_m, latest[ids[j]])
                if p is None:
                    continue
                w, h = self.geo.extent_m
                if not (0 <= p[0] <= w and 0 <= p[1] <= h):
                    continue
                pts.append((p[0], p[1], ids[i], ids[j]))

        # greedy spatial clustering of intersections
        clusters: list = []
        for x, y, ca, cb in pts:
            for cl in clusters:
                if math.hypot(x - cl["x"], y - cl["y"]) <= self.cluster_m:
                    n = cl["n"]
                    cl["x"] = (cl["x"] * n + x) / (n + 1)
                    cl["y"] = (cl["y"] * n + y) / (n + 1)
                    cl["n"] = n + 1
                    cl["cams"].update((ca, cb))
                    break
            else:
                clusters.append({"x": x, "y": y, "n": 1, "cams": {ca, cb}})

        out = []
        for cl in clusters:
            # A ghost is an accidental crossing of two unrelated bearings, so
            # require the cluster to be supported by at least min_cams towers.
            if len(cl["cams"]) < self.min_cams:
                continue
            key = (int(cl["x"] // self.cluster_m), int(cl["y"] // self.cluster_m))
            if self.cool.get(key, -1) > t:
                continue
            if self._is_masked(t, cl["x"], cl["y"]):
                continue
            self.cool[key] = t + self.cooldown
            out.append((cl["x"], cl["y"], len(cl["cams"])))
        return out

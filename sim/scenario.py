"""Scenario generator for a wildfire camera network.

Calibration note. The per-camera detector model is anchored to two published
numbers rather than invented:

  * TPR at good range comes from the companion repo's measured Jetson result
    (0.778 mAP50 for YOLOv5s @512px on D-Fire), so the sim inherits a detector
    whose accuracy was actually benchmarked on hardware.
  * Nuisance sources are tuned so that AFTER per-camera temporal confirmation
    each camera reports on the order of one false positive per day -- the rate
    ALERTCalifornia publishes for a deployed 1,000+ camera network.

The false-positive processes are the documented failure modes, not generic
noise: single-camera nuisances (road dust, lens glint, a cloud shadow crossing
one field of view), a persistent fixed source (geothermal steam, an industrial
stack), and a CORRELATED regional event (marine layer, smoke drift from a
distant incident) that many cameras see at once. The last one is the case that
defeats naive cross-camera voting.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from pyember.core import CLASS_FIRE, CLASS_SMOKE, TIER_SILENT, Node
from pyember.geo import Camera, GridGeometry

TICK_SECONDS = 10.0   # a PTZ tower cycles its presets; ~1 look per 10 s
DAY_TICKS = int(86400 / TICK_SECONDS)

# Measured on Jetson Orin Nano, YOLOv5s @512px TensorRT FP16, D-Fire.
JETSON_MAP50 = 0.778


@dataclass
class Ignition:
    """A real fire. Detectability ramps as the plume develops."""

    x_m: float
    y_m: float
    t_start: int
    growth_ticks: int = 90           # ~15 min to a clearly visible plume
    smoke_before_flame: int = 60     # smoke is visible well before flame
    duration_ticks: int = 1440       # 4 h, then contained and no longer visible

    def visibility(self, t: int) -> float:
        if t < self.t_start or t >= self.t_start + self.duration_ticks:
            return 0.0
        return min(1.0, (t - self.t_start) / max(1, self.growth_ticks))

    def cls(self, t: int) -> int:
        return CLASS_FIRE if (t - self.t_start) > self.smoke_before_flame else CLASS_SMOKE


@dataclass
class NuisanceSource:
    """Something that looks like smoke but is not."""

    cam_ids: list[int]               # which cameras can see it
    bearing_by_cam: dict[int, float]
    t_start: int
    duration: int
    strength: float = 0.5
    drift_deg_per_tick: float = 0.0  # cloud shadows move; steam vents do not
    arc_deg: float = 0.0             # angular EXTENT as seen from a tower

    def active(self, t: int) -> bool:
        return self.t_start <= t < self.t_start + self.duration

    def bearing(self, cam_id: int, t: int, rng=None) -> float:
        """Bearing of one detection from this source.

        arc_deg is what separates a point-like nuisance from an extended one.
        A steam vent or dust plume is a point: every detection comes back on
        essentially the same bearing. A marine layer or a regional smoke pall
        fills a wide swath of the tower's view, so successive detections land
        anywhere across tens of degrees. That difference is the whole reason
        the integrator can tell them apart -- point sources converge to a
        compact intersection, extended ones never converge at all.
        """
        b = self.bearing_by_cam[cam_id] + self.drift_deg_per_tick * (t - self.t_start)
        if self.arc_deg > 0.0 and rng is not None:
            b += rng.uniform(-0.5, 0.5) * self.arc_deg
        return b % 360.0


@dataclass
class Detection:
    cam_id: int
    bearing_deg: float
    cls: int
    conf: float


@dataclass
class Scenario:
    geo: GridGeometry
    cams: list[Camera]
    ignitions: list[Ignition] = field(default_factory=list)
    nuisances: list[NuisanceSource] = field(default_factory=list)
    seed: int = 0

    # detector model
    tpr_good_range: float = JETSON_MAP50
    p_nuisance_detect: float = 0.30
    conf_true_mu: float = 0.72
    conf_false_mu: float = 0.55

    def __post_init__(self):
        self.rng = np.random.default_rng(self.seed)

    def detections(self, t: int) -> list[Detection]:
        """Raw per-frame detector output for this tick, before any integration."""
        out: list[Detection] = []
        for cam in self.cams:
            for ig in self.ignitions:
                vis = ig.visibility(t)
                if vis <= 0.0:
                    continue
                r = cam.range_to(ig.x_m, ig.y_m)
                if r > cam.max_range_m:
                    continue
                # range falloff, same shape the geometry layer assumes
                rw = 1.0 if r <= cam.good_range_m else 1.0 / (
                    1.0 + ((r - cam.good_range_m) / cam.good_range_m) ** 2)
                p = self.tpr_good_range * rw * vis
                if self.rng.random() < p:
                    b = cam.bearing_to(ig.x_m, ig.y_m) + self.rng.normal(0, cam.bearing_sigma_deg)
                    out.append(Detection(cam.cam_id, b % 360.0, ig.cls(t),
                                         float(np.clip(self.rng.normal(self.conf_true_mu, 0.12), 0.05, 1.0))))
            for ns in self.nuisances:
                if not ns.active(t):
                    continue
                for cid in ns.cam_ids:
                    if self.rng.random() < self.p_nuisance_detect * ns.strength:
                        out.append(Detection(cid, ns.bearing(cid, t, self.rng), CLASS_SMOKE,
                                             float(np.clip(self.rng.normal(self.conf_false_mu, 0.15), 0.05, 1.0))))
        return out


def build_nuisances(geo: GridGeometry, cams: list[Camera], rng, n_days: float,
                    independent_per_cam_per_day: float = 8.0,
                    n_correlated_per_day: float = 4.0,
                    n_persistent: int = 1) -> list[NuisanceSource]:
    """Populate the three documented false-positive families."""
    out: list[NuisanceSource] = []
    total_ticks = int(n_days * DAY_TICKS)
    w, h = geo.extent_m

    # 1. independent single-camera nuisances: dust, glint, one cloud shadow
    for cam in cams:
        k = rng.poisson(independent_per_cam_per_day * n_days)
        for _ in range(k):
            out.append(NuisanceSource(
                cam_ids=[cam.cam_id],
                bearing_by_cam={cam.cam_id: rng.uniform(0, 360)},
                t_start=int(rng.integers(0, max(1, total_ticks))),
                duration=int(rng.integers(6, 60)),      # 1-10 min
                strength=float(rng.uniform(0.4, 1.0)),
                drift_deg_per_tick=float(rng.normal(0, 0.2)),
            ))

    # 2. a persistent fixed source every camera in range can see: steam vent
    for _ in range(n_persistent):
        px, py = rng.uniform(0.2 * w, 0.8 * w), rng.uniform(0.2 * h, 0.8 * h)
        seen = [c for c in cams if c.range_to(px, py) <= c.max_range_m]
        if len(seen) < 2:
            continue
        out.append(NuisanceSource(
            cam_ids=[c.cam_id for c in seen],
            bearing_by_cam={c.cam_id: c.bearing_to(px, py) for c in seen},
            t_start=0, duration=total_ticks, strength=0.30))

    # 3. CORRELATED regional events: marine layer / distant smoke drift.
    #    Every camera sees haze at a bearing pointing into the same broad
    #    region, so simple cross-camera voting corroborates a non-event.
    k = rng.poisson(n_correlated_per_day * n_days)
    for _ in range(k):
        hx, hy = rng.uniform(0, w), rng.uniform(0, h)
        out.append(NuisanceSource(
            cam_ids=[c.cam_id for c in cams],
            bearing_by_cam={c.cam_id: c.bearing_to(hx, hy) + rng.normal(0, 12) for c in cams},
            t_start=int(rng.integers(0, max(1, total_ticks))),
            duration=int(rng.integers(180, 720)),   # 30 min - 2 h
            strength=float(rng.uniform(0.5, 0.9)),
            drift_deg_per_tick=float(rng.normal(0, 0.1)),
            arc_deg=float(rng.uniform(40.0, 90.0))))
    return out


def make_scenario(n_cams: int = 8, n_days: float = 1.0, n_fires: int = 3,
                  seed: int = 0, cell_size_m: float = 500.0,
                  **cam_kw) -> Scenario:
    from pyember.geo import ring_network

    rng = np.random.default_rng(seed)
    geo = GridGeometry(cell_size_m=cell_size_m)
    cams = ring_network(geo, n_cams, **cam_kw)
    w, h = geo.extent_m
    total = int(n_days * DAY_TICKS)

    # Fires are placed in disjoint time slots. Overlapping fires would make
    # attribution ambiguous for the baselines, which produce no location and
    # can only be credited on timing.
    fires = []
    if n_fires:
        slot = total // n_fires
        for k in range(n_fires):
            lo = k * slot + int(0.05 * slot)
            fires.append(Ignition(
                x_m=float(rng.uniform(0.25 * w, 0.75 * w)),
                y_m=float(rng.uniform(0.25 * h, 0.75 * h)),
                t_start=int(rng.integers(lo, lo + max(1, int(0.35 * slot)))),
                duration_ticks=min(1440, int(0.55 * slot))))

    return Scenario(geo=geo, cams=cams, ignitions=fires,
                    nuisances=build_nuisances(geo, cams, rng, n_days), seed=seed)

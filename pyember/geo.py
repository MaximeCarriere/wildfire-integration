"""Bearing-only geometry: turning camera detections into grid injections.

Monocular range-to-smoke is poor -- a plume's distance is genuinely ambiguous
from one image -- and PTZ cameras slew continuously. So a detection is modelled
as a BEARING with a few degrees of uncertainty and essentially no range
information, which is what the sensor actually provides.

Localisation therefore comes from cross-bearing intersection: exactly how
staffed lookout towers worked for a century with the Osborne Firefinder. Two
towers, two bearings, one intersection. Nothing here computes an intersection
explicitly -- overlapping wedges simply sum in the grid, and the integrator's
center-surround stage finds where they cross.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from .core import GRID_H, GRID_W


@dataclass
class GridGeometry:
    """Local ENU grid. Metres, origin at the south-west corner."""

    cell_size_m: float = 500.0
    width: int = GRID_W
    height: int = GRID_H

    @property
    def extent_m(self) -> tuple[float, float]:
        return self.width * self.cell_size_m, self.height * self.cell_size_m

    def cell_centres(self) -> tuple[np.ndarray, np.ndarray]:
        xs = (np.arange(self.width) + 0.5) * self.cell_size_m
        ys = (np.arange(self.height) + 0.5) * self.cell_size_m
        return np.meshgrid(xs, ys)

    def cell_of(self, x_m: float, y_m: float) -> int:
        cx = min(max(int(x_m // self.cell_size_m), 0), self.width - 1)
        cy = min(max(int(y_m // self.cell_size_m), 0), self.height - 1)
        return cy * self.width + cx

    def centre_of(self, cell: int) -> tuple[float, float]:
        cx, cy = cell % self.width, cell // self.width
        return (cx + 0.5) * self.cell_size_m, (cy + 0.5) * self.cell_size_m


@dataclass
class Camera:
    """One tower. Bearings are compass degrees: 0 = north, 90 = east."""

    cam_id: int
    x_m: float
    y_m: float
    max_range_m: float = 20000.0
    good_range_m: float = 8000.0        # beyond this, detection degrades
    bearing_sigma_deg: float = 2.0      # angular uncertainty of a detection

    _geo: GridGeometry | None = field(default=None, repr=False)
    _bearing: np.ndarray | None = field(default=None, repr=False)
    _range: np.ndarray | None = field(default=None, repr=False)
    _rangew: np.ndarray | None = field(default=None, repr=False)

    def precompute(self, geo: GridGeometry) -> "Camera":
        """Cache per-cell bearing and range.

        On the MCU this table is built once on the Linux side and shipped to
        the Cortex-M33 as a lookup, so the real-time core never evaluates a
        trigonometric function.
        """
        gx, gy = geo.cell_centres()
        dx, dy = gx - self.x_m, gy - self.y_m
        self._geo = geo
        self._range = np.hypot(dx, dy)
        # compass bearing: atan2(east, north)
        self._bearing = np.degrees(np.arctan2(dx, dy)) % 360.0

        # Detection confidence falls off with distance: a plume subtends fewer
        # pixels the further away it is. Flat out to good_range, then decaying,
        # and hard zero past max_range.
        r = self._range
        w = np.ones_like(r)
        far = r > self.good_range_m
        w[far] = 1.0 / (1.0 + ((r[far] - self.good_range_m) / self.good_range_m) ** 2)
        w[r > self.max_range_m] = 0.0
        self._rangew = w
        return self

    def bearing_to(self, x_m: float, y_m: float) -> float:
        return math.degrees(math.atan2(x_m - self.x_m, y_m - self.y_m)) % 360.0

    def range_to(self, x_m: float, y_m: float) -> float:
        return math.hypot(x_m - self.x_m, y_m - self.y_m)

    def project(self, bearing_deg: float, sigma_deg: float | None = None,
                cutoff_sigma: float = 2.5):
        """Project a bearing-only detection into (cells, weights).

        Weights are peak-normalised, not sum-normalised. Sum-normalising would
        make a long wedge inject a thin smear and a short one a bright spot,
        which is backwards: the evidence a detection carries does not depend on
        how many cells its wedge happens to cross. Peak-normalising keeps a
        single camera's contribution bounded, so a lone wedge stays a
        low-contrast streak while two crossing wedges make a compact peak --
        which is precisely what the integrator's center-surround stage looks for.
        """
        if self._bearing is None:
            raise RuntimeError("call precompute(geo) first")
        sigma = self.bearing_sigma_deg if sigma_deg is None else sigma_deg

        d = np.abs((self._bearing - bearing_deg + 180.0) % 360.0 - 180.0)
        mask = (d <= cutoff_sigma * sigma) & (self._rangew > 0.0)
        if not mask.any():
            return np.empty(0, dtype=np.int32), np.empty(0, dtype=np.float32)

        w = np.exp(-0.5 * (d[mask] / sigma) ** 2) * self._rangew[mask]
        cells = np.flatnonzero(mask.ravel()).astype(np.int32)
        peak = w.max()
        if peak <= 0:
            return np.empty(0, dtype=np.int32), np.empty(0, dtype=np.float32)
        return cells, (w / peak).astype(np.float32)


def ring_network(geo: GridGeometry, n: int, radius_frac: float = 0.42,
                 **cam_kw) -> list[Camera]:
    """Cameras on a ring around the region -- towers on the ridgelines.

    A ring gives good bearing diversity for interior targets, which is what
    cross-bearing localisation needs: two towers nearly collinear with a fire
    intersect at a glancing angle and localise it poorly.
    """
    w, h = geo.extent_m
    cx, cy, r = w / 2.0, h / 2.0, min(w, h) * radius_frac
    cams = []
    for i in range(n):
        a = 2.0 * math.pi * i / n
        cams.append(Camera(cam_id=i,
                           x_m=cx + r * math.cos(a),
                           y_m=cy + r * math.sin(a),
                           **cam_kw).precompute(geo))
    return cams

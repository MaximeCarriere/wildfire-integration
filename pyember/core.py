"""Pythonic wrapper over the C core.

The simulator drives the *real* firmware code through cffi rather than a
reimplementation, so every number the evaluation harness reports comes from
the same instructions that will run on the Cortex-M33. Sim and device cannot
silently diverge.
"""
from __future__ import annotations

import pathlib
import sys
from dataclasses import dataclass

_BUILD = pathlib.Path(__file__).resolve().parents[1] / "build"
if str(_BUILD) not in sys.path:
    sys.path.insert(0, str(_BUILD))

try:
    import _ember  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "the ember C extension is not built -- run:\n"
        "    python3 bindings/python/build_ember.py"
    ) from exc

lib = _ember.lib
ffi = _ember.ffi

ONE = lib.EMBER_Q16_ONE
CELLS = lib.EMBER_CELLS
GRID_W = lib.EMBER_GRID_W
GRID_H = lib.EMBER_GRID_H
WIRE_BYTES = lib.EMBER_EVENT_WIRE_BYTES

CLASS_SMOKE = lib.EMBER_CLASS_SMOKE
CLASS_FIRE = lib.EMBER_CLASS_FIRE
TIER_SILENT, TIER_WEAK, TIER_STRONG = 0, 1, 2

PRESETS = {"normal": 1.00, "elevated": 0.85, "red_flag": 0.70}


class Q16:
    """Q16.16 conversions. Kept explicit so rounding is never accidental."""

    @staticmethod
    def of(x: float) -> int:
        return int(round(x * 65536.0))

    @staticmethod
    def to(q: int) -> float:
        return q / 65536.0


@dataclass
class Spike:
    cell: int
    x: int
    y: int
    response: float
    contributors: int
    n_contributors: int
    tick: int


@dataclass
class Event:
    """The 16-byte record a camera puts on the air."""

    t_decisec: int
    node_id: int
    bearing_ddeg: int
    tier: int
    cls: int
    conf: int
    bearing_sigma: int = 2
    seq: int = 0

    def pack(self) -> bytes:
        e = ffi.new("ember_event *")
        e.t_decisec = self.t_decisec
        e.node_id = self.node_id
        e.bearing_ddeg = self.bearing_ddeg
        e.tier = self.tier
        e.cls = self.cls
        e.conf = self.conf
        e.bearing_sigma = self.bearing_sigma
        e.seq = self.seq
        buf = ffi.new("uint8_t[]", WIRE_BYTES)
        lib.ember_event_pack(e, buf)
        return bytes(ffi.buffer(buf, WIRE_BYTES))

    @staticmethod
    def unpack(raw: bytes) -> "Event | None":
        """Returns None for a corrupt record. Never guesses."""
        assert len(raw) == WIRE_BYTES
        e = ffi.new("ember_event *")
        buf = ffi.new("uint8_t[]", list(raw))
        if lib.ember_event_unpack(e, buf) != 0:
            return None
        return Event(e.t_decisec, e.node_id, e.bearing_ddeg, e.tier,
                     e.cls, e.conf, e.bearing_sigma, e.seq)


class Node:
    """Layer 1 -- one per camera. Integrates that camera's detections in time."""

    def __init__(self, **overrides):
        self._p = ffi.new("ember_node_params *")
        lib.ember_node_defaults(self._p)
        for k, v in overrides.items():
            setattr(self._p, k, Q16.of(v) if k.startswith(("w_", "theta_", "v_")) else v)
        self._n = ffi.new("ember_node *")
        lib.ember_node_init(self._n)

    def observe(self, cls: int, conf: float) -> None:
        lib.ember_node_observe(self._n, self._p, cls, Q16.of(conf))

    def tick(self) -> int:
        return int(lib.ember_node_tick(self._n, self._p))

    @property
    def v(self) -> float:
        return Q16.to(self._n.v)


class Grid:
    """Layer 2 -- the regional integrator."""

    MAX_SPIKES = 32

    def __init__(self, **overrides):
        self._p = ffi.new("ember_grid_params *")
        lib.ember_grid_defaults(self._p)
        for k, v in overrides.items():
            if k in ("theta_base", "v_reset", "v_floor", "norm_k", "adapt_margin"):
                setattr(self._p, k, Q16.of(v))
            else:
                setattr(self._p, k, v)
        self._g = ffi.new("ember_grid *")
        lib.ember_grid_init(self._g, self._p)
        self._out = ffi.new("ember_spike[]", self.MAX_SPIKES)

    def inject(self, cell: int, current: float, camera_id: int) -> None:
        lib.ember_grid_inject(self._g, cell, Q16.of(current), camera_id)

    def inject_many(self, cells, weights, camera_id: int, scale: float = 1.0) -> None:
        """Bulk-inject one event's whole bearing wedge."""
        for c, w in zip(cells, weights):
            lib.ember_grid_inject(self._g, int(c), Q16.of(float(w) * scale), camera_id)

    def tick(self) -> list[Spike]:
        n = lib.ember_grid_tick(self._g, self._out, self.MAX_SPIKES)
        return [
            Spike(s.cell, s.x, s.y, Q16.to(s.v), s.contributors, s.n_contributors, s.tick)
            for s in (self._out[i] for i in range(n))
        ]

    def confirm(self, cell: int, verdict: int, observed_response: float) -> None:
        lib.ember_grid_confirm(self._g, cell, verdict, Q16.of(observed_response))

    def set_sensitivity(self, preset: str | float) -> None:
        scale = PRESETS[preset] if isinstance(preset, str) else preset
        lib.ember_grid_set_sensitivity(self._g, Q16.of(scale))

    def set_fire_danger(self, scale: float) -> None:
        """scale < 1 sharpens the whole network as fire weather worsens."""
        lib.ember_grid_set_fire_danger(self._g, Q16.of(scale))

    def theta(self, cell: int = 0) -> float:
        return Q16.to(lib.ember_grid_theta(self._g, cell))

    def response_field(self):
        import numpy as np
        buf = ffi.buffer(self._g.resp, CELLS * 4)
        return (np.frombuffer(buf, dtype="<i4").astype("float32") / 65536.0
                ).reshape(GRID_H, GRID_W)

    def potential_field(self):
        import numpy as np
        buf = ffi.buffer(self._g.v, CELLS * 4)
        return (np.frombuffer(buf, dtype="<i4").astype("float32") / 65536.0
                ).reshape(GRID_H, GRID_W)

    @property
    def tick_count(self) -> int:
        return self._g.tick

    @staticmethod
    def state_bytes() -> int:
        return lib.ember_grid_state_bytes()

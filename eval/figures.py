"""results/raw/sweep.json -> results/figures/*.png"""
from __future__ import annotations

import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Validated categorical palette (CVD dE 9.1 adjacent, normal-vision 22.9).
# Dark is the same four hues re-stepped for the dark surface -- a selected
# palette, not an inverted one.
THEME = {
    "light": dict(C={"ember": "#2a78d6", "triangulation": "#eb6834",
                     "temporal": "#1baf7a", "m_of_n": "#eda100"},
                  INK="#0b0b0b", INK2="#52514e", INK3="#8a8880",
                  SURFACE="#fcfcfb", GRID="#e6e5e0", SPINE="#d8d7d1",
                  LEGEDGE="#e0dfd9"),
    "dark": dict(C={"ember": "#3987e5", "triangulation": "#d95926",
                    "temporal": "#199e70", "m_of_n": "#c98500"},
                 INK="#ffffff", INK2="#c3c2b7", INK3="#8f8e85",
                 SURFACE="#1a1a19", GRID="#2e2e2c", SPINE="#3a3a37",
                 LEGEDGE="#3a3a37"),
}

LABEL = {"ember": "ember (spiking)", "triangulation": "cross-bearing triangulation",
         "temporal": "per-camera temporal only", "m_of_n": "M-of-N vote (no location)"}


def load(path="results/raw/sweep.json"):
    return json.loads((ROOT / path).read_text())


def pareto(data, out="results/figures/pareto.png", mode="light"):
    TH = THEME[mode]
    C, INK, INK2, INK3 = TH["C"], TH["INK"], TH["INK2"], TH["INK3"]
    SURFACE = TH["SURFACE"]
    rows = data["rows"]
    thetas = sorted({r["theta"] for r in rows})

    fig, ax = plt.subplots(figsize=(9.2, 5.8), dpi=170)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    # ember: the sweep, as a curve
    xs, ys = [], []
    for th in thetas:
        sel = [r["results"]["ember"] for r in rows if r["theta"] == th]
        xs.append(np.median([s["false_alerts_per_day"] for s in sel]))
        ys.append(np.mean([s["detection_rate"] for s in sel]) * 100)
    ax.plot(xs, ys, "-", lw=2, color=C["ember"], zorder=3, solid_capstyle="round")
    ax.plot(xs, ys, "o", ms=8, color=C["ember"], zorder=4,
            markeredgecolor=SURFACE, markeredgewidth=2)

    for th, x, y in zip(thetas, xs, ys):
        if th in (2.0, 5.0, 8.0, 10.0, 13.0):
            ax.annotate(f"θ={th:g}", (x, y), textcoords="offset points",
                        xytext=(0, 13 if th in (5.0, 2.0) else -19),
                        ha="center", fontsize=8.5, color=INK3)

    # baselines: single operating points. Offsets are hand-placed because
    # three of the four sit at 100% detection and would otherwise collide.
    OFF = {"triangulation": (11, -16, "left"),
           "temporal": (11, -17, "left"),
           "m_of_n": (0, 15, "center")}
    handles = [plt.Line2D([], [], color=C["ember"], lw=2, marker="o", ms=7,
                          markeredgecolor=SURFACE, markeredgewidth=1.5,
                          label=LABEL["ember"])]
    for m in ("triangulation", "temporal", "m_of_n"):
        sel = [r["results"][m] for r in rows if r["theta"] == thetas[0]]
        x = np.median([s["false_alerts_per_day"] for s in sel])
        y = np.mean([s["detection_rate"] for s in sel]) * 100
        mk = "D" if m == "triangulation" else "s"
        ax.plot([x], [y], mk, ms=9, color=C[m],
                markeredgecolor=SURFACE, markeredgewidth=2, zorder=5)
        dx, dy, ha = OFF[m]
        ax.annotate(LABEL[m], (x, y), textcoords="offset points",
                    xytext=(dx, dy), ha=ha, fontsize=9, color=INK2)
        handles.append(plt.Line2D([], [], color=C[m], lw=0, marker=mk, ms=8,
                                  markeredgecolor=SURFACE, markeredgewidth=1.5,
                                  label=LABEL[m]))

    ax.annotate("ember (spiking integrator)", (xs[-2], ys[-2]),
                textcoords="offset points", xytext=(14, -4),
                fontsize=9.5, color=INK, fontweight="semibold", va="center")

    leg = ax.legend(handles=handles, loc="lower right", frameon=True,
                    fontsize=8.5, borderpad=0.7, labelspacing=0.55,
                    handletextpad=0.7)
    leg.get_frame().set_facecolor(SURFACE)
    leg.get_frame().set_edgecolor(TH["LEGEDGE"])
    leg.get_frame().set_linewidth(0.8)
    for txt in leg.get_texts():
        txt.set_color(INK2)

    ax.set_xscale("log")
    ax.set_xlabel("false alerts per day  (network of 8 towers, log scale)",
                  fontsize=10, color=INK2)
    ax.set_ylabel("fires detected  (%)", fontsize=10, color=INK2)
    ax.set_ylim(68, 106)
    ax.set_title("Fewer false alarms at the same detection rate",
                 fontsize=13.5, color=INK, loc="left", pad=14)
    ax.text(0, 1.015, "better is up and to the left  ·  8 scenarios per point, 24 h each",
            transform=ax.transAxes, fontsize=9, color=INK3)

    ax.grid(True, which="major", color=TH["GRID"], lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(TH["SPINE"])
    ax.tick_params(colors=INK3, labelsize=9)

    fig.tight_layout()
    p = ROOT / out
    p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(p, facecolor=SURFACE)
    plt.close(fig)
    return p


if __name__ == "__main__":
    d = load()
    print("wrote", pareto(d, "results/figures/pareto.png", "light"))
    print("wrote", pareto(d, "results/figures/pareto-dark.png", "dark"))

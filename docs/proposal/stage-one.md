# A Neuromorphic Osborne Firefinder

### Spiking evidence fusion for wildfire camera networks

**Resilient America Preparedness Challenge — Stage One Proposal · Track A**
Pillars addressed: *anticipate and mitigate risk* · *enable real-time response* ·
*operate in mission-critical environments*

---

## 1. Problem statement

Abatzoglou and Williams (2016) attribute **more than half** of the observed
increase in fuel aridity across western US forests since the 1970s to
human-caused climate change, and find that it **doubled the cumulative
western-US forest fire area over 1984–2015**. Between 2000 and 2015 it added
75% more forested area experiencing high fire-danger conditions.
*(Impact of anthropogenic climate change on wildfire across western US
forests*, PNAS 113(42):11770–11775.)

That attribution is specifically to **western US forest** fire area over a
defined window. It is not a claim about all US land, and not a claim against a
pre-suppression baseline — measured against the 1930s, US area burned has
fallen, and we will not quote a decade that flatters us.

Federal suppression has averaged **$2.9 billion a year** over the last decade,
projected to rise a further 42% by 2050; counting health, property and
disruption, climate-exacerbated wildfire costs the US **$394–893 billion**
annually.

### The claim we do not make

It is tempting to argue that faster detection means smaller fires and lower
cost. The best study we found says otherwise. Analysing Western Canadian fires
2015–2020, Bałek et al. (PLOS ONE, 2024) find **no evidence that fire size
increases with reporting delay**; delays account for roughly 3% of suppression
costs, and cutting them by a full hour buys a 0.25% cost reduction. Their
conclusion is that detection investment is *"not justified on suppression cost
savings alone."*

Their setting is remote boreal fire, much of it monitored rather than fought,
and they measure suppression cost rather than evacuation lead time or property
loss. But it is good evidence and it points away from the easy version of our
pitch. **So we claim an operational result, not an outcome one:** we reduce the
number of alerts a human must adjudicate. Whether that converts into fewer
acres is unproven, and we have not tried to prove it.

### America already built the sensors, and cannot use them

ALERTCalifornia operates more than 1,000 AI-equipped cameras at a published rate
of "less than one false positive per day per camera." Across the network that is
on the order of **1,000 false alarms every day**, and each one is resolved the
same way it was in 1935: a human being looks at it. The failure modes are well
documented and stubborn — cloud, fog, dust, and geothermal or industrial steam.
Operators had to teach the system to ignore the Geysers steam field by hand.

The research literature already knows the fix. Temporal confirmation drops
false-alarm rates from 52% to 4%. But in every deployed network that
confirmation step is performed by a person, which means the confirmation layer —
not the camera, not the model — is the bottleneck. Every camera added to the
network adds detection capability *and* adds load to the one component that
cannot be scaled by buying more hardware.

Meanwhile the detectors keep improving and the networks keep growing. Both
trends make the fusion gap worse, not better.

**We are not proposing another smoke detector. We are proposing the layer above
them** — the part that reasons over many weak, unreliable, geographically
distributed signals and decides whether anything is actually burning, and where.

## 2. Affected community and beneficiaries

- **Wildland fire dispatchers and camera-network watchstanders**, who absorb the
  false-alarm load today and whose attention is the scarce resource during a
  red-flag event — precisely when alarm volume peaks.
- **Rural and wildland-urban-interface communities** in California, Oregon,
  Nevada, Colorado and across the West, where minutes between ignition and
  first response determine whether an incident stays a spot fire.
- **Volunteer and small municipal fire departments**, who cannot staff a
  24-hour camera watch and are therefore excluded from the benefits of the
  networks their counties are already paying for.
- **Tribal and remote land managers** operating where cellular backhaul is
  intermittent or absent, and where a system that needs the cloud to think is a
  system that stops thinking exactly when it is needed.

## 3. Technical approach

### 3.1 Cameras as sensory neurons

Each camera stops being an alarm source and becomes a sensory neuron, emitting a
**16-byte event** rather than a video stream. A two-layer spiking network fuses
those events:

| | runs on | integrates over | question it answers |
|---|---|---|---|
| **Layer 1** | the camera node | **time** | is this plume persisting? |
| **Layer 2** | Arduino UNO Q | **space** | do independent bearings agree? |

The two layers compute genuinely different things, which is what makes the
neuromorphic framing substantive rather than decorative. We state plainly that a
*single* leaky integrate-and-fire cell is mathematically an
exponentially-weighted moving average with a threshold; the contribution is the
**network** — coincidence detection across bearings, lateral coupling,
normalization, and adaptation.

Layer 1's output is **graded, not a gate** — a 2-bit rate-coded tier. A hard
local threshold would discard exactly the sub-threshold evidence Layer 2 exists
to combine: two cameras each at 60% of their own threshold are individually
silent, yet jointly they are the strongest signal in the network.

### 3.2 The spatial integrator

One LIF neuron per geographic cell, with four mechanisms:

1. **Coincidence gain** — current from N *distinct* cameras is superlinear. A
   dust plume in front of one camera cannot be corroborated from a different
   bearing. This rejects the single-camera false positives that dominate.
2. **Lateral coupling** (a discrete Laplacian) — absorbs bearing error and lets
   crossing wedges reinforce without inventing evidence.
3. **Center-surround with divisive gain control** — coincidence gain alone would
   *amplify* correlated false positives such as a marine layer or regional smoke
   drift. Center-surround separates them: haze is a shift in the local
   background, a fire is local contrast on top of it. This is the computation
   retinal ganglion cells use to stay contrast-invariant under changing
   illumination, and it is doing real work here: **our own measurements show
   that without the divisive term, a haze edge alone scores higher than a
   genuine two-camera fire.**
4. **Adaptation** — a rejected confirmation raises the threshold *at that place*,
   above the response that caused the false alarm. A steam vent stops
   re-alerting without desensitising the rest of the grid.

Sensitivity is an operator preset (Normal / Elevated / Red Flag) that otherwise
tracks the local fire-danger index automatically — the *anticipate and mitigate
risk* pillar, implemented rather than asserted.

### 3.3 Bearing-only sensing, by choice

Monocular range-to-smoke is poor and PTZ cameras slew continuously, so we model
a detection as a **bearing with a few degrees of uncertainty and no range**.
Localisation comes from cross-bearing intersection — exactly how staffed lookout
towers worked for a century with the Osborne Firefinder. Nothing computes an
intersection explicitly: overlapping wedges sum in the grid and the
center-surround stage finds where they cross.

Camera density beats per-camera precision. Error falls roughly as 1/√N, and the
larger gain is geometric: two towers nearly collinear with a fire intersect at a
glancing angle, and a third at a different bearing fixes it outright.

### 3.4 Tiered confirmation, and a drone used responsibly

The membrane potential sets the confirmation budget, so cost scales with
evidence strength:

| tier | asset | latency | when |
|---|---|---|---|
| 1 | PTZ slew-to-bearing + detector on the zoomed crop | seconds | any spike |
| 2 | drone, dispatched automatically | ~20 min | occlusion, out of range, night, ambiguity |
| 3 | crew dispatch | — | latched alarm |

Automated drone confirmation is legitimate at the **pre-confirmation** stage,
before any TFR exists or firefighting aircraft launch. The genuine operational
risk is the handoff: a drone still airborne when a fire is confirmed and aircraft
arrive becomes an incursion — the hazard that grounds air attack. The broker
therefore implements **automatic recall on confirmation or TFR issuance**.

### 3.5 Hardware mapping

The UNO Q's dual-brain architecture maps onto this design directly, and we use
both brains for what each is for:

- **STM32U585 (Cortex-M33)** — the always-on, low-power, deterministic LIF core.
  Fixed-point, no floating point, no allocator, bounded state.
- **Qualcomm Dragonwing QRB2210** (quad Cortex-A53 + Adreno, Debian) — event
  ingest over LoRa/cellular, the confirmation model on zoomed PTZ crops,
  dispatch and operator interface. GPU-assisted inference; we note the platform
  has **no discrete NPU** and have sized the confirmation model accordingly.

Camera view-cone tables are precomputed on the Linux side and shipped to the M33
as a lookup, so the real-time core never evaluates a trigonometric function.

## 4. Why this must run at the edge

Three reasons, none of them decorative:

1. **Bandwidth.** A 16-byte event survives LoRa duty-cycle limits, satellite
   backhaul and degraded cellular. Video does not. This is what lets the system
   reach towers that cannot justify a broadband link.
2. **Survivability.** Wildfire destroys communications infrastructure. When the
   uplink fails, an edge integrator keeps reasoning on whatever still arrives; a
   cloud service simply stops. The *operate in mission-critical environments*
   pillar is a hard requirement here, not an aspiration.
3. **Attention economics.** The scarce resource is the dispatcher, not the
   compute. Filtering at the edge means only corroborated, localised candidates
   ever reach a human.

## 5. Feasibility

**This is not a concept. The core is built, measured, and reproducible today.**

- The integrator is implemented in portable C99 — no floating point, no `libm`,
  no allocator, and no C library at all. It **cross-compiles clean for Cortex-M33
  (thumbv8m.main, freestanding, `-Werror`)** and passes 53 tests plus a pinned
  golden-vector hash.
- Because it is fixed-point, host and target output are **bit-identical**. A
  golden-vector hash proves the MCU port is correct *before the dev kit ships* —
  removing the single largest schedule risk in a hardware challenge.
- State is bounded and statically sized: **116 KB for a 64×64 cell grid**,
  comfortably inside the STM32U585's 786 KB SRAM, at **56 µs per tick** on the
  development host.
- The simulator drives the **real firmware code** through a cffi binding, so the
  numbers below and the shipped firmware cannot drift apart.

### Measured results

Eight independent 24-hour scenarios, 8 towers, three ignitions each, against
three documented false-positive families. Every method consumes the *same*
detector stream and receives the *same* confirmation feedback budget. The
simulated detector is anchored to a measured benchmark — 0.778 mAP50 for
YOLOv5s @512px on D-Fire, from our companion Jetson study — and nuisance rates
are tuned to reproduce the published ≈1 false positive per camera per day.

| method | false alerts/day | detected | latency | localises |
|---|---:|---:|---:|---|
| raw detector output | 29,820 | 100% | 0 min | no |
| cross-bearing triangulation | 208 | 96% | 12 min | 343 m |
| per-camera temporal only | 143 | 100% | 11 min | no |
| M-of-N vote | 30 | 100% | 11 min | no |
| **this work**, θ=5 | **113** | **100%** | 12 min | 674 m |
| **this work**, θ=8 | **47** | 96% | 13 min | 680 m |

**At matched detection rate, we produce 47 false alerts per day against
classical cross-bearing triangulation's 208 — a 4.4× reduction.** At θ=5 we
dominate triangulation on both axes simultaneously: fewer false alarms *and*
higher detection.

Against a persistent false source specifically — a steam vent two towers can
both see, every alert investigated and rejected — the system issues **12 alerts
over six hours against 2,700 raw detections, a 225× reduction**, while a real
ignition 12 km away is still caught immediately and at full strength.
Suppression stays local.

### What we state honestly

- M-of-N voting yields the lowest raw alarm count (30/day) but produces **no
  location**. Its alerts are not directly actionable; ours arrive with
  coordinates. That is a difference in kind, not a number we claim to win.
- Our localisation (≈650 m) is coarser than analytic triangulation (≈343 m)
  because we quantise to 500 m cells. Halving the cell size halves the error at
  four times the memory — a deliberate, adjustable trade.
- A spatially *compact* correlated event — a controlled burn, or smoke drifting
  from a real fire outside the region — is geometrically indistinguishable from
  an ignition. Only the confirmation tier resolves that case, and we do not
  claim otherwise.

### Stage Two plan

The prototype will run the integrator on the UNO Q with three to four physical
camera nodes emitting events over LoRa, an alert firing on-board, and PTZ
slew-to-confirm closing the loop with the detection model on the Dragonwing
side. The ingest layer is already designed for that topology, so Stage Two is
assembly and validation rather than rework.

## 6. Building in the open

We are not promising to; we already are.

- **Apache-2.0 from the first commit**, deliberately permissive, and kept
  separate from the AGPL detector by a process boundary rather than a
  licence argument.
- **The simulator is public too**, so anyone can attack our numbers using our
  own tools rather than taking them on trust. Every figure in this proposal
  regenerates with a single command.
- **Negative results are published at the same volume as positive ones.** An
  appendix of our deck is titled *"four things the measurements forced us to
  fix"* — a normalisation scheme that masked real fires, an adaptation rule
  that did nothing, a rate-coding bug of our own making. A build log that
  contains only successes is marketing.

Through Stage Two: build notes at each milestone recording what was tried,
what the measurement said and what changed as a result; hardware files
(wiring, radio choice, node build) published alongside the firmware so the
prototype is reproducible rather than merely watchable; and written guidance
on retargeting it, since the thresholds are deployment-specific and saying so
is more useful than shipping ours.

## 7. Team and licensing

Building on a prior measured study of wildfire detection on edge hardware
(D-Fire, TensorRT, Jetson Orin Nano), which supplies both the detector model and
the empirical grounding for this system's sensor assumptions.

The integrator is **Apache-2.0**. The detection model it consults is AGPL-3.0
via YOLOv5, so the integrator reaches it across a **process boundary** rather
than linking it — keeping both licences intact and the commercialisation
pathway open.

---

*Source: https://github.com/MaximeCarriere/wild-fire-integrator*

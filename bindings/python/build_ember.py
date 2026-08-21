"""Build the cffi extension that lets the simulator drive the real C core.

The point of binding rather than reimplementing: every number the evaluation
harness produces comes from the exact code that will run on the MCU, so the
proposal's claims and the firmware cannot drift apart.
"""
import os
import pathlib
from cffi import FFI

ROOT = pathlib.Path(__file__).resolve().parents[2]
CORE = ROOT / "core"

GRID_W = int(os.environ.get("EMBER_GRID_W", 64))
GRID_H = int(os.environ.get("EMBER_GRID_H", 64))

ffi = FFI()

ffi.cdef(r"""
typedef int32_t ember_q16;

typedef enum { EMBER_CLASS_NONE=0, EMBER_CLASS_SMOKE=1, EMBER_CLASS_FIRE=2 } ember_class;
typedef enum { EMBER_TIER_SILENT=0, EMBER_TIER_WEAK=1, EMBER_TIER_STRONG=2 } ember_tier;

typedef struct {
    ember_q16 w_smoke, w_fire;
    uint8_t   leak_shift;
    ember_q16 theta_weak, theta_strong, v_reset;
    uint16_t  refractory_ticks;
    ...;
} ember_node_params;

typedef struct { ember_q16 v, inject; uint16_t refractory; uint8_t tier; ...; } ember_node;

void       ember_node_init(ember_node *);
void       ember_node_defaults(ember_node_params *);
void       ember_node_observe(ember_node *, const ember_node_params *, ember_class, ember_q16);
ember_tier ember_node_tick(ember_node *, const ember_node_params *);

typedef struct {
    uint8_t   leak_shift, lateral_shift;
    ember_q16 gain_lut[...];
    ember_q16 theta_base, v_reset, v_floor;
    uint8_t   refractory_ticks;
    ember_q16 norm_k;
    uint8_t   surround_radius;
    uint16_t  coincidence_ticks;
    ember_q16 adapt_margin;
    uint8_t   adapt_decay_shift, nms_radius, confirm_radius;
    ...;
} ember_grid_params;

typedef struct {
    uint32_t  cell;
    uint16_t  x, y;
    ember_q16 v;
    uint32_t  contributors;
    uint8_t   n_contributors;
    uint32_t  tick;
    ...;
} ember_spike;

typedef struct {
    ember_grid_params p;
    ember_q16 v[...];
    ember_q16 bg[...];
    ember_q16 resp[...];
    ember_q16 theta_adapt[...];
    ember_q16 preset_scale, weather_scale, last_activity, last_peak_resp;
    uint32_t  tick;
    ...;
} ember_grid;

void      ember_grid_defaults(ember_grid_params *);
void      ember_grid_init(ember_grid *, const ember_grid_params *);
void      ember_grid_inject(ember_grid *, uint32_t, ember_q16, uint16_t);
int       ember_grid_tick(ember_grid *, ember_spike *, int);
void      ember_grid_confirm(ember_grid *, uint32_t, int, ember_q16);
void      ember_grid_set_sensitivity(ember_grid *, ember_q16);
void      ember_grid_set_fire_danger(ember_grid *, ember_q16);
ember_q16 ember_grid_theta(const ember_grid *, uint32_t);
ember_q16 ember_grid_response(const ember_grid *, uint32_t);
uint32_t  ember_grid_state_bytes(void);

typedef struct {
    uint32_t t_decisec;
    uint16_t node_id, bearing_ddeg;
    uint8_t  tier, cls, conf, bearing_sigma;
    uint16_t seq, crc;
    ...;
} ember_event;

void     ember_event_pack(const ember_event *, uint8_t *);
int      ember_event_unpack(ember_event *, const uint8_t *);
uint16_t ember_crc16(const uint8_t *, uint32_t);

#define EMBER_GRID_W ...
#define EMBER_GRID_H ...
#define EMBER_CELLS ...
#define EMBER_EVENT_WIRE_BYTES ...
#define EMBER_COINCIDENCE_SLOTS ...
#define EMBER_Q16_ONE ...
""")

ffi.set_source(
    "_ember",
    '#include "ember/ember.h"',
    sources=[str(p) for p in sorted((CORE / "src").glob("*.c"))],
    include_dirs=[str(CORE / "include")],
    define_macros=[("EMBER_GRID_W", str(GRID_W)), ("EMBER_GRID_H", str(GRID_H))],
    extra_compile_args=["-std=c99", "-O2"],
)

if __name__ == "__main__":
    ffi.compile(tmpdir=str(ROOT / "build"), verbose=False)
    print(f"built _ember for {GRID_W}x{GRID_H} grid")

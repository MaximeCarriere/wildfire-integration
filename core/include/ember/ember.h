/* SPDX-License-Identifier: Apache-2.0
 * ember.h -- two-layer spiking evidence fusion for wildfire sensor networks.
 *
 *   Layer 1 (ember_node)  runs on each camera. Integrates that camera's own
 *                         detections over TIME. Emits a graded 2-bit tier.
 *   Layer 2 (ember_grid)  runs on the UNO Q. Integrates node events over
 *                         SPACE via cross-bearing coincidence. Emits alerts.
 *
 * Portable C99. No float, no libm, no malloc -- host and Cortex-M33 builds
 * are bit-identical.
 */
#ifndef EMBER_H
#define EMBER_H

#include <stdint.h>
#include "ember/ember_fixed.h"
#include "ember/ember_config.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Detection classes, matching the on-the-wire signal alphabet. */
typedef enum {
    EMBER_CLASS_NONE  = 0,
    EMBER_CLASS_SMOKE = 1,
    EMBER_CLASS_FIRE  = 2
} ember_class;

/* Layer 1 output tier. Graded, NOT a gate: tier 1 forwards sub-threshold
 * evidence so Layer 2 can still combine it across cameras. */
typedef enum {
    EMBER_TIER_SILENT = 0,   /* below noise floor -- no uplink            */
    EMBER_TIER_WEAK   = 1,   /* sub-threshold evidence -- low spike rate  */
    EMBER_TIER_STRONG = 2    /* local threshold crossed -- high rate      */
} ember_tier;

/* ---------------------------------------------------------------- Layer 1 */

typedef struct {
    ember_q16 w_smoke;          /* current per unit confidence, smoke class  */
    ember_q16 w_fire;           /* ditto, fire class (w_fire > w_smoke)      */
    uint8_t   leak_shift;       /* V -= V >> leak_shift each tick            */
    ember_q16 theta_weak;       /* tier 0 -> 1 boundary                      */
    ember_q16 theta_strong;     /* tier 1 -> 2 boundary (fires and resets)   */
    ember_q16 v_reset;
    uint16_t  refractory_ticks;
} ember_node_params;

typedef struct {
    ember_q16 v;
    ember_q16 inject;       /* current-tick input, applied after leak */
    uint16_t  refractory;
    uint8_t   tier;
} ember_node;

void       ember_node_init(ember_node *n);
void       ember_node_defaults(ember_node_params *p);

/* Feed one detection. conf is Q16.16 in [0,1]. Safe to call repeatedly
 * between ticks; contributions accumulate. */
void       ember_node_observe(ember_node *n, const ember_node_params *p,
                              ember_class cls, ember_q16 conf);

/* Advance one tick. Returns the tier to transmit this tick. */
ember_tier ember_node_tick(ember_node *n, const ember_node_params *p);

/* ---------------------------------------------------------------- Layer 2 */

typedef struct {
    uint8_t   leak_shift;          /* membrane leak                          */
    uint8_t   lateral_shift;       /* neighbour coupling = 1 >> lateral_shift */
    ember_q16 gain_lut[EMBER_COINCIDENCE_SLOTS + 1]; /* by distinct-SOURCE count  */
    ember_q16 theta_base;
    ember_q16 v_reset;
    ember_q16 v_floor;             /* clamp; inhibition cannot run away       */
    ember_q16 v_ceiling;           /* clamp; bounds state so the surround sums
                                    * provably fit in 32 bits, which keeps the
                                    * box blur off 64-bit division -- ~8k
                                    * __aeabi_ldivmod calls per tick otherwise */
    uint8_t   refractory_ticks;
    ember_q16 norm_k;              /* divisive gain-control strength          */
    uint8_t   surround_radius;     /* center-surround background radius, cells */
    uint16_t  coincidence_ticks;   /* rolling window for distinct-source mask */
    ember_q16 adapt_margin;        /* safety factor over the rejected response */
    uint8_t   adapt_decay_shift;   /* how fast that bump forgets              */
    uint8_t   nms_radius;          /* focality: suppress non-maxima within this
                                    * radius. 0 disables. Should match the
                                    * expected spatial extent of one fire --
                                    * a 3x3 test cannot merge the several
                                    * near-equal peaks a smoothed blob has.  */
    uint8_t   confirm_radius;      /* confirmation applies to a place, not a cell */
} ember_grid_params;

typedef struct {
    uint32_t  cell;
    uint16_t  x, y;
    ember_q16 v;               /* membrane potential at firing               */
    uint32_t  contributors;    /* bitmask of distinct sources that drove it  */
    uint8_t   n_contributors;
    uint32_t  tick;
} ember_spike;

typedef struct {
    ember_grid_params p;

    ember_q16 v[EMBER_CELLS];
    ember_q16 inject[EMBER_CELLS];      /* current-tick input, also lateral scratch */
    uint32_t  contrib_cur[EMBER_CELLS]; /* distinct-source mask, current window     */
    uint32_t  contrib_prev[EMBER_CELLS];/* ...previous window (rolling)             */
    ember_q16 bg[EMBER_CELLS];          /* local surround background (box blur)     */
    ember_q16 resp[EMBER_CELLS];        /* center-surround response, cached per tick */
    ember_q16 theta_adapt[EMBER_CELLS]; /* per-cell learned threshold offset        */
    uint8_t   refractory[EMBER_CELLS];

    ember_q16 preset_scale;    /* operator sensitivity preset                */
    ember_q16 weather_scale;   /* fire-danger index modulation               */
    ember_q16 last_activity;   /* mean V last tick (diffuseness readout)     */
    ember_q16 last_peak_resp;  /* strongest contrast response last tick      */
    uint32_t  tick;
    uint16_t  window_age;
} ember_grid;

/* Operator sensitivity presets: scale theta_base. Lower scale == more sensitive. */
#define EMBER_PRESET_NORMAL   EMBER_Q16_ONE
#define EMBER_PRESET_ELEVATED EMBER_Q16_FROM_RATIO(85, 100)
#define EMBER_PRESET_REDFLAG  EMBER_Q16_FROM_RATIO(70, 100)

void ember_grid_defaults(ember_grid_params *p);
void ember_grid_init(ember_grid *g, const ember_grid_params *p);

/* Inject evidence into one cell. source_id is hashed into a coincidence slot.
 * Called once per (event, cell-in-view-wedge) pair by the geometry layer. */
void ember_grid_inject(ember_grid *g, uint32_t cell,
                       ember_q16 current, uint16_t source_id);

/* Advance one tick. Writes up to max_out spikes, returns how many. */
int  ember_grid_tick(ember_grid *g, ember_spike *out, int max_out);

/* Confirmation feedback for an alert that was investigated.
 *
 * verdict > 0 confirms fire: lowers the local bar and releases refractory.
 * verdict < 0 rejects it: inhibits and raises the local threshold ABOVE the
 * response that caused the false alarm, so the same source cannot re-trigger.
 *
 * observed_resp is the spike's .v field. Adapting to the actual stimulus
 * magnitude rather than a fixed step is what makes suppression reliable --
 * a fixed increment is useless against a source that scores well above it. */
void ember_grid_confirm(ember_grid *g, uint32_t cell, int verdict,
                        ember_q16 observed_resp);

void ember_grid_set_sensitivity(ember_grid *g, ember_q16 preset_scale);
void ember_grid_set_fire_danger(ember_grid *g, ember_q16 weather_scale);

/* Effective threshold for a cell, after preset, weather and adaptation. */
ember_q16 ember_grid_theta(const ember_grid *g, uint32_t cell);

/* Center-surround contrast response for a cell -- what is actually compared
 * against threshold. Computed once per tick and cached, so reading it is
 * free. Exposed for the dashboard and for tests. */
ember_q16 ember_grid_response(const ember_grid *g, uint32_t cell);

/* Total bytes of grid state -- quoted in the feasibility section. */
uint32_t ember_grid_state_bytes(void);

/* ------------------------------------------------------------ wire format */

/* Exactly 16 bytes on the wire. This is the whole reason the system works
 * over LoRa or satellite: a camera uplinks an *event*, never a frame. */
#define EMBER_EVENT_WIRE_BYTES 16

typedef struct {
    uint32_t t_decisec;      /* node clock, 0.1 s resolution                */
    uint16_t node_id;
    uint16_t bearing_ddeg;   /* 0..3599, tenths of a degree                 */
    uint8_t  tier;           /* ember_tier                                  */
    uint8_t  cls;            /* ember_class: 1 = smoke, 2 = fire            */
    uint8_t  conf;           /* 0..255 maps to [0,1]                        */
    uint8_t  bearing_sigma;  /* bearing uncertainty, whole degrees          */
    uint16_t seq;            /* per-node sequence, for loss accounting      */
    uint16_t crc;            /* CRC-16/CCITT-FALSE over the first 14 bytes  */
} ember_event;

/* Explicit little-endian pack/unpack -- never memcpy the struct, so the
 * format is identical across compilers, alignment rules and architectures. */
void ember_event_pack(const ember_event *e, uint8_t buf[EMBER_EVENT_WIRE_BYTES]);
int  ember_event_unpack(ember_event *e, const uint8_t buf[EMBER_EVENT_WIRE_BYTES]);
uint16_t ember_crc16(const uint8_t *data, uint32_t len);

/* conf byte (0..255) -> Q16.16 in [0,1] */
static inline ember_q16 ember_conf_to_q16(uint8_t conf)
{
    return (ember_q16)(((int32_t)conf * EMBER_Q16_ONE) / 255);
}

#ifdef __cplusplus
}
#endif
#endif /* EMBER_H */

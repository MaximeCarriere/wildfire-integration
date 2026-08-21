/* SPDX-License-Identifier: Apache-2.0
 * ember_grid.c -- Layer 2: regional spatial integrator.
 *
 * One LIF neuron per geographic cell. Node events are injected along
 * bearing wedges by the geometry layer; this file decides what that
 * accumulated evidence means.
 *
 * Per tick, in order:
 *   1. coincidence gain   -- superlinear in DISTINCT contributing cameras
 *   2. leak + input       -- V(t+1) = leak(V(t)) + gained input
 *   3. lateral excitation -- absorbs bearing error, yields triangulation
 *   4. divisive normalization -- suppresses diffuse, correlated activation
 *   5. threshold + NMS    -- focal firing, one alert per fire
 *
 * Steps 1 and 4 are a matched pair. Coincidence gain is what rejects
 * INDEPENDENT false positives (one camera's dust plume cannot be corroborated
 * from another bearing), but on its own it would AMPLIFY correlated ones -- a
 * marine layer or distant smoke drift lights up many cameras at once. The
 * geometry distinguishes them: a real ignition makes bearings converge on a
 * compact region, while regional haze is extended and near, so its bearings
 * never converge. Normalizing by total grid activity therefore suppresses the
 * diffuse case while a point source survives.
 */
#include <string.h>
#include "ember/ember.h"

#define IDX(x, y) ((uint32_t)((y) * EMBER_GRID_W + (x)))

void ember_grid_defaults(ember_grid_params *p)
{
    int i;

    p->leak_shift        = 5;                       /* tau ~ 32 ticks */
    p->lateral_shift     = 3;                       /* Laplacian coefficient 1/8 */
    p->theta_base        = EMBER_Q16_FROM_INT(3);
    p->v_reset           = 0;
    p->v_floor           = -EMBER_Q16_FROM_INT(2);  /* inhibition cannot run away */
    p->refractory_ticks  = 60;
    p->norm_k            = EMBER_Q16_FROM_RATIO(25, 100);
    p->surround_radius   = 10;
    p->coincidence_ticks = 30;
    p->adapt_margin      = EMBER_Q16_FROM_RATIO(130, 100);
    p->adapt_decay_shift = 12;   /* tau ~ 4096 ticks (~68 min at 1 Hz) */
    p->nms_radius        = 4;
    p->confirm_radius    = 5;

    /* Superlinear coincidence gain. Two cameras agreeing from different
     * bearings is far more than twice the evidence of one camera repeating
     * itself, because the dominant false-positive modes are single-camera. */
    p->gain_lut[0] = 0;
    p->gain_lut[1] = EMBER_Q16_ONE;
    p->gain_lut[2] = EMBER_Q16_FROM_RATIO(250, 100);
    p->gain_lut[3] = EMBER_Q16_FROM_RATIO(400, 100);
    for (i = 4; i <= EMBER_COINCIDENCE_SLOTS; ++i) {
        ember_q16 v = p->gain_lut[i - 1] + EMBER_Q16_FROM_RATIO(150, 100);
        p->gain_lut[i] = (v > EMBER_Q16_FROM_INT(24)) ? EMBER_Q16_FROM_INT(24) : v;
    }
}

void ember_grid_init(ember_grid *g, const ember_grid_params *p)
{
    memset(g, 0, sizeof(*g));
    g->p             = *p;
    g->preset_scale  = EMBER_PRESET_NORMAL;
    g->weather_scale = EMBER_Q16_ONE;
}

void ember_grid_inject(ember_grid *g, uint32_t cell,
                       ember_q16 current, uint16_t camera_id)
{
    if (cell >= (uint32_t)EMBER_CELLS) return;
    g->inject[cell] = ember_q16_add(g->inject[cell], current);
    /* Hash into a coincidence slot. Collisions forgo gain; they never
     * manufacture it, so a collision is conservative. */
    g->contrib_cur[cell] |= (uint32_t)1u << (camera_id % EMBER_COINCIDENCE_SLOTS);
}

ember_q16 ember_grid_theta(const ember_grid *g, uint32_t cell)
{
    ember_q16 t = ember_q16_mul(g->p.theta_base, g->preset_scale);
    t = ember_q16_mul(t, g->weather_scale);
    return ember_q16_add(t, g->theta_adapt[cell]);
}

/* Center-surround contrast with divisive gain control:
 *
 *      response = (V - surround) / (1 + k * surround)
 *
 * The subtraction removes the background (haze, marine layer, distant smoke
 * drift); the division makes the system progressively more conservative as
 * the scene gets hazier, without ever zeroing its sensitivity. Together these
 * are the canonical cortical normalization model. */
static ember_q16 compute_response(const ember_grid *g, uint32_t cell)
{
    ember_q16 bg       = g->bg[cell];
    ember_q16 contrast = ember_q16_add(g->v[cell], -bg);

    if (contrast <= 0) return 0;
    if (bg <= 0)       return contrast;
    return ember_q16_div(contrast,
                         ember_q16_add(EMBER_Q16_ONE,
                                       ember_q16_mul(g->p.norm_k, bg)));
}

ember_q16 ember_grid_response(const ember_grid *g, uint32_t cell)
{
    return (cell < (uint32_t)EMBER_CELLS) ? g->resp[cell] : 0;
}

static int is_local_max(const ember_grid *g, int x, int y, ember_q16 resp)
{
    int32_t r = (int32_t)g->p.nms_radius;
    int32_t dx, dy;

    for (dy = -r; dy <= r; ++dy) {
        for (dx = -r; dx <= r; ++dx) {
            int32_t  nx = x + dx, ny = y + dy;
            uint32_t ni;
            if (dx == 0 && dy == 0) continue;
            if (dx * dx + dy * dy > r * r) continue;
            if (nx < 0 || ny < 0 || nx >= EMBER_GRID_W || ny >= EMBER_GRID_H) continue;
            ni = IDX(nx, ny);
            /* Deterministic tie-break: on a plateau the lowest cell index
             * wins, so a broad blob still yields exactly one alert. */
            if (ni < IDX((uint32_t)x, (uint32_t)y)) { if (resp <= g->resp[ni]) return 0; }
            else                                    { if (resp <  g->resp[ni]) return 0; }
        }
    }
    return 1;
}

int ember_grid_tick(ember_grid *g, ember_spike *out, int max_out)
{
    int64_t   activity_sum = 0;
    ember_q16 mean_activity;
    int       n_out = 0, i_out;
    int       x, y;
    uint32_t  c;

    /* 1 + 2: coincidence gain, then leak and add input. */
    for (c = 0; c < (uint32_t)EMBER_CELLS; ++c) {
        uint32_t  mask = g->contrib_cur[c] | g->contrib_prev[c];
        int32_t   n    = ember_popcount32(mask);
        ember_q16 gained = ember_q16_mul(g->inject[c], g->p.gain_lut[n]);

        g->v[c] = ember_q16_add(ember_q16_leak(g->v[c], g->p.leak_shift), gained);
        if (g->v[c] < g->p.v_floor) g->v[c] = g->p.v_floor;

        /* Snapshot for lateral pass: reuse inject[], which is now consumed. */
        g->inject[c] = g->v[c];
    }

    /* 3: lateral coupling, as a discrete Laplacian over the pre-lateral
     * snapshot. Plain "add a fraction of each neighbour" would inject energy
     * every tick and a uniform field would run away; the Laplacian spreads a
     * peak into its neighbourhood while leaving a flat field untouched. That
     * is what we actually want -- it absorbs bearing error and lets two
     * crossing wedges reinforce, without inventing evidence. */
    for (y = 0; y < EMBER_GRID_H; ++y) {
        for (x = 0; x < EMBER_GRID_W; ++x) {
            uint32_t  i = IDX(x, y);
            ember_q16 s = 0;
            int32_t   n = 0;
            if (x > 0)                { s = ember_q16_add(s, g->inject[i - 1]); n++; }
            if (x < EMBER_GRID_W - 1) { s = ember_q16_add(s, g->inject[i + 1]); n++; }
            if (y > 0)                { s = ember_q16_add(s, g->inject[i - EMBER_GRID_W]); n++; }
            if (y < EMBER_GRID_H - 1) { s = ember_q16_add(s, g->inject[i + EMBER_GRID_W]); n++; }
            s = ember_q16_add(s, -ember_q16_mul(EMBER_Q16_FROM_INT(n), g->inject[i]));
            g->v[i] = ember_q16_add(g->v[i], s >> g->p.lateral_shift);
            if (g->v[i] > 0) activity_sum += g->v[i];
        }
    }

    /* 4: center-surround background, via a separable box blur.
     *
     * The first version of this divided every cell by total grid activity.
     * That killed diffuse haze correctly but ALSO masked a genuine fire
     * burning during haze -- a miss, which in wildfire terms is far worse
     * than a false alarm. Global scaling cannot separate the two because it
     * attenuates signal and background by the same factor.
     *
     * Center-surround can. Haze is a shift in the local background; a fire is
     * local contrast on top of it. Because leak is linear, evidence
     * superposes, so subtracting the surround isolates the fire's own
     * contribution regardless of how hazy the scene is. This is exactly what
     * retinal ganglion cells do to stay contrast-invariant under changing
     * illumination.
     *
     * Two running-sum passes, ~2 adds per cell, no division per cell. */
    {
        int32_t r = (int32_t)g->p.surround_radius;
        int32_t span;

        /* horizontal pass -> inject[] (free again after the lateral pass) */
        for (y = 0; y < EMBER_GRID_H; ++y) {
            int64_t sum = 0;
            for (x = 0; x <= r && x < EMBER_GRID_W; ++x) sum += g->v[IDX(x, y)];
            for (x = 0; x < EMBER_GRID_W; ++x) {
                int32_t lo = x - r, hi = x + r;
                if (hi >= EMBER_GRID_W) hi = EMBER_GRID_W - 1;
                if (lo < 0) lo = 0;
                span = hi - lo + 1;
                g->inject[IDX(x, y)] = (ember_q16)(sum / span);
                if (x + r + 1 < EMBER_GRID_W) sum += g->v[IDX(x + r + 1, y)];
                if (x - r >= 0)               sum -= g->v[IDX(x - r, y)];
            }
        }
        /* vertical pass -> bg[] */
        for (x = 0; x < EMBER_GRID_W; ++x) {
            int64_t sum = 0;
            for (y = 0; y <= r && y < EMBER_GRID_H; ++y) sum += g->inject[IDX(x, y)];
            for (y = 0; y < EMBER_GRID_H; ++y) {
                int32_t lo = y - r, hi = y + r;
                if (hi >= EMBER_GRID_H) hi = EMBER_GRID_H - 1;
                if (lo < 0) lo = 0;
                span = hi - lo + 1;
                g->bg[IDX(x, y)] = (ember_q16)(sum / span);
                if (y + r + 1 < EMBER_GRID_H) sum += g->inject[IDX(x, y + r + 1)];
                if (y - r >= 0)               sum -= g->inject[IDX(x, y - r)];
            }
        }
    }

    for (c = 0; c < (uint32_t)EMBER_CELLS; ++c)
        g->resp[c] = compute_response(g, c);

    mean_activity     = (ember_q16)(activity_sum / EMBER_CELLS);
    g->last_activity  = mean_activity;
    g->last_peak_resp = 0;

    /* 5: threshold, focality (NMS), fire.
     *
     * Detection and reset MUST be separate passes. Resetting a cell's
     * potential the moment it fires would corrupt the local-maximum test for
     * every cell examined after it: a neighbour would compare itself against
     * the just-zeroed cell, conclude it is also a peak, and fire too. One
     * ignition would emit a cluster of alerts instead of one. */
    for (y = 0; y < EMBER_GRID_H; ++y) {
        for (x = 0; x < EMBER_GRID_W; ++x) {
            uint32_t  i = IDX(x, y);
            ember_q16 theta, resp;

            if (g->refractory[i] > 0) { g->refractory[i]--; continue; }

            resp = g->resp[i];
            if (resp > g->last_peak_resp) g->last_peak_resp = resp;

            theta = ember_grid_theta(g, i);
            if (resp < theta) continue;
            if (g->p.nms_radius && !is_local_max(g, x, y, resp)) continue;

            if (n_out < max_out) {
                uint32_t mask = g->contrib_cur[i] | g->contrib_prev[i];
                out[n_out].cell           = i;
                out[n_out].x              = (uint16_t)x;
                out[n_out].y              = (uint16_t)y;
                out[n_out].v              = resp;
                out[n_out].contributors   = mask;
                out[n_out].n_contributors = (uint8_t)ember_popcount32(mask);
                out[n_out].tick           = g->tick;
                n_out++;
            }
        }
    }

    /* Second pass: now that every local-maximum test has been made against
     * unmodified state, apply the resets. */
    for (i_out = 0; i_out < n_out; ++i_out) {
        uint32_t i = out[i_out].cell;
        g->v[i]          = g->p.v_reset;
        g->refractory[i] = g->p.refractory_ticks;
    }

    /* Adaptation forgets slowly. The shift alone would stall at small values,
     * so step at least one unit toward zero. */
    for (c = 0; c < (uint32_t)EMBER_CELLS; ++c) {
        ember_q16 a = g->theta_adapt[c];
        if (a > 0)      g->theta_adapt[c] = a - ((a >> g->p.adapt_decay_shift) | 1);
        else if (a < 0) g->theta_adapt[c] = a + (((-a) >> g->p.adapt_decay_shift) | 1);
    }

    memset(g->inject, 0, sizeof(g->inject));

    /* Roll the coincidence window. Two half-windows OR'd together give a
     * sliding window without storing a timestamp per camera per cell. */
    if (++g->window_age >= g->p.coincidence_ticks) {
        memcpy(g->contrib_prev, g->contrib_cur, sizeof(g->contrib_cur));
        memset(g->contrib_cur, 0, sizeof(g->contrib_cur));
        g->window_age = 0;
    }

    g->tick++;
    return n_out;
}

void ember_grid_confirm(ember_grid *g, uint32_t cell, int verdict,
                        ember_q16 observed_resp)
{
    int32_t   r = (int32_t)g->p.confirm_radius;
    int32_t   cx, cy, dx, dy;
    ember_q16 base, target;

    if (cell >= (uint32_t)EMBER_CELLS || verdict == 0) return;

    cx = (int32_t)(cell % EMBER_GRID_W);
    cy = (int32_t)(cell / EMBER_GRID_W);

    /* Threshold this source must clear in future, with margin. */
    base   = ember_q16_mul(ember_q16_mul(g->p.theta_base, g->preset_scale),
                           g->weather_scale);
    target = ember_q16_add(ember_q16_mul(observed_resp, g->p.adapt_margin), -base);
    if (target < 0) target = 0;

    /* A verdict is about a LOCATION, not a single cell. Applied to one cell it
     * is useless: non-maximum suppression simply promotes a neighbour to local
     * max and the same false source re-alerts from the cell next door. */
    for (dy = -r; dy <= r; ++dy) {
        for (dx = -r; dx <= r; ++dx) {
            int32_t   x = cx + dx, y = cy + dy;
            int32_t   d2;
            uint32_t  i;
            ember_q16 step;

            if (x < 0 || y < 0 || x >= EMBER_GRID_W || y >= EMBER_GRID_H) continue;
            d2 = dx * dx + dy * dy;
            if (d2 > r * r) continue;

            i = IDX(x, y);
            /* Falls off with distance, but gently -- the whole blob must be
             * covered or the alert just migrates to its edge. */
            step = ember_q16_div(target, EMBER_Q16_FROM_INT(1) + (d2 << (EMBER_Q16_SHIFT - 3)));

            if (verdict > 0) {
                g->theta_adapt[i] = ember_q16_add(g->theta_adapt[i], -step);
                g->refractory[i]  = 0;
            } else {
                g->v[i] = g->p.v_floor;
                if (step > g->theta_adapt[i]) g->theta_adapt[i] = step;
                g->refractory[i] = g->p.refractory_ticks;
            }
        }
    }
}

void ember_grid_set_sensitivity(ember_grid *g, ember_q16 preset_scale)
{
    g->preset_scale = preset_scale;
}

void ember_grid_set_fire_danger(ember_grid *g, ember_q16 weather_scale)
{
    g->weather_scale = weather_scale;
}

uint32_t ember_grid_state_bytes(void)
{
    return (uint32_t)sizeof(ember_grid);
}

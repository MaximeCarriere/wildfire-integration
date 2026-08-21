/* SPDX-License-Identifier: Apache-2.0
 * golden_vec.c -- deterministic scenario, hashed.
 *
 * The point of this file: the SAME source runs on the host and on the
 * Cortex-M33, and both must produce the identical hash. Because the core is
 * fixed-point with no float, no libm and no malloc, that is guaranteed rather
 * than hoped for -- which is how the MCU port gets validated months before the
 * hardware arrives.
 */
#include "ember/ember.h"

static ember_grid        gg;
static ember_grid_params gp;

static uint32_t fnv1a(uint32_t h, const void *data, uint32_t len)
{
    const uint8_t *p = (const uint8_t *)data;
    uint32_t i;
    for (i = 0; i < len; ++i) { h ^= p[i]; h *= 16777619u; }
    return h;
}

uint32_t ember_golden_hash(void)
{
    ember_spike sp[EMBER_MAX_SPIKES_PER_TICK];
    uint32_t    h = 2166136261u;
    int         t, i, n, dx, dy, c;
    uint32_t    cell;

    /* --- Layer 1: three cameras, deterministic detection pattern --- */
    {
        ember_node        nd[3];
        ember_node_params np;
        ember_node_defaults(&np);
        for (i = 0; i < 3; ++i) ember_node_init(&nd[i]);
        for (t = 0; t < 500; ++t)
            for (i = 0; i < 3; ++i) {
                if ((t + i * 7) % (5 + i) == 0)
                    ember_node_observe(&nd[i], &np,
                                       ((t + i) % 3 == 0) ? EMBER_CLASS_FIRE : EMBER_CLASS_SMOKE,
                                       ember_conf_to_q16((uint8_t)(120 + ((t * 13 + i * 31) % 130))));
                {
                    uint8_t tier = (uint8_t)ember_node_tick(&nd[i], &np);
                    h = fnv1a(h, &tier, 1);
                    h = fnv1a(h, &nd[i].v, sizeof(nd[i].v));
                }
            }
    }

    /* --- Layer 2: two crossing sources, plus haze, plus a rejection --- */
    ember_grid_defaults(&gp);
    ember_grid_init(&gg, &gp);

    for (t = 0; t < 1200; ++t) {
        if (t % 8 == 0) {
            for (c = 0; c < 2; ++c)
                for (dy = -2; dy <= 2; ++dy)
                    for (dx = -2; dx <= 2; ++dx) {
                        int x = 40 + dx, y = 24 + dy;
                        cell = (uint32_t)(y * EMBER_GRID_W + x);
                        ember_grid_inject(&gg, cell,
                                          EMBER_Q16_ONE / (1 + dx * dx + dy * dy),
                                          (uint16_t)(10 + c));
                    }
            if (t > 400)
                for (dy = 0; dy < 12; ++dy)
                    for (dx = 0; dx < EMBER_GRID_W; ++dx)
                        ember_grid_inject(&gg, (uint32_t)(dy * EMBER_GRID_W + dx),
                                          EMBER_Q16_ONE / 2, (uint16_t)(dx % 3));
        }
        if (t == 600) ember_grid_set_sensitivity(&gg, EMBER_PRESET_REDFLAG);
        if (t == 900) ember_grid_set_fire_danger(&gg, EMBER_Q16_FROM_RATIO(70, 100));

        n = ember_grid_tick(&gg, sp, EMBER_MAX_SPIKES_PER_TICK);
        for (i = 0; i < n; ++i) {
            h = fnv1a(h, &sp[i].cell, sizeof(sp[i].cell));
            h = fnv1a(h, &sp[i].v, sizeof(sp[i].v));
            h = fnv1a(h, &sp[i].contributors, sizeof(sp[i].contributors));
            h = fnv1a(h, &sp[i].tick, sizeof(sp[i].tick));
            if (t % 3 == 0) ember_grid_confirm(&gg, sp[i].cell, -1, sp[i].v);
            else            ember_grid_confirm(&gg, sp[i].cell,  1, sp[i].v);
        }
    }

    /* Fold the whole final membrane state in, so any divergence anywhere
     * in the grid changes the hash. */
    for (cell = 0; cell < (uint32_t)EMBER_CELLS; ++cell) {
        h = fnv1a(h, &gg.v[cell], sizeof(gg.v[cell]));
        h = fnv1a(h, &gg.theta_adapt[cell], sizeof(gg.theta_adapt[cell]));
    }
    return h;
}

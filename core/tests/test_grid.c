/* SPDX-License-Identifier: Apache-2.0 -- Layer 2: regional spatial integrator */
#include <string.h>
#include "ember/ember.h"
#include "ember_test.h"

static ember_grid        g;
static ember_grid_params P;

/* Inject one node event as a small blob -- stands in for the geometry layer's
 * bearing-wedge projection until pyember/geo lands. */
static void blob(int cx, int cy, uint16_t cam)
{
    int dx, dy;
    for (dy = -2; dy <= 2; ++dy)
        for (dx = -2; dx <= 2; ++dx) {
            int x = cx + dx, y = cy + dy;
            if (x < 0 || y < 0 || x >= EMBER_GRID_W || y >= EMBER_GRID_H) continue;
            ember_grid_inject(&g, (uint32_t)(y * EMBER_GRID_W + x),
                              EMBER_Q16_ONE / (1 + dx * dx + dy * dy), cam);
        }
}

/* Extended, low-lying haze: marine layer / regional smoke drift. */
static void haze(double frac, int ncam)
{
    int rows = (int)(EMBER_GRID_H * frac), x, y, c;
    for (y = 0; y < rows; ++y)
        for (x = 0; x < EMBER_GRID_W; ++x)
            for (c = 1; c <= ncam; ++c)
                ember_grid_inject(&g, (uint32_t)(y * EMBER_GRID_W + x),
                                  EMBER_Q16_ONE / 2, (uint16_t)c);
}

/* Run a scenario; return total alerts, and first alert tick via *first. */
static int run(int ncams, double hazefrac, int fire_y, int ticks, int *first)
{
    ember_spike sp[EMBER_MAX_SPIKES_PER_TICK];
    int t, c, n, total = 0;

    ember_grid_defaults(&P);
    ember_grid_init(&g, &P);
    if (first) *first = -1;
    for (t = 0; t < ticks; ++t) {
        if (t % 8 == 0) {
            if (hazefrac > 0) haze(hazefrac, 3);
            for (c = 0; c < ncams; ++c) blob(32, fire_y, (uint16_t)(10 + c));
        }
        n = ember_grid_tick(&g, sp, EMBER_MAX_SPIKES_PER_TICK);
        if (n > 0 && first && *first < 0) *first = t;
        total += n;
    }
    return total;
}

void test_grid(void)
{
    int first;

    SECTION("Layer 2 -- coincidence across distinct cameras");

    /* THE headline behaviour. One camera repeating itself is the dominant
     * false-positive mode (dust, glint, a bug on the lens). It must not alert,
     * however long it persists. Two cameras agreeing from different bearings
     * must alert -- a dust plume cannot be corroborated from another angle. */
    CHECK(run(1, 0, 32, 400, &first) == 0,
          "single camera alerted after repeating itself for 400 ticks");
    OK("1 camera, 400 ticks of persistent detection -> no alert");

    CHECK(run(2, 0, 32, 400, &first) > 0, "two corroborating cameras never alerted");
    OK("2 cameras agreeing -> alert at t=%d", first);

    CHECK(run(3, 0, 32, 400, &first) > 0, "three cameras never alerted");
    OK("3 cameras agreeing -> alert at t=%d", first);

    SECTION("Layer 2 -- correlated false positives (the hard case)");

    /* Coincidence gain alone would AMPLIFY a marine layer seen by many
     * cameras at once. Center-surround is what separates the two. */
    CHECK(run(0, 0.30, 32, 400, &first) == 0,
          "large-area haze across 3 cameras produced a false alarm");
    OK("haze over 30%% of grid, 3 cameras -> no alert (extended, not focal)");

    CHECK(run(0, 0.50, 32, 400, &first) == 0, "50%% haze produced a false alarm");
    OK("haze over 50%% of grid -> no alert");

    /* The failure mode that killed the first design: a real fire burning
     * INSIDE the haze must still be caught. A miss is worse than a false alarm. */
    {
        int alerts = run(2, 0.30, 10, 400, &first);
        CHECK(alerts > 0, "fire burning inside haze was MASKED -- missed detection");
        OK("real fire inside 30%% haze -> still detected at t=%d", first);
    }
    {
        int alerts = run(2, 0.50, 10, 400, &first);
        CHECK(alerts > 0, "fire inside 50%% haze was masked");
        OK("real fire inside 50%% haze -> still detected at t=%d", first);
    }

    SECTION("Layer 2 -- focality (one alert per fire, not per cell)");
    {
        ember_spike sp[EMBER_MAX_SPIKES_PER_TICK];
        int t, n, maxper = 0;
        ember_grid_defaults(&P);
        ember_grid_init(&g, &P);
        for (t = 0; t < 200; ++t) {
            if (t % 8 == 0) { blob(32, 32, 10); blob(32, 32, 11); blob(32, 32, 12); }
            n = ember_grid_tick(&g, sp, EMBER_MAX_SPIKES_PER_TICK);
            if (n > maxper) maxper = n;
        }
        CHECK(maxper <= 1, "one fire produced %d simultaneous alerts (blob, not point)", maxper);
        OK("strong 3-camera fire yields at most %d alert per tick", maxper);
    }

    SECTION("Layer 2 -- sensitivity presets");
    {
        ember_q16 tn, te, tr;
        ember_grid_defaults(&P);
        ember_grid_init(&g, &P);
        ember_grid_set_sensitivity(&g, EMBER_PRESET_NORMAL);   tn = ember_grid_theta(&g, 0);
        ember_grid_set_sensitivity(&g, EMBER_PRESET_ELEVATED); te = ember_grid_theta(&g, 0);
        ember_grid_set_sensitivity(&g, EMBER_PRESET_REDFLAG);  tr = ember_grid_theta(&g, 0);
        CHECK(tn > te && te > tr, "presets not monotonic");
        OK("theta: normal %.2f > elevated %.2f > red flag %.2f", Q(tn), Q(te), Q(tr));

        /* Fire weather must sharpen the whole network without code changes. */
        ember_grid_set_sensitivity(&g, EMBER_PRESET_NORMAL);
        ember_grid_set_fire_danger(&g, EMBER_Q16_FROM_RATIO(60, 100));
        CHECK(ember_grid_theta(&g, 0) < tn, "fire-danger index did not lower threshold");
        OK("high fire-danger index lowers theta to %.2f", Q(ember_grid_theta(&g, 0)));
    }

    SECTION("Layer 2 -- confirmation feedback");
    {
        ember_spike sp[EMBER_MAX_SPIKES_PER_TICK];
        int t, i, n, raw = 0, alerts = 0, fire_first = -1;

        ember_grid_defaults(&P);
        ember_grid_init(&g, &P);

        /* A geothermal steam vent two cameras can both see, running 6 hours,
         * every alert investigated and rejected. */
        for (t = 0; t < 6 * 3600; ++t) {
            if (t % 8 == 0) { blob(20, 20, 1); blob(20, 20, 2); raw++; }
            n = ember_grid_tick(&g, sp, EMBER_MAX_SPIKES_PER_TICK);
            for (i = 0; i < n; ++i) {
                alerts++;
                ember_grid_confirm(&g, sp[i].cell, -1, sp[i].v);
            }
        }
        CHECK(alerts * 20 < raw, "rejected source still alerted %d times (raw %d)", alerts, raw);
        OK("persistent false source: %d alerts over 6h vs %d raw detections (%.0fx fewer)",
           alerts, raw, (double)raw / (alerts ? alerts : 1));

        /* Suppression must be LOCAL. If rejecting the vent desensitised the
         * grid, the system would go blind after a few false alarms. */
        for (t = 0; t < 600; ++t) {
            if (t % 8 == 0) { blob(20, 20, 1); blob(20, 20, 2); blob(45, 45, 7); blob(45, 45, 8); }
            n = ember_grid_tick(&g, sp, EMBER_MAX_SPIKES_PER_TICK);
            for (i = 0; i < n; ++i) {
                if (sp[i].x > 40 && sp[i].y > 40) { if (fire_first < 0) fire_first = t; }
                else ember_grid_confirm(&g, sp[i].cell, -1, sp[i].v);
            }
        }
        CHECK(fire_first >= 0, "real fire missed after 6h of suppressing an unrelated source");
        OK("real ignition 25 cells away still detected at t=%d -- suppression stays local", fire_first);
    }

    SECTION("Layer 2 -- footprint");
    {
        uint32_t b = ember_grid_state_bytes();
        CHECK(b > 0, "no state?");
        OK("%ux%u grid = %u cells, %u bytes (%.1f KB) of state",
           (unsigned)EMBER_GRID_W, (unsigned)EMBER_GRID_H,
           (unsigned)EMBER_CELLS, (unsigned)b, b / 1024.0);
    }
}

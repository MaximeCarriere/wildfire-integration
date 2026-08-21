/* SPDX-License-Identifier: Apache-2.0 -- Layer 1: per-camera temporal neuron */
#include "ember/ember.h"
#include "ember_test.h"

static int ticks_to_tier(ember_class cls, ember_q16 conf, ember_tier want, int max_ticks)
{
    ember_node        n;
    ember_node_params p;
    int t;

    ember_node_defaults(&p);
    ember_node_init(&n);
    for (t = 0; t < max_ticks; ++t) {
        ember_node_observe(&n, &p, cls, conf);
        if (ember_node_tick(&n, &p) >= want) return t;
    }
    return -1;
}

void test_node(void)
{
    ember_node        n;
    ember_node_params p;

    ember_node_defaults(&p);
    SECTION("Layer 1 -- per-camera temporal integrator");

    /* Nothing in, nothing out. */
    ember_node_init(&n);
    {
        int t, spoke = 0;
        for (t = 0; t < 100; ++t)
            if (ember_node_tick(&n, &p) != EMBER_TIER_SILENT) spoke = 1;
        CHECK(!spoke, "silent node transmitted");
        OK("no detections -> never transmits (0 bytes of uplink)");
    }

    /* A single isolated detection must decay away, not alert. This is the
     * flicker/glint case that dominates per-camera false positives. */
    ember_node_init(&n);
    ember_node_observe(&n, &p, EMBER_CLASS_SMOKE, EMBER_Q16_ONE);
    {
        int t, strong = 0;
        for (t = 0; t < 100; ++t)
            if (ember_node_tick(&n, &p) == EMBER_TIER_STRONG) strong = 1;
        CHECK(!strong, "one isolated smoke detection reached STRONG");
        CHECK(n.v < p.theta_weak, "potential failed to decay (V=%.3f)", Q(n.v));
        OK("single isolated detection decays away, never fires");
    }

    /* Persistence is what promotes evidence. */
    {
        int t_smoke = ticks_to_tier(EMBER_CLASS_SMOKE, EMBER_Q16_ONE, EMBER_TIER_STRONG, 200);
        int t_fire  = ticks_to_tier(EMBER_CLASS_FIRE,  EMBER_Q16_ONE, EMBER_TIER_STRONG, 200);
        CHECK(t_smoke > 0, "persistent smoke never fired");
        CHECK(t_fire  > 0, "persistent fire never fired");
        CHECK(t_fire < t_smoke, "fire (%d) should fire sooner than smoke (%d)", t_fire, t_smoke);
        OK("persistent smoke fires at t=%d, fire at t=%d -- fire is stronger evidence",
           t_smoke, t_fire);
    }

    /* Graded output: sub-threshold evidence must still be transmitted, or
     * Layer 2 can never combine two cameras that are each individually weak. */
    {
        int t, saw_weak = 0, saw_strong = 0;
        ember_node_init(&n);
        for (t = 0; t < 60; ++t) {
            ember_tier tr;
            ember_node_observe(&n, &p, EMBER_CLASS_SMOKE, EMBER_Q16_FROM_RATIO(30, 100));
            tr = ember_node_tick(&n, &p);
            if (tr == EMBER_TIER_WEAK)   saw_weak = 1;
            if (tr == EMBER_TIER_STRONG) saw_strong = 1;
        }
        CHECK(saw_weak, "weak evidence produced no WEAK tier -- Layer 2 would be blind to it");
        CHECK(!saw_strong, "weak evidence should not reach STRONG alone");
        OK("weak evidence reports tier 1, never tier 2 -- graded, not a gate");
    }

    /* Refractory suppresses firing but must NOT suppress perception. */
    {
        int t, fires = 0;
        ember_node_init(&n);
        for (t = 0; t < 40; ++t) {
            ember_node_observe(&n, &p, EMBER_CLASS_FIRE, EMBER_Q16_ONE);
            if (ember_node_tick(&n, &p) == EMBER_TIER_STRONG) fires++;
        }
        CHECK(fires > 0, "sustained fire never fired");
        CHECK(fires < 40, "refractory not limiting spike rate (%d/40)", fires);
        OK("refractory caps spike rate at %d/40 ticks -- bounded uplink under sustained fire", fires);
    }
}

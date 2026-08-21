/* SPDX-License-Identifier: Apache-2.0
 * ember_node.c -- Layer 1: per-camera temporal integrator.
 *
 * Runs on the camera node itself. Answers one question: "is this plume
 * persisting, or did it flicker once and vanish?" -- the temporal
 * confirmation step that the literature credits with the largest single
 * reduction in wildfire camera false alarms.
 *
 * Output is deliberately GRADED rather than a gate. A hard local threshold
 * would discard exactly the sub-threshold evidence that Layer 2 exists to
 * combine: two cameras each sitting at 60% of their local threshold are
 * individually silent, yet jointly they are the strongest signal in the
 * network. So tier 1 forwards "something is building" at a low spike rate.
 */
#include "ember/ember.h"

void ember_node_init(ember_node *n)
{
    n->v = 0;
    n->inject = 0;
    n->refractory = 0;
    n->tier = EMBER_TIER_SILENT;
}

void ember_node_defaults(ember_node_params *p)
{
    /* Smoke is early but noisy; fire is late but near-certain. A single fire
     * detection at full confidence should nearly fire the node alone, while
     * smoke requires persistence. */
    p->w_smoke         = EMBER_Q16_FROM_RATIO(35, 100);
    p->w_fire          = EMBER_Q16_FROM_RATIO(90, 100);
    p->leak_shift      = 4;                          /* tau ~ 16 ticks */
    p->theta_weak      = EMBER_Q16_FROM_RATIO(80, 100);
    p->theta_strong    = EMBER_Q16_FROM_INT(3);
    p->v_reset         = 0;
    p->refractory_ticks = 8;
}

void ember_node_observe(ember_node *n, const ember_node_params *p,
                        ember_class cls, ember_q16 conf)
{
    ember_q16 w;

    switch (cls) {
        case EMBER_CLASS_SMOKE: w = p->w_smoke; break;
        case EMBER_CLASS_FIRE:  w = p->w_fire;  break;
        default:                return;
    }
    /* Evidence accumulates even during refractory -- we suppress *firing*,
     * not perception. Losing input here would blind the node to a fire that
     * grows while it is recovering from its own last spike. */
    n->inject = ember_q16_add(n->inject, ember_q16_mul(w, conf));
}

ember_tier ember_node_tick(ember_node *n, const ember_node_params *p)
{
    n->v = ember_q16_add(ember_q16_leak(n->v, p->leak_shift), n->inject);
    n->inject = 0;
    if (n->v < 0) n->v = 0;

    if (n->refractory > 0) {
        n->refractory--;
        /* Still report sub-threshold state so Layer 2 keeps receiving evidence. */
        n->tier = (n->v >= p->theta_weak) ? EMBER_TIER_WEAK : EMBER_TIER_SILENT;
        return (ember_tier)n->tier;
    }

    if (n->v >= p->theta_strong) {
        n->tier       = EMBER_TIER_STRONG;
        n->v          = p->v_reset;
        n->refractory = p->refractory_ticks;
    } else if (n->v >= p->theta_weak) {
        n->tier = EMBER_TIER_WEAK;
    } else {
        n->tier = EMBER_TIER_SILENT;
    }
    return (ember_tier)n->tier;
}

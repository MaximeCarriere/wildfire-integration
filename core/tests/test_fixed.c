/* SPDX-License-Identifier: Apache-2.0 */
#include "ember/ember.h"
#include "ember_test.h"

void test_fixed(void)
{
    SECTION("fixed-point (Q16.16)");

    CHECK(ember_q16_mul(EMBER_Q16_ONE, EMBER_Q16_ONE) == EMBER_Q16_ONE, "1*1 != 1");
    CHECK(ember_q16_mul(EMBER_Q16_FROM_INT(3), EMBER_Q16_FROM_INT(4))
          == EMBER_Q16_FROM_INT(12), "3*4 != 12");
    CHECK(ember_q16_div(EMBER_Q16_FROM_INT(12), EMBER_Q16_FROM_INT(4))
          == EMBER_Q16_FROM_INT(3), "12/4 != 3");
    OK("mul/div exact on integers");

    /* Evidence accumulation must saturate, never wrap: a wrap would turn a
     * huge amount of corroborated evidence into a negative potential. */
    CHECK(ember_q16_add(EMBER_Q16_MAX, EMBER_Q16_ONE) == EMBER_Q16_MAX, "add did not saturate");
    CHECK(ember_q16_add(EMBER_Q16_MIN, -EMBER_Q16_ONE) == EMBER_Q16_MIN, "add did not saturate");
    CHECK(ember_q16_mul(EMBER_Q16_MAX, EMBER_Q16_FROM_INT(4)) == EMBER_Q16_MAX, "mul did not saturate");
    OK("saturating, never wrapping");

    CHECK(ember_q16_div(EMBER_Q16_ONE, 0) == EMBER_Q16_MAX, "div by zero unguarded");
    OK("division by zero guarded");

    /* Leak is a pure shift: identical on every target, no libm, no rounding mode. */
    {
        ember_q16 v = EMBER_Q16_FROM_INT(1000);
        int i;
        for (i = 0; i < 32; ++i) v = ember_q16_leak(v, 5);
        CHECK(v < EMBER_Q16_FROM_INT(1000) && v > 0, "leak should decay toward zero");
        CHECK(ember_q16_leak(0, 5) == 0, "leak of zero must stay zero");
        OK("leak decays monotonically (V=1000 -> %.1f after 32 ticks at tau=32)", Q(v));
    }

    CHECK(ember_popcount32(0u) == 0, "popcount(0)");
    CHECK(ember_popcount32(0xFFFFFFFFu) == 32, "popcount(all)");
    CHECK(ember_popcount32(0x80000001u) == 2, "popcount(2 bits)");
    OK("popcount correct (drives coincidence gain)");

    CHECK(ember_conf_to_q16(255) == EMBER_Q16_ONE, "conf 255 should be 1.0");
    CHECK(ember_conf_to_q16(0) == 0, "conf 0 should be 0.0");
    OK("confidence byte maps to [0,1]");
}

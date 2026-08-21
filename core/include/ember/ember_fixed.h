/* SPDX-License-Identifier: Apache-2.0
 * ember_fixed.h -- Q16.16 fixed-point arithmetic.
 *
 * The whole integrator is fixed-point so that host and Cortex-M33 builds
 * produce bit-identical output. No float, no libm, no malloc anywhere in core/.
 */
#ifndef EMBER_FIXED_H
#define EMBER_FIXED_H

#include <stdint.h>

typedef int32_t ember_q16;               /* Q16.16: 1.0 == 65536 */

#define EMBER_Q16_SHIFT   16
#define EMBER_Q16_ONE     ((ember_q16)(1 << EMBER_Q16_SHIFT))
#define EMBER_Q16_MAX     ((ember_q16)0x7FFFFFFF)
#define EMBER_Q16_MIN     ((ember_q16)0x80000000)

/* Convert a percentage / permille / ratio without touching float. */
#define EMBER_Q16_FROM_INT(i)        ((ember_q16)((i) << EMBER_Q16_SHIFT))
#define EMBER_Q16_FROM_RATIO(n, d)   ((ember_q16)(((int64_t)(n) << EMBER_Q16_SHIFT) / (d)))
#define EMBER_Q16_TO_INT(q)          ((int32_t)((q) >> EMBER_Q16_SHIFT))

/* Saturating add: evidence accumulation must never wrap into a false alarm. */
static inline ember_q16 ember_q16_add(ember_q16 a, ember_q16 b)
{
    int64_t r = (int64_t)a + (int64_t)b;
    if (r > (int64_t)EMBER_Q16_MAX) return EMBER_Q16_MAX;
    if (r < (int64_t)EMBER_Q16_MIN) return EMBER_Q16_MIN;
    return (ember_q16)r;
}

static inline ember_q16 ember_q16_mul(ember_q16 a, ember_q16 b)
{
    int64_t r = ((int64_t)a * (int64_t)b) >> EMBER_Q16_SHIFT;
    if (r > (int64_t)EMBER_Q16_MAX) return EMBER_Q16_MAX;
    if (r < (int64_t)EMBER_Q16_MIN) return EMBER_Q16_MIN;
    return (ember_q16)r;
}

static inline ember_q16 ember_q16_div(ember_q16 a, ember_q16 b)
{
    if (b == 0) return (a >= 0) ? EMBER_Q16_MAX : EMBER_Q16_MIN;
    {
        int64_t r = ((int64_t)a << EMBER_Q16_SHIFT) / (int64_t)b;
        if (r > (int64_t)EMBER_Q16_MAX) return EMBER_Q16_MAX;
        if (r < (int64_t)EMBER_Q16_MIN) return EMBER_Q16_MIN;
        return (ember_q16)r;
    }
}

/* Exponential leak as an arithmetic shift: V -= V >> k.
 * Exact, division-free, and identical on every target. k is the leak "time
 * constant" -- larger k leaks more slowly (tau ~= 2^k ticks). */
static inline ember_q16 ember_q16_leak(ember_q16 v, uint8_t shift)
{
    return v - (v >> shift);
}

static inline int32_t ember_popcount32(uint32_t x)
{
    /* Portable; GCC/Clang fold this to a single instruction where available. */
    x = x - ((x >> 1) & 0x55555555u);
    x = (x & 0x33333333u) + ((x >> 2) & 0x33333333u);
    x = (x + (x >> 4)) & 0x0F0F0F0Fu;
    return (int32_t)((x * 0x01010101u) >> 24);
}

#endif /* EMBER_FIXED_H */

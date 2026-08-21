/* SPDX-License-Identifier: Apache-2.0
 * Prints the golden hash. Built for host AND for cortex-m33; the two outputs
 * must match exactly. See mcu/Makefile target `parity`. */
#include <stdio.h>
#include "ember/ember.h"
uint32_t ember_golden_hash(void);
int main(void)
{
    printf("%08x %ux%u %u\n", ember_golden_hash(),
           (unsigned)EMBER_GRID_W, (unsigned)EMBER_GRID_H,
           (unsigned)ember_grid_state_bytes());
    return 0;
}

/* SPDX-License-Identifier: Apache-2.0 */
#include <stdio.h>
#include "ember/ember.h"
#include "ember_test.h"

int ember_test_fails = 0;
int ember_test_count = 0;

void test_fixed(void);
void test_event(void);
void test_node(void);
void test_grid(void);
uint32_t ember_golden_hash(void);

#ifndef EMBER_GOLDEN_EXPECTED
#define EMBER_GOLDEN_EXPECTED 0u
#endif

int main(void)
{
    printf("ember core tests -- %ux%u grid\n", (unsigned)EMBER_GRID_W, (unsigned)EMBER_GRID_H);

    test_fixed();
    test_event();
    test_node();
    test_grid();

    SECTION("golden vector (host <-> Cortex-M33 bit-parity)");
    {
        uint32_t h = ember_golden_hash();
        if (EMBER_GOLDEN_EXPECTED == 0u) {
            printf("  ..   no expected hash pinned; this run yields %08x\n", h);
        } else {
            CHECK(h == (uint32_t)EMBER_GOLDEN_EXPECTED,
                  "golden hash drifted: got %08x, expected %08x", h,
                  (uint32_t)EMBER_GOLDEN_EXPECTED);
            OK("golden hash %08x matches pinned value", h);
        }
    }

    printf("\n%s -- %d checks, %d failures\n",
           ember_test_fails ? "FAILED" : "PASSED", ember_test_count, ember_test_fails);
    return ember_test_fails ? 1 : 0;
}

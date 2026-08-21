/* SPDX-License-Identifier: Apache-2.0 -- minimal assertion harness */
#ifndef EMBER_TEST_H
#define EMBER_TEST_H
#include <stdio.h>
#include <stdlib.h>

extern int ember_test_fails;
extern int ember_test_count;

#define CHECK(cond, ...)                                                    \
    do {                                                                    \
        ember_test_count++;                                                 \
        if (!(cond)) {                                                      \
            ember_test_fails++;                                             \
            printf("  FAIL %s:%d: ", __FILE__, __LINE__);                   \
            printf(__VA_ARGS__); printf("\n");                              \
        }                                                                   \
    } while (0)

#define SECTION(name) printf("\n-- %s\n", name)
#define OK(...)       do { printf("  ok   "); printf(__VA_ARGS__); printf("\n"); } while (0)
#define Q(v)          ((double)(v) / 65536.0)

#endif

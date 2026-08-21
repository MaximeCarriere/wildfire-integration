/* SPDX-License-Identifier: Apache-2.0
 * ember_config.h -- compile-time sizing.
 *
 * All state is statically sized so core/ needs no allocator. Override any of
 * these with -D at build time; mcu/ uses a smaller grid than the host sim.
 */
#ifndef EMBER_CONFIG_H
#define EMBER_CONFIG_H

#ifndef EMBER_GRID_W
#define EMBER_GRID_W 64                  /* cells across */
#endif
#ifndef EMBER_GRID_H
#define EMBER_GRID_H 64                  /* cells down */
#endif

#define EMBER_CELLS (EMBER_GRID_W * EMBER_GRID_H)

/* Distinct-SOURCE coincidence is tracked as a 32-bit mask per cell, so at most
 * 32 sources can be distinguished *within one cell*. Networks larger than 32
 * hash into these slots; collisions merely forgo some coincidence gain, they
 * never manufacture it.
 *
 * A source is whatever produced the evidence: a camera today, but nothing in
 * this layer assumes that. A gas sensor, a lightning strike, a satellite
 * hotspot or a phone call all inject the same way. */
#define EMBER_COINCIDENCE_SLOTS 32

#ifndef EMBER_MAX_SPIKES_PER_TICK
#define EMBER_MAX_SPIKES_PER_TICK 32
#endif

#endif /* EMBER_CONFIG_H */

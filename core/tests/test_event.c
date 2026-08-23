/* SPDX-License-Identifier: Apache-2.0 */
#include <string.h>
#include "ember/ember.h"
#include "ember_test.h"

void test_event(void)
{
    uint8_t     buf[EMBER_EVENT_WIRE_BYTES];
    ember_event a, b;

    SECTION("wire format (16-byte camera event)");

    CHECK(EMBER_EVENT_WIRE_BYTES == 16, "wire record must be 16 bytes");
    OK("record is 16 bytes -- fits LoRa/satellite budgets that video cannot");

    memset(&a, 0, sizeof(a));
    a.t_decisec = 123456789u; a.node_id = 4242; a.bearing_ddeg = 2731;
    a.tier = EMBER_TIER_STRONG; a.cls = EMBER_CLASS_FIRE;
    a.conf = 200; a.bearing_sigma = 3; a.seq = 65535;

    ember_event_pack(&a, buf);
    CHECK(ember_event_unpack(&b, buf) == 0, "roundtrip should verify");
    CHECK(b.t_decisec == a.t_decisec && b.node_id == a.node_id
          && b.bearing_ddeg == a.bearing_ddeg && b.tier == a.tier
          && b.cls == a.cls && b.conf == a.conf
          && b.bearing_sigma == a.bearing_sigma && b.seq == a.seq,
          "roundtrip lost data");
    OK("pack/unpack roundtrip preserves every field");

    /* Corrupt each byte in turn: a damaged event must be dropped, never guessed.
     * Over a lossy radio this is the difference between a missed alert and a
     * fabricated one. */
    {
        int i, caught = 0;
        for (i = 0; i < 14; ++i) {
            uint8_t tmp[EMBER_EVENT_WIRE_BYTES];
            memcpy(tmp, buf, sizeof(tmp));
            tmp[i] ^= 0x40;
            if (ember_event_unpack(&b, tmp) != 0) caught++;
        }
        CHECK(caught == 14, "CRC missed %d of 14 single-byte corruptions", 14 - caught);
        OK("CRC-16 rejects all 14 single-byte corruptions");
    }

    SECTION("wire format -- 9-byte profile for the longest-range radio");
    {
        uint8_t     cb[EMBER_EVENT_COMPACT_BYTES];
        ember_event x, y;
        int         i, caught = 0;

        CHECK(EMBER_EVENT_COMPACT_BYTES == 9, "compact record must be 9 bytes");
        CHECK(EMBER_EVENT_COMPACT_BYTES <= 11,
              "must fit LoRaWAN US915 DR0, which caps the payload at 11 bytes");
        OK("9 bytes -- inside DR0's 11-byte cap, which the 16-byte record misses");

        memset(&x, 0, sizeof(x));
        x.node_id = 4242; x.bearing_ddeg = 2731; x.tier = EMBER_TIER_STRONG;
        x.cls = EMBER_CLASS_FIRE; x.conf = 200; x.bearing_sigma = 3; x.seq = 251;
        ember_event_pack_compact(&x, cb);
        CHECK(ember_event_unpack_compact(&y, cb) == 0, "compact roundtrip should verify");
        CHECK(y.node_id == x.node_id && y.bearing_ddeg == x.bearing_ddeg
              && y.tier == x.tier && y.cls == x.cls
              && y.bearing_sigma == x.bearing_sigma && y.seq == x.seq,
              "compact roundtrip lost a field");
        /* confidence is deliberately quantised to 6 bits */
        CHECK(y.conf <= x.conf && (x.conf - y.conf) < 4,
              "confidence quantisation too coarse: %u -> %u", x.conf, y.conf);
        OK("roundtrip exact except confidence, quantised to 6 bits (64 levels)");

        for (i = 0; i < 7; ++i) {
            uint8_t tmp[EMBER_EVENT_COMPACT_BYTES];
            memcpy(tmp, cb, sizeof(tmp));
            tmp[i] ^= 0x40;
            if (ember_event_unpack_compact(&y, tmp) != 0) caught++;
        }
        CHECK(caught == 7, "CRC missed %d of 7 corruptions", 7 - caught);
        OK("CRC-16 still rejects every single-byte corruption");
    }

    /* Out-of-range fields must be rejected even when the CRC is valid. */
    a.bearing_ddeg = 4000;
    ember_event_pack(&a, buf);
    CHECK(ember_event_unpack(&b, buf) != 0, "bearing >= 3600 should be rejected");
    a.bearing_ddeg = 100; a.cls = 9;
    ember_event_pack(&a, buf);
    CHECK(ember_event_unpack(&b, buf) != 0, "unknown class should be rejected");
    OK("range checks reject valid-CRC but impossible records");
}

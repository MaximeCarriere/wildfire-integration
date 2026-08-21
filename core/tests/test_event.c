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

    /* Out-of-range fields must be rejected even when the CRC is valid. */
    a.bearing_ddeg = 4000;
    ember_event_pack(&a, buf);
    CHECK(ember_event_unpack(&b, buf) != 0, "bearing >= 3600 should be rejected");
    a.bearing_ddeg = 100; a.cls = 9;
    ember_event_pack(&a, buf);
    CHECK(ember_event_unpack(&b, buf) != 0, "unknown class should be rejected");
    OK("range checks reject valid-CRC but impossible records");
}

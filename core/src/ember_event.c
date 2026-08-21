/* SPDX-License-Identifier: Apache-2.0
 * ember_event.c -- 16-byte camera-node event record.
 *
 * A camera transmits one of these only when its Layer 1 neuron has something
 * to say. Sixteen bytes survives LoRa duty-cycle limits, satellite backhaul
 * and degraded cellular; video does not. When the uplink fails entirely, the
 * integrator keeps reasoning on whatever still arrives.
 */
#include "ember/ember.h"

uint16_t ember_crc16(const uint8_t *data, uint32_t len)
{
    uint16_t crc = 0xFFFF;      /* CRC-16/CCITT-FALSE */
    uint32_t i;
    int      b;

    for (i = 0; i < len; ++i) {
        crc ^= (uint16_t)data[i] << 8;
        for (b = 0; b < 8; ++b)
            crc = (crc & 0x8000) ? (uint16_t)((crc << 1) ^ 0x1021)
                                 : (uint16_t)(crc << 1);
    }
    return crc;
}

void ember_event_pack(const ember_event *e, uint8_t buf[EMBER_EVENT_WIRE_BYTES])
{
    uint16_t crc;

    buf[0]  = (uint8_t)(e->t_decisec        & 0xFF);
    buf[1]  = (uint8_t)((e->t_decisec >> 8)  & 0xFF);
    buf[2]  = (uint8_t)((e->t_decisec >> 16) & 0xFF);
    buf[3]  = (uint8_t)((e->t_decisec >> 24) & 0xFF);
    buf[4]  = (uint8_t)(e->node_id          & 0xFF);
    buf[5]  = (uint8_t)((e->node_id >> 8)    & 0xFF);
    buf[6]  = (uint8_t)(e->bearing_ddeg     & 0xFF);
    buf[7]  = (uint8_t)((e->bearing_ddeg >> 8) & 0xFF);
    buf[8]  = e->tier;
    buf[9]  = e->cls;
    buf[10] = e->conf;
    buf[11] = e->bearing_sigma;
    buf[12] = (uint8_t)(e->seq & 0xFF);
    buf[13] = (uint8_t)((e->seq >> 8) & 0xFF);

    crc     = ember_crc16(buf, 14);
    buf[14] = (uint8_t)(crc & 0xFF);
    buf[15] = (uint8_t)((crc >> 8) & 0xFF);
}

int ember_event_unpack(ember_event *e, const uint8_t buf[EMBER_EVENT_WIRE_BYTES])
{
    uint16_t crc_calc = ember_crc16(buf, 14);
    uint16_t crc_wire = (uint16_t)(buf[14] | ((uint16_t)buf[15] << 8));

    if (crc_calc != crc_wire) return -1;   /* corrupt: drop, never guess */

    e->t_decisec     = (uint32_t)buf[0] | ((uint32_t)buf[1] << 8)
                     | ((uint32_t)buf[2] << 16) | ((uint32_t)buf[3] << 24);
    e->node_id       = (uint16_t)(buf[4] | ((uint16_t)buf[5] << 8));
    e->bearing_ddeg  = (uint16_t)(buf[6] | ((uint16_t)buf[7] << 8));
    e->tier          = buf[8];
    e->cls           = buf[9];
    e->conf          = buf[10];
    e->bearing_sigma = buf[11];
    e->seq           = (uint16_t)(buf[12] | ((uint16_t)buf[13] << 8));
    e->crc           = crc_wire;

    if (e->bearing_ddeg >= 3600) return -1;
    if (e->tier > EMBER_TIER_STRONG) return -1;
    if (e->cls > EMBER_CLASS_FIRE)   return -1;
    return 0;
}

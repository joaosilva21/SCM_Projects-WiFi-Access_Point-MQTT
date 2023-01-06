//Inês Martins Marçal, nº2019215917
//João Carlos Borges Silva, nº2019216753

#ifndef _MQTT_SNIFF_H_
#define _MQTT_SNIFF_H_

#include "sdk_structs.h"
#include "ieee80211_structs.h"
#include "string_utils.h"

#include <Adafruit_MQTT.h>
#include <Adafruit_MQTT_Client.h>

wifi_promiscuous_pkt_type_t packet_type_parser(uint16_t len);
void wifi_sniffer_packet_handler(uint8_t *buff, uint16_t len);
void macaddresses_received(String mar);
void MQTT_connect();

#endif

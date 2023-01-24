//Inês Martins Marçal, nº2019215917
//João Carlos Borges Silva, nº2019216753

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include "sdk_structs.h"
#include "ieee80211_structs.h"
#include "string_utils.h"
#include "mqtt_sniff.h"

#include <Adafruit_MQTT.h>
#include <Adafruit_MQTT_Client.h>

#define SSid "AndroidAP" 
#define PASS "1234567890" 

#define server_ip "YOUR_MQTT_BROKER_IP"
#define port 1883

extern WiFiClient client;
extern Adafruit_MQTT_Client client_mqtt;
extern Adafruit_MQTT_Publish topic_to_send;\

extern int arduino_id;
extern int mac_num;
extern int chn, prm, id;
extern char** macaddresses;
extern String information;

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <Adafruit_MQTT.h>
#include <Adafruit_MQTT_Client.h>

#define SSid "GalaxyA21s24AA"
#define PASS "zuyu4125"
#define server_ip "YOUR_MQTT_IP"
#define port 1883
#define topic_to_s_light_update "mqtt/light/from_sensor/B"
#define topic_to_s_avac_update "mqtt/avac/from_sensor/B"
#define topic_to_s_human_presence_update "mqtt/human_presence/from_sensor/B"
#define topic_to_s_connect "mqtt/connect/from_sensor/B"
#define topic_to_r_update "mqtt/update/B"

char* versione = "1.00";
String parameter = "", value = "";

WiFiClient client;
Adafruit_MQTT_Client client_mqtt = Adafruit_MQTT_Client(&client, server_ip, port);
Adafruit_MQTT_Publish topic_to_send_light_update = Adafruit_MQTT_Publish(&client_mqtt,  topic_to_s_light_update);
Adafruit_MQTT_Publish topic_to_send_avac_update = Adafruit_MQTT_Publish(&client_mqtt,  topic_to_s_avac_update);
Adafruit_MQTT_Publish topic_to_send_human_presence_update = Adafruit_MQTT_Publish(&client_mqtt,  topic_to_s_human_presence_update);
Adafruit_MQTT_Publish topic_to_send_connect = Adafruit_MQTT_Publish(&client_mqtt,  topic_to_s_connect);
Adafruit_MQTT_Subscribe topic_to_receive_update = Adafruit_MQTT_Subscribe(&client_mqtt, topic_to_r_update);

void MQTT_connect(){
  int8_t ret;
  
  //Ligar ao Broker MQTT
  if (client_mqtt.connected()) {
    return;
  }
  
  Serial.print("Connecting to MQTT... ");

  while ((ret = client_mqtt.connect()) != 0) { // connect will return 0 for connected
       Serial.println(client_mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       client_mqtt.disconnect();
       delay(5000);  // wait 5 seconds
  }
  Serial.println("MQTT Connected!");
}

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, 1);

  //Ligar ao wifi
  WiFi.begin(SSid, PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");

  client_mqtt.subscribe(&topic_to_receive_update);
  MQTT_connect();
  topic_to_send_connect.publish("ola");
}

void loop() {
  if(Serial.available() != 0){
    parameter = Serial.readStringUntil('\n');  
    Serial.print(parameter + ": ");
    while(Serial.available() == 0);
    value = Serial.readStringUntil('\n');
    Serial.println(value);
      
    MQTT_connect();
    if(!strcmp(parameter.c_str(), "temp")){
      Serial.println("Sending temperature...");
      topic_to_send_avac_update.publish((parameter + ";" + value).c_str());
    }
    else if(!strcmp(parameter.c_str(), "co2")){
      Serial.println("Sending co2...");
      topic_to_send_avac_update.publish((parameter + ";" + value).c_str());
    }
    else if(!strcmp(parameter.c_str(), "light")){
      Serial.println("Sending light...");
      topic_to_send_light_update.publish((value).c_str());
    }
    else if(!strcmp(parameter.c_str(), "human")){
      Serial.println("Sending human presence...");
      topic_to_send_human_presence_update.publish((value).c_str());
    }

  }
  else{  
    client_mqtt.subscribe(&topic_to_receive_update);
    MQTT_connect();
    if (client_mqtt.readSubscription(5000) == &topic_to_receive_update && strcmp((char*)topic_to_receive_update.lastread, versione) != 0 ) {
      sprintf(versione, "%s", (char*)topic_to_receive_update.lastread);
      Serial.println(versione);
      digitalWrite(LED_BUILTIN, 0);
      delay(2000);
      digitalWrite(LED_BUILTIN, 1);
    }
  }

  client_mqtt.disconnect();
  delay(2500);
}

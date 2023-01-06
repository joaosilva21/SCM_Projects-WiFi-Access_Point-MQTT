#include <ESP8266WiFi.h>
#include <WiFiClient.h>

#ifndef APSSID
#define APSSID "ESPap"
#define APPSK  "thereisnospoon"
#endif

const char *ssid = APSSID;
const char *password = APPSK;
String num;

void setup() {
  delay(1000);
  Serial.begin(9600);
  Serial.println();
  Serial.println("Configuring access point...");
  Serial.print("Introduce the channel: ");
  while(Serial.available() == 0);

  //Read the channel number to use in access point
  num = Serial.readString();
  
  //You can remove the password parameter if you want the AP to be open
  WiFi.softAP(ssid, password, num.toInt());

  Serial.println(WiFi.channel());
  Serial.println("SSID: " + WiFi.softAPSSID());

  uint8_t macAddr[6];
  WiFi.softAPmacAddress(macAddr);
  Serial.printf("MAC address: %02x:%02x:%02x:%02x:%02x:%02x\n", 
                macAddr[0], macAddr[1], macAddr[2], macAddr[3], macAddr[4], macAddr[5]);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  Serial.println("HTTP server started");

  WiFi.setPhyMode(WIFI_PHY_MODE_11G);
}

void loop(){
  Serial.printf("Stations connected = %d\n", WiFi.softAPgetStationNum());
  delay(3000);
}

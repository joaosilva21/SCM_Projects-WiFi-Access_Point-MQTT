//Inês Martins Marçal   Nº: 2019215917
//João Carlos Borges Silva  Nª: 201916753

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#ifndef STASSID
#define STASSID "GalaxyA21s24AA" //nome do hotspot
#define STAPSK  "zuyu4125" //password do hotspot
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "192.168.250.242";
const uint16_t port = 25;

ESP8266WiFiMulti WiFiMulti;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  // We start by connecting to a WiFi network
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(ssid, password);

  Serial.println();
  Serial.println();
  Serial.print("Wait for WiFi... ");

  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(500);
}


void loop() {
  Serial.print("connecting to ");
  Serial.print(host);
  Serial.print(':');
  Serial.println(port);

  // Use WiFiClient class to create TCP connections
  WiFiClient client;

  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    Serial.println("wait 5 sec...");
    delay(5000);
    return;
  }
  
  //the only thing added/changed
  String req = "";
  String string = "";
  int variant_num;
  String variant = "";
  
  do{
    
    //if there exists something to read from serial monitor
    if(Serial.available() !=  0){ 
       string = Serial.readString(); 
       client.print(string); 
    }
    //if there exists something to read from client side then
    else if(client.available() != 0){ 
      req = client.readStringUntil('\n'); 
      //depeding on the "command" received
      //ON - turn on my led
      //OFF - turn off my led
      //WIFI - retrieve info about my wifi connection (SSID, channel, RSSI, 802.11 variant)
      if(req == "ON"){
        Serial.println(req+"|");
        digitalWrite(LED_BUILTIN, 0);
        client.println("Other LED turned on");
      }
      else if(req == "OFF"){
        digitalWrite(LED_BUILTIN, 1);
        client.println("Other LED turned off");
      }
      else if(req == "WIFI"){
         Serial.println(req+"|");
          variant_num = WiFi.getPhyMode();
        
          if(variant_num == WIFI_PHY_MODE_11B){
            variant = "802.11 b";
          }
          else if(variant_num == WIFI_PHY_MODE_11G){
            variant = "802.11 g";
          }
          else if(variant_num == WIFI_PHY_MODE_11N){
            variant = "802.11 n";
          }
          else{
            variant = "802.11 (other version)";
          }
          client.println("Name of the network: " + WiFi.SSID() + "\nChannel used: " + WiFi.channel() + "\nRSSI of the network: " + WiFi.RSSI() + "dbm\n802.11 variant: " + variant);
      }else if(req == "STOP"){
        string ="STOP\n";
      }
      else{
         Serial.println(req+"|");
      }
    } 
      req= "";
  }while(string != "STOP\n");

  Serial.println("closing connection");
  client.stop();

  //Serial.println("wait 5 sec...");
  delay(5000);
}

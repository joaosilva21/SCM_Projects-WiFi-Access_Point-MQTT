//Inês Martins Marçal   Nº: 2019215917
//João Carlos Borges Silva   Nº: 2029216753

#include <ESP8266WiFi.h>

#ifndef STASSID
#define STASSID "GalaxyA21s24AA" //"joaophone"
#define STAPSK  "zuyu4125" //"123456789"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(25);

void setup() {
  Serial.begin(9600);

  // prepare LED
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, 0);

  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print(F("Connecting to "));
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }
  Serial.println();
  Serial.println(F("WiFi connected"));

  // Start the server
  server.begin();
  Serial.println(F("Server started"));

  // Print the IP address
  Serial.println(WiFi.localIP());
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  Serial.println(F("new client"));

  client.setTimeout(5000); // default is 1000

  // Match the request
  /*int val;
  if (req.indexOf(F("/gpio/0")) != -1) {
    val = 0;
  } else if (req.indexOf(F("/gpio/1")) != -1) {
    val = 1;
  } else {
    Serial.println(F("invalid request"));
    val = digitalRead(LED_BUILTIN);
  }

  // Set LED according to the request
  digitalWrite(LED_BUILTIN, val);*/

  // read/ignore the rest of the request
  // do not client.flush(): it is for output only, see below

  //the only thing added/changed
  String req = "";
  String string = "";
  int variant_num;
  String variant = "";

  do{
    
    //if there exists something to read from client side then
    if(client.available() != 0){
      req = client.readStringUntil('\n');
      //depeding on the "command" received
      //ON - turn on my led
      //OFF - turn off my led
      //WIFI - retrieve info about my wifi connection (SSID, channel, RSSI)
      if(req == "ON"){
          digitalWrite(LED_BUILTIN, 0);
          client.println("Other LED turned on");
      }
      else if(req == "OFF"){
          digitalWrite(LED_BUILTIN, 1);
          client.println("Other LED turned off");
      }
      else if(req == "WIFI"){
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
        
          client.println("Name of the network: " + WiFi.SSID() + "\nChannel used: " + WiFi.channel() 
                          + "\nRSSI of the network: " + WiFi.RSSI() + "dbm\n802.11 variant: " + variant);
      }
      else if(req == "STOP"){
          string = "STOP\n";
      }
      else{
          Serial.println(req);
      }
    }
    //if there exists something to read from serial monitor
    else if(Serial.available() != 0){
      string = Serial.readString();
      client.print(string);
    }

    req = "";
  }while (string != "STOP\n");

  Serial.println("Closing connection...");
}

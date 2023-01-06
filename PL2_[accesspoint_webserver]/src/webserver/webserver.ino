#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#ifndef STASSID
#define STASSID "ESPap" //nome do hotspot
#define STAPSK "thereisnospoon" //password do hotspot
#endif

const char *ssid = STASSID; 
const char *password = STAPSK;
int i=0, temp, hum;
String command;

ESP8266WebServer server(80);

//página que irá fornecer informação acerca da temperatura e humidade
void handleRoot(){
  server.send(200, "text/html", "<h1>Temperature: " + String(temp) +
                                "<br>Humidity: " + String(hum) + "</h1>");
}

void setup(){
  Serial.begin(9600);

  //Ligar ao WiFi
  Serial.println();
  Serial.println();
  Serial.print(F("Connecting to "));
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(F("."));
  }

  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  //este link será suportado pela função handleRoot
  server.on("/", handleRoot);
  //inicia o webserver
  server.begin();
  Serial.println("HTTP server started");

  delay(500);
}

void loop(){
  server.handleClient();

  //se o user escrever algo
  if(Serial.available() != 0){
    command = Serial.readString();
    if(command == "TEMP\n"){
      Serial.print("Temperature: ");
      while(Serial.available() == 0);

      //modifica a temperatura
      temp = Serial.readString().toInt();
      Serial.println(temp);
    }
    else if(command == "HUM\n"){
      Serial.print("Humidity: ");
      while(Serial.available() == 0);

      //modifica a temperatura
      hum = Serial.readString().toInt();
      Serial.println(hum);
    }
  }
}

//Inês Martins Marçal, nº2019215917
//João Carlos Borges Silva, nº2019216753

#include "PL3.h"

//Id of sensor to differentiate from others
int arduino_id = 1;

WiFiClient client;
Adafruit_MQTT_Client client_mqtt = Adafruit_MQTT_Client(&client, server_ip, port);
Adafruit_MQTT_Publish topic_to_send = Adafruit_MQTT_Publish(&client_mqtt, ("macadd/found_devices/1") );  //("macadd/found_devices/" + String(arduino_id)).c_str()
Adafruit_MQTT_Subscribe topic_to_receive = Adafruit_MQTT_Subscribe(&client_mqtt, "macadd/to_found_devices");

//count of how many macaddresses is suppose to detect
int mac_num;
//chn -> changing channel
//prm -> when is 1 indicates that the macaddress was found
//id -> id of every new message
int chn = 1, prm = -1, id = 1;
//array of strings (mac addresses)
char** macaddresses;
//string to construct the information to send to webpage
String information = "";

extern "C"
{
  #include "user_interface.h"
}

void setup(){
  // Serial setup
  Serial.begin(9600);
  
  client_mqtt.subscribe(&topic_to_receive);
  MQTT_connect();

  while (true) {    
    //if reads something from this topic
    if (client_mqtt.readSubscription(200) == &topic_to_receive) {
      Serial.print(F("Got: "));
      //parse the input readed
      macaddresses_received((char *)topic_to_receive.lastread);

      break;
    }
  }
  prm = 0;
  Serial.println("SUBSCRIBED TOPIC: macadd/found_devices/" + String(arduino_id) + "\n");
  
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, 1);
  
  delay(1000);
  wifi_set_channel(1);

  // Wifi setup
  wifi_set_opmode(STATION_MODE);
  wifi_promiscuous_enable(0);
  WiFi.disconnect();

  // Set sniffer callback
  wifi_set_promiscuous_rx_cb(wifi_sniffer_packet_handler);
  wifi_promiscuous_enable(1);
}

void loop(){
  chn = chn % 13 + 1;
  wifi_set_channel(chn);

  //if we found the packet with macaddress that we indicate
  if(prm == 1){
    //the promiscuous mode only works if wifi is turn off, but mqtt needs wifi to work
    //so, if is needes to publicate something via mqtt we turn off the promiscuous mode first
    //turn wifi on and connect to mqtt broker, publicatates the information and finally turn off the wifi again
    //and turns on the promiscuous mode again

    //turn off promiscuous mode
    wifi_promiscuous_enable(0);
    digitalWrite(LED_BUILTIN, 0);
    Serial.println("PACKET FOUND: LED ON AND SENDING INFORMATION");

    //turn on wifi and connect to mqtt broker
    MQTT_connect();  
    //publicated the information on topic
    topic_to_send.publish(information.c_str());
    
    delay(2000);  
    digitalWrite(LED_BUILTIN, 1);
      
    prm = 0;
    id++;
    //disconnect from wifi
    WiFi.disconnect();
    //reactivate promiscuous mode
    wifi_promiscuous_enable(1);
  }
  else if(prm == 0){
    Serial.println("SEARCHING");
  }

  
  delay(3000);
}

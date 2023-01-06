//Inês Martins Marçal, nº2019215917
//João Carlos Borges Silva, nº2019216753

#include "PL3.h"

char addr[18];

// According to the SDK documentation, the packet type can be inferred from the
// size of the buffer. We are ignoring this information and parsing the type-subtype
// from the packet header itself. Still, this is here for reference.
wifi_promiscuous_pkt_type_t packet_type_parser(uint16_t len){
    switch(len)
    {
      // If only rx_ctrl is returned, this is an unsupported packet
      case sizeof(wifi_pkt_rx_ctrl_t):
      return WIFI_PKT_MISC;

      // Management packet
      case sizeof(wifi_pkt_mgmt_t):
      return WIFI_PKT_MGMT;

      // Data packet
      default:
      return WIFI_PKT_DATA;
    }
}

// In this example, the packet handler function does all the parsing and output work.
// This is NOT ideal.
void wifi_sniffer_packet_handler(uint8_t *buff, uint16_t len){
  // First layer: type cast the received buffer into our generic SDK structure
  const wifi_promiscuous_pkt_t *ppkt = (wifi_promiscuous_pkt_t *)buff;
  // Second layer: define pointer to where the actual 802.11 packet is within the structure
  const wifi_ieee80211_packet_t *ipkt = (wifi_ieee80211_packet_t *)ppkt->payload;
  // Third layer: define pointers to the 802.11 packet header and payload
  const wifi_ieee80211_mac_hdr_t *hdr = &ipkt->hdr;
  const uint8_t *data = ipkt->payload;

  // Pointer to the frame control section within the packet header
  const wifi_header_frame_control_t *frame_ctrl = (wifi_header_frame_control_t *)&hdr->frame_ctrl;
  char ssid[32] = "NULL";

  // Parse MAC addresses contained in packet header into human-readable strings
  char addr1[] = "00:00:00:00:00:00";
  char addr2[] = "00:00:00:00:00:00";
  char addr3[] = "00:00:00:00:00:00";

  mac2str(hdr->addr1, addr1);
  mac2str(hdr->addr2, addr2);
  mac2str(hdr->addr3, addr3);

  if (frame_ctrl->type == WIFI_PKT_MGMT && frame_ctrl->subtype == BEACON)
  {
    const wifi_mgmt_beacon_t *beacon_frame = (wifi_mgmt_beacon_t*) ipkt->payload;

    if (beacon_frame->tag_length >= 32)
    {
      strncpy(ssid, beacon_frame->ssid, 31);
    }
    else
    {
      strncpy(ssid, beacon_frame->ssid, beacon_frame->tag_length);
    }
  }

  //Serial.printf("%s | %s | %s\n", addr1, addr2, addr3);

  //Mac addresses to find
  //"36:b5:82:47:17:24"; //mac @dei
  //18:01:f1:5c:2d:ca // @home 1
  //78:17:be:b8:17:80 // @home 2
  //34:2c:c4:d4:0c:9c // @home 3

  //if one of the mac addresses is found on packets
  for(int i=0; i < mac_num; i++){
    //se encontrar o macaddress
    if(!strcmp(addr1, macaddresses[i]) || !strcmp(addr2, macaddresses[i]) || !strcmp(addr3, macaddresses[i])){
      prm = 1;
      strcpy(addr, macaddresses[i]);
      break;
    }
   
  }

  information = "<br>SENSOR_ID: " + String(arduino_id) + "<br>ID: " + String(id) + "<br>MAC Address: " + String(addr) + "<br>RSSI: " + String(ppkt->rx_ctrl.rssi) + "dB<br>Channel: " + 
                  String(wifi_get_channel()) + "<br>SSID: " + String(ssid) + "<br>-------------------------------------<br><br><br>";
}

//function to parse the string that contains macaddresses
//example: 3;18:01:f1:5c:2d:ca;78:17:be:b8:17:80;34:2c:c4:d4:0c:9c
void macaddresses_received(String mar){
  //pos -> posição do próximo ";"
  //subsize -> tamanho da substring
  int pos = mar.indexOf(";"), sub_size = mar.length();
  mac_num = mar.substring(0,pos).toInt();
  macaddresses = (char**)malloc(sizeof(char)*(18*mac_num+1));

  Serial.println(mac_num);
  mar = mar.substring(pos + 1,sub_size);
  
  for(int i=0; i<mac_num; i++){
    sub_size = mar.length();
    pos = mar.indexOf(";");
    macaddresses[i] = (char*)malloc(sizeof(char)*18);
    strcpy(macaddresses[i], mar.substring(0,pos).c_str());
    
    mar = mar.substring(pos+1, sub_size);
  }

  for(int i=0; i<mac_num; i++){
    Serial.println(macaddresses[i]);
  }

  Serial.println("MAC ADDRESSES RECEIVED");
}

void MQTT_connect(){
  int8_t ret;

  //connect to wifi
  WiFi.begin(SSid, PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");

  //connect to mqtt broker
  //stop if already connected.
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

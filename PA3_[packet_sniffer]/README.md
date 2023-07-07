# SCM_Project-Packet_Sniffer

- [x] Finished

## Index:
- [Description](#description)
- [To run this project](#to-run-this-project)
- [Notes important to read](#notes-important-to-read)

## Description:
A simple packet sniffer that captures packet in your network from the mac addresses choose. The information is sent through MQTT topics subscribed by the Python code and then are showed in a webpage.

## To run this project:
[WARNING] Arduino IDE must be installed<br>
You have one way to run this project:
- Turn on your MQTT broker (for example, Mosquitto)
- Run the python code and enter the MAC addresses:
  ```shellscript
  [your-disk]:[name-path]> python mqtt_client.py
  ```
  ![image](https://i.imgur.com/abP9ca5.png)
  
- Simply connect one Arduino (or more, you can have more than one packet sniffer acting), upload the respective codes (packet sniffer)
- After that open the website to see when a packet is found

## Notes important to read
- You must have a MQTT Broker, like [Mosquitto](https://mosquitto.org/download/) 
- Don't forget to change the IPs in both codes to your MQTT Broker IP.
- If you gonna use more than one Arduino change the ID in top of the Arduino code.
- To understand more about how this project works see the statement and report files.


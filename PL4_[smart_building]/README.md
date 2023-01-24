# SCM_Project-Smart_Building

- [x] Finished

## Index:
- [Description](#description)
- [To run this project](#to-run-this-project)
- [Notes important to read](#notes-important-to-read)

## Description:
A Smart Builder system with HVAC, Light Sensor and Debug (simulates by Python Applications). Arduinos (sensors) send updates about temperatures, humidity, CO2, human presence and light to MQTT topic that the other applications are subscribed.

## To run this project:
[WARNING] Arduino IDE must be installed<br>
You have one way to run this project:
- Turn on your MQTT broker (for example, Mosquitto)
- Run the python code for each application (on manage_mqtt some information must be inserted):
  ```shellscript
  [your-disk]:[name-path]> python manage_mqtt.py
  ```
  ![image](https://i.imgur.com/2hZiT28.png)
  ```shellscript
  [your-disk]:[name-path]> python avac_mqtt.py
  ```
  ```shellscript
  [your-disk]:[name-path]> python light_mqtt.py
  ```
  ```shellscript
  [your-disk]:[name-path]> python debug_mqtt.py
  ```
  
- Simply connect one Arduino (or more, you can have more than one sensor), upload the respective codes
- After that open the Serial Monitor and introduce the commands to update the values from temperature, humidity, co2, human presence and light

## Notes important to read
- You must have a MQTT Broker, like [Mosquitto](https://mosquitto.org/download/) 
- Don't forget to change the IPs in both codes to your MQTT Broker IP.
- If you gonna use more than one Arduino change the ID in top of the Arduino code.
- To understand more about how this project works see the statement and report files.


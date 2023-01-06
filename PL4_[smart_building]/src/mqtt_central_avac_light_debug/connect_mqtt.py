import threading, sys

from paho.mqtt import client as mqtt_client

class MQTT:
    def __init__(self):
        self.port = 1883
        self.broker = '192.168.115.54' #'192.168.1.156'
        self.topic_to_receive_connect_from_sensor = "mqtt/connect/from_sensor/#"
        self.topic_to_receive_light_from_sensor = "mqtt/light/from_sensor/#"
        self.topic_to_receive_avac_from_sensor = "mqtt/avac/from_sensor/#"
        self.topic_to_receive_human_presence_from_sensor = "mqtt/human_presence/from_sensor/#"
        self.topic_to_receive_condition = "mqtt/avac/condition/#"
        self.topic_to_receive_will = "mqtt/will"
        self.topic_to_send_info = "mqtt/avac/info/"
        self.topic_to_send_update = "mqtt/update/"
        self.topic_to_send_avac_update = "mqtt/avac/update/"
        self.topic_to_send_light_update = "mqtt/light/update/"
        self.client_id = "SCM_PL4_manage"
        self.connect = False
        #[room]:[Temp, CO2, H/S, Light, avac, lights, versione]
        self.arduinos = {}
        self.arduinos_light_thresholds = {}

    def start(self):
        self.t = threading.Thread(target = self.run)
        self.t.start()

    #função que a thread corre
    def run(self):
        self.connect_mqtt()
        print("Connected to MQTT Broker! Manage Application starting..")
        self.connect = True

        self.subscribe()
        self.client.loop_forever()
    
    #função para criar um cliente mqtt e ligar ao broker
    def connect_mqtt(self):
        self.client = mqtt_client.Client(self.client_id)
        
        try:
            self.client.connect(self.broker, self.port)
        except:
            print("Failed to connect")
            sys.exit(0)
    
    def subscribe(self):
        def on_message(client, userdata, msg):
            #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            value = msg.payload.decode().split(";")

            if(msg.topic[:25] == self.topic_to_receive_connect_from_sensor[:25]):
                #print(msg.topic[25:])
                self.arduinos[msg.topic[25:]] = ["Unknown"]*2+["H"]+["Unknown"]+["off"]*2+[1.00]
                self.arduinos_light_thresholds[msg.topic[25:]] = int(self.parameters[6])
                self.client.publish(self.topic_to_send_info + msg.topic[25:], ";".join(self.parameters[:6] + self.parameters[7:]), retain = True)
            elif(msg.topic[:23] == self.topic_to_receive_light_from_sensor[:23]):
                if(int(value[0]) < self.arduinos_light_thresholds[msg.topic[23:]]):
                    print("\nLights on room", msg.topic[23:], "under the threshold\n\nSCM@manage-application:~$", end="")

                self.arduinos[msg.topic[23:]][3] = int(value[0])
            elif(msg.topic[:22] == self.topic_to_receive_avac_from_sensor[:22]):
                if(value[0] == "temp"):
                    self.arduinos[msg.topic[22:]][0] = int(value[1])
                elif(value[0] == "co2"):
                    self.arduinos[msg.topic[22:]][1] = int(value[1])
            elif(msg.topic[:32] == self.topic_to_receive_human_presence_from_sensor[:32]):
                self.arduinos[msg.topic[32:]][2] = value[0]

                if(value[0] == "H"):
                    self.client.publish(self.topic_to_send_avac_update + msg.topic[32:], "10;1")
                else:
                    self.client.publish(self.topic_to_send_avac_update + msg.topic[32:], "10;0")
            elif(msg.topic[:20] == self.topic_to_receive_condition[:20]):
                if(int(value[0]) == 1 and int(value[2]) == 1):
                    self.arduinos[msg.topic[20:]][4] = "working.. cooling and ventilating"
                elif(int(value[1]) == 1 and int(value[2]) == 1):
                    self.arduinos[msg.topic[20:]][4] = "working.. heating and ventilating"
                elif(int(value[0]) == 1):
                    self.arduinos[msg.topic[20:]][4] = "working.. cooling"
                elif(int(value[1]) == 1):
                    self.arduinos[msg.topic[20:]][4] = "working.. heating"
                elif(int(value[2]) == 1):
                    self.arduinos[msg.topic[20:]][4] = "working.. ventilating"
                else:
                    self.arduinos[msg.topic[20:]][4] = "off"
            elif(msg.topic == self.topic_to_receive_will):
                print(value[0] + "\n\nSCM@manage-application:~$", end="")

        self.client.subscribe(self.topic_to_receive_condition) #receive changes of avac, if it is or not heating/cooling/ventilating
        self.client.subscribe(self.topic_to_receive_connect_from_sensor) #receive a new conection of arduino
        self.client.subscribe(self.topic_to_receive_light_from_sensor) #receive a new light value of arduino
        self.client.subscribe(self.topic_to_receive_avac_from_sensor) #receive a new temperature value of arduino
        self.client.subscribe(self.topic_to_receive_human_presence_from_sensor) #receive a new human presence value of arduino
        self.client.subscribe(self.topic_to_receive_will) #receive values from wills
        self.client.on_message = on_message

    def get_connect(self):
        return self.connect

    def set_parameters(self, parameters):
        #[tempMinPresentH, tempMaxPresentH, tempMinSPresentH, tempMaxSPresentH, safeCo2, maxCo2, lightthreshold, avac heating, avac cooling, avac ventilating, human presence]
        self.parameters = parameters.split(";") + ["0"]*3 + ["1"]

    def get_condition(self, room_name):
        if(room_name not in self.arduinos):
            print("Room doesn't exist\n")
            return

        arduino = self.arduinos[room_name]

        print("Condition of room", room_name, ":\n"\
              "  -> Temperature(ºC):", arduino[0], "\n"\
              "  -> CO2(%):", arduino[1], "\n"\
              "  -> Human Presence:", arduino[2], "\n"\
              "  -> Light(%):", arduino[3], "\n"\
              "  -> Avac status:", arduino[4], "\n"\
              "  -> Light status:", arduino[5], "\n"\
              "  -> Versione:", arduino[6], "\n")

    #[room_name] [what limits] [value]
    def publish_config(self, room_name, to_change, value):
        if(room_name not in self.arduinos):
            print("Room doesn't exist\n")
            return
        
        if(int(to_change) < 1 or int(to_change) > 7):
            print("The value should be between 1 and 6\
                  \n1 - minimum temperature with human presence\
                  \n2 - maximum temperature with human presence\
                  \n3 - minimum temperature without human presence\
                  \n4 - maximum temperature without human presence\
                  \n5 - safe co2\
                  \n6 - maximum co2\
                  \n7 - light threshold\n")
            return

        if(int(to_change) == 7):
            self.arduinos_light_thresholds[room_name] = int(value)
        else:
            self.client.publish(self.topic_to_send_avac_update + room_name, to_change+";"+value)
            
    
    def publish_update(self, room_name):
        if(room_name not in self.arduinos):
            print("Room doesn't exist\n")
            return

        self.arduinos[room_name][6]+=0.01
        self.client.publish(self.topic_to_send_update + room_name, str(self.arduinos[room_name][6]), retain = True)

    def publish_light(self, room_name, on_or_off):
        if(room_name not in self.arduinos):
            print("Room doesn't exist\n")
            return

        if(self.arduinos[room_name][5] != on_or_off):
            self.arduinos[room_name][5] = on_or_off
            self.client.publish(self.topic_to_send_light_update + room_name, on_or_off)

    #função para desconectar o cliente mqtt do broker e por sua vez parar a thread
    def shutdown(self):
        self.client.disconnect()
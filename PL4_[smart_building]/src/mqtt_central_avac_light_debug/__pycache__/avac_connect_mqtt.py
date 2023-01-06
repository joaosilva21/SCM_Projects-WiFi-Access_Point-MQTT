import threading, sys

from paho.mqtt import client as mqtt_client

#tópico -> mqtt/avac/from_sensor/# -> receber alterações de temperatura ou Co2 do arduino --> arduino mede e manda para o avac
#       -> mqtt/avac/info/# -> receber os valores dos limites de temperatura e Co2 para cada arduino --> o arduino conecta-se o avac recebe estes valores 

class AVAC_MQTT():
    def __init__(self):
        self.broker = '192.168.115.138' #'192.168.1.156'
        self.port = 1883
        self.topic_to_receive_from_sensor = "mqtt/avac/from_sensor/#" 
        self.topic_to_receive_info = "mqtt/avac/info/#"
        self.topic_to_receive_update = "mqtt/avac/update/#"
        self.topic_to_send_condition = "mqtt/avac/condition/"
        self.topic_to_send_will = "mqtt/will"
        self.arduinos = {}
        self.client_id = "SCM_PL4_avac" 

        self.t = threading.Thread(target = self.run)
        self.t.start()

    def run(self):
        self.connect_mqtt()
        self.subscribe()
        print("connect_mqtt")
        self.client.will_set(topic_to_send_will, "Avac leaving...")
        self.client.loop_forever()

    def connect_mqtt(self):
        self.client = mqtt_client.Client(self.client_id)

        try:
            self.client.connect(broker, port)
            
        except:
            print("Failed to connect")
            exit(1)

    def subscribe(client):
        def on_message(client, userdata, msg):
            #print(msg.payload.decode())
            #dicionario -> [room] : [tempMinPresentH, tempMaxPresentH, tempMinSPresentH, tempMaxSPresentH, safeCo2, maxCo2, avac(heat), avac(cool), avac(co2), H/S]
            if(msg.topic[:15] == self.topic_to_receive_info[:15]):
                arduino = msg.payload.decode().split(";")
                self.arduinos[msg.topic[15:]] = list(map(int,arduino))
                print("Values for room", msg.topic[15:], "received.")
                
            #[temp/co2, valor]
            elif(msg.topic[:22] == self.topic_to_receive_from_sensor[:22]): #meti [:22]
                value = msg.payload.decode().split(";")
                value[1] = int(value[1])

                if(value[0] == "temp"):
                    #com presenca humana
                    if(self.arduinos[msg.topic[22:]][9] == 1):
                        if(value[1] >= self.arduinos[msg.topic[22:]][1]):
                            if(self.arduinos[msg.topic[22:]][6] == 0):
                                if(self.arduinos[msg.topic[22:]][7] == 0 and self.arduinos[msg.topic[22:]][8] == 0):
                                    print("Avac booting on room", msg.topic[22:])
                                self.arduinos[msg.topic[22:]][6] = 1
                                self.arduinos[msg.topic[22:]][7] = 0
                                print("Avac cooling on room", msg.topic[22:])
                        elif(value[1] <= self.arduinos[msg.topic[22:]][0]):
                            if(self.arduinos[msg.topic[22:]][7] == 0):
                                if(self.arduinos[msg.topic[22:]][6] == 0 and self.arduinos[msg.topic[22:]][8] == 0):
                                    print("Avac booting on room", msg.topic[22:])
                                self.arduinos[msg.topic[22:]][7] = 1
                                self.arduinos[msg.topic[22:]][6] = 0
                                print("Avac heating on room", msg.topic[22:])
                        elif((self.arduinos[msg.topic[22:]][6] == 1 and self.arduinos[msg.topic[22:]][7] == 0) or (self.arduinos[msg.topic[22:]][6] == 0 and self.arduinos[msg.topic[22:]][7] == 1)):
                            print("Avac not heating/cooling on room", msg.topic[22:])
                            if(self.arduinos[msg.topic[22:]][8] == 0):   
                                print("Avac shutingdown on room", msg.topic[22:])
                            self.arduinos[msg.topic[22:]][6] = 0
                            self.arduinos[msg.topic[22:]][7] = 0
                    #sem presenca humana
                    else:
                        if(value[1] >= self.arduinos[msg.topic[22:]][3]):
                            if(self.arduinos[msg.topic[22:]][6] == 0):
                                if(self.arduinos[msg.topic[22:]][7] == 0 and self.arduinos[msg.topic[22:]][8] == 0):
                                    print("Avac booting on room", msg.topic[22:])
                                self.arduinos[msg.topic[22:]][6] = 1
                                self.arduinos[msg.topic[22:]][7] = 0
                                print("Avac cooling on room", msg.topic[22:])
                        elif(value[1] <= self.arduinos[msg.topic[22:]][2]):
                            if(self.arduinos[msg.topic[22:]][7] == 0):
                                if(self.arduinos[msg.topic[22:]][6] == 0 and self.arduinos[msg.topic[22:]][8] == 0):
                                    print("Avac booting on room", msg.topic[22:])
                                self.arduinos[msg.topic[22:]][7] = 1
                                self.arduinos[msg.topic[22:]][6] = 0
                                print("Avac heating on room", msg.topic[22:])
                        elif((self.arduinos[msg.topic[22:]][6] == 1 and self.arduinos[msg.topic[22:]][7] == 0) or (self.arduinos[msg.topic[22:]][6] == 0 and self.arduinos[msg.topic[22:]][7] == 1)):
                            print("Avac not heating/cooling on room", msg.topic[22:])
                            if(self.arduinos[msg.topic[22:]][8] == 0): 
                                print("Avac shutingdown on room", msg.topic[22:])
                            self.arduinos[msg.topic[22:]][6] = 0
                            self.arduinos[msg.topic[22:]][7] = 0
                    client.publish(self.topic_to_send_condition + msg.topic[22:], str(self.arduinos[msg.topic[22:]][6]) + ";" + str(self.arduinos[msg.topic[22:]][7]) + ";" + str(self.arduinos[msg.topic[22:]][8]))
                else:
                    if(value[1] >= self.arduinos[msg.topic[22:]][5] or value[1] <= self.arduinos[msg.topic[22:]][4]):
                        if(self.arduinos[msg.topic[22:]][8] == 0):
                            if(self.arduinos[msg.topic[22:]][6] == 0 and self.arduinos[msg.topic[22:]][7] == 0):
                                print("Avac booting on room", msg.topic[22:])
                            self.arduinos[msg.topic[22:]][8] = 1                    
                            print("Avac ventilating on room", msg.topic[22:])
                    elif(self.arduinos[msg.topic[22:]][8] == 1):
                        print("Avac not ventilating on room", msg.topic[22:])
                        if(self.arduinos[msg.topic[22:]][6] == 0 and arduinos[msg.topic[22:]][7] == 0):
                            print("Avac shutingdown on room", msg.topic[22:])
                        self.arduinos[msg.topic[22:]][8] = 0
                    client.publish(self.topic_to_send_condition + msg.topic[22:], str(self.arduinos[msg.topic[22:]][6]) + ";" + str(self.arduinos[msg.topic[22:]][7]) + ";" + str(self.arduinos[msg.topic[22:]][8]))

            #[nome room, posição a alterar indice (1 a 6), valor]
            elif(msg.topic[:17] == self.topic_to_receive_update[:17]): #meti [:17]
                update = msg.payload.decode().split(";")
                self.arduinos[msg.topic[17:]][int(update[0])-1] = int(update[1])
                print("Update in limits done on room", msg.topic[17:])
            
        client.subscribe(topic_to_receive_from_sensor)
        client.subscribe(topic_to_receive_info)
        client.subscribe(topic_to_receive_update)
        client.on_message = on_message

    def shutdown(self):
        self.client.disconnect()


from paho.mqtt import client as mqtt_client
import time

broker = 'YOUR_MQTT_IP'
port = 1883
topic_to_receive_from_sensor = "mqtt/avac/from_sensor/#" 
topic_to_receive_info = "mqtt/avac/info/#"
topic_to_receive_update = "mqtt/avac/update/#"
topic_to_send_condition = "mqtt/avac/condition/"
topic_to_send_will = "mqtt/will"
arduinos = {}
client_id = "SCM_PL4_avac" 

def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(client_id)
    client.will_set(topic_to_send_will, " Avac leaving...")

    try:    
        client.connect(broker, port)
        return client
        
    except:
        print("Failed to connect")
        exit(1)

def subscribe(client):
    def on_message(client, userdata, msg):
        #print(msg.payload.decode())
        #dicionario -> [room] : [tempMinPresentH, tempMaxPresentH, tempMinSPresentH, tempMaxSPresentH, safeCo2, maxCo2, avac(heat), avac(cool), avac(co2), H/S]
        if(msg.topic[:15] == topic_to_receive_info[:15]):
            arduino = msg.payload.decode().split(";")
            arduinos[msg.topic[15:]] = list(map(int,arduino))
            print("Values for room", msg.topic[15:], "received.")
            
        #[temp/co2, valor]
        elif(msg.topic[:22] == topic_to_receive_from_sensor[:22]): #meti [:22]
            value = msg.payload.decode().split(";")
            value[1] = int(value[1])

            if(value[0] == "temp"):
                #com presenca humana
                if(arduinos[msg.topic[22:]][9] == 1):
                    if(value[1] >= arduinos[msg.topic[22:]][1]):
                        if(arduinos[msg.topic[22:]][6] == 0):
                            if(arduinos[msg.topic[22:]][7] == 0 and arduinos[msg.topic[22:]][8] == 0):
                                print("Avac booting on room", msg.topic[22:])
                            arduinos[msg.topic[22:]][6] = 1
                            arduinos[msg.topic[22:]][7] = 0
                            print("Avac cooling on room", msg.topic[22:])
                    elif(value[1] <= arduinos[msg.topic[22:]][0]):
                        if(arduinos[msg.topic[22:]][7] == 0):
                            if(arduinos[msg.topic[22:]][6] == 0 and arduinos[msg.topic[22:]][8] == 0):
                                print("Avac booting on room", msg.topic[22:])
                            arduinos[msg.topic[22:]][7] = 1
                            arduinos[msg.topic[22:]][6] = 0
                            print("Avac heating on room", msg.topic[22:])
                    elif((arduinos[msg.topic[22:]][6] == 1 and arduinos[msg.topic[22:]][7] == 0) or (arduinos[msg.topic[22:]][6] == 0 and arduinos[msg.topic[22:]][7] == 1)):
                        print("Avac not heating/cooling on room", msg.topic[22:])
                        if(arduinos[msg.topic[22:]][8] == 0):   
                            print("Avac shuttingdown on room", msg.topic[22:])
                        arduinos[msg.topic[22:]][6] = 0
                        arduinos[msg.topic[22:]][7] = 0
                #sem presenca humana
                else:
                    if(value[1] >= arduinos[msg.topic[22:]][3]):
                        if(arduinos[msg.topic[22:]][6] == 0):
                            if(arduinos[msg.topic[22:]][7] == 0 and arduinos[msg.topic[22:]][8] == 0):
                                print("Avac booting on room", msg.topic[22:])
                            arduinos[msg.topic[22:]][6] = 1
                            arduinos[msg.topic[22:]][7] = 0
                            print("Avac cooling on room", msg.topic[22:])
                    elif(value[1] <= arduinos[msg.topic[22:]][2]):
                        if(arduinos[msg.topic[22:]][7] == 0):
                            if(arduinos[msg.topic[22:]][6] == 0 and arduinos[msg.topic[22:]][8] == 0):
                                print("Avac booting on room", msg.topic[22:])
                            arduinos[msg.topic[22:]][7] = 1
                            arduinos[msg.topic[22:]][6] = 0
                            print("Avac heating on room", msg.topic[22:])
                    elif((arduinos[msg.topic[22:]][6] == 1 and arduinos[msg.topic[22:]][7] == 0) or (arduinos[msg.topic[22:]][6] == 0 and arduinos[msg.topic[22:]][7] == 1)):
                        print("Avac not heating/cooling on room", msg.topic[22:])
                        if(arduinos[msg.topic[22:]][8] == 0): 
                            print("Avac shuttingdown on room", msg.topic[22:])
                        arduinos[msg.topic[22:]][6] = 0
                        arduinos[msg.topic[22:]][7] = 0
                client.publish(topic_to_send_condition + msg.topic[22:], str(arduinos[msg.topic[22:]][6]) + ";" + str(arduinos[msg.topic[22:]][7]) + ";" + str(arduinos[msg.topic[22:]][8]))
            else:
                if(value[1] >= arduinos[msg.topic[22:]][5] or value[1] <= arduinos[msg.topic[22:]][4]):
                    if(arduinos[msg.topic[22:]][8] == 0):
                        if(arduinos[msg.topic[22:]][6] == 0 and arduinos[msg.topic[22:]][7] == 0):
                            print("Avac booting on room", msg.topic[22:])
                        arduinos[msg.topic[22:]][8] = 1                    
                        print("Avac ventilating on room", msg.topic[22:])
                elif(arduinos[msg.topic[22:]][8] == 1):
                    print("Avac not ventilating on room", msg.topic[22:])
                    if(arduinos[msg.topic[22:]][6] == 0 and arduinos[msg.topic[22:]][7] == 0):
                        print("Avac shuttingdown on room", msg.topic[22:])
                    arduinos[msg.topic[22:]][8] = 0
                client.publish(topic_to_send_condition + msg.topic[22:], str(arduinos[msg.topic[22:]][6]) + ";" + str(arduinos[msg.topic[22:]][7]) + ";" + str(arduinos[msg.topic[22:]][8]))

        #[nome room, posição a alterar indice (1 a 6), valor]
        elif(msg.topic[:17] == topic_to_receive_update[:17]): #meti [:17]
            update = msg.payload.decode().split(";")
            arduinos[msg.topic[17:]][int(update[0])-1] = int(update[1])
            print("Update in limits done on room", msg.topic[17:])
        
    client.subscribe(topic_to_receive_from_sensor)
    client.subscribe(topic_to_receive_info)
    client.subscribe(topic_to_receive_update)
    client.on_message = on_message

def main():
    global client
    client = connect_mqtt()
    subscribe(client)
    print("connect_mqtt")
    client.loop_forever()

if __name__ == '__main__':    
    try:
        main()
    except KeyboardInterrupt:
        print("Avac shutting down")
        client.loop_stop()

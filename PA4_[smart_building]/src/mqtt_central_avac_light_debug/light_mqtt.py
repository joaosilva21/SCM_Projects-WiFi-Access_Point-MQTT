
from paho.mqtt import client as mqtt_client

broker = 'YOUR_MQTT_IP'
port = 1883
topic_to_receive_update = "mqtt/light/update/#"
topic_to_send_will = "mqtt/will"
client_id = "SCM_PL4_ligths" 

def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(client_id)
    client.will_set(topic_to_send_will, " Lights leaving...")

    try:
        client.connect(broker, port)
        return client
        
    except:
        print("Failed to connect")
        exit(1)

def subscribe(client):
    def on_message(client, userdata, msg):
        print("Lights of room", msg.topic[18:], "turned", msg.payload.decode())
        
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
        print("Lights shutting down")
        client.loop_stop()

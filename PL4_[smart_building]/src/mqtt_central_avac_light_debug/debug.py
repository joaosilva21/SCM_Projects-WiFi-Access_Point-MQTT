
from paho.mqtt import client as mqtt_client

broker = '192.168.115.54' #'192.168.1.156'
port = 1883
topic_to_receive = "mqtt/#"
client_id = "SCM_PL4_debug" 


def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(client_id)

    try:
        client.connect(broker, port)
        return client
        
    except:
        print("Failed to connect")
        exit(1)

def subscribe(client):
    def on_message(client, userdata, msg):
        print("Topic: " + msg.topic +"\n"\
            + "Content: " + msg.payload.decode() + "\n")

    client.subscribe(topic_to_receive)
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
        print("Debug shutting down")
        client.disconnect()
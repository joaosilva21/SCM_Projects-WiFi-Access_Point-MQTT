import random, threading, regex, sys

from paho.mqtt import client as mqtt_client

class MQTT:
    #construtor da classe, neste caso nao recebe valores
    #define-se alguns parametros da classe que podem ser usados "globalmente" ao longo da classe
    #é aqui que também temos o ponto de partida da classe
    def __init__(self):
        #ip do broker a conectar
        self.broker = '192.168.1.156'
        #porta do broker a conectar
        self.port = 1883
        #topico ao qual o cliente mqtt vai subscrever para receber informaçao do arduino
        self.topic_to_receive = "macadd/found_devices/#"
        #topico onde o mqtt cliente vai escrever para o arduino saber os dispotivos a detetar
        self.topic_to_send = "macadd/to_found_devices"
        self.client_id = "SCM_PL3"
        #ultima mensagem lida do topico
        self.message = None
        self.error = 1
        
        #a própria classe vai correr como uma thread
        #vai executar a função def run(self):
        self.t = threading.Thread(target = self.run)
        #iniciar a thread
        self.t.start()

    #função que a thread corre
    def run(self):
        #crio um cliente e ligo ao broker
        self.connect_mqtt()
        #aqui envio os macaddresses para o arduino
        self.send_devices()

        if(self.error == 0):
            print("Connected to MQTT Broker!")
            
            #aqui subscrevo o topico e vou lendo as mensagens do mesmo
            self.subscribe()
            #obriga o cliente a ficar ligado para ir lendo as mensagens
            self.client.loop_forever()
    
    #função para criar um cliente mqtt e ligar ao broker
    def connect_mqtt(self) -> mqtt_client:
        #crio um cliente com determinado id
        #este self.client é "global" na classe, ou seja, pode ser usado em qualquer lado na classe
        self.client = mqtt_client.Client(self.client_id)
        
        #tenta conectar ao broker
        try:
            #liga ao broker com ip e porta definidos no construtor
            self.client.connect(self.broker, self.port)
        #se falhar, semplesmente faz este print
        except:
            print("Failed to connect")
            sys.exit(0)
    
    #função para subscrever ao tópico e ir vendo as mensagens que lá estão
    def subscribe(self):
        #função para guardar a mensagem nova do tópico na variável self.message
        #é chamada se o client mqtt detetar que há algo novo no tópico para ler
        def on_message(client, userdata, msg):
            #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.message = msg.payload.decode()

        #subscrever no tópico
        self.client.subscribe(self.topic_to_receive)
        #quando existir uma nova mensagem, ele chama a função on_message
        self.client.on_message = on_message

    #função para dar input dos macaddresses e dar publish neles num tópico
    #o arduino virá a este tópico ler quais macaddresses tem de ler
    def send_devices(self):
        #string a enviar que tem os macaddresses todos juntos separados por ;
        list_macs = ""
        i = 1
        string = ""

        try:
            #enquanto o input nao for "STOP"
            while(string != "STOP"):
                #pede input ao utilizador
                string = input("Enter the mac address of device " + str(i) + ": ")

                #se o input nao for STOP
                if(string != "STOP"):
                    #se o input inserido nao for um macaddress que siga expressao regular
                    if(regex.match(r'[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}', string) == None):
                        print("Invalid MAC Address")
                    #se o input for um macaddress valido
                    else:
                        #junta o macaddress à string com ;
                        list_macs += ";" + string
                        i+=1
                print()

            #dá publish dos macaddresses no topico que o arduino vai estar à espera para ler
            #exemplo: 3;18:01:f1:5c:2d:ca;78:17:be:b8:17:80;34:2c:c4:d4:0c:9c
            #NOTA: o primeiro número 3 é o número de macaddresses a ler que adicionado na linha em baixo
            #      antes de enviar (na parte str(i-1 + list_macs))
            self.client.publish(self.topic_to_send, str(i-1)+ list_macs)
            self.error = 0

        except: 
            print("\nInput interrupted")

    #função chamada no main para obter a mensagem mais recente lida pelo cliente mqtt
    def get_message(self):
        return self.message

    #função para desconectar o cliente mqtt do broker e por sua vez parar a thread
    def shutdown(self):
        self.client.disconnect()
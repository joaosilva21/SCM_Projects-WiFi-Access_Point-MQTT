# python3.6
from mqtt_connect import MQTT
from webapp import Packets

import signal, time, sys

#crio objetos do tipo Packets e MQTT
#estes objetos vao ser basicamente threads
# p -> website -> escrever a informação que cliente mqtt escreve num site
# m -> client mqtt -> receber informação do arduino dos dispositivos encontrados
p = Packets()
m = MQTT()

#função usada quando carrego no Ctrl+C
def signal_handler(sig, frame):
    print("Closing app...")
    m.shutdown() # -> para parar a thread -> ver a função na classe MQTT
    p.shutdown() # -> para parar a thread -> ver a função na classe Packets
    sys.exit(0) # fechar o programa
    

def main():
    message = None
    getMessage = None
    p.update_message(None)

    while(True):
        #vai vendo a última mensagem lida no client mqtt (do topico que ele está subscrito)
        getMessage = m.get_message()

        #se a mensagem que foi lida é diferente da anterior quer dizer que há um novo pacote detetado
        if(message != getMessage):
            #muda a mensagem
            message = getMessage
            #atualiza as mensagens no website
            p.update_message(message)

        #dorme durante 1 segundo
        time.sleep(1)

if __name__ == '__main__':    
    #para dar handle do Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    main()

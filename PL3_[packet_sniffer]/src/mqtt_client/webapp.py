from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class Packets():
    def __init__(self):
        self.ip = 'YOUR_WIFI_IP'
        self.port = 8000

        #a própria classe vai correr como uma thread
        #vai executar a função def run(self):
        self.t = threading.Thread(target = self.run)
        #iniciar a thread
        self.t.start()

    def run(self):
        #cria-se um webserver
        #no ip -> YOUR_WIFI_IP
        #na porta -> 8000
        #suportado pelo site
        self.server = HTTPServer((self.ip, self.port), site)
        self.server.serve_forever()

    def update_message(self, msg):
        #mensagem que vai tanto atualizar nesta classe como na classe do website
        #é definida globalmente para poder ser usada noutra classe
        global message

        #quando msg nao for None (ou seja null), atualiza mensagem que
        #fica display no site com as novas informações
        if(msg == None):
            message = ""
        else:
            message += msg

    #função para desligar o webserver por sua vez parar a thread
    def shutdown(self):
        self.server.shutdown()

#base do website
class site(BaseHTTPRequestHandler):
    def do_GET(self):
        #request com o código 200 - OK
        self.send_response(200)
        #tipo de conteudo é html
        self.send_header('content-type', 'text/html')
        self.end_headers()
        #messagem escrita no website
        #é codificada para ser possível passar para o html
        self.wfile.write(message.encode())

    def log_message(self, format, *args):
        return

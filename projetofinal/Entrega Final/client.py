import socket, threading
from env import PORT, SERVER

PROMPT = 'Escolha uma das opções do menu: info - ping - active - dns - download ou !q para sair \n'
tempo_resposta = True

def servInteraction():
    msg = ' '
    while msg != '':
        try:
            msg = sock.recv(512)
            print (f'=>>{msg.decode("utf-8")}')
        except:
            msg = ''
    closeSocket()

def userInteraction():
    msg = ''
    while msg != '!q':
        
        try:
            msg = input()
            if msg != '': 
                sock.send(msg.encode('utf-8'))
        except:
            msg = '!q'
    closeSocket()

def closeSocket():
    try:
        sock.close()
    except:
        None

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER, PORT))

    print ("Conectado a: ", (SERVER, PORT))
    tServer = threading.Thread(target=servInteraction)
    tUser = threading.Thread(target=userInteraction)

    tServer.start()
    tUser.start()

    tServer.join()
    tUser.join()
except Exception as e:
    print ("Falha ", e)

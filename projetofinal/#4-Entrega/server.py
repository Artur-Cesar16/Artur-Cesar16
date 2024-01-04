import socket, threading
from env import PORT, SERVER
from telegram import telegramInteraction

def cliInteraction(sockConn, addr):
    msg = ''
    while msg != '!q':
        try:
            msg = sockConn.recv(512)
            responseOption(msg, addr)
            broadCast (msg, addr)
        except:
            msg = '!q'
    allSocks.remove ((sockConn, addr))
    sockConn.close()


def broadCast(msg, addrSource):
    msg = f"{addrSource} -> {msg.decode('utf-8')}"

    for sockConn, addr in allSocks:
        if addr != addrSource:
            sockConn.send(msg.encode('utf-8'))

def responseOption(message, addrSource):
    if message == b'info':
        send_message_to_requester('Informações básicas sobre a rede (ip, máscara, gateway).', addrSource)
    elif message == b'ping':
        send_message_to_requester('Tempo médio de ping (quatro pacotes) entre a máquina do bot e seu gateway.', addrSource)
    elif message == b'active':
        send_message_to_requester('Informa se o ip está respondendo.', addrSource)
    elif message == b'dns':
        send_message_to_requester('Informa o servidor de DNS da máquina do bot.', addrSource)
    elif message == b'download':
        send_message_to_requester('Download de uma imagem da internet no servidor.', addrSource)
    else:
        send_message_to_requester(f'Olá, {addrSource}. Escolha uma das opções do menu: info - ping - active - dns - download ou !q para sair', addrSource)
    
def send_message_to_requester(message, addrSource):
    for sockConn, addr in allSocks:
        if addr == addrSource:
            sockConn.send(message.encode('utf-8'))

try:
    allSocks = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER, PORT))

    print ("Listening in: ", (SERVER, PORT))
    sock.listen(5)

    telegramThread = threading.Thread(target=telegramInteraction)
    telegramThread.start()
    
    while True:
        sockConn, addr = sock.accept()
        print ("Connection from: ", addr)
        allSocks.append((sockConn, addr))
        tClient = threading.Thread(target=cliInteraction, args=(sockConn, addr))
        tClient.start()
except Exception as e:
    print ("Fail: ", e)

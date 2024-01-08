import socket, threading
from env import PORT, SERVER
from telegram import telegramInteraction
import info

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
    message = message.decode("utf-8")
    if message == 'info':
        send_message_to_requester(info.info_redes(), addrSource)
        send_message_to_requester(f'Olá, {addrSource}. Escolha uma das opções do menu: info - ping - active - dns - download ou !q para sair', addrSource)
    elif message == 'ping':
        send_message_to_requester(info.tempo_medio_de_ping(), addrSource)
        send_message_to_requester(f'Olá, {addrSource}. Escolha uma das opções do menu: info - ping - active - dns - download ou !q para sair', addrSource)
    elif message == 'active':
        send_message_to_requester(info.resposta_ip(), addrSource)
        send_message_to_requester(f'Olá, {addrSource}. Escolha uma das opções do menu: info - ping - active - dns - download ou !q para sair', addrSource)
    elif message == 'dns':
        send_message_to_requester(info.dns(), addrSource)
        send_message_to_requester(f'Olá, {addrSource}. Escolha uma das opções do menu: info - ping - active - dns - download ou !q para sair', addrSource)
    elif message == 'download':
        send_message_to_requester('Envie o link da imagem começando com >http< ou >https<', addrSource)
        send_message_to_requester(f'Olá, {addrSource}. Escolha uma das opções do menu: info - ping - active - dns - download ou !q para sair', addrSource)
    elif 'http' in message or 'https' in message:
        send_message_to_requester(info.download_imagem(message), addrSource)
        send_message_to_requester(f'Olá, {addrSource}. Escolha uma das opções do menu: info - ping - active - dns - download ou !q para sair', addrSource)
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
        send_message_to_requester(f'Olá. Escolha uma das opções do menu: info - ping - active - dns - download ou !q para sair',  addr)
        tClient = threading.Thread(target=cliInteraction, args=(sockConn, addr))
        tClient.start()
except Exception as e:
    print ("Fail: ", e)

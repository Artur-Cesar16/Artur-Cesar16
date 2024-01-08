import socket
from socket_constants import *

   
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((HOST_SERVER, SOCKET_PORT))

while True:
    # Lendo a mensagem do usuário
    mensagem = input("Digite a mensagem: ")

    if mensagem:
        mensagem_bytes = mensagem.encode(CODE_PAGE)
        tcp_socket.sendall(mensagem_bytes)

        data_retorno = tcp_socket.recv(BUFFER_SIZE)
        mensagem_retorno = data_retorno.decode(CODE_PAGE).strip()
        print("Echo Recebido:", mensagem_retorno)

tcp_socket.close()

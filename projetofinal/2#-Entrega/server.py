import socket
from socket_constants import *

# Criando o socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", SOCKET_PORT))
server_socket.listen(MAX_LISTEN)

print("Recebendo Mensagens...\n\n")

while True:
    client_socket, endereço = server_socket.accept()
    print(f"Conectado por: {endereço}")

    with client_socket:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            mensagem = data.decode(CODE_PAGE)
            print(f"{endereço} {mensagem}")

            # Devolvendo uma mensagem (echo) ao cliente
            mensagem_retorno = f"Devolvendo...{mensagem}"
            client_socket.sendall(mensagem_retorno.encode(CODE_PAGE))

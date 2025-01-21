import socket

escolha = input("Você é um servidor ou cliente?[S/C] ").lower()
if escolha == 's':
    HOST = socket.gethostbyname_ex(socket.gethostname())[2][0] 
    PORT = 65432 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        print("Esperando conexão...")
        socket_server.bind((HOST, PORT))
        socket_server.listen()
        connection, address = socket_server.accept()
        print(f"Endereço do cliente: {address}")
        while True:
            dados = connection.recv(1024) 
            if not dados:
                break
            mensagem = dados.decode()



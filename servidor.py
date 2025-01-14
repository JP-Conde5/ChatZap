#Fazer o ngc de página
import socket
import tkinter as tk
import sys

def pos_escolha():
    janela= tk.Tk()
    exit()
    if( escolha.get() == 'c'):
        tk.Label(master, text="Digite o IP DO SERVIDOR: ").grid(row=0)
        HOST = tk.Entry(master).grid(row=0, column=1) #IP da máquina que está o servidor
        PORT = 65432 #Porta que o cliente estará ouvindo 

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
            socket_client.connect((HOST, PORT)) #Função que busca conectar com um servidor
            print("Conectado ao servidor")
            while True:
                msg = input("Digite sua mensagem: ").encode()
                socket_client.sendall(msg) 
                if msg.lower() == 'sair':
                    resp = socket_client.recv(1024).decode()
                    print(f"{resp}")
                    break
                resp = socket_client.recv(1024).decode()
                if resp == 'n':
                    break
                print(f"{resp}")
        print("Conexão encerrada")
        janela.mainloop()
    sys.exit()
    #TCP entrega pacotes em ordem, enquanto UDP não
    janela2= tk.Tk()
    if( escolha.get() == 's'):
        local_hostname = socket.gethostname()
        HOST = socket.gethostbyname_ex(socket.gethostname())[2][0] #Onde será executad0o
        PORT = 65432 #Porta que será solicitada ao SO, quando for executado
        print('Seu ip é:', HOST)
        
        #with abre um trecho de código que após ele o objeto inicializado é apagado
        #1° parâmetro = protocolo da camada de rede => IP
        #2° parâmetro = protocolo da camada de transporte => TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
            socket_server.bind((HOST, PORT)) #bind faz a solicitação da porta ao SO
            socket_server.listen()
            print("Na escuta, aguardando alguém conectar :)")
            connection, address = socket_server.accept() #Função que aceita a requisição de conexão que retorna uma tupla com dois valores: o objeto que representa conexão (envia e recebe) e o endereço IP do cliente
            with connection:
                print(f"Conexão feito com {address}")
                while True:
                    dados = connection.recv(1024) #Função recv serve para receber dados de um computador cliente, o parâmetro é o tamanho do buffer, isto é, o maior tamanho de dado que ele recebe
                    dados = dados.decode() #Como recv retorna bytes, essa função decodifica esses dados
                    if not dados: #Se dados nulos
                        break
                    print(f"Cliente: {dados}")
                    resp = input("Quer enviar de volta? [s]/[n]")
                    if resp.lower() == "s":
                        resp = input("Sua mensagem: ")
                        connection.sendall(resp.encode())
                    elif resp.lower() == 'n':
                        resp = "n".encode() #transforma uma string em um vetor de bytes
                        connection.sendall(resp) #envia para todos conectados
                        break

    

master = tk.Tk()

tk.Label(master, text="Você é o servidor [S] ou cliente [C]: ").grid(row=0)
master.title('ChatZap')
escolha = tk.Entry(master)
escolha.grid(row=0, column=1)
tk.Button(master, text='Entre', command=pos_escolha).grid(row=2, column=0, sticky=tk.W,pady=4)
tk.mainloop()



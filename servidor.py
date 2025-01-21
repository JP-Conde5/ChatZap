#Fazer o ngc de página
import socket
import tkinter as tk
import sys
def servidor(master):
    print("Na escuta, aguardando alguém conectar :)")

    HOST = socket.gethostbyname_ex(socket.gethostname())[2][0] #Onde será executad0o
    PORT = 65432 #Porta que será solicitada ao SO, quando for executado
    linha = 0
    tk.Label(master, text=f"Seu ip é:, {HOST}").grid(row=linha)

    linha += 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        socket_server.bind((HOST, PORT)) #bind faz a solicitação da porta ao SO
        socket_server.listen()
        tk.Label(master, text="Na escuta, aguardando alguém conectar :)").grid(row=linha)
        linha += 1
        connection, address = socket_server.accept() #Função que aceita a requisição de conexão que retorna uma tupla com dois valores: o objeto que representa conexão (envia e recebe) e o endereço IP do cliente
        with connection:
            tk.Label(master, text=f"Conexão feito com {address}").grid(row=linha)

            while True:
                linha += 1
                coluna = 0
                dados = connection.recv(1024) #Função recv serve para receber dados de um computador cliente, o parâmetro é o tamanho do buffer, isto é, o maior tamanho de dado que ele recebe
                dados = dados.decode() #Como recv retorna bytes, essa função decodifica esses dados
                if not dados: #Se dados nulos
                    break
                tk.Label(master, text=f"Cliente: {dados}. Quer enviar de volta? [s]/[n]").grid(row=linha, column=coluna)
                coluna += 1
                resp = tk.Entry(master).grid(row=linha,column=coluna)
                coluna = 0
                linha += 1
                if resp.lower() == "s":
                    tk.Label(master, text=f"Sua mensagem:").grid(row=linha, column=coluna)
                    coluna += 1
                    resp = tk.Entry(master).grid(row=linha, column=coluna)
                    connection.sendall(resp.encode())
                elif resp.lower() == 'n':
                    connection.sendall(resp.encode()) #envia para todos conectados
                    break
        tk.mainloop()

def cliente(master):
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
    tk.mainloop()
    #TCP entrega pacotes em ordem, enquanto UDP não
    
def pos_escolha(master):
    if escolha.get().lower() == 's':
        servidor(master)
    elif escolha.get().lower == 'c':
        cliente(master)


master = tk.Tk()
master.geometry("800x600")
tk.Label(master, text="Você é o servidor [S] ou cliente [C]: ").grid(row=0)
master.title('ChatZap')
escolha = tk.Entry(master)
escolha.grid(row=0, column=1)
tk.Button(master, text='Entre', command=pos_escolha(master)).grid(row=2, column=0, sticky=tk.W,pady=4)
tk.mainloop()



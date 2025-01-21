#Fazer o ngc de página
import socket
import tkinter as tk
from threading import Thread

def servidor():
    janela_servidor = tk.Toplevel()
    janela_servidor.geometry("800x600")
    HOST = socket.gethostbyname_ex(socket.gethostname())[2][0] #Onde será executad0o
    PORT = 65432 #Porta que será solicitada ao SO, quando for executado
    linha = 0
    tk.Label(janela_servidor, text=f"Seu ip é:, {HOST}").grid(row=linha)
    linha += 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        socket_server.bind((HOST, PORT)) #bind faz a solicitação da porta ao SO
        socket_server.listen()
        tk.Label(janela_servidor, text="Na escuta, aguardando alguém conectar :)").grid(row=linha)
        linha += 1
        connection, address = socket_server.accept() #Função que aceita a requisição de conexão que retorna uma tupla com dois valores: o objeto que representa conexão (envia e recebe) e o endereço IP do cliente
        with connection:
            tk.Label(janela_servidor, text=f"Conexão feito com {address}").grid(row=linha)
            while True:
                linha += 1
                coluna = 0
                dados = connection.recv(1024) #Função recv serve para receber dados de um computador cliente, o parâmetro é o tamanho do buffer, isto é, o maior tamanho de dado que ele recebe
                dados = dados.decode() #Como recv retorna bytes, essa função decodifica esses dados
                if not dados: #Se dados nulos
                    break
                tk.Label(janela_servidor, text=f"Cliente: {dados}. Quer enviar de volta? [s]/[n]").grid(row=linha, column=coluna)
                coluna += 1
                resp = tk.Entry(janela_servidor).grid(row=linha,column=coluna)
                coluna = 0
                linha += 1
                if resp.get().lower() == "s":
                    tk.Label(janela_servidor, text=f"Sua mensagem:").grid(row=linha, column=coluna)
                    coluna += 1
                    resp = tk.Entry(janela_servidor).grid(row=linha, column=coluna)
                    connection.sendall(resp.get().encode())
                elif resp.get().lower() == 'n':
                    connection.sendall(resp.get().encode()) #envia para todos conectados
                    break
    janela_servidor.destroy()

def cliente():
    janela_cliente = tk.Toplevel()
    linha = 0
    tk.Label(janela_cliente, text="Digite o IP DO SERVIDOR: ").grid(row=linha)
    HOST = tk.Entry(janela_cliente).grid(row=0, column=1) #IP da máquina que está o servidor
    HOST = HOST.get()
    PORT = 65432 #Porta que o cliente estará ouvindo 
    linha += 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
        socket_client.connect((HOST, PORT)) #Função que busca conectar com um servidor
        tk.Label(master, text="Conectado ao servidor").grid(row=linha)
        linha += 1
        while True:
            coluna = 0
            tk.Label(master, text="Sua mensagem: ").grid(row=linha, column=coluna)
            coluna += 1
            msg = tk.Entry(master).grid(row=linha, column=coluna)
            coluna = 0
            linha += 1
            socket_client.sendall(msg) 
            if msg.get().lower() == 'sair':
                resp = socket_client.recv(1024).decode()
                tk.Label(master, text=f"{resp}").grid(row=linha, column=coluna)
                break
            resp = socket_client.recv(1024).decode()
            if resp == 'n':
                break
            tk.Label(master, text=f"{resp}").grid(row=linha, column=coluna)
    janela_cliente.destroy()
    print("Conexão encerrada")
    #TCP entrega pacotes em ordem, enquanto UDP não
    
def pos_escolha():
    if escolha.get().lower() == 's':
        Thread(target=servidor, daemon=True).start()  # Executa servidor em uma thread
    elif escolha.get().lower == 'c':
        Thread(target=cliente, daemon=True).start()  # Executa servidor em uma thread


master = tk.Tk()
master.geometry("800x600")
tk.Label(master, text="Você é o servidor [S] ou cliente [C]: ").grid(row=0)
master.title('ChatZap')
escolha = tk.Entry(master)
escolha.grid(row=0, column=1)
tk.Button(master, text='Entre', command=pos_escolha).grid(row=2, column=0, sticky=tk.W,pady=4)
tk.mainloop()



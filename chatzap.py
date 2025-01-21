import tkinter as tk
from threading import Thread
import socket

def iniciar_cliente():
    janela_cliente = tk.Toplevel()
    janela_cliente.geometry("800x600")
    janela_cliente.title("Cliente")
    linha = 0

    tk.Label(janela_cliente, text="Digite o IP do servidor: ").grid(row=linha, column=0)
    ip = tk.Entry(janela_cliente)
    ip.grid(row=linha, column=1)
    linha += 1

    def conectar_cliente():
        linha_local = linha
        HOST = ip.get()
        PORT = 65432
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
            socket_client.connect((HOST, PORT))
            tk.Label(janela_cliente, text="Conecado ao servido").grid(row=linha_local, column=0)
            flag = [True]
            while flag[0]:
                linha_local += 1
                tk.Label(janela_cliente, text="Sua mensagem").grid(row=linha_local, column=0)
                mensagem = tk.Entry(janela_cliente)
                mensagem.grid(row=linha_local, column=1)
                mensagem = mensagem.get()
                def enviar_mensagem():
                    socket_client.sendall(mensagem.encode())
                    while True:
                        dados = socket_client.recv(1024)  # Recebe dados do servidor
                        if not dados:
                            flag[0] = False
                            break
                        dados = dados.decode()
                        tk.Label(janela_cliente, text=f"Servidor: {mensagem}").grid(row=linha, column=0)
                tk.Button(janela_cliente, text="Enviar e espera", command=enviar_mensagem)
    tk.Button(janela_cliente, text="Conectar", command=conectar_cliente)
        
    


def iniciar_servidor():
    janela_servidor = tk.Toplevel()
    janela_servidor.geometry("800x600")
    janela_servidor.title("Servidor")
    linha = 0

    HOST = socket.gethostbyname_ex(socket.gethostname())[2][0] 
    PORT = 65432 
    tk.Label(janela_servidor, text=f"Seu IP é: {HOST}").grid(row=linha, column=0)
    linha += 1
    tk.Label(janela_servidor, text="Aguardando conexão...").grid(row=linha, column=0)
    linha += 1
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        socket_server.bind((HOST, PORT))
        socket_server.listen()

        tk.Label(janela_servidor, text="Servidor pronto, aguardando cliente...").grid(row=linha, column=0)
        linha += 1

        connection, address = socket_server.accept()
        tk.Label(janela_servidor, text=f"Cliente conectado: {address}").grid(row=linha, column=0)
        linha += 1

        
        while True:
            dados = connection.recv(1024)  # Recebe dados do cliente
            if not dados:
                break
            mensagem = dados.decode()
            tk.Label(janela_servidor, text=f"Cliente: {mensagem}").grid(row=linha, column=0)
            linha+=1
        tk.Label(janela_servidor, text=f"Sua mensagem: ").grid(row=linha, column=0)
        entrada_mensagem = tk.Entry(janela_servidor)
        entrada_mensagem.grid(row=linha, column=1)
        linha+=1
        def enviar_mensagem():
            mensagem = entrada_mensagem.get()
            connection.sendall(mensagem.encode())
            tk.Label(janela_servidor, text=f"Servidor: {mensagem}").grid(row=linha, column=0)
            entrada_mensagem.delete(0, tk.END)

        tk.Button(janela_servidor, text="Enviar", command=enviar_mensagem).grid(row=linha, column=1)


def gerencia_escolha():
    x_escolha = escolha.get().lower()
    if x_escolha == 's':
        print("Servidor")
        Thread(target=iniciar_servidor, daemon=True).start()
    elif x_escolha == 'c':
        print("Cliente")
        Thread(target=iniciar_cliente, daemon=True).start()

master = tk.Tk()
master.title('Chatzap')
master.geometry("800x600")
tk.Label(master, text="Você é um servidor ou cliente?[S/C] ").grid(row=0)
escolha = tk.Entry(master)
escolha.grid(row=0, column=1)
tk.Button(master, text="Confirmar", command=gerencia_escolha).grid(row=1)
master.mainloop()
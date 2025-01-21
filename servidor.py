import socket
import tkinter as tk
from threading import Thread

def servidor():
    janela_servidor = tk.Toplevel()
    janela_servidor.geometry("800x600")
    janela_servidor.title("Servidor")
    linha = 0

    HOST = socket.gethostbyname_ex(socket.gethostname())[2][0]  # IP do servidor
    PORT = 65432  # Porta usada pelo servidor

    tk.Label(janela_servidor, text=f"Seu IP é: {HOST}").grid(row=linha, column=0)
    linha += 1

    tk.Label(janela_servidor, text="Aguardando conexão...").grid(row=linha, column=0)
    linha += 1

    # Função para receber mensagens do cliente
    def receber_mensagens(connection):
        while True:
            try:
                dados = connection.recv(1024)  # Recebe dados do cliente
                if not dados:
                    break
                mensagem = dados.decode()
                tk.Label(janela_servidor, text=f"Cliente: {mensagem}").grid(row=linha, column=0)
            except:
                break

    # Inicializa o socket do servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        socket_server.bind((HOST, PORT))
        socket_server.listen()

        tk.Label(janela_servidor, text="Servidor pronto, aguardando cliente...").grid(row=linha, column=0)
        linha += 1

        connection, address = socket_server.accept()
        tk.Label(janela_servidor, text=f"Cliente conectado: {address}").grid(row=linha, column=0)
        linha += 1

        Thread(target=receber_mensagens, args=(connection,), daemon=True).start()

        # Função para enviar mensagens ao cliente
        def enviar_mensagem():
            mensagem = entrada_mensagem.get()
            connection.sendall(mensagem.encode())
            tk.Label(janela_servidor, text=f"Servidor: {mensagem}").grid(row=linha, column=0)
            entrada_mensagem.delete(0, tk.END)

        entrada_mensagem = tk.Entry(janela_servidor)
        entrada_mensagem.grid(row=linha, column=0)
        tk.Button(janela_servidor, text="Enviar", command=enviar_mensagem).grid(row=linha, column=1)

    janela_servidor.destroy()

def cliente():
    janela_cliente = tk.Toplevel()
    janela_cliente.geometry("800x600")
    janela_cliente.title("Cliente")
    linha = 0

    tk.Label(janela_cliente, text="Digite o IP do servidor: ").grid(row=linha, column=0)
    entrada_ip = tk.Entry(janela_cliente)
    entrada_ip.grid(row=linha, column=1)
    linha += 1

    tk.Label(janela_cliente, text="Conectando ao servidor...").grid(row=linha, column=0)
    linha += 1

    def conectar():
        HOST = entrada_ip.get()
        PORT = 65432  # Porta usada pelo servidor

        # Inicializa o socket do cliente
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
            try:
                socket_client.connect((HOST, PORT))
                tk.Label(janela_cliente, text="Conectado ao servidor").grid(row=linha, column=0)

                # Função para receber mensagens do servidor
                def receber_mensagens():
                    while True:
                        try:
                            dados = socket_client.recv(1024)  # Recebe dados do servidor
                            if not dados:
                                break
                            mensagem = dados.decode()
                            tk.Label(janela_cliente, text=f"Servidor: {mensagem}").grid(row=linha, column=0)
                        except:
                            break

                Thread(target=receber_mensagens, daemon=True).start()

                # Função para enviar mensagens ao servidor
                def enviar_mensagem():
                    mensagem = entrada_mensagem.get()
                    socket_client.sendall(mensagem.encode())
                    tk.Label(janela_cliente, text=f"Cliente: {mensagem}").grid(row=linha, column=0)
                    entrada_mensagem.delete(0, tk.END)

                entrada_mensagem = tk.Entry(janela_cliente)
                entrada_mensagem.grid(row=linha, column=0)
                tk.Button(janela_cliente, text="Enviar", command=enviar_mensagem).grid(row=linha, column=1)
            except Exception as e:
                tk.Label(janela_cliente, text=f"Erro: {e}").grid(row=linha, column=0)

    tk.Button(janela_cliente, text="Conectar", command=conectar).grid(row=linha, column=0)

def pos_escolha():
    if escolha.get().lower() == 's':
        Thread(target=servidor, daemon=True).start()  # Executa o servidor em uma thread
    elif escolha.get().lower() == 'c':
        Thread(target=cliente, daemon=True).start()  # Executa o cliente em uma thread

# Interface principal
master = tk.Tk()
master.geometry("800x600")
master.title('ChatZap')

tk.Label(master, text="Você é o servidor [S] ou cliente [C]: ").grid(row=0, column=0)
escolha = tk.Entry(master)
escolha.grid(row=0, column=1)

tk.Button(master, text='Entre', command=pos_escolha).grid(row=1, column=0, sticky=tk.W, pady=4)

master.mainloop()

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
                        break
                    dados = dados.decode()
                    tk.Label(janela_cliente, text=f"Servidor: {mensagem}").grid(row=linha, column=0)
            tk.Button(janela_cliente, text="Enviar e espera", command=enviar_mensagem)

    
    tk.Button(janela_cliente, text="Conectar", command=conectar_cliente)
        
    


def iniciar_servidor():
    print("oi")


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
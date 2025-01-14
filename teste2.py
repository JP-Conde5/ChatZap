from tkinter import *
import sys

janela1 = Tk()
b1 = Button(janela1, text="Janela 2")
b1.grid()
b2 = Button(janela1, command=exit, text="Janela 3")
b2.grid()
janela1.geometry("200x100")
janela1.mainloop()

sys.exit()

janela2 = Tk()
b3 = Button(janela2, text="Voltar")
b3.grid()
janela2.geometry("200x100")
janela2.mainloop()

janela3 = Tk()
b4 = Button(janela3, text="Voltar")
b4.grid()
janela3.geometry("200x100")
janela3.mainloop()
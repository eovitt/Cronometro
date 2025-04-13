import tkinter as tk
from threading import Thread
import time
import datetime

class Cronometro:

    def __init__(self):

        # Inicializa a janela principal do Tkinter
        self.root = tk.Tk()
        self.root.title("Cronômetro")

        # Configura a alternância de tela cheia
        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        # Cria e empacota o rótulo principal que exibe o tempo
        self.label = tk.Label(self.root, text="00:00:00", font=('Arial', 48))
        self.label.pack(expand=True)

        # Cria um frame para os botões e o empacota
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack(expand=True)

        # Botão Iniciar/Parar
        self.button_iniciar = tk.Button(self.frame_buttons, text="Iniciar", command=self.iniciar)
        self.button_iniciar.pack(side=tk.LEFT, padx=5)

        # Botão Resetar
        self.button_resetar = tk.Button(self.frame_buttons, text="Resetar", command=self.resetar, state=tk.DISABLED)
        self.button_resetar.pack(side=tk.LEFT, padx=5)

        # Botão Volta
        self.button_volta = tk.Button(self.frame_buttons, text="Volta", command=self.volta, state=tk.DISABLED)
        self.button_volta.pack(side=tk.LEFT, padx=5)

        # Rótulo para o display de voltas
        self.voltas_label = tk.Label(self.root, text="Voltas:", font=('Arial', 14))
        self.voltas_label.pack()

        # Display de voltas
        self.voltas_display = tk.Text(self.root, height=10, width=30, state=tk.DISABLED)
        self.voltas_display.pack(expand=True)

        # Inicializa variáveis de controle
        self.running = False
        self.thread = None
        self.start_time = None
        self.elapsed_time = 0

    def toggle_fullscreen(self, event=None):

        # Alterna entre o modo de tela cheia e o modo janela
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):

        # Sai do modo de tela cheia
        self.fullscreen = False
        self.root.attributes("-fullscreen", self.fullscreen)

    def iniciar(self):

        # Inicia ou para o cronômetro
        if not self.running:
            self.button_iniciar.config(text="Parar", command=self.parar)
            self.button_resetar.config(state=tk.DISABLED)
            self.button_volta.config(state=tk.NORMAL)
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.thread = Thread(target=self.contar)
            self.thread.start()
        else:
            self.parar()

    def parar(self):

        # Para o cronômetro
        self.button_iniciar.config(text="Iniciar", command=self.iniciar)
        self.button_resetar.config(state=tk.NORMAL)
        self.button_volta.config(state=tk.DISABLED)
        self.running = False

    def resetar(self):

        # Reseta o cronômetro e limpa o display de voltas
        self.parar()
        self.elapsed_time = 0
        self.label.config(text="00:00:00")
        self.voltas_display.config(state=tk.NORMAL)
        self.voltas_display.delete(1.0, tk.END)
        self.voltas_display.config(state=tk.DISABLED)

    def volta(self):

        # Registra uma volta e a exibe no display de voltas
        if self.running:
            formatted_time = str(datetime.timedelta(seconds=int(self.elapsed_time)))
            self.voltas_display.config(state=tk.NORMAL)
            self.voltas_display.insert(tk.END, formatted_time + "\n")
            self.voltas_display.config(state=tk.DISABLED)

    def contar(self):

        # Contador do cronômetro que atualiza o rótulo com o tempo decorrido
        while self.running:
            self.elapsed_time = time.time() - self.start_time
            formatted_time = str(datetime.timedelta(seconds=int(self.elapsed_time)))
            self.label.config(text=formatted_time)
            time.sleep(1)

    def run(self):

        # Inicia o loop principal do Tkinter
        self.root.mainloop()

if __name__ == "__main__":
    
    # Cria uma instância do cronômetro e inicia a aplicação
    cronometro = Cronometro()
    cronometro.run()
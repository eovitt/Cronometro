import flet as ft
import time
import datetime
from threading import Thread

class CronometroApp:

    def __init__(self):
        self.running = False
        self.elapsed_time = 0
        self.start_time = None
        self.thread = None
        self.voltas = []

    def main(self, page: ft.Page):
        self.page = page
        page.title = "Cronômetro"
        page.scroll = ft.ScrollMode.AUTO

        self.timer_text = ft.Text("00:00:00", size=48, text_align=ft.TextAlign.CENTER)
        self.voltas_display = ft.TextField(value="", multiline=True, read_only=True, height=200)

        self.iniciar_btn = ft.ElevatedButton("Iniciar", on_click=self.iniciar)
        self.resetar_btn = ft.ElevatedButton("Resetar", on_click=self.resetar, disabled=True)
        self.volta_btn = ft.ElevatedButton("Volta", on_click=self.volta, disabled=True)

        buttons_row = ft.Row(
            controls=[self.iniciar_btn, self.resetar_btn, self.volta_btn],
            alignment=ft.MainAxisAlignment.CENTER
        )

        page.add(
            ft.Column(
                [
                    self.timer_text,
                    buttons_row,
                    ft.Text("Voltas:", size=16),
                    self.voltas_display,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        )

    def iniciar(self, e):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.iniciar_btn.text = "Parar"
            self.iniciar_btn.on_click = self.parar
            self.resetar_btn.disabled = True
            self.volta_btn.disabled = False
            self.page.update()

            self.thread = Thread(target=self.contar)
            self.thread.daemon = True
            self.thread.start()
        else:
            self.parar(e)

    def parar(self, e):
        self.running = False
        self.iniciar_btn.text = "Iniciar"
        self.iniciar_btn.on_click = self.iniciar
        self.resetar_btn.disabled = False
        self.volta_btn.disabled = True
        self.page.update()

    def resetar(self, e):
        self.parar(e)
        self.elapsed_time = 0
        self.timer_text.value = "00:00:00"
        self.voltas_display.value = ""
        self.voltas.clear()
        self.page.update()

    def volta(self, e):
        if self.running:
            formatted_time = str(datetime.timedelta(seconds=int(self.elapsed_time)))
            self.voltas.append(formatted_time)
            self.voltas_display.value = "\n".join(self.voltas)
            self.page.update()

    def contar(self):
        while self.running:
            self.elapsed_time = time.time() - self.start_time
            formatted_time = str(datetime.timedelta(seconds=int(self.elapsed_time)))
            self.timer_text.value = formatted_time
            self.page.update()
            time.sleep(1)

# Rodar o app
if __name__ == "__main__":
    app = CronometroApp()
    ft.app(target=app.main)

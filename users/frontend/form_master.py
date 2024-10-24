import tkinter as tk
from tkinter.font import BOLD
import util.utilidades as utl  
from util.utilidades import leer_imagen,resource_path
import os
class MasterPanel:
    def __init__(self, on_close_callback,mensaje):
        
        self.ventana = tk.Tk()
        self.ventana.title(mensaje)
        w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()
        icon_path = resource_path('assets_2/logo_biblioteca.ico')
        if os.path.exists(icon_path):
            self.ventana.iconbitmap(icon_path)
        else:
            print(f"Archivo no encontrado: {icon_path}")
        self.ventana.geometry("%dx%d+0+0" % (w, h))
        self.ventana.config(bg="#6bb16b")
        self.ventana.wm_resizable(width=0, height=0)

        logo_path = resource_path("assets_2/Logo-user-blanco.png")
        logo = leer_imagen(logo_path, (200, 200))
        self.logo_label = tk.Label(self.ventana, image=logo, bg="#041022")
        self.logo_label.image = logo  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector
        self.logo_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Guardar el callback de cierre
        self.on_close_callback = on_close_callback
        
        # Configurar el protocolo de cierre de la ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Destruir la ventana
        self.ventana.destroy()
        
        # Llamar al callback de cierre
        self.on_close_callback()

    def show(self):
        # Iniciar el bucle principal de tkinter
        self.ventana.mainloop()

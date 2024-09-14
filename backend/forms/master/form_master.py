import tkinter as tk
from tkinter.font import BOLD
import util.ventana as utl  

class MasterPanel:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Iniciando Sesión")
        w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()
        
        self.ventana.geometry("%dx%d+0+0" % (w, h))
        self.ventana.config(bg="#6bb16b")
        self.ventana.wm_resizable(width= 0,height= 0)

        logo = utl.leer_imagen("assets_2/Logo-user-blanco.png", (200, 200))
        label = tk.Label(self.ventana, image= logo, bg="#75C99A")
        label.place(x=0,y=0,relwidth=1, relheight=1)
        self.ventana.mainloop()
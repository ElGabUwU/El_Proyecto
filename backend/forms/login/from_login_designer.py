import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import util.ventana as utl


class FormLoginDesigner:

    def on_enter(self, event, nex_widget):
        nex_widget.focus_set()

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Inicio de Sesion")
        self.ventana.geometry("800x500")
        self.ventana.config(bg="#fcfcfc")
        self.ventana.resizable(width=0, height=0)
        utl.centrar_ventana(self.ventana, 800, 500)

        logo = utl.leer_imagen("assets_2/Logo-user-blanco.png", (200, 200))
        
        # frame_logo
        frame_logo = tk.Frame(self.ventana, bd=0, width=320, relief=tk.SOLID, padx=10, pady=10, bg="#75C99A")
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg="#75C99A")
        label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # frame_form
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg="white")
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        #frame_form_top
        frame_form_top = tk.Frame(
            frame_form, 
            height= 50, 
            bd=0, 
            relief=tk.SOLID, 
            bg="black")
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion",font=("Arial",30),fg="#666a88", bg="white",pady=50)
        title.pack(expand=tk.YES,fill=tk.BOTH)

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0,relief=tk.SOLID,bg="white")
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        etiqueta_user = tk.Label(frame_form_fill,text="Usuario", font=("Arial",14),fg="#666a88", bg="white",anchor="w")
        etiqueta_user.pack(fill=tk.X, padx=20, pady=5)
        self.user = ttk.Entry(frame_form_fill, font=("Arial",14))
        self.user.pack(fill=tk.X,padx=20,pady=10),
        self.user.bind("<Return>", self.verificar)
        


        etiqueta_password = tk.Label(frame_form_fill,text="Contraseña", font=("Arial",14),fg="#666a88",bg="white",anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20,pady=5)
        self.password = ttk.Entry(frame_form_fill, font=("Arial",14))
        self.password.pack(fill=tk.X,padx=20,pady=10)
        self.password.config(show="*")
        self.password.bind("<Return>", self.verificar)

        inicio = tk.Button(frame_form_fill,text="Iniciar Sesion",font=("Arial",14,BOLD),bg="#3a7ff6",bd=0,fg="#fff",command=self.verificar)
        inicio.pack(fill=tk.X, padx=20,pady=20)
        #inicio.bind("<Return>", self.verificar)
        self.ventana.mainloop()


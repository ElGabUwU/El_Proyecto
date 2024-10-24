import tkinter as tk
from tkinter import ttk
from tkinter.font import BOLD
import util.utilidades as utl
from util.utilidades import resource_path,centrar_ventana,leer_imagen
import os
from validations.user_validations import *
from PIL import ImageTk, Image


class FormLoginDesigner:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Inicio de Sesion")
        self.ventana.geometry("800x500")
        self.ventana.config(bg="#042344")
        
        # Usar ruta relativa para el icono
        icon_path = resource_path('assets_2/logo_biblioteca.ico')
        if os.path.exists(icon_path):
            self.ventana.iconbitmap(icon_path)
        else:
            print(f"Archivo no encontrado: {icon_path}")

        self.ventana.resizable(width=0, height=0)
        centrar_ventana(self.ventana, 800, 500)

        logo_path = resource_path("assets_2/Logo-user-blanco.png")
        logo = leer_imagen(logo_path, (200, 200))

        # frame_logo
        frame_logo = tk.Frame(self.ventana, bd=0, width=320, relief=tk.SOLID, padx=10, pady=10, bg="#041022")
        frame_logo.pack(side="left", expand=tk.NO, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg="#041022")
        label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # frame_form
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg="#042344")
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # frame_form_top
        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg="black")
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion", font=("Arial", 30), fg="#666a88", bg="white", pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg="white")
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        etiqueta_user = tk.Label(frame_form_fill, text="Usuario", font=("Arial", 14), fg="#666a88", bg="white", anchor="w")
        etiqueta_user.pack(fill=tk.X, padx=20, pady=5)
        self.user = ttk.Entry(frame_form_fill, font=("Arial", 14))
        self.user.pack(fill=tk.X, padx=20, pady=10)
        self.user.bind("<KeyPress>", self.on_key_press_user_login)
        self.user.bind("<Return>", lambda event: self.on_enter(event, self.password))

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=("Arial", 14), fg="#666a88", bg="white", anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=("Arial", 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")
        self.password.bind("<KeyPress>", self.on_key_press_user_login)
        self.password.bind("<Return>", self.verificar)

        inicio = tk.Button(frame_form_fill, text="Iniciar Sesion", font=("Arial", 14, 'bold'), bg="#3a7ff6", bd=0, fg="#fff", command=self.verificar)
        inicio.pack(fill=tk.X, padx=20, pady=20)

        self.ventana.mainloop()

    
    def on_key_press_user_login(self, event):
        widget = event.widget
        current_text = widget.get()
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'):
            return
        
        # Guardar la posición del cursor antes de añadir el nuevo carácter
        cursor_position = widget.index(tk.INSERT)
        
        # Añadir el nuevo carácter al texto actual en la posición del cursor
        new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
        
        # Aplicar condicionales según el widget
        if widget == self.user:
            # Limitar la longitud a 12 caracteres
            new_text = limit_length(new_text, 12)
            # Permitir solo caracteres específicos
            formatted_text = allow_permitted_characters(new_text)
        elif widget == self.password:
            # Limitar la longitud a 16 caracteres
            new_text = limit_length(new_text, 16)
            # Para contraseña se permiten todos los caracteres
            formatted_text = new_text
        
        # Actualizar el campo de entrada
        widget.delete(0, tk.END)
        widget.insert(0, formatted_text)
        
        # Restaurar la posición del cursor
        widget.icursor(cursor_position + 1)
        
        return "break"
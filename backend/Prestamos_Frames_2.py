import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from Library.librerias import recoger_sesion, drop_sesion

from Vistas.listas import *
import random


def validate_number_input(text):
        if text == "":
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False

def relative_to_assets(path: str) -> str:
    return f"./assets_2/{path}"

class P_Registrar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        
        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del nuevo usuario a agregar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cedula", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 152.0, anchor="nw", text="Nombre", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 152.0, anchor="nw", text="Apellido", fill="#000000", font=("Montserrat Regular", 15))

        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Numero de teléfono", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Dirección", fill="#000000", font=("Montserrat Regular", 15))
        
        
        #fila 3
        
        
        
        #fila 4
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        
        #primera fila
        
        
        self.input_cedula = tk.Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0, 
            borderwidth=0.5, 
            relief="solid",
            validate="key",
            validatecommand=(validate_number, "%P")
        )
        self.input_cedula.place(x=263.0, y=182.0, width=237.0, height=38.0)
        
        self.input_nombre = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_nombre.place(x=520.0, y=182.0, width=237.0, height=38.0)
 
        self.input_apellido = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_apellido.place(x=779.0, y=182.0, width=237.0, height=37.5)
        
        #segunda fila
        
        
        self.input_telefono = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_telefono.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.input_direccion = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_direccion.place(x=520.0, y=282.0, width=237.0, height=38.0)
        
        
        
        
       
        #tercera fila
        

        
        
        #-------------------------------------------------------------------------------
        # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("R_Boton_registrar.png"))

        # Crear el botón
        boton_R = self.images['boton_R']
        tk.Button(
            self,
            image=boton_R,
            borderwidth=0,
            highlightthickness=0,
            #command=lambda: self.add_pokemon(),
            relief="flat",
        ).place(x=265.0, y=365.0, width=130.0, height=40.0)
        
        
        
        
class P_Modificar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        #validate_number = self.register(validate_number_input)
        self.images = {}
        
        #hacer algo similar a R_selection para decidir si modificar los libros que tiene un cliente asignados o la informacion de este?
        #o hacer que solo se pueda modificar la informacion de cliente o los libros
        #tomar esta misma decicion para eliminar
        
        
        
        
        

class P_Eliminar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Formulario para el eliminar
        self.label_info = self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del cliente a Eliminar de la lista de prestamos", fill="#4C4C4C", font=("Montserrat Medium", 15))
        
        # Texto para el nombre
        self.label_cedula = self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cedula", fill="#000000", font=("Montserrat Regular", 15))
        
        self.input_cedula = tk.Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0, 
            borderwidth=0.5, 
            relief="solid",
            validate="key",
            validatecommand=(validate_number, "%P")
        )
        self.input_cedula.place(x=263.0, y=182.0, width=237.0, height=38.0)
        
        # Cargar y almacenar las imágenes
        self.images['boton_Eliminar_f'] = tk.PhotoImage(file=relative_to_assets("Boton_eliminar.png"))
        
        # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
            self,
            image=self.images['boton_Eliminar_f'],
            borderwidth=0,
            highlightthickness=0,
            #command=lambda:self.Delete_Pokion(),
            relief="flat"
        )
        self.button_e.place(x=265.0, y=264.0, width=130.0, height=40.0)
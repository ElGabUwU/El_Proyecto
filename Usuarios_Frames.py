import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from Library.librerias import recoger_sesion, drop_sesion
from Library.db_pokimon import  create_pokemon,delete_pokemon,update_pokemon
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

class U_Registrar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        
        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del nuevo usuario a agregar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cargo", fill="#000000", font=("Montserrat Regular", 15))

        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Nombre", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Apellido", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 252.0, anchor="nw", text="Cedula", fill="#000000", font=("Montserrat Regular", 15))
        
        
        #fila 3
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Nombre de usuario", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Contraseña", fill="#000000", font=("Montserrat Regular", 15))
        
        
        #fila 4
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        #primera fila
        self.altura = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.altura.place(x=520.0, y=282.0, width=237.0, height=38.0)
 
        self.peso = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.peso.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.entry1 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry1.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        
        #segunda fila
        self.entry3 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry3.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.entry4 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry4.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
       
        #tercera fila
        
        
        
        #Select tipo de pokemon
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox",
                        fieldbackground="#FFFFFF",  # Fondo del campo de entrada
                        background="#FF0000",  # Fondo del desplegable
                        bordercolor="#000716",  # Color del borde
                        arrowcolor="#FFFFFF",  # Color de la flecha
                        padding= "9",
                        ) # padding para agrandar la altura del select
        
        pokemon_types = [
        "Agua", "Bicho", "Dragón", "Electrico", "Fuego", "Hielo",
        "Lucha", "Normal", "Planta", "Psiquico", "Roca", "Tierra",
        "Veneno", "Volador"
        ]
         
        self.combobox1 = ttk.Combobox(self, values=pokemon_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.combobox1.place(x=263.0, y=181.5)
        
        
        #-------------------------------------------------------------------------------
        # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("R_Boton_registrar.png"))

        

        
        # Crear el botón con la imagen inicial


        # Crear el botón
        boton_R = self.images['boton_R']
        tk.Button(
            self,
            image=boton_R,
            borderwidth=0,
            highlightthickness=0,
            #command=lambda: self.add_pokemon(),
            relief="flat",
        ).place(x=265.0, y=465.0, width=130.0, height=40.0)
        
class U_Modificar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        
        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del usuario a modificar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cargo", fill="#000000", font=("Montserrat Regular", 15))

        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Nombre", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Apellido", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 252.0, anchor="nw", text="Cedula", fill="#000000", font=("Montserrat Regular", 15))
        
        
        #fila 3
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Nombre de usuario", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Contraseña", fill="#000000", font=("Montserrat Regular", 15))
        
        
        #fila 4
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        #primera fila
        self.altura = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.altura.place(x=520.0, y=282.0, width=237.0, height=38.0)
 
        self.peso = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.peso.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.entry1 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry1.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        
        #segunda fila
        self.entry3 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry3.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.entry4 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry4.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        #Select tipo de pokemon
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox",
                        fieldbackground="#FFFFFF",  # Fondo del campo de entrada
                        background="#FF0000",  # Fondo del desplegable
                        bordercolor="#000716",  # Color del borde
                        arrowcolor="#FFFFFF",  # Color de la flecha
                        padding= "9",
                        ) # padding para agrandar la altura del select
        
        pokemon_types = [
        "Agua", "Bicho", "Dragón", "Electrico", "Fuego", "Hada", "Hielo",
        "Lucha", "Normal", "Planta", "Psíquico", "Roca", "Siniestro", "Tierra",
        "Veneno", "Volador"
        ]
        
        self.combobox1 = ttk.Combobox(self, values=pokemon_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.combobox1.place(x=263.0, y=181.5)
        #-------------------------------------------------------------------------------
      
        

        #-------------------------------------------------------------------------------
        # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("M_Boton.png"))

        # Crear el botón con la imagen inicial

        # Crear el botón
        boton_R = self.images['boton_R']
        tk.Button(
            self,
            image=boton_R,
            borderwidth=0,
            highlightthickness=0,
            #command=lambda: self.mod_pokemon(),
            relief="flat",
        ).place(x=265.0, y=465.0, width=130.0, height=40.0)
        
      
        
        
        
class U_Eliminar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        #validate_number = self.register(validate_number_input)
        self.images = {}

        # Formulario para el eliminar
        self.label_info = self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del usuario a Eliminar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        
        # Texto para el nombre
        self.label_nombre = self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cedula", fill="#000000", font=("Montserrat Regular", 15))
        
        self.input_nombre = tk.Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0, 
            borderwidth=0.5, 
            relief="solid"
        )
        self.input_nombre.place(x=263.0, y=182.0, width=237.0, height=38.0)
        
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
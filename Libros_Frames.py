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

class L_Registrar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        
        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del libro a agregar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Formato", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 152.0, anchor="nw", text="Sala", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 152.0, anchor="nw", text="Genero", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Cota", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Numero de registro", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 252.0, anchor="nw", text="Edición", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(1036.0, 252.0, anchor="nw", text=" N° volumen", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 3
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Titulo", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Autor", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 352.0, anchor="nw", text="Editorial", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 4
        self.canvas.create_text(263.0, 452.0, anchor="nw", text="Año", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 452.0, anchor="nw", text="Cantidad de ejemplares", fill="#000000", font=("Montserrat Regular", 15))
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        #primera fila
        
        
        """
        validate="key": Configura el widget para que valide la entrada cada vez que se presiona una tecla.
        validatecommand=(validate_number, "%P"): Define el comando de validación. validate_number es una función que se llamará para validar la entrada, y "%P" es un marcador de posición que representa el contenido del widget después de la edición.
        """
        
        self.input_cota = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_cota.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.input_N_registro = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_N_registro.place(x=520.0, y=282.0, width=237.0, height=38.0)
 
        self.input_edicion = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_edicion.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        self.input_N_volumen = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_N_volumen.place(x=1036.0, y=282.0, width=237.0, height=37.5)
        #segunda fila
        self.input_titulo = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_titulo.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.input_autor = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_autor.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        self.input_editorial = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_editorial.place(x=779.0, y=382.0, width=237.0, height=37.5)
        #tercera fila
        
        self.input_año = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_año.place(x=263.0, y=482.0, width=237.0, height=37.5)
        
        self.input_ejemplares = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_ejemplares.place(x=520.0, y=482.0, width=237.0, height=37.5)
        
        
        
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
        
        self.tipos_de_pokemones = ttk.Combobox(self, values=pokemon_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.tipos_de_pokemones.place(x=520.0, y=181.5)

        self.combobox3 = ttk.Combobox(self, values=pokemon_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.combobox3.place(x=779.0, y=181.5)
        
        
        
        
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
        ).place(x=265.0, y=555.0, width=130.0, height=40.0)
        
class L_Modificar(tk.Frame):
    
        
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
    # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del libro a modificar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Formato", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 152.0, anchor="nw", text="Sala", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 152.0, anchor="nw", text="Genero", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Cota", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Numero de registro", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 252.0, anchor="nw", text="Edición", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(1036.0, 252.0, anchor="nw", text=" N° volumen", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 3
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Titulo", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Autor", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 352.0, anchor="nw", text="Editorial", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 4
        self.canvas.create_text(263.0, 452.0, anchor="nw", text="Año", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 452.0, anchor="nw", text="Cantidad de ejemplares", fill="#000000", font=("Montserrat Regular", 15))
        #fila 5
        self.canvas.create_text(263.0, 552.0, anchor="nw", text="ID", fill="#000000", font=("Montserrat Regular", 15))
        
        
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        #primera fila
        self.input_cota = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_cota.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.input_N_registro = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_N_registro.place(x=520.0, y=282.0, width=237.0, height=38.0)
 
        self.input_edicion = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_edicion.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        self.input_N_volumen = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_N_volumen.place(x=1036.0, y=282.0, width=237.0, height=37.5)
        #segunda fila
        self.input_titulo = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_titulo.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.input_autor = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_autor.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        self.input_editorial = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_editorial.place(x=779.0, y=382.0, width=237.0, height=37.5)
        #tercera fila
        
        self.input_año = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_año.place(x=263.0, y=482.0, width=237.0, height=37.5)
        
        self.input_ejemplares = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_ejemplares.place(x=520.0, y=482.0, width=237.0, height=37.5)
        
        #cuarta fila
        
        self.input_id = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_id.place(x=263.0, y=582.0, width=237.0, height=37.5)
        
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
        
        self.tipos_de_pokemones = ttk.Combobox(self, values=pokemon_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.tipos_de_pokemones.place(x=520.0, y=181.5)

        self.combobox3 = ttk.Combobox(self, values=pokemon_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.combobox3.place(x=779.0, y=181.5)
        
        self.combobox1 = ttk.Combobox(self, values=pokemon_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.combobox1.place(x=263.0, y=181.5)
       
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("M_Boton.png"))

        # Crear el botón
        boton_R = self.images['boton_R']
        tk.Button(
            self,
            image=boton_R,
            borderwidth=0,
            highlightthickness=0,
           # command=lambda: self.mod_pokemon(),
            relief="flat",
        ).place(x=263.0, y=635.0, width=130.0, height=40.0)
        
       
        
        
        # Obtener el tipo seleccionado del combobox
        tipo_combobox = self.tipos_de_pokemones.get()
        print(tipo_combobox)
        # Obtener el valor numérico del tipo de Pokémon seleccionado
        #tipo = pokemon_types.get(tipo_combobox, 0) 
        """
        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "El campo 'Nombre' es obligatorio.")
            return
        if sexo == None:
            messagebox.showerror("Error", "El campo 'Sexo' es obligatorio.")
            return
        if not descripcion:
            messagebox.showerror("Error", "El campo 'Descripción' es obligatorio.")
            return

        try:
            peso = float(peso) if peso else 0
        except ValueError:
            messagebox.showerror("Error", "El campo 'Peso' debe ser un número válido.")
            return

        try:
            altura = float(altura) if altura else 0
        except ValueError:
            messagebox.showerror("Error", "El campo 'Altura' debe ser un número válido.")
            return
        """
        
        #se nesesitan implementar validaciones a las entrys de este codigo


class L_Eliminar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Formulario para el eliminar
        self.label_info = self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del libro a Eliminar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        
        # Texto para el nombre
        self.label_id = self.canvas.create_text(263.0, 152.0, anchor="nw", text="ID", fill="#000000", font=("Montserrat Regular", 15))
        
        self.input_id = tk.Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0, 
            borderwidth=0.5, 
            relief="solid",
            validate="key",
            validatecommand=(validate_number, "%P")
        ).place(x=263.0, y=182.0, width=237.0, height=38.0)
        
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
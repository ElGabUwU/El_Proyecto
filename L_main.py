import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from Library.librerias import recoger_sesion, drop_sesion
from Library.db_pokimon import  create_pokemon,delete_pokemon,update_pokemon
from Vistas.listas import *
import random

#hola xd

# Rutas relativas de las imágenes
ASSETS_PATH = Path(r"C:\El_Proyecto\assets_2")

# Función para asignar la ruta a las imágenes
def relative_to_assets(path: str) -> Path:
    
    full_path = ASSETS_PATH / Path(path)
    if not full_path.exists():
        raise FileNotFoundError(f"Image not found: {full_path}")
    return full_path
        
# Clase principal de la aplicación
class Balls(tk.Tk):
    def __init__(self, rol_usuario = None):
        self.rol_usuario = "administrador"
        super().__init__()
        self.title("Pokedex")
        self.geometry("1366x768")
        self.container = tk.Frame(self)
        self.resizable(False, False)  # No permitir cambiar el tamaño de la ventana
        self.container.pack(fill="both", expand=True)
        self.current_frame = None
        self.iconbitmap(relative_to_assets('PokeBall.ico'))
        self.show_frame(SecondaryPage)
        
        # Vincula la función on_closing al evento de cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        drop_sesion()
        self.destroy()

    def show_frame(self, page_class):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        self.current_frame = page_class(self.container, self, self.rol_usuario)
        self.current_frame.pack(fill="both", expand=True)

    def open(self):
        self.mainloop()

class SecondaryPage(tk.Frame):
    def __init__(self, parent, controller, rol_usuario):
        super().__init__(parent)
        self.controller = controller
        self.rol_usuario = rol_usuario
        main_page = Main_PW(self, controller, rol_usuario)
        main_page.pack(fill="both", expand=True)

class Main_PW(tk.Frame):
    def __init__(self, parent, controller, rol_usuario):
        super().__init__(parent)
        self.controller = controller
        self.rol_usuario = rol_usuario
        usuario=recoger_sesion()
        self.usuario=usuario
        self.config(bg="#FFFFFF")
        self.create_widgets()

    def create_widgets(self):
        self.images = {}
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=768,
            width=1366,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Cargar y almacenar las imágenes
        self.images["image_1"] = tk.PhotoImage(file=relative_to_assets("main_relleno_lateral.png"))
        canvas.create_image(107.0, 412.0, image=self.images["image_1"])

        self.images["image_2"] = tk.PhotoImage(file=relative_to_assets("main_relleno_general.png"))
        canvas.create_image(789.0, 413.0, image=self.images["image_2"])

        self.images["image_3"] = tk.PhotoImage(file=relative_to_assets("header.png"))
        canvas.create_image(682.0, 29.0, image=self.images["image_3"])

        self.images["button_volver"] = tk.PhotoImage(file=relative_to_assets("U_volver.png"))
        tk.Button(
            self,
            image=self.images["button_volver"],
            borderwidth=0,
            highlightthickness=0,
            activebackground="#E83030",
            command=self.open_seleccion,
            relief="flat"
        ).place(x=1135.0, y=15.0, width=208.0, height=29.0)
        
        self.images["registrar"] = tk.PhotoImage(file=relative_to_assets("main_boton_registrar.png"))
        tk.Button(
            self,
            image=self.images["registrar"],
            borderwidth=0,
            highlightthickness=0,
            command=self.open_registrar,
            relief="flat"
        ).place(x=1.0, y=57.0, width=213.0, height=58.0)

        self.images["button_image_2"] = tk.PhotoImage(file=relative_to_assets("main_boton_modificar.png"))
        tk.Button(
            self,
            image=self.images["button_image_2"],
            borderwidth=0,
            highlightthickness=0,
            command=self.open_modificar,
            relief="flat"
        ).place(x=1.0, y=173.0, width=213.0, height=58.0)

        self.images["button_image_3"] = tk.PhotoImage(file=relative_to_assets("main_boton_listado.png"))
        tk.Button(
            self,
            image=self.images["button_image_3"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: { self.controller.destroy(), show_pokemons() },
            relief="flat"
        ).place(x=1.0, y=115.0, width=213.0, height=58.0)

        self.images["button_image_4"] = tk.PhotoImage(file=relative_to_assets("main_boton_eliminar.png"))
        tk.Button(
            self,
            image=self.images["button_image_4"],
            borderwidth=0,
            highlightthickness=0,
            command=self.open_eliminar,
            relief="flat"
        ).place(x=1.0, y=231.0, width=213.0, height=58.0)
        
        #Texto en el navbar para mostrar
        canvas.create_text(
            600.0,
            141.0,
            anchor="nw",
            text="Bienvenido",
            fill="#191919",
            font=("Inter", 64 * -1)
        )
        canvas.create_text(
            226.0,
            5.0,
            anchor="nw",
            text="Sistema de Inventario",
            fill="#000000",
            font=("Inter", 40 * -1)
        )
        canvas.create_text(
            26.0,
            9.0,
            anchor="nw",
            text=self.usuario,
            fill="#000000",
            font=("Inter", 18 * -1)
        )
        canvas.create_text(
            26.0,
            31.0,
            anchor="nw",
            text=self.rol_usuario,
            fill="#000000",
            font=("Inter", 14 * -1)
        )

    def open_seleccion(self):
        self.controller.destroy()  ##### Cierra solo la ventana  actual
        from Vistas.R_selection import selection
        selection().open() 
        
    def open_registrar(self):
        if self.rol_usuario == "administrador":
            self.controller.show_frame(Registrar)
        else:
            self.show_permission_error()

    def open_modificar(self):
        if self.rol_usuario == "administrador":
            self.controller.show_frame(Modificar)
        else:
            self.show_permission_error()

    def open_eliminar(self):
        if self.rol_usuario == "administrador":
            self.controller.show_frame(Eliminar)
        else:
            self.show_permission_error()

    def show_permission_error(self):
        messagebox.showerror("Permiso Denegado", "No tienes los permisos necesarios para acceder a esta funcionalidad.")

class Registrar(tk.Frame):
    def __init__(self, parent, controller, rol_usuario):
        super().__init__(parent)
        self.rol_usuario = rol_usuario
        usuario=recoger_sesion()
        self.usuario=usuario
        self.controller = controller
        self.config(bg="#FFFFFF")
        self.create_widgets()
         
    def validate_number_input(self,text):
        if text == "":
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False

    def create_widgets(self):
        self.images = {}  # Diccionario para almacenar las imagenes
        validate_number = self.register(self.validate_number_input)

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=768,
            width=1366,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Cargar y almacenar las imagenes
        self.images["image_1"] = tk.PhotoImage(file=relative_to_assets("main_relleno_lateral.png"))
        canvas.create_image(107.0, 412.0, image=self.images["image_1"])

        self.images["image_2"] = tk.PhotoImage(file=relative_to_assets("main_relleno_general.png"))
        canvas.create_image(789.0, 413.0, image=self.images["image_2"])

        self.images["image_3"] = tk.PhotoImage(file=relative_to_assets("header.png"))
        canvas.create_image(682.0, 29.0, image=self.images["image_3"])

        # Cargar y almacenar las imagenes
        self.images["button_volver"] = tk.PhotoImage(file=relative_to_assets("U_volver.png"))
        tk.Button(
            self,
            image=self.images["button_volver"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.open_seleccion(),
            activebackground="#E83030",
            relief="flat"
        ).place(x=1135.0, y=15.0, width=208.0, height=29.0)
        
        self.images["button_image_5"] = tk.PhotoImage(file=relative_to_assets("main_boton_registrar.png"))
        tk.Button(
            self,
            image=self.images["button_image_5"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: {self.hide_widgets(), self.controller.show_frame(Registrar)},
            relief="flat"
        ).place(x=1.0, y=57.0, width=213.0, height=58.0)

        self.images["button_image_2"] = tk.PhotoImage(file=relative_to_assets("main_boton_modificar.png"))
        tk.Button(
            self,
            image=self.images["button_image_2"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: {self.controller.show_frame(Modificar)},
            relief="flat"
        ).place(x=1.0, y=173.0, width=213.0, height=58.0)

        self.images["button_image_3"] = tk.PhotoImage(file=relative_to_assets("main_boton_listado.png"))
        tk.Button(
            self,
            image=self.images["button_image_3"],
            borderwidth=0,
            highlightthickness=0,
              command=lambda: { self.controller.destroy(), show_pokemons() },
            relief="flat"
        ).place(x=1.0, y=115.0, width=213.0, height=58.0)

        self.images["button_image_4"] = tk.PhotoImage(file=relative_to_assets("main_boton_eliminar.png"))
        tk.Button(
            self,
            image=self.images["button_image_4"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: {self.controller.show_frame(Eliminar)},
            relief="flat"
        ).place(x=1.0, y=231.0, width=213.0, height=58.0)
        
        #Formulario para el registro
        
        # Titulos de los inputs
        canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del libro a agregar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        #fila 1
        canvas.create_text(263.0, 152.0, anchor="nw", text="Formato", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(520.0, 152.0, anchor="nw", text="Sala", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(779.0, 152.0, anchor="nw", text="Genero", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 2
        canvas.create_text(263.0, 252.0, anchor="nw", text="Cota", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(520.0, 252.0, anchor="nw", text="Numero de registro", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(779.0, 252.0, anchor="nw", text="Edición", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(1036.0, 252.0, anchor="nw", text=" N° volumen", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 3
        canvas.create_text(263.0, 352.0, anchor="nw", text="Titulo", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(520.0, 352.0, anchor="nw", text="Autor", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(779.0, 352.0, anchor="nw", text="Editorial", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 4
        canvas.create_text(263.0, 452.0, anchor="nw", text="Año", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(520.0, 452.0, anchor="nw", text="Cantidad de ejemplares", fill="#000000", font=("Montserrat Regular", 15))
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        #primera fila
        
        
        """
        validate="key": Configura el widget para que valide la entrada cada vez que se presiona una tecla.
        validatecommand=(validate_number, "%P"): Define el comando de validación. validate_number es una función que se llamará para validar la entrada, y "%P" es un marcador de posición que representa el contenido del widget después de la edición.
        """
        
        self.cota = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.cota.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.altura = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.altura.place(x=520.0, y=282.0, width=237.0, height=38.0)
 
        self.entry1 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry1.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        self.entry2 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry2.place(x=1036.0, y=282.0, width=237.0, height=37.5)
        #segunda fila
        self.entry3 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.entry3.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.entry4 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.entry4.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        self.entry5 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.entry5.place(x=779.0, y=382.0, width=237.0, height=37.5)
        #tercera fila
        
        self.entry6 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry6.place(x=263.0, y=482.0, width=237.0, height=37.5)
        
        self.entry7 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry7.place(x=520.0, y=482.0, width=237.0, height=37.5)
        
        
        
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
        
        self.tipos_de_pokemones = ttk.Combobox(self, values=pokemon_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.tipos_de_pokemones.place(x=520.0, y=181.5)

        self.combobox3 = ttk.Combobox(self, values=pokemon_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.combobox3.place(x=779.0, y=181.5)
        
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
            command=lambda: self.add_pokemon(),
            relief="flat",
        ).place(x=265.0, y=635.0, width=130.0, height=40.0)
        
        canvas.create_text(
            226.0,
            5.0,
            anchor="nw",
            text="Registrar",
            fill="#000000",
            font=("Inter", 40 * -1)
        )
        canvas.create_text(
            26.0,
            9.0,
            anchor="nw",
            text=self.usuario,
            fill="#000000",
            font=("Inter", 18 * -1)
        )
        canvas.create_text(
            26.0,
            31.0,
            anchor="nw",
            text=self.rol_usuario,
            fill="#000000",
            font=("Inter", 14 * -1)
        )
        
     # Guarda el canvas para poder ocultarlo
        self.canvas = canvas
        
    def add_pokemon(self):
        nombre = self.nombre.get()
        peso = float(self.peso.get()) if self.peso.get() else 0
        altura = float(self.altura.get()) if self.altura.get() else 0
        sexo = self.pokemon_sex.get(self.tipos_de_sexo.get()) 
        descripcion = self.text_area.get("1.0", "end-1c")
        # Diccionario de tipos de Pokémon
        pokemon_types = {
            "Normal": 1, "Lucha": 2, "Volador": 3, "Veneno": 4, "Tierra": 5, "Roca": 6,
            "Bicho": 7, "Fantasma": 8, "Fuego": 9, "Agua": 10, "Planta": 11, "Electrico": 12,
            "Psiquico": 13, "Hielo": 14, "Dragón": 15
        }

        # Obtener el tipo seleccionado del combobox
        tipo_combobox = self.tipos_de_pokemones.get()
        print(tipo_combobox)
        # Obtener el valor numérico del tipo de Pokémon seleccionado
        tipo = pokemon_types.get(tipo_combobox, 0) 

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
        
        if create_pokemon(nombre, tipo, peso, altura, sexo, descripcion):
            #Limpia el formulario
            self.nombre.delete(0, 'end')
            self.tipos_de_pokemones.set('') 
            self.peso.delete(0, 'end')
            self.altura.delete(0, 'end')
            self.tipos_de_sexo.set('')
            self.text_area.delete("1.0", "end")
            messagebox.showinfo("Éxito", "Pokémon registrado exitosamente")
        else:
            messagebox.showerror("Error", "Error al registrar el Pokémon")
        
    def hide_widgets(self):
        self.button_registrar.place_forget()
        self.button_volver.place_forget()
        self.button_modificar.place_forget()
        self.button_listado.place_forget()
        self.button_eliminar.place_forget()
        self.input_nombre.place_forget()
        self.button_e.place_forget()
        self.canvas.itemconfigure(self.label_info, state='hidden')
        self.canvas.itemconfigure(self.label_nombre, state='hidden')
        self.canvas.itemconfigure(self.navbar_title, state='hidden')
        self.canvas.itemconfigure(self.navbar_subtitle_1, state='hidden')
        self.canvas.itemconfigure(self.navbar_subtitle_2, state='hidden')
        
    def open_seleccion(self):
        self.controller.destroy()  ##### Cierra solo la ventana  actual
        from Vistas.R_selection import selection
        selection().open()

class Eliminar(tk.Frame):
    def __init__(self, parent, controller, rol_usuario):
        super().__init__(parent)
        self.rol_usuario = rol_usuario
        self.controller = controller
        usuario=recoger_sesion()
        self.usuario=usuario
        self.config(bg="#FFFFFF")
        self.create_widgets()

    def create_widgets(self):
        self.images = {}  # Diccionario para almacenar las imágenes

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=768,
            width=1366,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Cargar y almacenar las imágenes de las esquinas
        self.images["image_1"] = tk.PhotoImage(file=relative_to_assets("main_relleno_lateral.png"))
        canvas.create_image(107.0, 412.0, image=self.images["image_1"])

        self.images["image_2"] = tk.PhotoImage(file=relative_to_assets("main_relleno_general.png"))
        canvas.create_image(789.0, 413.0, image=self.images["image_2"])

        self.images["image_3"] = tk.PhotoImage(file=relative_to_assets("header.png"))
        canvas.create_image(682.0, 29.0, image=self.images["image_3"])

        # Cargar y almacenar las imágenes de los botones

        self.images["button_image_1"] = tk.PhotoImage(file=relative_to_assets("U_volver.png"))
        self.button_volver = tk.Button(
            self,
            image=self.images["button_image_1"],
            borderwidth=0,
            command=lambda:self.open_seleccion(),
            activebackground="#E83030",
            highlightthickness=0,
            relief="flat"
        )
        self.button_volver.place(x=1135.0, y=15.0, width=208.0, height=29.0)
        
        self.images["button_image_5"] = tk.PhotoImage(file=relative_to_assets("main_boton_registrar.png"))
        self.button_registrar = tk.Button(
            self,
            image=self.images["button_image_5"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: {self.hide_widgets(), self.controller.show_frame(Registrar)},
            relief="flat"
        )
        self.button_registrar.place(x=1.0, y=57.0, width=213.0, height=58.0)

        self.images["button_image_2"] = tk.PhotoImage(file=relative_to_assets("main_boton_modificar.png"))
        self.button_modificar = tk.Button(
            self,
            image=self.images["button_image_2"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: {self.hide_widgets(), self.controller.show_frame(Modificar)},
            relief="flat"
        )
        self.button_modificar.place(x=1.0, y=173.0, width=213.0, height=58.0)

        self.images["button_image_3"] = tk.PhotoImage(file=relative_to_assets("main_boton_listado.png"))
        self.button_listado = tk.Button(
            self,
            image=self.images["button_image_3"],
            borderwidth=0,
            highlightthickness=0,
              command=lambda: { self.controller.destroy(), show_pokemons() },
            relief="flat"
        )
        self.button_listado.place(x=1.0, y=115.0, width=213.0, height=58.0)

        self.images["button_image_4"] = tk.PhotoImage(file=relative_to_assets("main_boton_eliminar.png"))
        self.button_eliminar = tk.Button(
            self,
            image=self.images["button_image_4"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: {self.controller.show_frame(Eliminar)},
            relief="flat"
        )
        self.button_eliminar.place(x=1.0, y=231.0, width=213.0, height=58.0)
        
        # Formulario para el eliminar
        self.label_info = canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del libro a Eliminar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        
        # Texto para el nombre
        self.label_nombre = canvas.create_text(263.0, 152.0, anchor="nw", text="ID", fill="#000000", font=("Montserrat Regular", 15))
        
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
            image=self.images['boton_Eliminar_f'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.Delete_Pokion(),
            relief="flat"
        )
        self.button_e.place(x=265.0, y=264.0, width=130.0, height=40.0)
        
        # Texto del navbar
        self.navbar_title = canvas.create_text(226.0, 5.0, anchor="nw", text="Eliminar", fill="#000000", font=("Inter", 40 * -1))
        self.navbar_subtitle_1 = canvas.create_text(26.0, 9.0, anchor="nw", text=self.usuario, fill="#000000", font=("Inter", 18 * -1))
        self.navbar_subtitle_2 = canvas.create_text(26.0, 31.0, anchor="nw", text=self.rol_usuario, fill="#000000", font=("Inter", 14 * -1))

        # Guarda el canvas para poder ocultarlo
        self.canvas = canvas
    
    def Delete_Pokion(self):
        name=self.input_nombre.get()

        if delete_pokemon(name):
            self.input_nombre.delete(0, 'end')
            messagebox.showinfo("Fracaso", "Pokemon Eliminado Exitosamente")
        else:
            messagebox.showinfo("Fracaso", "No se puede Eliminar el pokemon")


    def hide_widgets(self):
        self.button_registrar.place_forget()
        self.button_volver.place_forget()
        self.button_modificar.place_forget()
        self.button_listado.place_forget()
        self.button_eliminar.place_forget()
        self.input_nombre.place_forget()
        self.button_e.place_forget()
        self.canvas.itemconfigure(self.label_info, state='hidden')
        self.canvas.itemconfigure(self.label_nombre, state='hidden')
        self.canvas.itemconfigure(self.navbar_title, state='hidden')
        self.canvas.itemconfigure(self.navbar_subtitle_1, state='hidden')
        self.canvas.itemconfigure(self.navbar_subtitle_2, state='hidden')
        
    def open_seleccion(self):
        self.controller.destroy()  ##### Cierra solo la ventana  actual
        from Vistas.R_selection import selection
        selection().open() 


class Modificar(tk.Frame):
    def __init__(self, parent, controller, rol_usuario):
        self.rol_usuario = rol_usuario
        usuario=recoger_sesion()
        self.usuario=usuario
        super().__init__(parent)
        self.controller = controller
        self.config(bg="#FFFFFF")
        self.create_widgets()

    def validate_number_input(self,text):
        if text == "":
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False
    
    def create_widgets(self):
        self.images = {}  # Diccionario para almacenar las imagenes
        validate_number = self.register(self.validate_number_input)
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=768,
            width=1366,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)

        # Cargar y almacenar las imagenes
        self.images["image_1"] = tk.PhotoImage(file=relative_to_assets("main_relleno_lateral.png"))
        canvas.create_image(107.0, 412.0, image=self.images["image_1"])

        self.images["image_2"] = tk.PhotoImage(file=relative_to_assets("main_relleno_general.png"))
        canvas.create_image(789.0, 413.0, image=self.images["image_2"])

        self.images["image_3"] = tk.PhotoImage(file=relative_to_assets("header.png"))
        canvas.create_image(682.0, 29.0, image=self.images["image_3"])

        # Cargar y almacenar las imagenes
        self.images["button_volver"] = tk.PhotoImage(file=relative_to_assets("U_volver.png"))
        tk.Button(
            self,
            image=self.images["button_volver"],
            activebackground="#E83030",
            borderwidth=0,
            command=lambda:self.open_seleccion(),
            highlightthickness=0,
            relief="flat"
        ).place(x=1135.0, y=15.0, width=208.0, height=29.0)
        
        self.images["button_image_5"] = tk.PhotoImage(file=relative_to_assets("main_boton_registrar.png"))
        tk.Button(
            self,
            image=self.images["button_image_5"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: {self.controller.show_frame(Registrar)},
            relief="flat"
        ).place(x=1.0, y=57.0, width=213.0, height=58.0)

        self.images["button_image_2"] = tk.PhotoImage(file=relative_to_assets("main_boton_modificar.png"))
        tk.Button(
            self,
            image=self.images["button_image_2"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: {self.hide_widgets(), self.controller.show_frame(Modificar)},
            relief="flat"
        ).place(x=1.0, y=173.0, width=213.0, height=58.0)

        self.images["button_image_3"] = tk.PhotoImage(file=relative_to_assets("main_boton_listado.png"))
        tk.Button(
            self,
            image=self.images["button_image_3"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: { self.controller.destroy(), show_pokemons() },
            relief="flat"
        ).place(x=1.0, y=115.0, width=213.0, height=58.0)

        self.images["button_image_4"] = tk.PhotoImage(file=relative_to_assets("main_boton_eliminar.png"))
        tk.Button(
            self,
            image=self.images["button_image_4"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: {self.controller.show_frame(Eliminar)},
            relief="flat"
        ).place(x=1.0, y=231.0, width=213.0, height=58.0)
        
        # Titulos de los inputs
        canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del libro a modificar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        #fila 1
        canvas.create_text(263.0, 152.0, anchor="nw", text="Formato", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(520.0, 152.0, anchor="nw", text="Sala", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(779.0, 152.0, anchor="nw", text="Genero", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 2
        canvas.create_text(263.0, 252.0, anchor="nw", text="Cota", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(520.0, 252.0, anchor="nw", text="Numero de registro", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(779.0, 252.0, anchor="nw", text="Edición", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(1036.0, 252.0, anchor="nw", text=" N° volumen", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 3
        canvas.create_text(263.0, 352.0, anchor="nw", text="Titulo", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(520.0, 352.0, anchor="nw", text="Autor", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(779.0, 352.0, anchor="nw", text="Editorial", fill="#000000", font=("Montserrat Regular", 15))
        
        #fila 4
        canvas.create_text(263.0, 452.0, anchor="nw", text="Año", fill="#000000", font=("Montserrat Regular", 15))
        canvas.create_text(520.0, 452.0, anchor="nw", text="Cantidad de ejemplares", fill="#000000", font=("Montserrat Regular", 15))
        #fila 5
        canvas.create_text(263.0, 552.0, anchor="nw", text="ID", fill="#000000", font=("Montserrat Regular", 15))
        
        
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        #primera fila
        self.altura = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.altura.place(x=520.0, y=282.0, width=237.0, height=38.0)
 
        self.peso = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.peso.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.entry1 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry1.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        self.entry2 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry2.place(x=1036.0, y=282.0, width=237.0, height=37.5)
        #segunda fila
        self.entry3 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry3.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.entry4 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry4.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        self.entry5 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry5.place(x=779.0, y=382.0, width=237.0, height=37.5)
        #tercera fila
        
        self.entry6 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry6.place(x=263.0, y=482.0, width=237.0, height=37.5)
        
        self.entry7 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry7.place(x=520.0, y=482.0, width=237.0, height=37.5)
        
        #cuarta fila
        
        self.entry8 = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.entry8.place(x=263.0, y=582.0, width=237.0, height=37.5)
        
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
            command=lambda: self.mod_pokemon(),
            relief="flat",
        ).place(x=1163.0, y=635.0, width=130.0, height=40.0)
        
        canvas.create_text(
            226.0,
            5.0,
            anchor="nw",
            text="Modificar",
            fill="#000000",
            font=("Inter", 40 * -1)
        )
        canvas.create_text(
            26.0,
            9.0,
            anchor="nw",
            text=self.usuario,
            fill="#000000",
            font=("Inter", 18 * -1)
        )
        canvas.create_text(
            26.0,
            31.0,
            anchor="nw",
            text=self.rol_usuario,
            fill="#000000",
            font=("Inter", 14 * -1)
        )
        
     # Guarda el canvas para poder ocultarlo
        self.canvas = canvas
        
    def hide_widgets(self):
        self.button_registrar.place_forget()
        self.button_volver.place_forget()
        self.button_modificar.place_forget()
        self.button_listado.place_forget()
        self.button_eliminar.place_forget()
        self.input_nombre.place_forget()
        self.button_e.place_forget()
        self.canvas.itemconfigure(self.label_info, state='hidden')
        self.canvas.itemconfigure(self.label_nombre, state='hidden')
        self.canvas.itemconfigure(self.navbar_title, state='hidden')
        self.canvas.itemconfigure(self.navbar_subtitle_1, state='hidden')
        self.canvas.itemconfigure(self.navbar_subtitle_2, state='hidden')
    
    def open_seleccion(self):
        self.controller.destroy()  ##### Cierra solo la ventana  actual
        from Vistas.R_selection import selection
        selection().open() 

    def mod_pokemon(self):
        pokemon_types = {"Normal": 1, "Lucha": 2, "Volador": 3, "Veneno": 4, "Tierra": 5, "Roca": 6, "Bicho": 7, "Fantasma": 8, "Fuego": 9, "Agua": 10, "Planta": 11, "Electrico": 12, "Psiquico": 13, "Hielo": 14, "Dragon": 15}
        
        tipo_combobox = self.tipos_de_pokemones.get()
        tipo = 0
        for values in pokemon_types.keys():
            if values == tipo_combobox:
                tipo = pokemon_types[tipo_combobox]
        nombre = self.nombre.get().strip()
        peso = self.peso.get().strip()
        altura = self.altura.get().strip()
        sexo = self.tipos_de_sexo.get().strip()
        descripcion = self.text_area.get("1.0", "end-1c").strip()

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

        # Intentar actualizar el Pokémon
        if update_pokemon(nombre, tipo, peso, altura, sexo, descripcion):
            # Limpiar el formulario
            self.nombre.delete(0, 'end')
            self.tipos_de_pokemones.set('')
            self.peso.delete(0, 'end')
            self.altura.delete(0, 'end')
            self.tipos_de_sexo.set('')
            self.text_area.delete("1.0", "end")
            messagebox.showinfo("Éxito", "Pokémon actualizado exitosamente.")
        else:
            messagebox.showerror("Error", "Error al actualizar el Pokémon.")

class Listado(tk.Frame):
    pass
       
# Crear y ejecutar la aplicación
if __name__ == "__main__":
    app = Balls()
    app.mainloop()
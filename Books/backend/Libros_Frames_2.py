import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import font
#from Library.librerias import recoger_sesion, drop_sesion
from Books.backend.db_books import *
from PIL import Image,ImageTk
from Vistas.listas import *
import random
from db.conexion import establecer_conexion
from validations.books_validations import *

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

class L_Registrar(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FFFFFF", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        
        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del libro a agregar", fill="#a6a6a6", font=("Bold", 17))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Sala", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(520.0, 152.0, anchor="nw", text="Categoria", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(779.0, 152.0, anchor="nw", text="Asignatura", fill="#031A33", font=("Bold", 17))
        
        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Cota", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Numero de registro", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(779.0, 252.0, anchor="nw", text="Edición", fill="#031A33", font=("MBold", 17))
        self.canvas.create_text(1036.0, 252.0, anchor="nw", text=" N° volumen", fill="#031A33", font=("Bold", 17))
        
        #fila 3
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Titulo", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Autor", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(779.0, 352.0, anchor="nw", text="Editorial", fill="#031A33", font=("Bold", 17))
        
        #fila 4
        self.canvas.create_text(263.0, 452.0, anchor="nw", text="Año", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(520.0, 452.0, anchor="nw", text="Cantidad de ejemplares", fill="#031A33", font=("Bold", 17))
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        #primera fila
        

        """
        validate="key": Configura el widget para que valide la entrada cada vez que se presiona una tecla.
        validatecommand=(validate_number, "%P"): Define el comando de validación. validate_number es una función que se llamará para validar la entrada, y "%P" es un marcador de posición que representa el contenido del widget después de la edición.
        """
        
        self.cota = tk.Entry(self, bd=0, bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="solid" , borderwidth=0.5)
        self.cota.place(x=263.0, y=282.0, width=237.0, height=37.5)
        self.message_shown = False  # Definir la variable de control en el __init__
        self.registro= tk.Entry(self, bd=0, bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.registro.place(x=520.0, y=282.0, width=237.0, height=38.0)
        self.registro.bind("<FocusIn>", self.show_message)
 
        self.edicion = tk.Entry(self, bd=0, bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.edicion.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        self.volumen = tk.Entry(self, bd=0,bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.volumen.place(x=1036.0, y=282.0, width=237.0, height=37.5)
        #segunda fila
        self.titulo = tk.Entry(self, bd=0, bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.titulo.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.autor = tk.Entry(self, bd=0,bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.autor.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        self.editorial = tk.Entry(self, bd=0, bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.editorial.place(x=779.0, y=382.0, width=237.0, height=37.5)
        #tercera fila
        
        self.año = tk.Entry(self, bd=0, bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.año.place(x=263.0, y=482.0, width=237.0, height=37.5)
        
        self.ejemplares = tk.Entry(self, bd=0, bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.ejemplares.place(x=520.0, y=482.0, width=237.0, height=37.5)
        
        self.salas_types = [
        "3G" or "3g", "2E", "1I"
        ]
        self.categoria_types_general=["Ciencias de la Computación, Información y Obras Generales", "Filosofía y Psicología", "Religión-Teología", "Ciencias Sociales","Lenguas",
        "Ciencias Básicas","Tecnología y Ciencias Aplicadas","Artes y recreación","Literatura","Historia y Geografía"]
                
        self.asignature_type_general= ["Almanaques Mundiales","Computacion","Enciclopedia","Enciclopedia y Diccionarios","Filosofía","Filosofía-Diccionarios",
        "Informática","Metodología de la Investigación","Periodismo","Psicología","Psicología-Diccioanrios","Religión",
        "Educación Familiar y Ciudadana","Sociología","Medios de Comunicación","Mujer y Familia","Estadística Social",
        "Ciencias Políticas", "Economía Venezolana","Geografía Económica","Microeconomía","Macroeconomía","Derecho",
        "Derecho Constitucional","Derecho Laboral","Derecho Penal","Límites y Fronteras","Administración Pública","Premilitar","Servicios Sociales", "Filosofía de la Educación","Educación","Educación Rural","Pedagogía","Técnicas de Estudio",
        "Orientación", "Educación Preescolar","Educación Superior","Medios de Transporte","Currículo","Educación Básica","Publicaciones Oficiales-Folklore","Lenguaje",
        "Linguística-Diccionarios","Lengua y Comunicación","Castellano y Literatura","Inglés","Castellano","Química-Física-Diccionarios",
        "Botánica-Zoología-Diccionarios","Matemática","Ciencia","Estudios de la Naturaleza", "Álgebra","Matemática Financiera",
        "Cálculo","Geometría","Astronomía","Física","Electricidad","Electrónica", "Química","Fisioquímica","Química Orgánica",
        "Ciencias de la Tierra","Biología","Medicina-Diccionarios","Agricultura-Diccionarios","Biología Celular","Zoología",
        "Ecología","Bioquímica","Enfermería","Anatomía Humana","Contaminación Ambiental","Seguridad Industrial","Naturismo","Drogar",
        "Enfermedades Varias","Pediatría","Ingeniería","Reciclaje","Agricultura","Fertilizantes","Cultivos","Fruticultura","Ganadería",
        "Comercio","Contabilidad","Administración","Administración de Emperesa","Avicultura","Nutrición","Ganadería","Zootecnia",
        "Administración de Personal","Mercadotecnia","Historial del Arte","Dibujo","Arte y Recreación-Diccionarios","Artística",
        "Artes Plásticas y Escultura","Pintura","Música","Educación Física","Deportes","Literatura-Diccioanrios","Literatura",
        "Novelas","Novelas Venezolanas","Poesías","Historia Universal","Geografía General","Geografía de Venezuela",
        "Historia","Historia de América","Historia Europea","Historia-Diccionarios"]

        self.categoria_types_state=["Estadal-B"]

        self.asignature_types_state= ["Bibliografia-Estadal","Historia Local-Rubio-Junin","Publicaciones Periódicas"]

        self.categoria_types_children=["Infantil-X"]
        
        self.asignature_types_children= ["Matemáticas","Castellano y Literatura","Ciencias Naturales","Petróleo","Agricultura","Cuentos Venezolanos",
        "Fábulas","Novelas Históricas","Sección de los más pequeños","Cuentos de Animales","Novelas de Aventuras",
        "Cuentos de Hadas y Fantasía","Cuentos Realistas","Poesías y Canciones Venezolanas","Cuentos de Aventuras",
        "Teatro","Teatro Venezolano","Fábulas Venezolanas","Mitos y Leyendas Venezolanas"]


        #Select tipo de campo
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                        fieldbackground="#2E59A7",  # Fondo del campo de entrada
                        background="#2E59A7",  # Fondo del desplegable
                        bordercolor="#041022",  # Color del borde
                        arrowcolor="#ffffff",  # Color de la flecha
                        padding= "9",
                        ) # padding para agrandar la altura del select
        #Sala
        self.combobox1=ttk.Combobox(self, values=self.salas_types, state="readonly", width=30, font=("Bold", 10), style="TCombobox")
        self.combobox1.place(x=263.0, y=181.5)
        self.combobox1.bind("<<ComboboxSelected>>",self.validacion_sala)
        self.menu_actual = None

    def validacion_sala(self,event):
            #Select tipo de campo
            stylebox = ttk.Style()
            stylebox.theme_use('clam')
            stylebox.configure("TCombobox",
                            fieldbackground="#2E59A7",  # Fondo del campo de entrada
                            background="#2E59A7",  # Fondo del desplegable
                            bordercolor="#041022",  # Color del borde
                            arrowcolor="#ffffff",  # Color de la flecha
                            padding= "9",
                            ) # padding para agrandar la altura del select
            validacion_salas=self.combobox1.get()
            if self.menu_actual:
                self.menu_actual.destroy()
            if validacion_salas=="3G" or "3g":
            # Categoria-Sala General
                self.menu_actual = ttk.Combobox(self, values=self.categoria_types_general, state="readonly", width=30, font=("Montserrat Medium", 10), style="TCombobox")
                self.menu_actual.place(x=520.0, y=181.5)
            # Asignatura-Sala General
                self.combobox3 = ttk.Combobox(self, values=self.asignature_type_general, state="readonly", width=30, font=("Montserrat Medium", 10), style="TCombobox")
                self.combobox3.place(x=779.0, y=181.5)
            elif validacion_salas=="2E":
            # Categoria-Sala Estadal
                self.menu_actual = ttk.Combobox(self, values=self.categoria_types_state, state="readonly", width=30, font=("Montserrat Medium", 10), style="TCombobox")
                self.menu_actual.place(x=520.0, y=181.5)
            # Asignatura-Sala Estadal
                self.combobox3 = ttk.Combobox(self, values=self.asignature_types_state, state="readonly", width=30, font=("Montserrat Medium", 10), style="TCombobox")
                self.combobox3.place(x=779.0, y=181.5)
            elif validacion_salas=="1I":
            # Categoria-Sala Infantil
                self.menu_actual = ttk.Combobox(self, values=self.categoria_types_children, state="readonly", width=30, font=("Montserrat Medium", 10), style="TCombobox")
                self.menu_actual.place(x=520.0, y=181.5)
            # Asignatura-Sala Infantil
                self.combobox3 = ttk.Combobox(self, values=self.asignature_types_children, state="readonly", width=30, font=("Montserrat Medium", 10), style="TCombobox")
                self.combobox3.place(x=779.0, y=181.5)                 
            else:
                messagebox.showwarning("Validación", "Por favor, seleccione una opción.")
            
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
                command=lambda: register_book(),
                relief="flat",
                bg="#FFFFFF",
                activebackground="#FFFFFF",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"  # Color del texto cuando el botón está activo
            ).place(x=265.0, y=635.0, width=130.0, height=40.0)
        
            def register_book():
                    ID_Sala= self.combobox1.get() #self.cota.get()
                    ID_Categoria = self.menu_actual.get() if self.menu_actual else None #self.combobox1.get()
                    ID_Asignatura = self.combobox3.get() if self.combobox3 else None #self.menu_actual.get() if self.menu_actual else None
                    Cota= self.cota.get() #self.combobox3.get() if self.combobox3 else None
                    n_registro=self.registro.get()
                    edicion=self.edicion.get()
                    n_volumenes=self.volumen.get()
                    titulo=self.titulo.get()
                    autor=self.autor.get()
                    editorial=self.editorial.get()
                    año=self.año.get()
                    n_ejemplares=self.ejemplares.get()
                    if create_books(ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares):
                        messagebox.showinfo("Éxito", "Registro del libro éxitoso.")
                        self.clear_entries_register()
                    else:
                        messagebox.showinfo("Registro fallido", "Libro mantiene sus valores.")

    def clear_entries_register(self):
        self.combobox1.delete(0, tk.END)
        #self.menu_actual.delete(0, tk.END)
        self.combobox3.delete(0, tk.END)
        self.cota.delete(0, tk.END)
        self.registro.delete(0, tk.END)
        self.edicion.delete(0, tk.END)
        self.volumen.delete(0, tk.END)
        self.titulo.delete(0, tk.END)
        self.autor.delete(0, tk.END)
        self.editorial.delete(0, tk.END)
        self.año.delete(0, tk.END)
        self.ejemplares.delete(0, tk.END)
    
    def show_message(self, event):
        if not self.message_shown:
            messagebox.showinfo("Información", "En caso de ser varios ejemplares seguidos, puede digitar los datos de la siguiente forma: 11.498-11.500")
            self.message_shown = True  # Marcar que el mensaje ya se mostró

def contar_ejemplares(libros):
    ejemplares_dict = {}
    for libro in libros:
        key = (libro[1], libro[2], libro[3], libro[4], libro[5], libro[6], libro[7], libro[8], libro[9], libro[10], libro[11], libro[12], libro[13])
        if key in ejemplares_dict:
            ejemplares_dict[key]['total'] += 1
            if libro[14] == 'Sí':  # Suponiendo que el estado de préstamo está en la posición 14
                ejemplares_dict[key]['prestamo'] += 1
        else:
            ejemplares_dict[key] = {'total': 1, 'prestamo': 1 if libro[14] == 'Sí' else 0}
    return ejemplares_dict

class L_Listar(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="right", fill="both", expand=True)
        self.images = {}

        # Crear el marco izquierdo para el menú de navegación
        self.left_frame_list = tk.Frame(self.canvas, bg="#FFFFFF")
        self.left_frame_list.place(x=200, y=205, height=450, width=1180)
        
        self.label_nombre = self.canvas.create_text(265.0, 100.0, anchor="nw", text="Buscar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1110.0, 170.0, text="Editar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1240.0, 170.0, text="Eliminar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(980.0, 170.0, text="Refrescar", fill="#031A33", font=("Bold", 17))

        stylebotn = ttk.Style()
        stylebotn.configure("Rounded.TEntry", 
                            fieldbackground="#031A33", 
                            foreground="#a6a6a6", 
                            borderwidth=0.5, 
                            relief="solid", 
                            padding=5)
        stylebotn.map("Rounded.TEntry",
                      focuscolor=[('focus', '#FFFFFF')],
                      bordercolor=[('focus', '#000716')])

        self.left_frame_list = tk.Frame(self.canvas, bg="#FAFAFA")
        self.left_frame_list.pack(expand=True, side="left", fill="both") #padx=212, pady=150, ipady=80
        self.left_frame_list.place(x=215,y=205, height=480, width=1150)

        # Títulos para los Treeviews
        bold_font = font.Font(family="Bold", size=15, weight="bold")
        self.label_usuarios = tk.Label(self.canvas, text="Tabla Libros", bg="#FAFAFA", fg="#031A33", font=bold_font)
        self.label_usuarios.place(x=660.0, y=170.0, width=225.0, height=38.0)


        """"self.cota = tk.Entry(self, bd=0, bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="solid" , borderwidth=0.5)
        self.cota.place(x=263.0, y=282.0, width=237.0, height=37.5)"""
        
        self.buscar = tk.Entry(self, bg="#FAFAFA", fg="#031A33", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.buscar.place(x=265.0, y=130.0, width=267.0, height=48.0)

        # Cargar y almacenar la imagen del botón
        self.images['boton_refrescar'] = tk.PhotoImage(file=relative_to_assets("16.png"))

# Definir button_e antes de usarlo
        self.button_e = tk.Button(
        self,
        image=self.images['boton_refrescar'],
        borderwidth=0,
        highlightthickness=0,
        command=lambda: self.reading_books(self.book_table_list),
        relief="flat",
        bg="#031A33",
        activebackground="#031A33",  # Mismo color que el fondo del botón
        activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=935.0, y=60.0, width=90.0, height=100.0)

        # Crear textos en el canvas
        self.label_nombre = self.canvas.create_text(265.0, 100.0, anchor="nw", text="Buscar", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1110.0, 170.0, text="Editar", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1240.0, 170.0, text="Eliminar", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(980.0, 170.0, text="Refrescar", fill="#a6a6a6", font=("Bold", 17))

        self.label_nombre = self.canvas.create_text(265.0, 100.0, anchor="nw", text="Buscar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1110.0, 170.0, text="Editar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1240.0, 170.0, text="Eliminar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(980.0, 170.0, text="Refrescar", fill="#040F21", font=("Bold", 17))
        # Para llamar a read_books cuando se presiona Enter
        self.buscar.bind("<Return>", self.boton_buscar)
        
                    #Boton Cargar Libros
            # Cargar y almacenar las imágenes
        self.images['boton_refrescar'] = tk.PhotoImage(file=relative_to_assets("16.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_refrescar'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.reading_books(self.book_table_list),
                relief="flat",
                bg="#FFFFFF",
                activebackground="#FFFFFF",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=935.0, y=60.0, width=90.0, height=100.0)

        

        self.images['boton_Eliminar'] = tk.PhotoImage(file=relative_to_assets("7_eliminar.png"))
                    # Cargar y almacenar la imagen del botón
        self.button_dl = tk.Button(
            self,
            image=self.images['boton_Eliminar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: delete_selected(self),
            relief="flat",
            bg="#FFFFFF",
            activebackground="#FFFFFF",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_dl.place(x=1195.0, y=60.0, width=90.0, height=100.0)

        self.images['boton_modificar'] = tk.PhotoImage(file=relative_to_assets("6_editar.png"))
            # Cargar y almacenar la imagen del botón
        self.button_dl = tk.Button(
            self,
            image=self.images['boton_modificar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_modificar_window(),
            relief="flat",
            bg="#FFFFFF",
            activebackground="#FFFFFF",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_dl.place(x=1065.0, y=60.0, width=90.0, height=100.0)
    
#ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, titulo, autor, editorial, año, edicion
            # Tabla de libros usando Treeview
        # Configurar estilo para Treeview
        style = ttk.Style()
        style.configure("Rounded.Treeview", 
                        borderwidth=2, 
                        relief="groove", 
                        bordercolor="blue", 
                        lightcolor="lightblue", 
                        darkcolor="darkblue",
                        rowheight=30,
                        background="#FFFFFF", 
                        fieldbackground="#f0f0f0")

        # Configurar estilo para las cabeceras
        style.configure("Rounded.Treeview.Heading", 
                        font=('Helvetica', 10, 'bold'), 
                        background="#2E59A7", 
                        foreground="#000000",
                        borderwidth=0)


        # Aplica el estilo al Treeview listado de libros
        tree = ("ID", "Sala", "Categoria", "Asignatura", "Cota", "N. Registro", "Título", "Autor", "Editorial", "Año", "Edición", "N° Ejemplares", "N° Volúmenes")
        self.book_table_list = ttk.Treeview(self.left_frame_list, columns=tree, show='headings', style="Rounded.Treeview")

        # Set specific widths for "ID" and "Sala"
        self.book_table_list.column("ID", width=50, anchor="center")
        self.book_table_list.column("Sala", width=50, anchor="center")

        # Set larger widths for the other columns
        for col in tree:
            if col not in ("ID", "Sala"):
                self.book_table_list.column(col, width=85, anchor="center")
            self.book_table_list.heading(col, text=col)

        # self.toggle_button = tk.Button(self.left_frame_list, text="Toggle Copies", command=self.toggle_copies)
        # self.toggle_button.pack(side=tk.BOTTOM, pady=10)

        self.book_table_list.pack(expand=True, fill="both", padx=30, pady=5)

        scrollbar_pt = ttk.Scrollbar(self.book_table_list, orient="vertical", command=self.book_table_list.yview)
        self.book_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")

        # #Aplicar el estilo al Treeview listado de Ejemplares-Condición Libros
        # detail_columns = ("N° Ejemplares", "N° Registro", "N° Edición", "Condición Préstamo")
        # self.detail_table_list = ttk.Treeview(self.right_frame_detail, columns=detail_columns, show='headings', style="Rounded.Treeview")

        # for col in detail_columns:
        #         self.detail_table_list.column(col, width=80, anchor="center")
        #         self.detail_table_list.heading(col, text=col)

        # self.detail_table_list.pack(expand=True, fill="both", padx=30, pady=5)

        #     # Bind the selection event
        # self.book_table_list.bind("<<TreeviewSelect>>", self.on_book_select)
        

    def open_modificar_window(self):
        selected_items = self.book_table_list.selection()
        if selected_items:
            selected_item = selected_items[0]
            item_values = self.book_table_list.item(selected_item, "values")
            L_Modificar(self.parent, item_values)
        else:
            print("No hay ningún elemento seleccionado.")

    def boton_buscar(self, event):
        busqueda= self.buscar.get()
        try:
             mariadb_conexion = establecer_conexion()
             if mariadb_conexion:#.is_connected():
                        cursor = mariadb_conexion.cursor()
                        cursor.execute("""SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota,
                                        n_registro, titulo, autor, editorial, año, edicion FROM libro WHERE 
                                        ID_Libro=%s OR ID_Sala=%s OR ID_Categoria=%s OR 
                                        ID_Asignatura=%s OR Cota=%s OR n_registro=%s OR 
                                        titulo=%s OR autor=%s OR editorial=%s OR 
                                        año=%s OR edicion=%s""", 
                           (busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda))
                        resultados = cursor.fetchall() 

                        self.book_table_list.delete(*self.book_table_list.get_children())
                        for fila in resultados:
                            self.book_table_list.insert("", "end", values=tuple(fila))
                            if busqueda in fila:
                                self.book_table_list.item(self.book_table_list.get_children()[-1], tags='match')
                            else:
                                self.book_table_list.item(self.book_table_list.get_children()[-1], tags='nomatch')
                        self.book_table_list.tag_configure('match', background='green')
                        self.book_table_list.tag_configure('nomatch', background='gray')
                        if resultados:
                            messagebox.showinfo("Busqueda Éxitosa", "Resultados en pantalla.")
                        else:
                            messagebox.showinfo("Busqueda Fallida", "No se encontraron resultados.")
        except mariadb.Error as ex:
                print("Error durante la conexión:", ex)
  
    def open_filter_window(self,parent):
        filter_window = tk.Toplevel(self)
        filter_window.title("Filtrar")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))

        self.bg_image = tk.PhotoImage(file=relative_to_assets("Fondo Botones V1.png"))
        # Crear un Label para la imagen de fondo
        bg_label = tk.Label(filter_window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(filter_window, text="Sala", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=0, column=0, padx=10, pady=5)
        self.sala_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.sala_entry.pack(expand=False)

        tk.Label(filter_window, text="Categoria", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=0, column=2, padx=10, pady=5)
        self.categoria_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.categoria_entry.pack(expand=False)

        tk.Label(filter_window, text="Asignatura", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=0, column=4, padx=10, pady=5)
        self.asignatura_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.asignatura_entry.pack(expand=False)

        tk.Label(filter_window, text="Cota", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=0, column=6, padx=10, pady=5)
        self.cota_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.cota_entry.pack(expand=False)

        tk.Label(filter_window, text="Autor", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=1, column=0, padx=10, pady=5)
        self.autor_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.autor_entry.pack(expand=False)

        tk.Label(filter_window, text="Titulo", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=1, column=2, padx=10, pady=5)
        self.titulo_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.titulo_entry.pack(expand=False)

        tk.Label(filter_window, text="N° Registro", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=1, column=4, padx=10, pady=5)
        self.n_registro_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.n_registro_entry.pack(expand=False)

        tk.Label(filter_window, text="Año", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=2, column=0, padx=10, pady=5)
        self.año_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.año_entry.pack(expand=False)

        tk.Label(filter_window, text="Edicion", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=2, column=2, padx=10, pady=5)
        self.edicion_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.edicion_entry.pack(expand=False)

        tk.Label(filter_window, text="Editorial", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=2, column=4, padx=10, pady=5)
        self.editorial_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.editorial_entry.pack(expand=False)
        
        # Crear un estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TButton", background="#f80000", foreground="black")

        search_button = ttk.Button(filter_window, text="Buscar", command=self.filter_books, style="Custom.TButton")
        search_button.pack(pady=5, expand=False)

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.pack(pady=5, expand=False)

        # Vincular el evento de escritura
        self.n_registro_entry.bind("<KeyRelease>", lambda event: self.format_n_registro(event))

    def format_n_registro(self, event):
        # Obtener el texto actual del campo de entrada
        text = self.n_registro_entry.get().replace(".", "")
        
        # Formatear el texto para insertar un punto después de las tres primeras cifras
        if len(text)> 1:
            formatted_text = text[:1] + "." + text[1:]
        else:
            formatted_text = text

        # Actualizar el campo de entrada con el texto formateado
        self.n_registro_entry.delete(0, tk.END)
        self.n_registro_entry.insert(0, formatted_text)

    def filter_books(self):
        sala = self.sala_entry.get().lower() or self.sala_entry.get().upper()
        categoria = self.categoria_entry.get().lower() or self.sala_entry.get().upper()
        asignatura = self.asignatura_entry.get().lower() or self.sala_entry.get().upper()
        cota = self.cota_entry.get().lower() or self.sala_entry.get().upper()
        autor = self.autor_entry.get().lower() or self.sala_entry.get().upper()
        titulo = self.titulo_entry.get().lower() or self.sala_entry.get().upper()
        n_registro = self.n_registro_entry.get().lower() or self.sala_entry.get().upper()
        año = self.año_entry.get().lower() or self.sala_entry.get().upper()
        edicion = self.edicion_entry.get().lower() or self.sala_entry.get().upper()
        editorial = self.editorial_entry.get().lower() or self.sala_entry.get().upper()
        self.salas_types = [
        "3G", "2E", "1I","3g","2e","1i"
        ]
        for row in self.book_table_list.get_children():
            values = self.book_table_list.item(row, "values")
              # Convertir los valores a enteros si es posible, de lo contrario mantenerlos como cadenas
            converted_values = []
            for value in values:
                try:
                    converted_values.append(int(value))
                except ValueError:
                    converted_values.append(value)
            values = [str(value) for value in values]
            if (sala in self.salas_types and
                categoria in values[2].lower() and values[2].upper() and
                asignatura in values[3].lower() and values[3].upper() and
                cota in values[4].lower() and values[4].upper() and
                autor in values[7].lower() and values[7].upper() and
                titulo in values[6].lower() and values[6].upper() and
                n_registro in values[5].lower() and values[5].upper() and
                año in values[9].lower() and values[9].upper() and
                edicion in values[10].lower() and values[10].upper() and
                editorial in values[8].lower() and values[8].upper()):
                self.book_table_list.item(row, tags='match')
            else:
                self.book_table_list.item(row, tags='nomatch')

        self.book_table_list.tag_configure('match', background='green')
        self.book_table_list.tag_configure('nomatch', background='gray')
    
    def reading_books(self,book_table_list):
                            try:
                                mariadb_conexion = establecer_conexion()
                                if mariadb_conexion:#.is_connected():
                                    cursor = mariadb_conexion.cursor()
                                    cursor.execute('SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, titulo, autor, editorial, año, edicion, n_ejemplares, n_volumenes FROM libro')
                                    resultados = cursor.fetchall() 
                                    for row in book_table_list.get_children():
                                        book_table_list.delete(row)
                                         # Configurar las etiquetas para los colores
                                    book_table_list.tag_configure('multiple', background='lightblue')
                                    book_table_list.tag_configure('single', background='#E5E1D7')
                                        
                                        # Insertar los datos en el Treeview
                                    for fila in resultados:
                                        book_id = fila[0]
                                        n_ejemplares = fila[11]
                                        tag = 'multiple' if n_ejemplares > 1 else 'single'
                                        parent = book_table_list.insert("", "end", values=tuple(fila), tags=(tag,))
                                        # # Create and place the button
                                        # button = tk.Button(self.book_table_list, text="Toggle Copies", command=lambda p=parent: self.toggle_copies(p))
                                        # button.grid(row=0, column=0)
                                                            
                                        if n_ejemplares > 1:
                                            for i in range(1, n_ejemplares + 1):
                                                # book_table_list.insert(parent, "end", text=f"Ejemplar {i}", values=("", "", "", "", "", "", "", "", "", "", "", "", ""), tags=('single',))
                                                book_table_list.insert(parent, "end", text=f"Ejemplar {i}", values=tuple(fila), tags=('single',))
                                    mariadb_conexion.close()
                            except mariadb.Error as ex:
                                    print("Error durante la conexión:", ex)
                            except subprocess.CalledProcessError as e:
                                print("Error al importar el archivo SQL:", e)

    def cancelar(self, window):
        window.destroy()  # Esto cerrará la ventana de filtro

class L_Modificar(tk.Toplevel):      
    def __init__(self,book_data, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.title("Modificar")
        self.book_data = book_data
        self.grab_set()
        self.geometry("1366x768")
    
        
        self.images = {}
        self.crear_boton_modificar()
        
        self.salas_types = ["1I", "2E", "3G"]
        self.categoria_types_general=["Ciencias de la Computación, Información y Obras Generales", "Filosofía y Psicología", "Religión-Teología", "Ciencias Sociales","Lenguas",
        "Ciencias Básicas","Tecnología y Ciencias Aplicadas","Artes y recreación","Literatura","Historia y Geografía"]
        self.asignature_type_general= ["Almanaques Mundiales","Computacion","Enciclopedia","Enciclopedia y Diccionarios","Filosofía","Filosofía-Diccionarios",
        "Informática","Metodología de la Investigación","Periodismo","Psicología","Psicología-Diccioanrios","Religión",
        "Educación Familiar y Ciudadana","Sociología","Medios de Comunicación","Mujer y Familia","Estadística Social",
        "Ciencias Políticas", "Economía Venezolana","Geografía Económica","Microeconomía","Macroeconomía","Derecho",
        "Derecho Constitucional","Derecho Laboral","Derecho Penal","Límites y Fronteras","Administración Pública","Premilitar",                                  "Servicios Sociales", "Filosofía de la Educación","Educación","Educación Rural","Pedagogía","Técnicas de Estudio",
        "Orientación", "Educación Preescolar","Educación Superior","Medios de Transporte","Currículo","Educación Básica",                                  "Publicaciones Oficiales-Folklore","Lenguaje","Linguística-Diccionarios","Lengua y Comunicación","Castellano y Literatura",
        "Inglés","Castellano","Química-Física-Diccionarios","Botánica-Zoología-Diccionarios","Matemática","Ciencia",
        "Estudios de la Naturaleza", "Álgebra","Matemática Financiera","Cálculo","Geometría","Astronomía","Física","Electricidad",
        "Electrónica", "Química","Fisioquímica","Química Orgánica","Ciencias de la Tierra","Biología","Medicina-Diccionarios",
        "Agricultura-Diccionarios","Biología Celular","Zoología","Ecología","Bioquímica","Enfermería","Anatomía Humana",
        "Contaminación Ambiental","Seguridad Industrial","Naturismo","Drogar","Enfermedades Varias","Pediatría","Ingeniería","Reciclaje",
        "Agricultura","Fertilizantes","Cultivos","Fruticultura","Ganadería","Comercio","Contabilidad","Administración",
        "Administración de Emperesa","Avicultura","Nutrición","Ganadería","Zootecnia","Administración de Personal","Mercadotecnia",
        "Historial del Arte","Dibujo","Arte y Recreación-Diccionarios","Artística","Artes Plásticas y Escultura","Pintura","Música",
        "Educación Física","Deportes","Literatura-Diccioanrios","Literatura","Novelas","Novelas Venezolanas","Poesías","Historia Universal",
        "Geografía General","Geografía de Venezuela","Historia","Historia de América","Historia Europea","Historia-Diccionarios"]
        self.categoria_types_state=["Estadal-B"]
        self.asignature_types_state= ["Bibliografia-Estadal","Historia Local-Rubio-Junin","Publicaciones Periódicas"]
        self.categoria_types_children=["Infantil-X"]
        self.asignature_types_children= ["Matemáticas","Castellano y Literatura","Ciencias Naturales","Petróleo","Agricultura","Cuentos Venezolanos",
        "Fábulas","Novelas Históricas","Sección de los más pequeños","Cuentos de Animales","Novelas de Aventuras",
        "Cuentos de Hadas y Fantasía","Cuentos Realistas","Poesías y Canciones Venezolanas","Cuentos de Aventuras",
        "Teatro","Teatro Venezolano","Fábulas Venezolanas","Mitos y Leyendas Venezolanas"]
        
        # Convertir book_data en un diccionario manteniendo los índices originales
        self.book_data = {
            "ID": book_data[0],
            "ID_Sala": book_data[1],
            "ID_Categoria": book_data[2],
            "ID_Asignatura": book_data[3],
            "Cota": book_data[4],
            "n_registro": book_data[5],
            "Titulo": book_data[6],
            "Autor": book_data[7],
            "Editorial": book_data[8],
            "Año": book_data[9],
            "Edicion": book_data[10],
            "Volumen": book_data[12],  # Repetido intencionalmente
            "Ejemplares": book_data[12]  # Repetido intencionalmente
        }
        
        self.original_values = self.book_data.copy()  # Copia el diccionario

        # Imprimir los datos recibidos
        print("Datos del libro seleccionados:")
        print(f"ID: {book_data[0]}")
        print(f"Sala: {book_data[1]}")
        print(f"Categoria: {book_data[2]}")
        print(f"Asignatura: {book_data[3]}")
        print(f"Cota: {book_data[4]}")
        print(f"Registro: {book_data[5]}")
        print(f"Edición: {book_data[10]}")
        print(f"Volumen: {book_data[10]}")
        print(f"Título: {book_data[6]}")
        print(f"Autor: {book_data[7]}")
        print(f"Editorial: {book_data[8]}")
        print(f"Año: {book_data[9]}")
        print(f"Ejemplares: {book_data[10]}")

        self.canvas = tk.Canvas(self, bg="#031A33", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        
        
        self.inicializar_titulos()
        self.inicializar_campos_y_widgets()
        self.menu_actual = None
        
        
      
        # Validar y actualizar comboboxes basados en los datos iniciales
        self.validacion_sala(None)
        self.crear_boton_modificar()

    
    def inicializar_titulos(self):
        # Títulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text=f"Modificación del libro con el ID:{self.book_data['ID']}", fill="#a6a6a6", font=("Bold", 17))
        
        # Fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Sala", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 152.0, anchor="nw", text="Categoría", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(779.0, 152.0, anchor="nw", text="Asignatura", fill="#a6a6a6", font=("Bold", 17))
        
        # Fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Cota", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Número de registro", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(779.0, 252.0, anchor="nw", text="Edición", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1036.0, 252.0, anchor="nw", text="N° volumen", fill="#a6a6a6", font=("Bold", 17))
        
        # Fila 3
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Título", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Autor", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(779.0, 352.0, anchor="nw", text="Editorial", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1036.0, 352.0, anchor="nw", text="Año", fill="#a6a6a6", font=("Bold", 17))

        
    
        
    def inicializar_campos_y_widgets(self):
        validate_number = self.register(validate_number_input)
        # Configuración del estilo de los Combobox
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                            fieldbackground="#2E59A7",
                            background="#2E59A7",
                            bordercolor="#041022",
                            arrowcolor="#ffffff",
                            padding="9")

        # Combobox para Sala
        self.combobox1 = ttk.Combobox(self, values=self.salas_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.combobox1.place(x=263.0, y=181.5)
        self.combobox1.set(self.book_data["ID_Sala"])
        self.combobox1.bind("<<ComboboxSelected>>", self.validacion_sala)
        
        
        # Combobox para Categoría
        self.categoria_cb = ttk.Combobox(self, values=self.categoria_types_general, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.categoria_cb.place(x=520.0, y=181.5)
        self.categoria_cb.set(self.book_data["ID_Categoria"])
        self.categoria_cb.bind("<<ComboboxSelected>>", self.check_changes)

        # Combobox para Asignatura
        self.asignatura_cb = ttk.Combobox(self, values=self.asignature_type_general, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.asignatura_cb.place(x=779.0, y=181.5)
        self.asignatura_cb.set(self.book_data["ID_Asignatura"])
        self.asignatura_cb.bind("<<ComboboxSelected>>", self.check_changes)

        # Crear y colocar los widgets
        # Primera fila
        self.cota = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.cota.place(x=263.0, y=282.0, width=237.0, height=37.5)
        self.cota.insert(0, self.book_data["Cota"])
        self.cota.bind("<Return>", self.focus_next_widget)
        self.cota.bind("<KeyRelease>", self.check_changes)
        self.cota.bind("<KeyPress>", self.allow_only_letters_numbers_dots)
        self.cota.bind("<KeyPress>", self.convert_to_uppercase, add='+')

        self.registro_m = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.registro_m.place(x=520.0, y=282.0, width=237.0, height=38.0)
        self.registro_m.insert(0, self.book_data["n_registro"])
        self.registro_m.bind("<Return>", self.focus_next_widget)
        self.registro_m.bind("<KeyRelease>", self.check_changes)

        self.edicion_m = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.edicion_m.place(x=779.0, y=282.0, width=237.0, height=37.5)
        self.edicion_m.insert(0, self.book_data["Edicion"])
        self.edicion_m.bind("<Return>", self.focus_next_widget)
        self.edicion_m.bind("<KeyRelease>", self.check_changes)

        self.volumen_m = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.volumen_m.place(x=1036.0, y=282.0, width=237.0, height=37.5)
        self.volumen_m.insert(0, self.book_data["Volumen"])
        self.volumen_m.bind("<Return>", self.focus_next_widget)
        self.volumen_m.bind("<KeyRelease>", self.check_changes)

        # Segunda fila
        self.titulo_m = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.titulo_m.place(x=263.0, y=382.0, width=237.0, height=37.5)
        self.titulo_m.insert(0, self.book_data["Titulo"])
        self.titulo_m.bind("<Return>", self.focus_next_widget)
        self.titulo_m.bind("<KeyRelease>", self.check_changes)
        self.titulo_m.bind("<KeyPress>", self.format_title)  # Formatear al perder el foco
        self.titulo_m.bind("<KeyPress>", self.schedule_validation)


        self.autor_m = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key")
        self.autor_m.place(x=520.0, y=382.0, width=237.0, height=37.5)
        self.autor_m.insert(0, self.book_data["Autor"])
        self.autor_m.bind("<Return>", self.focus_next_widget)
        
        self.autor_m.bind("<KeyRelease>", self.check_changes)
       
        self.autor_m.bind('<KeyPress>', lambda event: self.validate_and_format_text(self.autor_m))
        

        self.editorial_m = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key")
        self.editorial_m.place(x=779.0, y=382.0, width=237.0, height=37.5)
        self.editorial_m.insert(0, self.book_data["Editorial"])
        self.editorial_m.bind("<Return>", self.focus_next_widget)
        self.editorial_m.bind("<KeyRelease>", self.check_changes)
        self.editorial_m.bind('<KeyPress>', lambda event: self.validate_and_format_text(self.editorial_m))

        self.ano_m = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.ano_m.place(x=1036.0, y=382.0, width=237.0, height=37.5)
        self.ano_m.insert(0, self.book_data["Año"])
        self.ano_m.bind("<Return>", self.focus_next_widget)
        self.ano_m.bind("<KeyRelease>", self.check_changes)
        
    #AUTOR Y EDITORAL
    def validate_and_format_text(self, entry_widget):
        current_text = entry_widget.get()
        
        # Validar y formatear el texto usando la función genérica
        formatted_text = validar_y_formatear_texto(current_text)
        
        # Guardar la posición del cursor
        cursor_position = entry_widget.index(tk.INSERT)
        
        # Actualizar el campo de entrada
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, formatted_text)
        
        # Restaurar la posición del cursor
        entry_widget.icursor(cursor_position)
    #COTA
    def convert_to_uppercase(self, event):
        self.after(1, self._convert_to_uppercase)

    def _convert_to_uppercase(self):
        cota = self.cota.get().upper()
        cursor_position = self.autor_m.index(tk.INSERT)
        self.cota.delete(0, tk.END)
        self.cota.insert(0, cota)
        self.autor_m.icursor(cursor_position)
    
    def allow_only_letters_numbers_dots(self, event):
        if event.keysym in ('BackSpace', 'Delete',"Left", "Right"):
            return
        if not re.match(r'^[a-zA-Z0-9.]$', event.char):
            return "break"

###AUTOR

    

    
#TITULO
   

    def format_title(self, event):
        # Formatear el título para capitalizar solo la primera letra
        current_text = self.titulo_m.get()
        if current_text:  # Verificar que el texto no esté vacío
            formatted_text = current_text[0].upper() + current_text[1:]  # Capitalizar solo la primera letra
            self.titulo_m.delete(0, tk.END)
            self.titulo_m.insert(0, formatted_text)
    def schedule_validation(self, event):
        # Cancelar cualquier validación programada previamente
        if hasattr(self, 'validation_id'):
            self.after_cancel(self.validation_id)
        
        # Programar la validación y formateo con un retraso de 1 milisegundo
        self.validation_id = self.after(1, self.validate_and_format_title)

    def validate_and_format_title(self):
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áéíóúÁÉÍÓÚñÑ.,;:!?-"
        current_text = self.titulo_m.get()
        
        # Filtrar caracteres no permitidos
        filtered_text = ''.join([char for char in current_text if char in allowed_chars])
        
        # Formatear el texto para capitalizar solo la primera letra
        if filtered_text:
            formatted_text = filtered_text[0].upper() + filtered_text[1:]
        else:
            formatted_text = filtered_text
        
        # Actualizar el campo de entrada
        self.titulo_m.delete(0, tk.END)
        self.titulo_m.insert(0, formatted_text)

        
    def check_changes(self, *args):
     try:
        current_values = {
            "ID_Sala": self.combobox1.get().strip(),
            "ID_Categoria": self.categoria_cb.get().strip(),
            "ID_Asignatura": self.asignatura_cb.get().strip(),
            "Cota": self.cota.get().strip(),
            "n_registro": self.registro_m.get().strip(),
            "Titulo": self.titulo_m.get().strip(),
            "Autor": self.autor_m.get().strip(),
            "Editorial": self.editorial_m.get().strip(),
            "Año": self.ano_m.get().strip(),
            "Edicion": self.edicion_m.get().strip(),
            "Volumen": self.volumen_m.get().strip(),
        }

        # Agrega depuración para ver los valores actuales y originales
        print("Valores actuales:", current_values)
        print("Valores originales:", self.original_values)

        # Comparar valores clave por clave
        differences = []
        for key in current_values:
            if current_values[key] != self.original_values[key]:
                differences.append(f"Diferencia en {key}: {current_values[key]} (actual) != {self.original_values[key]} (original)")

        if differences:
            for diff in differences:
                print(diff)
            self.mostrar_boton_modificar()
            print("Se detectaron cambios. Botón 'Modificar' mostrado.")
        else:
            self.ocultar_boton_modificar()
            print("No se detectaron cambios. Botón 'Modificar' oculto.")
     except Exception as e:
        print(f"Error en check_changes: {e}")




    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def mostrar_opciones(self, categoria_values, asignatura_values):

        self.categoria_cb['values'] = categoria_values
        self.asignatura_cb['values'] = asignatura_values
        self.check_changes()
        
    def actualizar_opciones(self, combobox, values):
        combobox['values'] = values
        combobox.set('')
        self.check_changes()

    def validacion_sala(self, event):
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                            fieldbackground="#2E59A7",  # Fondo del campo de entrada
                            background="#2E59A7",  # Fondo del desplegable
                            bordercolor="#041022",  # Color del borde
                            arrowcolor="#ffffff",  # Color de la flecha
                            padding="9",
                            )  # padding para agrandar la altura del select
        sala_seleccionada = self.combobox1.get()
        
        if sala_seleccionada == self.book_data["ID_Sala"]:
            self.categoria_cb.set(self.book_data["ID_Categoria"])
            self.asignatura_cb.set(self.book_data["ID_Asignatura"])
        else:
            self.categoria_cb.set("No se ha seleccionado una categoría")
            self.asignatura_cb.set("No se ha seleccionado una asignatura")

        if sala_seleccionada == "1I":
            self.mostrar_opciones(self.categoria_types_children, self.asignature_types_children)
            
        elif sala_seleccionada == "2E":
            self.mostrar_opciones(self.categoria_types_state, self.asignature_types_state)
            
        elif sala_seleccionada == "3G":
            self.mostrar_opciones(self.categoria_types_general, self.asignature_type_general)
            
        else:
            messagebox.showwarning("Validación", "Por favor, seleccione una opción válida.")
        
        self.check_changes()
        
    
    def modify_book(self):
    # Recoger los valores de los campos
        nuevos_valores = {
        "ID_Sala": self.combobox1.get(),
        "ID_Categoria": self.categoria_cb.get(),
        "ID_Asignatura": self.asignatura_cb.get(),
        "Cota": self.cota.get(),
        "n_registro": self.registro_m.get(),
        "Edicion": self.edicion_m.get(),
        "n_volumenes": self.volumen_m.get(),
        "Titulo": self.titulo_m.get(),
        "Autor": self.autor_m.get(),
        "Editorial": self.editorial_m.get(),
        "Año": self.ano_m.get()
    }
        errores = validar_campos(self.cota.get(), self.titulo_m.get())
        if errores:
            messagebox.showerror("Validation Errors", "\n".join(errores))
            return

    # Validar que se haya seleccionado una categoría y una asignatura
        if nuevos_valores["ID_Categoria"] == "No se ha seleccionado una categoría" or not nuevos_valores["ID_Categoria"]:
            messagebox.showerror("Error", "Debe seleccionar una categoría.")
            return
        if nuevos_valores["ID_Asignatura"] == "No se ha seleccionado una asignatura" or not nuevos_valores["ID_Asignatura"]:
            messagebox.showerror("Error", "Debe seleccionar una asignatura.")
            return

        print("Datos recogidos:")
        for key, value in nuevos_valores.items():
            print(f"{key}: {value}")

        # Actualizar los libros con los nuevos valores
        if update_books(self.book_data, nuevos_valores):
                messagebox.showinfo("Éxito", "Modificación del libro exitosa.")
                self.clear_entries_modify()
        else:
            messagebox.showinfo("Modificación fallida", "Libro mantiene sus valores.")




    def crear_boton_modificar(self):
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("M_Boton.png"))
         # Crear el botón
         
        self.boton_modificar = tk.Button(
            self,
            image=self.images["boton_R"],
            borderwidth=0,
            highlightthickness=0,
            command=self.modify_book,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
         )
         # Asignar la posición del botón
        self.boton_modificar.place(x=263.0, y=635.0, width=130.0, height=40.0)
        self.boton_modificar.place_forget()  # Ocultar el botón inicialmente
        print("Botón 'Modificar' creado y oculto inicialmente.")
        
    def mostrar_boton_modificar(self):
        self.boton_modificar.place(x=263.0, y=635.0, width=130.0, height=40.0)
        print("Botón 'Modificar' mostrado.")

    def ocultar_boton_modificar(self):
        self.boton_modificar.place_forget()
        print("Botón 'Modificar' oculto.")

    def clear_entries_modify(self):
        self.combobox1.delete(0, tk.END)
        #self.menu_actual.delete(0, tk.END)
        self.combobox1.delete(0, tk.END)
        self.cota.delete(0, tk.END)
        self.registro_m.delete(0, tk.END)
        self.edicion_m.delete(0, tk.END)
        self.volumen_m.delete(0, tk.END)
        self.titulo_m.delete(0, tk.END)
        self.autor_m.delete(0, tk.END)
        self.editorial_m.delete(0, tk.END)
        self.registro_m.delete(0, tk.END)
        self.ano_m.delete(0, tk.END)
        
        
class L_Eliminar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#031A33", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Formulario para el eliminar
        self.label_info = self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del libro a Eliminar", fill="#a6a6a6", font=("Bold", 15))
        
        # Texto para el nombre
        self.label_nombre = self.canvas.create_text(263.0, 152.0, anchor="nw", text="ID", fill="#a6a6a6", font=("Bold", 17))
        
        self.id_eliminar = tk.Entry(self, bd=0,bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.id_eliminar.place(x=263.0, y=182.0, width=237.0, height=38.0)

        # Cargar y almacenar las imágenes
        self.images['boton_Eliminar_f'] = tk.PhotoImage(file=relative_to_assets("Boton_eliminar.png"))
        
        # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
            self,
            image=self.images['boton_Eliminar_f'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: delete_book(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_e.place(x=265.0, y=264.0, width=130.0, height=40.0)
        
        def delete_book(self):
            ID_Libro=self.id_eliminar.get() if self.id_eliminar else None
            if ID_Libro:
                # Confirmación antes de eliminar
                respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar este libro?")
                if respuesta:
                    if delete_books(ID_Libro):
                        messagebox.showinfo("Éxito", "Eliminación exitosa del libro.")
                        self.clear_entries_delete()
                    else:
                        messagebox.showinfo("Falla en la Eliminación", "El libro no existe o ya fue eliminado.")
                else:
                    messagebox.showinfo("Cancelado", "Eliminación cancelada.")
            else:
                messagebox.showinfo("Error", "Por favor, proporciona un ID de libro válido.")
        
    def clear_entries_delete(self):
        self.id_eliminar.delete(0, tk.END)

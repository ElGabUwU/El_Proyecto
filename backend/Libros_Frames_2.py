import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import font
#from Library.librerias import recoger_sesion, drop_sesion
from Library.db_pokimon import *
from PIL import Image,ImageTk
from Vistas.listas import *
import random
from db.conexion import establecer_conexion
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
        "3G", "2E", "1I"
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
            if validacion_salas=="3G":
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
                    # print("ID SALA", {ID_Sala}, "ID CATEGORIA", {ID_Categoria}, "ID ASIGNATURA", {ID_Asignatura}, "COTA", {Cota}, "REGISTRO", {n_registro})
                    # print("Edicion", {edicion}, "VOLUMEN", {n_volumenes}, "TITULO", {titulo}, "AUTOR", {autor}, "EDITORIAL", {editorial}, "AÑO", {año}, "EJEMPLARES", {n_ejemplares})
                    # print("\n")
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

class L_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="right", fill="both", expand=True)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Crear el marco izquierdo para el menú de navegación
        self.left_frame_list = tk.Frame(self.canvas, bg="#FAFAFA")
        self.left_frame_list.pack(expand=True, side="left", fill="both") #padx=212, pady=150, ipady=80
        self.left_frame_list.place(x=215,y=205, height=480, width=1150)


        """"self.cota = tk.Entry(self, bd=0, bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="solid" , borderwidth=0.5)
        self.cota.place(x=263.0, y=282.0, width=237.0, height=37.5)"""
        
        self.buscar = tk.Entry(self, bd=0, bg="#FAFAFA", fg="#031A33", relief="solid" , borderwidth=0.5)
        self.buscar.place(x=265.0, y=130.0, width=267.0, height=48.0)
        
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
                bg="#031A33",
                activebackground="#031A33",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=935.0, y=60.0, width=90.0, height=100.0)

            # Cargar y almacenar las imágenes
        # self.images['boton_filtrar_f'] = tk.PhotoImage(file=relative_to_assets("boton_filtrar.png"))
            
        #     # Cargar y almacenar la imagen del botón
        # self.button_e = tk.Button(
        #     self,
        #     image=self.images['boton_filtrar_f'],
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: self.open_filter_window(self),
        #     relief="flat",
        #     bg="white" 
        #     )
        # self.button_e.place(x=1095.0, y=110.0, width=130.0, height=40.0)

        self.images['boton_Eliminar'] = tk.PhotoImage(file=relative_to_assets("7_eliminar.png"))
                    # Cargar y almacenar la imagen del botón
        self.button_dl = tk.Button(
            self,
            image=self.images['boton_Eliminar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: delete_selected(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
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
            #command=lambda: delete_selected(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
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
                        background="#E5E1D7", 
                        fieldbackground="#f0f0f0")

        # Configurar estilo para las cabeceras
        style.configure("Rounded.Treeview.Heading", 
                        font=('Helvetica', 10, 'bold'), 
                        background="#2E59A7", 
                        foreground="#000000",
                        borderwidth=0)


        # Aplica el estilo al Treeview
        columns = ("ID", "Sala", "Categoria", "Asignatura", "Cota", "N. Registro", "Título", "Autor", "Editorial", "Año", "Edición")
        self.book_table_list = ttk.Treeview(self.left_frame_list, columns=columns, show='headings', style="Rounded.Treeview")
        for col in columns:
            self.book_table_list.heading(col, text=col)
            self.book_table_list.column(col, width=90)
        self.book_table_list.pack(expand=True, fill="both", padx=70, pady=5)

        scrollbar_pt = ttk.Scrollbar(self.book_table_list, orient="vertical", command=self.book_table_list.yview)
        self.book_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")

        
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
                                    cursor.execute('SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, titulo, autor, editorial, año, edicion FROM libro')
                                    resultados = cursor.fetchall() 
                                    for row in book_table_list.get_children():
                                        book_table_list.delete(row)
                                        
                                        # Insertar los datos en el Treeview
                                    for fila in resultados:
                                        book_table_list.insert("", "end", values=tuple(fila))
                                    mariadb_conexion.close()
                            except mariadb.Error as ex:
                                    print("Error durante la conexión:", ex)
                            except subprocess.CalledProcessError as e:
                                print("Error al importar el archivo SQL:", e)

    def cancelar(self, window):
        window.destroy()  # Esto cerrará la ventana de filtro

class L_Modificar(tk.Frame):      
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#031A33", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
    # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del libro a modificar", fill="#a6a6a6", font=("Bold", 17))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Sala", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 152.0, anchor="nw", text="Categoria", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(779.0, 152.0, anchor="nw", text="Asignatura", fill="#a6a6a6", font=("Bold", 17))
        
        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Cota", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Numero de registro", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(779.0, 252.0, anchor="nw", text="Edición", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1036.0, 252.0, anchor="nw", text=" N° volumen", fill="#a6a6a6", font=("Bold", 17))
        
        #fila 3
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Titulo", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Autor", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(779.0, 352.0, anchor="nw", text="Editorial", fill="#a6a6a6", font=("Bold", 17))
        
        #fila 4
        self.canvas.create_text(263.0, 452.0, anchor="nw", text="Año", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 452.0, anchor="nw", text="Cantidad de ejemplares", fill="#a6a6a6", font=("Bold", 17))
        #fila 5
        self.canvas.create_text(263.0, 552.0, anchor="nw", text="ID", fill="#a6a6a6", font=("Bold", 17))
        
        
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        #primera fila
        self.cota = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.cota.place(x=263.0, y=282.0, width=237.0, height=37.5)

        self.registro_m = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.registro_m.place(x=520.0, y=282.0, width=237.0, height=38.0)
        
        self.edicion_m = tk.Entry(self, bd=0,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.edicion_m.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        self.volumen_m = tk.Entry(self, bd=0,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.volumen_m.place(x=1036.0, y=282.0, width=237.0, height=37.5)
        #segunda fila
        self.titulo_m = tk.Entry(self, bd=0,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.titulo_m.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.autor_m = tk.Entry(self, bd=0,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key")
        self.autor_m.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        self.editorial_m = tk.Entry(self, bd=0,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key")
        self.editorial_m.place(x=779.0, y=382.0, width=237.0, height=37.5)
        #tercera fila
        
        self.año_m = tk.Entry(self, bd=0,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.año_m.place(x=263.0, y=482.0, width=237.0, height=37.5)
        
        self.ejemplares_m = tk.Entry(self, bd=0,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.ejemplares_m.place(x=520.0, y=482.0, width=237.0, height=37.5)
        
        #cuarta fila
        
        self.id_m = tk.Entry(self, bd=0,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.id_m.place(x=263.0, y=582.0, width=237.0, height=37.5)
        #Select tipo de pokemon
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                            fieldbackground="#2E59A7",  # Fondo del campo de entrada
                            background="#2E59A7",  # Fondo del desplegable
                            bordercolor="#041022",  # Color del borde
                            arrowcolor="#ffffff",  # Color de la flecha
                            padding= "9",
                            ) # padding para agrandar la altura del select
        
        self.salas_types = [
        "3G", "2E", "1I"
        ]
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

        #Sala
        self.combobox1=ttk.Combobox(self, values=self.salas_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.combobox1.place(x=263.0, y=181.5)
        self.combobox1.bind("<<ComboboxSelected>>",self.validacion_sala)
        self.menu_actual = None

    def validacion_sala(self,event):
            #Select tipo de pokemon
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
            if validacion_salas=="3G":
            # Categoria-Sala General
                self.menu_actual = ttk.Combobox(self, values=self.categoria_types_general, state="readonly", width=30, font=("Montserrat Medium", 10))
                self.menu_actual.place(x=520.0, y=181.5)
            # Asignatura-Sala General
                self.combobox3 = ttk.Combobox(self, values=self.asignature_type_general, state="readonly", width=30, font=("Montserrat Medium", 10))
                self.combobox3.place(x=779.0, y=181.5)
            elif validacion_salas=="2E":
            # Categoria-Sala Estadal
                self.menu_actual = ttk.Combobox(self, values=self.categoria_types_state, state="readonly", width=30, font=("Montserrat Medium", 10))
                self.menu_actual.place(x=520.0, y=181.5)
            # Asignatura-Sala Estadal
                self.combobox3 = ttk.Combobox(self, values=self.asignature_types_state, state="readonly", width=30, font=("Montserrat Medium", 10))
                self.combobox3.place(x=779.0, y=181.5)
            elif validacion_salas=="1I":
            # Categoria-Sala Infantil
                self.menu_actual = ttk.Combobox(self, values=self.categoria_types_children, state="readonly", width=30, font=("Montserrat Medium", 10))
                self.menu_actual.place(x=520.0, y=181.5)
            # Asignatura-Sala Infantil
                self.combobox3 = ttk.Combobox(self, values=self.asignature_types_children, state="readonly", width=30, font=("Montserrat Medium", 10))
                self.combobox3.place(x=779.0, y=181.5)                 
            else:
                messagebox.showwarning("Validación", "Por favor, seleccione una opción.")
       
            self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("M_Boton.png"))

            # Crear el botón
            boton_R = self.images['boton_R']
            tk.Button(
                self,
                image=boton_R,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: modify_book(),
                relief="flat",
                bg="#031A33",
                activebackground="#031A33",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            ).place(x=263.0, y=635.0, width=130.0, height=40.0)
            
            def modify_book():
                ID_Sala= self.combobox1.get() #self.cota.get()
                ID_Categoria = self.menu_actual.get() if self.menu_actual else None #self.combobox1.get()
                ID_Asignatura = self.combobox3.get() if self.combobox3 else None #self.menu_actual.get() if self.menu_actual else None
                Cota= self.cota.get() #self.combobox3.get() if self.combobox3 else None
                n_registro=self.registro_m.get()
                edicion=self.edicion_m.get()
                n_volumenes=self.volumen_m.get()
                titulo=self.titulo_m.get()
                autor=self.autor_m.get()
                editorial=self.editorial_m.get()
                año=self.año_m.get()
                n_ejemplares=self.ejemplares_m.get()
                ID_Libro=self.id_m.get()
                print("ID SALA", {ID_Sala}, "ID CATEGORIA", {ID_Categoria}, "ID ASIGNATURA", {ID_Asignatura}, "COTA", {Cota}, "REGISTRO", {n_registro})
                print("Edicion", {edicion}, "VOLUMEN", {n_volumenes}, "TITULO", {titulo}, "AUTOR", {autor}, "EDITORIAL", {editorial}, "AÑO", {año}, "EJEMPLARES", {n_ejemplares}, "IDLIBRO", {ID_Libro})
                print("\n")
                if update_books(ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares, ID_Libro):
                    messagebox.showinfo("Éxito", "Modificación del libro éxitoso.")
                    self.clear_entries_modify()
                else:
                    messagebox.showinfo("Modificación fallida", "Libro mantiene sus valores.")
       
    def clear_entries_modify(self):
        self.combobox1.delete(0, tk.END)
        #self.menu_actual.delete(0, tk.END)
        self.combobox3.delete(0, tk.END)
        self.cota.delete(0, tk.END)
        self.registro_m.delete(0, tk.END)
        self.edicion_m.delete(0, tk.END)
        self.volumen_m.delete(0, tk.END)
        self.titulo_m.delete(0, tk.END)
        self.autor_m.delete(0, tk.END)
        self.editorial_m.delete(0, tk.END)
        self.registro_m.delete(0, tk.END)
        self.año_m.delete(0, tk.END)
        self.ejemplares_m.delete(0, tk.END)
        self.id_m.delete(0, tk.END)
        
        # Obtener el tipo seleccionado del combobox
        #tipo_combobox = self.tipos_de_pokemones.get()
        #print(tipo_combobox)
        # Obtener el valor numérico del tipo de Pokémon seleccionado
        #tipo = salas_types.get(tipo_combobox, 0) 
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

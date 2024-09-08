import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from Library.librerias import recoger_sesion, drop_sesion
from Library.db_pokimon import *
from PIL import Image,ImageTk
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
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Sala", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 152.0, anchor="nw", text="Categoria", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 152.0, anchor="nw", text="Asignatura", fill="#000000", font=("Montserrat Regular", 15))
        
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
        
        self.cota = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.cota.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.registro= tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.registro.place(x=520.0, y=282.0, width=237.0, height=38.0)
 
        self.edicion = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.edicion.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        self.volumen = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.volumen.place(x=1036.0, y=282.0, width=237.0, height=37.5)
        #segunda fila
        self.titulo = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.titulo.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.autor = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.autor.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        self.editorial = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.editorial.place(x=779.0, y=382.0, width=237.0, height=37.5)
        #tercera fila
        
        self.año = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.año.place(x=263.0, y=482.0, width=237.0, height=37.5)
        
        self.ejemplares = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.ejemplares.place(x=520.0, y=482.0, width=237.0, height=37.5)
        
        
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

        #Sala
        self.combobox1=ttk.Combobox(self, values=self.salas_types, state="readonly", width=30, font=("Montserrat Medium", 10))
        self.combobox1.place(x=263.0, y=181.5)
        self.combobox1.bind("<<ComboboxSelected>>",self.validacion_sala)
        self.menu_actual = None

    def validacion_sala(self,event):
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
                    else:
                        messagebox.showinfo("Registro fallido", "Libro mantiene sus valores.")

class L_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="right", fill="both", expand=True)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Crear el marco izquierdo para el menú de navegación
        self.left_frame_list = tk.Frame(self.canvas, bg="white")
        self.left_frame_list.pack(expand=True, side="left", fill="both") #padx=212, pady=150, ipady=80
        self.left_frame_list.place(x=215,y=155, height=550, width=1150)

        # self.right_frame = tk.Frame(self)
        # self.right_frame.pack(side="right", expand=True, fill="both")

        # Texto para el nombre
        self.label_nombre = self.canvas.create_text(635.0, 85.0, anchor="nw", text="Buscar", fill="#000000", font=("Montserrat Regular", 15))
        
        self.buscar = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key")
        self.buscar.place(x=635.0, y=110.0, width=237.0, height=38.0)
        # Para llamar a read_books cuando se presiona Enter
        self.buscar.bind("<Return>", lambda event: boton_buscar())
        
        def boton_buscar():
            try:
             mariadb_conexion = mariadb.connect(
                                        host='localhost',
                                        port='3306',
                                        password='2525',
                                        database='basedatosbiblioteca'
            )
             if mariadb_conexion.is_connected():
                        cursor = mariadb_conexion.cursor()
                        cursor.execute('SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, titulo, autor, editorial, año, edicion FROM libro')
                        btn_buscar= self.buscar.get()
                        resultados = cursor.fetchall() 
                        for fila in resultados:
                            self.book_table_list.insert("", "end", values=tuple(fila))
                            if btn_buscar in fila:
                                self.book_table_list.item(self.book_table_list.get_children()[-1], tags='match')
                            else:
                                self.book_table_list.item(self.book_table_list.get_children()[-1], tags='nomatch')
                            self.book_table_list.tag_configure('match', background='green')
                            self.book_table_list.tag_configure('nomatch', background='gray')
                        if read_books(btn_buscar):
                            messagebox.showinfo("Busqueda Éxitosa", "Resultados en pantalla.")
                        else:
                            messagebox.showinfo("Busqueda Fallida", "No se encontraron resultados.")
            except mariadb.Error as ex:
                    print("Error durante la conexión:", ex)
        #Boton Cargar Libros
        # Cargar y almacenar las imágenes
        self.images['boton_cargar'] = tk.PhotoImage(file=relative_to_assets("Cargar_rojo.png"))
        
        # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
            self,
            image=self.images['boton_cargar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.reading_books(self.book_table_list),
            relief="flat"
        )
        self.button_e.place(x=915.0, y=110.0, width=130.0, height=40.0)

        # Cargar y almacenar las imágenes
        self.images['boton_filtrar_f'] = tk.PhotoImage(file=relative_to_assets("boton_filtrar.png"))
        
        # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
            self,
            image=self.images['boton_filtrar_f'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_filter_window(parent),
            relief="flat"
        )
        self.button_e.place(x=1095.0, y=110.0, width=130.0, height=40.0)
        
        # Botones del menú de navegación
        #buttons = ["Libros", "Prestamos", "Usuarios", "Mi Perfil"]
        #for button in buttons:
        #    tk.Button(self.right_frame, text=button, bg="lightgray").pack(fill="y", padx=5, pady=5)
        
        ##Crear el marco derecho para el área principal de contenido
        # self.right_frame = tk.Frame(self)
        # self.right_frame.pack(side="right", expand=True, fill="both")
        
        # Barra de búsqueda en la parte superior
        #search_frame = tk.Frame(self.left_frame)
        #search_frame.pack(fill="x", padx=10, pady=10)
        #tk.Label(search_frame, text="Buscar:").pack(side="left")
        #tk.Entry(search_frame).pack(side="left", fill="x", expand=True)
        #tk.Button(search_frame, text="Filtrar Sesión").pack(side="left", padx=5)
        
    # Tabla de libros usando Treeview
        columns = ("ID","Sala", "Categoria", "Asignatura", "Cota", "N. Registro", "Título", "Autor", "Editorial", "Año", "Edición")
        self.book_table_list= ttk.Treeview(self.left_frame_list, columns=columns, show='headings')
        for col in columns:
            self.book_table_list.heading(col, text=col)
            self.book_table_list.column(col, width=90)
        self.book_table_list.pack(expand=True, fill="both", padx=70, pady=45)

        scrollbar_pt = ttk.Scrollbar(self.book_table_list, orient="vertical", command=self.book_table_list.yview)
        self.book_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
  
    def open_filter_window(self,parent):
        filter_window = tk.Toplevel(self)
        filter_window.title("Filtrar")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))

        tk.Label(filter_window, text="Sala").grid(row=0, column=0, padx=10, pady=5)
        self.sala_entry = tk.Entry(filter_window)
        self.sala_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="Categoria").grid(row=0, column=2, padx=10, pady=5)
        self.categoria_entry = tk.Entry(filter_window)
        self.categoria_entry.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(filter_window, text="Asignatura").grid(row=0, column=4, padx=10, pady=5)
        self.asignatura_entry = tk.Entry(filter_window)
        self.asignatura_entry.grid(row=0, column=5, padx=10, pady=5)

        tk.Label(filter_window, text="Cota").grid(row=0, column=6, padx=10, pady=5)
        self.cota_entry = tk.Entry(filter_window)
        self.cota_entry.grid(row=0, column=7, padx=10, pady=5)

        tk.Label(filter_window, text="Autor").grid(row=1, column=0, padx=10, pady=5)
        self.autor_entry = tk.Entry(filter_window)
        self.autor_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="Titulo").grid(row=1, column=2, padx=10, pady=5)
        self.titulo_entry = tk.Entry(filter_window)
        self.titulo_entry.grid(row=1, column=3, padx=10, pady=5)

        tk.Label(filter_window, text="N° Registro").grid(row=1, column=4, padx=10, pady=5)
        self.n_registro_entry = tk.Entry(filter_window)
        self.n_registro_entry.grid(row=1, column=5, padx=10, pady=5)

        tk.Label(filter_window, text="Año").grid(row=2, column=0, padx=10, pady=5)
        self.año_entry = tk.Entry(filter_window)
        self.año_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="Edicion").grid(row=2, column=2, padx=10, pady=5)
        self.edicion_entry = tk.Entry(filter_window)
        self.edicion_entry.grid(row=2, column=3, padx=10, pady=5)

        tk.Label(filter_window, text="Editorial").grid(row=2, column=4, padx=10, pady=5)
        self.editorial_entry = tk.Entry(filter_window)
        self.editorial_entry.grid(row=2, column=5, padx=10, pady=5)

        search_button = ttk.Button(filter_window, text="Buscar", command=self.filter_books)
        search_button.grid(row=3, column=7, columnspan=1, pady=10)

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=self.filter_books)
        button_cancel.grid(row=3, column=6, columnspan=1, pady=10)

        # Vincular el evento de escritura
        self.n_registro_entry.bind("<KeyRelease>", lambda event: self.format_n_registro(event))

    def format_n_registro(self, event):
        # Obtener el texto actual del campo de entrada
        text = self.n_registro_entry.get().replace(".", "")
        
        # Formatear el texto para insertar un punto después de las tres primeras cifras
        if len(text)> 2:
            formatted_text = text[:2] + "." + text[2:]
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
            if (sala in values[1].lower() and values[1].upper() and
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
    
    def reading_books(self,book_table):
                            try:
                                # subprocess.run(['mysql', '-u', 'root', '-p2525', 'basedatosbiblioteca', '<', 'backend/BD_BIBLIOTECA_V7.sql'], check=True)
                                mariadb_conexion = mariadb.connect(
                                                            host='localhost',
                                                            port='3306',
                                                            password='2525',
                                                            database='basedatosbiblioteca'
                                )
                                if mariadb_conexion.is_connected():
                                    cursor = mariadb_conexion.cursor()
                                    cursor.execute('SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, titulo, autor, editorial, año, edicion FROM libro')
                                    resultados = cursor.fetchall() 
                                    for row in book_table.get_children():
                                        book_table.delete(row)
                                        
                                        # Insertar los datos en el Treeview
                                    for fila in resultados:
                                        book_table.insert("", "end", values=tuple(fila))
                                    mariadb_conexion.close()
                            except mariadb.Error as ex:
                                    print("Error durante la conexión:", ex)
                            except subprocess.CalledProcessError as e:
                                print("Error al importar el archivo SQL:", e)

    def cancelar(self):
        self.cancelar.destroy()  # Esto cerrará la ventana principal


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
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Sala", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 152.0, anchor="nw", text="Categoria", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 152.0, anchor="nw", text="Asignatura", fill="#000000", font=("Montserrat Regular", 15))
        
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
        self.cota = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.cota.place(x=263.0, y=282.0, width=237.0, height=37.5)

        self.registro_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.registro_m.place(x=520.0, y=282.0, width=237.0, height=38.0)
        
        self.edicion_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.edicion_m.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        self.volumen_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.volumen_m.place(x=1036.0, y=282.0, width=237.0, height=37.5)
        #segunda fila
        self.titulo_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.titulo_m.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.autor_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key")
        self.autor_m.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        self.editorial_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key")
        self.editorial_m.place(x=779.0, y=382.0, width=237.0, height=37.5)
        #tercera fila
        
        self.año_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.año_m.place(x=263.0, y=482.0, width=237.0, height=37.5)
        
        self.ejemplares_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.ejemplares_m.place(x=520.0, y=482.0, width=237.0, height=37.5)
        
        #cuarta fila
        
        self.id_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.id_m.place(x=263.0, y=582.0, width=237.0, height=37.5)
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
                else:
                    messagebox.showinfo("Modificación fallida", "Libro mantiene sus valores.")
       
        
        
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
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Formulario para el eliminar
        self.label_info = self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del libro a Eliminar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        
        # Texto para el nombre
        self.label_nombre = self.canvas.create_text(263.0, 152.0, anchor="nw", text="ID", fill="#000000", font=("Montserrat Regular", 15))
        
        self.id_eliminar = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
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
            relief="flat"
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
                    else:
                        messagebox.showinfo("Falla en la Eliminación", "El libro no existe o ya fue eliminado.")
                else:
                    messagebox.showinfo("Cancelado", "Eliminación cancelada.")
            else:
                messagebox.showinfo("Error", "Por favor, proporciona un ID de libro válido.")
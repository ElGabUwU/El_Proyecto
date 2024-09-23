import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import font
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
#from Library.librerias import recoger_sesion, drop_sesion
from Library.db_prestamos import *
from Library.bd_prestamo_listado_Frames2 import *
from Vistas.listas import *
from tkcalendar import Calendar
from datetime import datetime, timedelta
import random
import string
from backend.Filtrados_Prestamo import *

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
        self.canvas = tk.Canvas(self, bg="#031A33", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        self.right_frame_list_loans = tk.Frame(self.canvas, bg="#031A33")
        self.right_frame_list_loans.pack(expand=True, side="right", fill="both") #padx=212, pady=150, ipady=80
        self.right_frame_list_loans.place(x=355,y=340, height=350, width=950)

        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del cliente y su préstamo a agregar", fill="#a6a6a6", font=("Bold", 17))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cedula", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 152.0, anchor="nw", text="Nombre", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(779.0, 152.0, anchor="nw", text="Apellido", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1039.0, 152.0, anchor="nw", text="Cantidad", fill="#a6a6a6", font=("Bold", 17))

        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Numero de teléfono", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Dirección", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(779.0, 252.0, anchor="nw", text="Fecha del Registro", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1039.0, 252.0, anchor="nw", text="Fecha Límite", fill="#a6a6a6", font=("Bold", 17))
        #primera fila
    
        self.input_cedula = tk.Entry(
            self,
            bd=0,
            bg="#031A33",
            fg="#a6a6a6",
            highlightthickness=2,
            highlightbackground="#ffffff",
            highlightcolor="#ffffff",
            borderwidth=0.5, 
            relief="solid",
            validate="key",
            validatecommand=(validate_number, "%P")
        )
        self.input_cedula.place(x=263.0, y=182.0, width=237.0, height=38.0)
        
        self.input_nombre = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_nombre.place(x=520.0, y=182.0, width=237.0, height=38.0)
 
        self.input_apellido = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_apellido.place(x=779.0, y=182.0, width=237.0, height=37.5)

        self.input_cantidad = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_cantidad.place(x=1039.0, y=182.0, width=237.0, height=37.5)
        
        #segunda fila
        
        self.input_telefono = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_telefono.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.input_direccion = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_direccion.place(x=520.0, y=282.0, width=237.0, height=38.0)

        # Campo para la fecha límite
        self.fecha_registrar = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.fecha_registrar.place(x=779.0, y=282.0, width=237.0, height=38.0)

        self.fecha_limite = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.fecha_limite.place(x=1039.0, y=282.0, width=237.0, height=38.0)

        # Establecer las fechas automáticamente
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        fecha_limite = (datetime.now() + timedelta(days=20)).strftime("%d/%m/%Y")

        self.fecha_registrar.insert(0, fecha_actual)
        self.fecha_limite.insert(0, fecha_limite)

        # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("R_Boton_registrar.png"))

        boton_R = self.images['boton_R']
        boton_R = tk.Button(
            self,
            image=boton_R,
            borderwidth=0,
            highlightthickness=0,
            command= self.register_client,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        ).place(x=265.0, y=365.0, width=130.0, height=40.0)

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

        columns = ("ID","Sala", "Categoria", "Asignatura", "Cota", "N. Registro", "Título", "Autor", "Editorial", "Año", "Edición")
        self.book_table_list_loans= ttk.Treeview(self.right_frame_list_loans, columns=columns, show='headings', selectmode='extended', style="Rounded.Treeview")
        for col in columns:
            self.book_table_list_loans.heading(col, text=col)
            self.book_table_list_loans.column(col, width=40)
        self.book_table_list_loans.pack(expand=True, fill="both", padx=70, pady=25)

        scrollbar_pt = ttk.Scrollbar(self.book_table_list_loans, orient="vertical", command=self.book_table_list_loans.yview)
        self.book_table_list_loans.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")

        # # Botón para obtener las filas seleccionadas
        # self.select_button = tk.Button(self.canvas, text="Seleccionar Libros", command=self.get_selected_books)
        # self.select_button.place(x=265.0, y=435.0, width=130.0, height=40.0)


        self.reading_books(self.book_table_list_loans)

    def register_client(self):
            ID_Cedula= self.input_cedula.get() #self.cota.get()
            nombre = self.input_nombre.get()#self.combobox1.get()
            apellido = self.input_apellido.get()#self.menu_actual.get() if self.menu_actual else None
            telefono= int(self.input_telefono.get()) #self.combobox3.get() if self.combobox3 else None
            direccion=self.input_direccion.get()
            ID_Prestamo = self.generate_alphanumeric_id()#random.randint(100000, 999999)  # Genera una cadena alfanumérica de 8 caracteres
            ID_Libro_Prestamo = self.generate_id_libro_prestamo()  # Generar ID_Libro_Prestamo
            fecha_registrar = self.format_date(self.fecha_registrar.get())
            fecha_limite = self.format_date(self.fecha_limite.get())
            Cantidad = int(self.input_cantidad.get())  
            if fecha_registrar and fecha_limite:
                if self.cedula_existe(ID_Cedula):
                    messagebox.showinfo("Error", "La cédula ya está registrada.")
                    return
                if create_loan(ID_Prestamo, fecha_registrar, fecha_limite):
                        ID_Cliente = create_client_loans(ID_Cedula, nombre, apellido, telefono, direccion, ID_Prestamo)
                        if ID_Cliente:
                            selected_items = self.book_table_list_loans.selection()
                            if len(selected_items) > 5:
                                messagebox.showinfo("Error", "Solo puedes seleccionar un máximo de 5 libros.")
                                return
                            selected_books = []
                            for item in selected_items:
                                book_info = self.book_table_list_loans.item(item, "values")
                                ID_Libro = book_info[0]
                                selected_books.append(ID_Libro)
                            self.save_books_to_db(selected_books, ID_Prestamo, Cantidad)

                            if not libro_prestamo_exists(ID_Libro_Prestamo):
                                create_libro_prestamo(ID_Libro_Prestamo, ID_Prestamo, Cantidad)
                                if update_prestamo_with_cliente(ID_Prestamo, ID_Cliente, ID_Libro_Prestamo):
                                    messagebox.showinfo("Éxito", f"""
Registro éxitoso del cliente y del libro. 
ID Préstamo: {ID_Prestamo}
Libros seleccionados: {selected_books}
                    """)
                                    self.clear_entries_register_loans()
                                else:
                                    messagebox.showinfo("Error", "No se pudo registrar el libro en el préstamo.")
                            else:
                                messagebox.showinfo("Error", "No se pudo actualizar el préstamo con el cliente.")
                        else:
                            messagebox.showinfo("Registro fallido", "Cliente no pudo ser registrado.")
                else:
                        messagebox.showinfo("Error", "No se pudo crear el préstamo.")
            else:
                    messagebox.showinfo("Error", "Formato de fecha incorrecto.")
        
    def format_date(self, date_str):
        try:
            # Convertir la fecha del formato DD/MM/YYYY al formato YYYY-MM-DD
            formatted_date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            return formatted_date
        except ValueError as e:
            print(f"Error al formatear la fecha: {e}")
            return None
    def clear_entries_register_loans(self):
        self.input_cedula.delete(0, tk.END)
        self.input_nombre.delete(0, tk.END)
        self.input_apellido.delete(0, tk.END)
        self.input_telefono.delete(0, tk.END)
        self.input_direccion.delete(0, tk.END)
        self.input_cantidad.delete(0, tk.END)
        
    def generate_id_libro_prestamo(self):
        return random.randint(100000, 999999)
    
    def generate_alphanumeric_id(self, length=8):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))
    
    # def get_selected_books(self):
    #     selected_items = self.book_table_list_loans.selection()
    #     if len(selected_items) > 5:
    #         print("Solo puedes seleccionar un máximo de 5 libros.")
    #         return

    #     selected_books = []
    #     for item in selected_items:
    #         book_info = self.book_table_list_loans.item(item, "values")
    #         selected_books.append(book_info[0])
        
    #     self.save_books_to_db(selected_books)
    
    def save_books_to_db(self, book_ids, id_prestamo, cantidad):
        try:
            mariadb_conexion = connect()
            if mariadb_conexion.is_connected():
                cursor = mariadb_conexion.cursor()
                mariadb_conexion.start_transaction()
                for book_id in book_ids:
                    id_libro_prestamo = self.generate_id_libro_prestamo()
                    cursor.execute("INSERT INTO libros_prestamo (ID_Libro_Prestamo, ID_Libro, ID_Prestamo, Cantidad) VALUES (%s, %s, %s, %s)", 
                                (id_libro_prestamo, book_id, id_prestamo, cantidad))
                    cursor.execute("UPDATE libro SET ID_Libro_Prestamo = %s WHERE ID_Libro = %s", 
                                (id_libro_prestamo, book_id))
                mariadb_conexion.commit()
                print("Libros guardados en la tabla libro_prestamo y actualizados en la tabla libro:", book_ids)
        except mariadb.Error as e:
            print(f"Error al conectar con MariaDB: {e}")
            if mariadb_conexion:
                mariadb_conexion.rollback()
        finally:
            if mariadb_conexion.is_connected():
                cursor.close()
                mariadb_conexion.close()
        
    def cedula_existe(self,cedula):
        mariadb_conexion = mariadb.connect(
                                        host='localhost',
                                        port='3306',
                                        password='2525',
                                        database='basedatosbiblioteca'
        )
        if mariadb_conexion.is_connected():
            cursor = mariadb_conexion.cursor()
            query = "SELECT COUNT(*) FROM cliente WHERE Cedula_Cliente = %s"
            cursor.execute(query, (cedula,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0

    def reading_books(self, book_table_list_loans):
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
                resultados = cursor.fetchall() 
                for row in book_table_list_loans.get_children():
                    book_table_list_loans.delete(row)
                    # Insertar los datos en el Treeview
                for fila in resultados:
                    book_table_list_loans.insert("", "end", values=tuple(fila))
                mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)

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
        
class P_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#031A33", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        #validate_number = self.register(validate_number_input)
        self.images = {}

        # Crear el marco izquierdo para el menú de navegación
        #Marco listado clientes
        self.left_frame = tk.Frame(self.canvas, bg="#031A33")
        self.left_frame.pack(expand=True, side="left", fill="both")
        self.left_frame.place(x=165,y=155, height=250, width=650)
        #Marco listado libros prestamo
        self.left_frame1 = tk.Frame(self.canvas, bg="#031A33")
        self.left_frame1.pack(expand=True, side="left", fill="both") 
        self.left_frame1.place(x=165,y=365, height=350, width=650)
        #Marco listado prestamo-clientes
        self.left_frame2 = tk.Frame(self.canvas, bg="#031A33")
        self.left_frame2.pack(expand=True, side="right", fill="both")
        self.left_frame2.place(x=740,y=365, height=350, width=650)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", expand=True, fill="both")

        # Texto para el nombre
        self.label_nombre = self.canvas.create_text(615.0, 60.0, anchor="nw", text="Buscar", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(960.0, 355.0, text="Editar", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1135.0, 355.0, text="Eliminar", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(960.0, 220.0, text="Refrescar", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1135.0, 220.0, text="Filtrar", fill="#a6a6a6", font=("Bold", 17))

       # Títulos para los Treeviews
        bold_font = font.Font(family="Bold", size=15, weight="bold")
        self.label_clientes = tk.Label(self.left_frame, text="Tabla Clientes", bg="#031A33", fg="#a6a6a6", font=bold_font)
        self.label_clientes.place(x=205.0, y=5.0, width=237.0, height=38.0)

        self.label_libros_prestado = tk.Label(self.left_frame1, text="Tabla Libros Prestados", bg="#031A33", fg="#a6a6a6", font=bold_font)
        self.label_libros_prestado.place(x=220.0, y=5.0, width=237.0, height=38.0)

        self.label_prestamos = tk.Label(self.left_frame2, text="Tabla Prestamos", bg="#031A33", fg="#a6a6a6", font=bold_font)
        self.label_prestamos.place(x=215.0, y=5.0, width=237.0, height=38.0)

        styleboton = ttk.Style()
        styleboton.configure("Rounded.TEntry", 
                        fieldbackground="#031A33", 
                        foreground="#a6a6a6", 
                        borderwidth=0.5, 
                        relief="solid", 
                        padding=5)
        styleboton.map("Rounded.TEntry",
                  focuscolor=[('focus', '#FFFFFF')],
                  bordercolor=[('focus', '#000716')])
        #Título de boton buscar
        self.buscar = ttk.Entry(self, style="Rounded.TEntry")
        self.buscar.place(x=615.0, y=90.0, width=267.0, height=48.0)
        # Para llamar a read_books cuando se presiona Enter
        self.buscar.bind("<Return>", self.boton_buscar)

        #Boton Clientes
        # Cargar y almacenar las imágenes
        self.images['boton_refrescar'] = tk.PhotoImage(file=relative_to_assets("16.png"))
        # Cargar y almacenar la imagen del botón
        self.button_c = tk.Button(
            self,
            image=self.images['boton_refrescar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: lists_clients(self) or lists_clients_loans(self) or lists_books_loans(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_c.place(x=915.0, y=110.0, width=90.0, height=100.0)

        #Boton Filtrar
        # Cargar y almacenar las imágenes
        self.images['boton_filtrar_f'] = tk.PhotoImage(file=relative_to_assets("15.png"))
        # Cargar y almacenar la imagen del botón
        self.button_f = tk.Button(
            self,
            image=self.images['boton_filtrar_f'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_filter_window(parent),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_f.place(x=1070.0, y=110.0, width=130.0, height=100.0)

        #Boton Modificar
        # Cargar y almacenar las imágenes
        self.images['boton_modificar'] = tk.PhotoImage(file=relative_to_assets("6_editar.png"))
        # Cargar y almacenar la imagen del botón
        self.button_m = tk.Button(
            self,
            image=self.images['boton_modificar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_filter_window_modify(parent),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_m.place(x=915.0, y=240.0, width=90.0, height=100.0)

        self.images['boton_Eliminar_f'] = tk.PhotoImage(file=relative_to_assets("7_eliminar.png"))
        
        # Cargar y almacenar la imagen del botón
        self.button_d = tk.Button(
            self,
            image=self.images['boton_Eliminar_f'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: delete_selected_cliente(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"  # Color del texto cuando el botón está activo
        )
        self.button_d.place(x=1090, y=240.0, width=90.0, height=100.0)

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
    # Tabla de clientes mostrados en el Treeview
        #Columnas Clientes
        columns = ("ID", "Cedula", "Nombre", "Apellido", "Telefono", "Direccion")
        self.book_table = ttk.Treeview(self.left_frame, columns=columns, show='headings', style="Rounded.Treeview")
        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, width=30)
        self.book_table.pack(expand=True, fill="both", padx=80, pady=45)
        #Columnas Libro Prestamo
        columns1 = ("ID Libro Prestamo", "ID Libro", "ID Prestamo", "Cantidad")
        self.libro_prestamo_table = ttk.Treeview(self.left_frame1, columns=columns1, show='headings', style="Rounded.Treeview")
        for col1 in columns1:
            self.libro_prestamo_table.heading(col1, text=col1)
            self.libro_prestamo_table.column(col1, width=40)
        self.libro_prestamo_table.pack(expand=True, fill="both", padx=80, pady=45)
        #Columnas Prestamo
        columns2 = ("ID Prestamo", "ID Cliente", "Usuario", "ID Libro Prestamo", "F.Registro", "F.Limite")
        self.prestamo_table = ttk.Treeview(self.left_frame2, columns=columns2, show='headings', style="Rounded.Treeview")
        for col2 in columns2:
            self.prestamo_table.heading(col2, text=col2)
            self.prestamo_table.column(col2, width=10)
        self.prestamo_table.pack(expand=True, fill="both", padx=45, pady=45)
        # Agregar scrollbar a cada tabla
        scrollbar_bt = ttk.Scrollbar(self.book_table, orient="vertical", command=self.book_table.yview)
        self.book_table.configure(yscrollcommand=scrollbar_bt.set)
        scrollbar_bt.pack(side="right", fill="y")

        scrollbar_lpt = ttk.Scrollbar(self.libro_prestamo_table, orient="vertical", command=self.libro_prestamo_table.yview)
        self.libro_prestamo_table.configure(yscrollcommand=scrollbar_lpt.set)
        scrollbar_lpt.pack(side="right", fill="y")

        scrollbar_pt = ttk.Scrollbar(self.prestamo_table, orient="vertical", command=self.prestamo_table.yview)
        self.prestamo_table.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
        #Estilos para las tablas
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#75C99A")
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25, background="white")
  
    def boton_buscar(self,event):  
        busqueda = self.buscar.get()
        try:
             mariadb_conexion = mariadb.connect(
                                        host='localhost',
                                        port='3306',
                                        password='2525',
                                        database='basedatosbiblioteca'
            )
             if mariadb_conexion.is_connected():
                        cursor = mariadb_conexion.cursor()
                        self.book_table.delete(*self.book_table.get_children())
                        self.libro_prestamo_table.delete(*self.libro_prestamo_table.get_children())
                        self.prestamo_table.delete(*self.prestamo_table.get_children())
                         # Ejecutar y procesar la primera consulta
                        cursor.execute("""SELECT ID_Cliente, Cedula_Cliente, Nombre,
                                        Apellido, Telefono, Direccion FROM cliente WHERE 
                                        ID_Cliente=%s OR Cedula_Cliente=%s OR 
                                        Nombre=%s OR Apellido=%s OR Telefono=%s OR Direccion=%s""", 
                                    (busqueda, busqueda, busqueda, busqueda, busqueda, busqueda))
                        resultados_cliente = cursor.fetchall() 
                        for fila in resultados_cliente:
                            self.book_table.insert("", "end", values=tuple(fila))
                        # Ejecutar y procesar la segunda consulta
                        cursor.execute("""SELECT ID_Libro_Prestamo, ID_Libro, ID_Prestamo, Cantidad FROM libros_prestamo WHERE 
                                        ID_Libro_Prestamo=%s OR ID_Libro=%s OR ID_Prestamo=%s OR Cantidad=%s""", 
                                    (busqueda, busqueda, busqueda, busqueda))
                        resultados_libro_prestamo = cursor.fetchall()
                        for fila in resultados_libro_prestamo:
                            self.libro_prestamo_table.insert("", "end", values=tuple(fila))
                        # Ejecutar y procesar la tercera consulta
                        cursor.execute("""SELECT ID_Prestamo, ID_Cliente, ID_Usuario, ID_Libro_Prestamo, Fecha_Registro, Fecha_Limite FROM prestamo WHERE 
                                        ID_Prestamo=%s OR ID_Cliente=%s OR ID_Libro_Prestamo=%s""", 
                                    (busqueda, busqueda, busqueda))
                        resultados_prestamo = cursor.fetchall()
                        for fila in resultados_prestamo:
                            self.prestamo_table.insert("", "end", values=tuple(fila))
                        for fila in resultados_cliente + resultados_libro_prestamo + resultados_prestamo:
                            if busqueda in fila:
                                if self.book_table.get_children():
                                    self.book_table.item(self.book_table.get_children()[-1], tags='match')
                                if self.libro_prestamo_table.get_children():
                                    self.libro_prestamo_table.item(self.libro_prestamo_table.get_children()[-1], tags='match')
                                if self.prestamo_table.get_children():
                                    self.prestamo_table.item(self.prestamo_table.get_children()[-1], tags='match')
                            else:
                                if self.book_table.get_children():
                                    self.book_table.item(self.book_table.get_children()[-1], tags='nomatch')
                                if self.libro_prestamo_table.get_children():
                                    self.libro_prestamo_table.item(self.libro_prestamo_table.get_children()[-1], tags='nomatch')
                                if self.prestamo_table.get_children():
                                    self.prestamo_table.item(self.prestamo_table.get_children()[-1], tags='nomatch')
                        self.book_table.tag_configure('match', background='green')
                        self.book_table.tag_configure('nomatch', background='gray')
                        self.libro_prestamo_table.tag_configure('match', background='green')
                        self.libro_prestamo_table.tag_configure('nomatch', background='gray')
                        self.prestamo_table.tag_configure('match', background='green')
                        self.prestamo_table.tag_configure('nomatch', background='gray')
                        if resultados_cliente or resultados_prestamo or resultados_libro_prestamo:
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

        tk.Label(filter_window, text="TABLA CLIENTES", fg="black", bg="white", font=("Helvetica", 15)).pack(pady=20,expand=False)#grid(row=0, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese el número de cédula", fg="black", bg="white").pack(pady=5, expand=False)
        tk.Label(filter_window, text="Cedula", fg="black", bg="white").pack(pady=5,expand=False)#grid(row=1, column=0, padx=10, pady=5)
        self.id_cedula_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_cedula_entry.pack(expand=False)#.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="TABLA LIBRO PRESTAMO", fg="black", bg="white", font=("Helvetica", 15)).pack(pady=20,expand=False)#.grid(row=2, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese el ID de Prestamo", fg="black", bg="white").pack(pady=5, expand=False)
        tk.Label(filter_window, text="ID Prestamo", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=3, column=0, padx=10, pady=5)
        self.id_prestamo_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_prestamo_entry.pack(expand=False)#.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="TABLA PRESTAMOS", fg="black", bg="white", font=("Helvetica", 15)).pack(pady=20,expand=False)#.grid(row=4, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese el ID de Prestamo, Cliente y Libro Prestamo", fg="black", bg="white").pack(pady=10, expand=False)
        tk.Label(filter_window, text="ID Prestamo", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=5, column=0, padx=10, pady=5)
        self.id_prestamo_dos_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_prestamo_dos_entry.pack(expand=False)#.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="ID Cliente", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.id_cliente_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_cliente_entry.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="ID Libro Prestamo", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=7, column=0, padx=10, pady=5)
        self.id_libro_cliente_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_libro_cliente_entry.pack(expand=False)#.grid(row=7, column=1, padx=10, pady=5)

        # Botón para filtrar
        self.filter_button = tk.Button(filter_window, text="Filtrar", bg="#f80000" ,fg="black",command=self.apply_filters)
        self.filter_button.pack(expand=True)#.place(x=390, y=400)

        # Crear un estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TButton", background="#f80000", foreground="black")

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.pack(pady=5, expand=False)
    
    def open_filter_window_modify(self,parent):
        filter_window = tk.Toplevel(self)
        filter_window.title("Modificar")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        
        # Cargar la imagen de fondo
        self.bg_image = tk.PhotoImage(file=relative_to_assets("Fondo Botones V1.png"))
        
        # Crear un Label para la imagen de fondo
        bg_label = tk.Label(filter_window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        

        tk.Label(filter_window, text="Modificación de Préstamos", fg="black", bg="white", font=("Helvetica", 20)).pack(pady=20,expand=False)
        tk.Label(filter_window, text="Ingrese ID del Prestamo a modificar", fg="black", bg="white").pack(pady=5, expand=False)#.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="ID Prestamo", fg="black", bg="white").pack(expand=False)#.grid(row=2, column=0, padx=10, pady=5)
        self.id_prestamo_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_prestamo_entry.pack(expand=False)#.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="Ingrese la nueva cantidad de libros a ingresar", fg="black", bg="white").pack(pady=5, expand=False)#.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="Cantidad", fg="black", bg="white").pack(expand=False)#grid(row=4, column=0, padx=10, pady=5)
        self.cantidad_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.cantidad_entry.pack(expand=False)#.grid(row=4, column=1, padx=10, pady=5)


        tk.Label(filter_window, text="Ingrese la nueva fecha límite", fg="black", bg="white").pack(pady=5, expand=False)#.grid(row=5, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="Fecha Límite", fg="black", bg="white").pack(expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.fecha_limite_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.fecha_limite_entry.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)


        # Botón para filtrar
        self.filter_button = tk.Button(filter_window, text="Modificar", bg="#f80000" ,fg="black",command=self.apply_filters_modify)
        self.filter_button.pack (expand=True)#.place(x=390, y=400)

        # Crear un estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TButton", background="#f80000", foreground="black")

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.pack(pady=5, expand=False)

    def apply_filters_modify(self):
        id_prestamo= self.id_prestamo_entry.get() #self.cota.get()
        cantidad = self.cantidad_entry.get()#self.combobox1.get()
        fecha_limite = self.fecha_limite_entry.get()#self.menu_actual.get() if self.menu_actual else None
        try:
            fecha_limite = datetime.strptime(fecha_limite, '%Y-%m-%d')
        except ValueError:
            messagebox.showinfo("Error", "Por favor, proporciona una fecha válida en el formato YYYY-MM-DD.")
            return
        if id_prestamo:
            respuesta = messagebox.askyesno("Confirmar modificación", "¿Desea modificar?")
            if respuesta:
                if update_client_loans(id_prestamo, cantidad, fecha_limite):
                    messagebox.showinfo("Éxito", "Modificación éxitosa del prestamo del cliente")
                    self.clear_entries_list()
                        #return True
                else:
                    messagebox.showinfo("Fallido", "La modificación del prestamo no pudo ejecutarse.")
                        #return False
            else:
                    messagebox.showinfo("Cancelado", "Modificación cancelada.")
        else:
                messagebox.showinfo("Error", "Por favor, proporciona una ID válida.")

    # def delete_client(self):
    #         ID_Cedula=self.id_ceddelete_entry.get() if self.id_ceddelete_entry else None
    #         if ID_Cedula:
    #             # Confirmación antes de eliminar
    #             respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que desea eliminar al cliente?")
    #             if respuesta:
    #                 if delete_client_loans(ID_Cedula):
    #                     messagebox.showinfo("Éxito", "Eliminación exitosa del cliente.")
    #                 else:
    #                     messagebox.showinfo("Falla en la Eliminación", "El cliente no existe o ya fue eliminado.")
    #             else:
    #                 messagebox.showinfo("Cancelado", "Eliminación cancelada.")
    #         else:
    #             messagebox.showinfo("Error", "Por favor, proporciona una ID válida.")
        
    #Boton de filtrado del Menú Lista-Prestamos
    def apply_filters(self):
        filter_books_one(self)
        filter_books_two(self)
        filter_books_three(self)

    def clear_entries_list(self):
        self.id_prestamo_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.fecha_limite_entry.delete(0, tk.END)

    def cancelar(self, window):
        window.destroy()  # Esto cerrará la ventana de filtro

        # Vincular el evento de escritura
        # self.n_registro_entry.bind("<KeyRelease>", lambda event: self.format_n_registro(event))

    # def format_n_registro(self, event):
    #     # Obtener el texto actual del campo de entrada
    #     text = self.n_registro_entry.get().replace(".", "")
        
    #     # Formatear el texto para insertar un punto después de las tres primeras cifras
    #     if len(text)> 2:
    #         formatted_text = text[:2] + "." + text[2:]
    #     else:
    #         formatted_text = text

    #     # Actualizar el campo de entrada con el texto formateado
    #     self.n_registro_entry.delete(0, tk.END)
    #     self.n_registro_entry.insert(0, formatted_text)
        
        

class P_Eliminar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#031A33", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Formulario para el eliminar
        self.label_info = self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del cliente a Eliminar de la lista de prestamos", fill="#a6a6a6", font=("Bold", 17))
        
        # Texto para el nombre
        self.label_cedula = self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cedula", fill="#a6a6a6", font=("Bold", 17))
        
        self.input_cedula = tk.Entry(
            self,
            bd=0,
            bg="#031A33",
            fg="#a6a6a6",
            highlightthickness=2,
            highlightbackground="#ffffff", 
            highlightcolor="#ffffff",
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
            command=lambda:delete_client(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"  # Color del texto cuando el botón está activo
        )
        self.button_e.place(x=265.0, y=264.0, width=130.0, height=40.0)

        def delete_client(self):
            ID_Cedula=self.input_cedula.get() if self.input_cedula else None
            if ID_Cedula:
                # Confirmación antes de eliminar
                respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que desea eliminar al cliente?")
                if respuesta:
                    if delete_client_loans(ID_Cedula):
                        messagebox.showinfo("Éxito", "Eliminación exitosa del cliente.")
                    else:
                        messagebox.showinfo("Falla en la Eliminación", "El cliente no existe o ya fue eliminado.")
                else:
                    messagebox.showinfo("Cancelado", "Eliminación cancelada.")
            else:
                messagebox.showinfo("Error", "Por favor, proporciona una ID válida.")
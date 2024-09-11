import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
#from Library.librerias import recoger_sesion, drop_sesion
from Library.db_prestamos import *
from Library.bd_prestamo_listado_Frames2 import *
from Vistas.listas import *
from tkcalendar import Calendar
from datetime import datetime
import random
import subprocess
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
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        self.parent=parent

        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del nuevo cliente a agregar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cedula", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 152.0, anchor="nw", text="Nombre", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 152.0, anchor="nw", text="Apellido", fill="#000000", font=("Montserrat Regular", 15))

        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Numero de teléfono", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Dirección", fill="#000000", font=("Montserrat Regular", 15))
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
        
        #-------------------------------------------------------------------------------
        # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("R_Boton_registrar.png"))

        # # Crear el botón
        # boton_R = self.images['boton_R']
        # boton_R=tk.Button(
        #     self,
        #     image=boton_R,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: register_client(self, parent),
        #     relief="flat",
        # ).place(x=265.0, y=365.0, width=130.0, height=40.0)

        boton_R = self.images['boton_R']
        boton_R = tk.Button(
            self,
            image=boton_R,
            borderwidth=0,
            highlightthickness=0,
            command= self.mostrar_registrar2,
            relief="flat",
        ).place(x=265.0, y=365.0, width=130.0, height=40.0)

    def mostrar_registrar2(self):
        P_Registrar2(self.parent).place(x=0, y=0)
        self.parent.P_frame_registrar.place_forget()
        self.parent.frame_header.lift()
        self.parent.frame_menu.lift()
        
    def register_client(self, parent):
            ID_Cedula= self.input_cedula.get() #self.cota.get()
            nombre = self.input_nombre.get()#self.combobox1.get()
            apellido = self.input_apellido.get()#self.menu_actual.get() if self.menu_actual else None
            telefono= int(self.input_telefono.get()) #self.combobox3.get() if self.combobox3 else None
            direccion=self.input_direccion.get()
            if create_client_loans(ID_Cedula, nombre, apellido, telefono, direccion):
                messagebox.showinfo("Éxito", "Registro éxitoso del cliente.")
                    #return True
            else:
                messagebox.showinfo("Registro fallido", "Cliente no pudo ser registrado.")
                    #return False

class P_Registrar2 (tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        #validate_number = self.register(validate_number_input)
        self.images = {}
        self.parent=parent

        messagebox.showinfo("Selección","Seleccione algún libro")
        self.left_frame = tk.Frame(self.canvas, bg="white")
        self.left_frame.place(x=215,y=155, height=550)
                    
        self.columns = ("ID","Sala", "Categoria", "Asignatura", "Cota", "N. Registro", "Título", "Autor", "Editorial", "Año", "Edición")
        self.book_table = ttk.Treeview(self.left_frame, columns=self.columns, show='headings')
        for col in self.columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, width=90)
            self.book_table.pack(expand=True, fill="both", padx=70, pady=45)
            # Vincular el evento de selección
            #self.book_table.bind("<<TreeviewSelect>>", self.on_row_selected)
            respuesta = messagebox.askyesno("Confirmar elección","¿Elección final?")
            if respuesta:
            # Confirmación antes de eliminar
                self.book_table.bind("<<TreeviewSelect>>", self.on_row_selected)
                self.book_table.tag_configure('match', background='lightgreen')
                respuesta2 = messagebox.askyesno("Confirmar elección")
               #class p_registrar3
                if respuesta2:
                    messagebox.showinfo("Éxito", "Registro éxitoso del cliente.")
                    #return True
                else:
                    messagebox.showinfo("Registro fallido", "Cliente no pudo ser registrado.")

    def on_row_selected(self, event):
        selected_item = event.widget.selection()[0]
        selected_values = event.widget.item(selected_item, "values")
        print("Fila seleccionada:", selected_values)

    def mostrar_registrar2(self):
        P_Registrar3(self.parent).place(x=0, y=0)
        self.parent.P_frame_registrar.place_forget()
        self.parent.frame_header.lift()
        self.parent.frame_menu.lift()
        

class P_Registrar3 (tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        #validate_number = self.register(validate_number_input)
        self.images = {}  
        canvas3 = tk.Canvas(self, bg="white", width=1366, height=768)
        canvas3.pack(side="left", fill="both", expand=False)
        canvas3.create_text(263.0, 106.0, anchor="nw", text="Selecciona el libro para otorgar el prestamo", fill="#4C4C4C", font=("Montserrat Medium", 15))
        canvas3.create_text(263.0, 152.0, anchor="nw", text="Fecha de Registro", fill="#000000", font=("Montserrat Regular", 15))
        canvas3.create_text(520.0, 152.0, anchor="nw", text="Fecha Límite", fill="#000000", font=("Montserrat Regular", 15))
        canvas3.create_text(779.0, 152.0, anchor="nw", text="Cantidad", fill="#000000", font=("Montserrat Regular", 15))
                                                        
        fecha_registro = Calendar(canvas3, selectmode='day', year=2024, month=9, day=3)
        fecha_registro.pack(pady=20)
        fecha_registro.place(x=263.0, y=182.0, width=237.0, height=38.0)
                                
        boton = tk.Button(canvas3, text="Obtener Fecha", command=self.obtener_fecha)
        boton.pack(pady=10)

        fecha_limite = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        fecha_limite.place(x=520.0, y=182.0, width=237.0, height=38.0)
                        
        cantidad = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        cantidad.place(x=779.0, y=182.0, width=237.0, height=37.5)

    def obtener_fecha(self):
        print(self.fecha_registro.get_date())

    def lists_books(self,book_table):
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
                                for row in book_table.get_children():
                                    book_table.delete(row)
                                    
                                    # Insertar los datos en el Treeview
                                for fila in resultados:
                                    book_table.insert("", "end", values=tuple(fila))
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
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        #validate_number = self.register(validate_number_input)
        self.images = {}

        # Crear el marco izquierdo para el menú de navegación
        #Marco listado clientes
        self.left_frame = tk.Frame(self.canvas, bg="white")
        self.left_frame.pack(expand=True, side="left", fill="both")
        self.left_frame.place(x=165,y=155, height=250, width=650)
        #Marco listado libros prestamo
        self.left_frame1 = tk.Frame(self.canvas, bg="white")
        self.left_frame1.pack(expand=True, side="left", fill="both") 
        self.left_frame1.place(x=165,y=365, height=350, width=650)
        #Marco listado prestamo-clientes
        self.left_frame2 = tk.Frame(self.canvas, bg="white")
        self.left_frame2.pack(expand=True, side="right", fill="both")
        self.left_frame2.place(x=740,y=365, height=350, width=650)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", expand=True, fill="both")

        # Texto para el nombre
        self.label_nombre = self.canvas.create_text(635.0, 85.0, anchor="nw", text="Buscar", fill="#000000", font=("Montserrat Regular", 15))
        
        self.buscar = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key")
        self.buscar.place(x=635.0, y=110.0, width=237.0, height=38.0)
        # Para llamar a read_books cuando se presiona Enter
        self.buscar.bind("<Return>", self.boton_buscar)

        #Boton Cargar Libros
        # Cargar y almacenar las imágenes
        self.images['boton_cargar'] = tk.PhotoImage(file=relative_to_assets("Cargar_rojo.png"))
        
        # Cargar y almacenar la imagen del botón
        self.button_l = tk.Button(
            self,
            image=self.images['boton_cargar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: lists_books_loans(self),
            relief="flat"
        )
        self.button_l.place(x=915.0, y=280.0, width=130.0, height=40.0)

        #Boton Clientes
        # Cargar y almacenar las imágenes
        self.images['boton_clientes'] = tk.PhotoImage(file=relative_to_assets("cargar_cliente.png"))
        # Cargar y almacenar la imagen del botón
        self.button_c = tk.Button(
            self,
            image=self.images['boton_clientes'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: lists_clients(self) or lists_clients_loans(self),
            relief="flat"
        )
        self.button_c.place(x=915.0, y=200.0, width=130.0, height=40.0)

        #Boton Filtrar
        # Cargar y almacenar las imágenes
        self.images['boton_filtrar_f'] = tk.PhotoImage(file=relative_to_assets("boton_filtrar.png"))
        # Cargar y almacenar la imagen del botón
        self.button_f = tk.Button(
            self,
            image=self.images['boton_filtrar_f'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_filter_window(parent),
            relief="flat"
        )
        self.button_f.place(x=1095.0, y=200.0, width=130.0, height=40.0)

        #Boton Modificar
        # Cargar y almacenar las imágenes
        self.images['boton_modificar'] = tk.PhotoImage(file=relative_to_assets("M_boton.png"))
        # Cargar y almacenar la imagen del botón
        self.button_m = tk.Button(
            self,
            image=self.images['boton_modificar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_filter_window_modify(parent),
            relief="flat"
        )
        self.button_m.place(x=1095.0, y=280.0, width=130.0, height=40.0)

    # Tabla de clientes mostrados en el Treeview
        #Columnas Clientes
        columns = ("ID", "Cedula", "Nombre", "Apellido", "Telefono", "Direccion")
        self.book_table = ttk.Treeview(self.left_frame, columns=columns, show='headings')
        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, width=30)
        self.book_table.pack(expand=True, fill="both", padx=80, pady=45)
        #Columnas Libro Prestamo
        columns1 = ("ID Libro Prestamo", "ID Libro", "ID Prestamo", "Cantidad")
        self.libro_prestamo_table = ttk.Treeview(self.left_frame1, columns=columns1, show='headings')
        for col1 in columns1:
            self.libro_prestamo_table.heading(col1, text=col1)
            self.libro_prestamo_table.column(col1, width=40)
        self.libro_prestamo_table.pack(expand=True, fill="both", padx=80, pady=45)
        #Columnas Prestamo
        columns2 = ("ID Prestamo", "ID Cliente", "Usuario", "ID Libro Prestamo", "F.Registro", "F.Limite")
        self.prestamo_table = ttk.Treeview(self.left_frame2, columns=columns2, show='headings')
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
                        cursor.execute("""SELECT ID_Cliente, ID_Prestamo, Cedula_Cliente, Nombre,
                                        Apellido, Telefono, Direccion FROM cliente WHERE 
                                        ID_Cliente=%s OR ID_Prestamo=%s OR Cedula_Cliente=%s OR 
                                        Nombre=%s OR Apellido=%s OR Telefono=%s OR Direccion=%s""", 
                                    (busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda))
                        resultados_cliente = cursor.fetchall() 
                        for fila in resultados_cliente:
                            self.book_table.insert("", "end", values=tuple(fila))
                        # Ejecutar y procesar la segunda consulta
                        cursor.execute("""SELECT ID_Libro_Prestamo, ID_Prestamo, Cantidad FROM libros_prestamo WHERE 
                                        ID_Libro_Prestamo=%s OR ID_Libro=%s OR ID_Prestamo=%s OR Cantidad=%s""", 
                                    (busqueda, busqueda, busqueda, busqueda))
                        resultados_libro_prestamo = cursor.fetchall()
                        for fila in resultados_libro_prestamo:
                            self.libro_prestamo_table.insert("", "end", values=tuple(fila))
                        # Ejecutar y procesar la tercera consulta
                        cursor.execute("""SELECT ID_Prestamo, ID_Cliente, ID_Libro_Prestamo FROM prestamo WHERE 
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

        self.bg_image = tk.PhotoImage(file=relative_to_assets("logo_biblioteca.png"))
        # Crear un Label para la imagen de fondo
        bg_label = tk.Label(filter_window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(filter_window, text="TABLA CLIENTES", fg="black", bg="white", font=("Helvetica", 15)).pack(pady=20,expand=False)#grid(row=0, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese el número de cédula", fg="black", bg="white").pack(pady=10, expand=False)
        tk.Label(filter_window, text="Cedula", fg="black", bg="white").pack(pady=10,expand=False)#grid(row=1, column=0, padx=10, pady=5)
        self.id_cedula_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_cedula_entry.pack(expand=False)#.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="TABLA LIBRO PRESTAMO", fg="black", bg="white", font=("Helvetica", 15)).pack(pady=20,expand=False)#.grid(row=2, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese el ID de Prestamo", fg="black", bg="white").pack(pady=10, expand=False)
        tk.Label(filter_window, text="ID Prestamo", fg="black", bg="white").pack(pady=10,expand=False)#.grid(row=3, column=0, padx=10, pady=5)
        self.id_prestamo_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_prestamo_entry.pack(expand=False)#.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="TABLA PRESTAMOS", fg="black", bg="white", font=("Helvetica", 15)).pack(pady=20,expand=False)#.grid(row=4, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese el ID de Prestamo, Cliente y Libro Prestamo", fg="black", bg="white").pack(pady=10, expand=False)
        tk.Label(filter_window, text="ID Prestamo", fg="black", bg="white").pack(pady=10,expand=False)#.grid(row=5, column=0, padx=10, pady=5)
        self.id_prestamo_dos_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_prestamo_dos_entry.pack(expand=False)#.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="ID Cliente", fg="black", bg="white").pack(pady=10,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.id_cliente_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_cliente_entry.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="ID Libro Prestamo", fg="black", bg="white").pack(pady=10,expand=False)#.grid(row=7, column=0, padx=10, pady=5)
        self.id_libro_cliente_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_libro_cliente_entry.pack(expand=False)#.grid(row=7, column=1, padx=10, pady=5)

        # Botón para filtrar
        self.filter_button = tk.Button(filter_window, text="Filtrar", bg="#f80000" ,fg="black",command=self.apply_filters)
        self.filter_button.pack(expand=True)#.place(x=390, y=400)
    
    def open_filter_window_modify(self,parent):
        filter_window = tk.Toplevel(self)
        filter_window.title("Modificar")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        
        # Cargar la imagen de fondo
        self.bg_image = tk.PhotoImage(file=relative_to_assets("logo_biblioteca.png"))
        
        # Crear un Label para la imagen de fondo
        bg_label = tk.Label(filter_window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        

        tk.Label(filter_window, text="Modificación de Préstamos", fg="black", bg="white", font=("Helvetica", 20)).pack(pady=20,expand=False)
        tk.Label(filter_window, text="Ingrese ID del Prestamo a modificar", fg="black", bg="white").pack(pady=10, expand=False)#.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="ID Prestamo", fg="black", bg="white").pack(expand=False)#.grid(row=2, column=0, padx=10, pady=5)
        self.id_prestamo_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_prestamo_entry.pack(expand=False)#.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="Ingrese la nueva cantidad de libros a ingresar", fg="black", bg="white").pack(pady=10, expand=False)#.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="Cantidad", fg="black", bg="white").pack(expand=False)#grid(row=4, column=0, padx=10, pady=5)
        self.cantidad_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.cantidad_entry.pack(expand=False)#.grid(row=4, column=1, padx=10, pady=5)


        tk.Label(filter_window, text="Ingrese la nueva fecha límite", fg="black", bg="white").pack(pady=10, expand=False)#.grid(row=5, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="Fecha Límite", fg="black", bg="white").pack(expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.fecha_limite_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.fecha_limite_entry.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)


        # Botón para filtrar
        self.filter_button = tk.Button(filter_window, text="Modificar", bg="#f80000" ,fg="black",command=self.apply_filters_modify)
        self.filter_button.pack (expand=True)#.place(x=390, y=400)

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
        
    #Boton de filtrado del Menú Lista-Prestamos
    def apply_filters(self):
        filter_books_one(self)
        filter_books_two(self)
        filter_books_three(self)

    def clear_entries_list(self):
        self.id_prestamo_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
        self.fecha_limite_entry.delete(0, tk.END)

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
            command=lambda:delete_client(self),
            relief="flat"
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
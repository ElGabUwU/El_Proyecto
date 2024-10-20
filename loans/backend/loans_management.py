import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import font
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from loans.backend.db_loans import *
from Library.bd_prestamo_listado_Frames2 import *
from tkcalendar import Calendar
from datetime import datetime, timedelta
import random
import string
from backend.loans_filters import *
from db.conexion import establecer_conexion
from util.Reporte_PDF import generar_pdf
from loans.backend.models import Cliente, Libro
from validations import loans_validations


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

        
class P_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.parent = parent
        #validate_number = self.register(validate_number_input)
        self.images = {}

        self.left_frame2 = tk.Frame(self.canvas, bg="#FAFAFA")
        self.left_frame2.pack(expand=True, side="right", fill="both")
        self.left_frame2.place(x=200,y=220, height=490, width=1180)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", expand=True, fill="both")

        # Texto para el nombre

        self.label_nombre = self.canvas.create_text(265.0, 100.0, anchor="nw", text="Buscar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1035.0, 200.0, text="Editar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1135.0, 200.0, text="Eliminar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(735.0, 200.0, text="Imprimir", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(835.0, 200.0, text="Refrescar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(935.0, 200.0, text="Agregar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1235.0, 200.0, text="Filtrar", fill="#031A33", font=("Bold", 17))

       # Títulos para los Treeviews
        bold_font = font.Font(family="Bold", size=15, weight="bold")
        self.label_prestamos = tk.Label(self.left_frame2, text="Tabla Prestamos", bg="#FAFAFA", fg="#031A33", font=bold_font)
        self.label_prestamos.place(x=445.0, y=4.0, width=237.0, height=35.0)


        self.buscar = tk.Entry(self, bg="#FAFAFA", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.buscar.place(x=265.0, y=130.0, width=267.0, height=48.0)
        self.buscar.bind("<Return>", self.boton_buscar)
        self.images['boton_imprimir'] = tk.PhotoImage(file=relative_to_assets("4_imprimir.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_imprimir'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.imprimir_seleccionado(),
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=695.0, y=90.0, width=90.0, height=100.0)
        # Cargar y almacenar las imágenes
        self.images['boton_agregar'] = tk.PhotoImage(file=relative_to_assets("5_agregar.png"))
        # Cargar y almacenar la imagen del botón
        self.button_c = tk.Button(
            self,
            image=self.images['boton_agregar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_register_loan(),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_c.place(x=890.0, y=90.0, width=90.0, height=100.0)

        self.images['boton_refrescar'] = tk.PhotoImage(file=relative_to_assets("16_refrescar.png"))
        # Cargar y almacenar la imagen del botón
        self.button_c = tk.Button(
            self,
            image=self.images['boton_refrescar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: lists_clients_loans(self), #or lists_clients(self),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_c.place(x=790.0, y=90.0, width=90.0, height=100.0)

        #Boton Filtrar
        # Cargar y almacenar las imágenes
        self.images['boton_filtrar_f'] = tk.PhotoImage(file=relative_to_assets("14_filtrar.png"))
        # Cargar y almacenar la imagen del botón
        self.button_f = tk.Button(
            self,
            image=self.images['boton_filtrar_f'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_filter_window(parent),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_f.place(x=1190.0, y=90.0, width=90.0, height=100.0)

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
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_m.place(x=990.0, y=90.0, width=90.0, height=100.0)

        self.images['boton_Eliminar_f'] = tk.PhotoImage(file=relative_to_assets("7_eliminar.png"))
        
        # Cargar y almacenar la imagen del botón
        self.button_d = tk.Button(
            self,
            image=self.images['boton_Eliminar_f'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.verificar_eliminar(),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"  # Color del texto cuando el botón está activo
        )
        self.button_d.place(x=1090, y=90.0, width=90.0, height=100.0)

        styletrees = ttk.Style()
        styletrees.configure("Rounded.Treeview", 
                        borderwidth=2, 
                        relief="groove", 
                        bordercolor="blue", 
                        lightcolor="lightblue", 
                        darkcolor="darkblue",
                        rowheight=30,

                        # background="#FFFFFF", 
                        # fieldbackground="#f0f0f0")

                        background="#E5E1D7", 
                        fieldbackground="#z")


        # Configurar estilo para las cabeceras
        styletrees.configure("Rounded.Treeview.Heading", 
                        font=('Helvetica', 10, 'bold'), 
                        background="#2E59A7", 
                        foreground="#000000",
                        borderwidth=0)

        #Columnas Prestamo
        columns2 = ("ID Prestamo", "ID Libro", "ID Cliente","Nombre","ID Libro Prestamo", "Titulo","Ejemplares", "F.Registro", "F.Limite", "Encargado")
        self.prestamo_table = ttk.Treeview(self.left_frame2, columns=columns2, show='headings', style="Rounded.Treeview")
        for col2 in columns2:
            self.prestamo_table.heading(col2, text=col2)
            self.prestamo_table.column(col2, width=90, anchor="center")
        self.prestamo_table.pack(expand=True, fill="both", padx=40, pady=45)

        self.prestamo_table.bind("<Double-1>", self.on_loans_double_click)#SELECCION DE TODOS LOS EJEMPLARES CON DOBLE CLICK
        scrollbar_pt = ttk.Scrollbar(self.prestamo_table, orient="vertical", command=self.prestamo_table.yview)
        self.prestamo_table.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
    
    def imprimir_seleccionado(self):
        selected_items = self.prestamo_table.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún préstamo.")
            return

        selected_item = self.prestamo_table.item(selected_items[0], 'values')
        imprimir = ImprimirPrestamo(selected_item)
        imprimir.obtener_datos()
    
    def verificar_eliminar(self):
        if self.parent.id_rol == 1:
            print("Sin permisos suficientes para eliminar!")
            messagebox.showinfo("AVISO", "Sin permisos suficientes para eliminar!")
        
        else:
            delete_selected_prestamo(self)
    
    def open_register_loan(self):
        register_loan_window = tk.Toplevel(self)
        register_loan_window.title("Registrar Préstamo")
        register_loan_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        register_loan_window.geometry("1355x600")
        register_loan_window.config(bg="#042344")
        register_loan_window.resizable(False, False)
        register_loan_window.grab_set()
        register_loan_window.protocol("WM_DELETE_WINDOW", lambda:self.cancelar(register_loan_window))
        self.register_loan_window=register_loan_window

        # Crear el marco izquierdo para el menú de navegación
        self.left_frame_list = tk.Frame(register_loan_window, bg="#042344")
        self.left_frame_list.place(x=170, y=160, height=400, width=1200)
        
        rectangulo_color = tk.Label(register_loan_window, bg="#2E59A7", width=200, height=3)
        rectangulo_color.place(x=0, y=0)  # Posición del rectángulo dentro de la ventana
        tk.Label(register_loan_window, text="Tabla Prestamos",fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=505.0, y=8.0, width=450.0, height=35.0)
        tk.Label(register_loan_window, text="ID Cliente", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=600.0, y=70.0, width=160.0, height=35.0)
        self.id_cliente = tk.Entry(register_loan_window,  bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.id_cliente.place(x=630.0, y=100.0, width=190.0, height=35.0)

        tk.Label(register_loan_window, text="Fecha Registrar", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=22.0, y=140.0, width=160.0, height=35.0)
        self.fecha_registrar = tk.Entry(register_loan_window,  bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.fecha_registrar.place(x=20.0, y=170.0, width=170.0, height=35.0)
        
        
        tk.Label(register_loan_window, text="Fecha Limite", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=7.0, y=240.0, width=160.0, height=35.0)
        self.fecha_limite = tk.Entry(register_loan_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.fecha_limite.place(x=20.0, y=270.0, width=170.0, height=35.0)

        # tk.Label(filter_window, text="Cantidad", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=15.0, y=340, width=105.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        # self.input_cantidad = tk.Entry(filter_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        # self.input_cantidad.place(x=20.0, y=370.0, width=170.0, height=35.0)#.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)

        # Establecer las fechas automáticamente
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        fecha_limite = (datetime.now() + timedelta(days=20)).strftime("%d/%m/%Y")

        self.fecha_registrar.insert(0, fecha_actual)
        self.fecha_limite.insert(0, fecha_limite)
        # Configurar los campos de entrada como solo lectura
        self.fecha_registrar.config(state='readonly')
        self.fecha_limite.config(state='readonly')

        # Aplica el estilo al Treeview listado de libros
        tree = ("ID", "Sala", "Categoria", "Asignatura", "Cota", "N° Registro", "Titulo", "Autor", "Editorial", "Año", "Edición", "N° Ejemplares", "N° Volúmenes")
        self.book_table_list = ttk.Treeview(self.left_frame_list, columns=tree, show='headings', style="Rounded.Treeview")

        # Set specific widths for "ID" and "Sala"
        self.book_table_list.column("ID", width=40, anchor="center")
        self.book_table_list.column("Sala", width=40, anchor="center")
        self.book_table_list.column("Cota", width=30, anchor="center")
        self.book_table_list.column("N° Registro", width=50, anchor="center")
        self.book_table_list.column("Titulo", width=100, anchor="center")
        self.book_table_list.column("Año", width=30, anchor="center")
        self.book_table_list.column("Edición", width=30, anchor="center")
        self.book_table_list.column("N° Ejemplares", width=70, anchor="center")
        self.book_table_list.column("N° Volúmenes", width=70, anchor="center")

        # Set larger widths for the other columns
        for col in tree:
            if col not in ("ID", "Sala","Cota","N° Registro", "Titulo", "Año","N° Ejemplares", "N° Volúmenes"):
                self.book_table_list.column(col, width=95, anchor="center")
            self.book_table_list.heading(col, text=col)

        self.book_table_list.pack(expand=True, fill="both", padx=30, pady=5)

        scrollbar_pt = ttk.Scrollbar(self.book_table_list, orient="vertical", command=self.book_table_list.yview)
        self.book_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")

        # Asociar el evento de selección del Treeview a la función on_treeview_select
        self.book_table_list.bind('<<TreeviewSelect>>', self.on_treeview_select)

        self.reading_books(self.book_table_list)

        self.images['boton_r'] = tk.PhotoImage(file=relative_to_assets("R_button_light_blue.png"))

        self.boton_R = tk.Button(
            register_loan_window,
            image=self.images['boton_r'],
            borderwidth=0,
            highlightthickness=0,
            command=self.save_modifications,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_R.place(x=265.0, y=450.0, width=130.0, height=40.0)
        self.boton_R.place_forget()  # Ocultar el botón inicialmente

        self.id_cliente.bind("<KeyRelease>", lambda event: loans_validations.validate_entries(self, event))

        # self.input_cantidad.bind("<KeyRelease>", self.validate_entries)

    def boton_buscar(self,event=None):  
        busqueda = self.buscar.get()
        try:
             mariadb_conexion = establecer_conexion()
             if mariadb_conexion:
                        cursor = mariadb_conexion.cursor()
                        self.prestamo_table.delete(*self.prestamo_table.get_children())
                         # Ejecutar y procesar la primera consulta
                        cursor.execute("""SELECT prestamo.ID_Prestamo, cliente.ID_Cliente, cliente.Nombre, 
                        libro.ID_Libro, libro.titulo, libro.n_ejemplares, prestamo.Fecha_Registro, 
                        prestamo.Fecha_Limite, prestamo.ID_Usuario
                        FROM prestamo 
                        JOIN cliente ON prestamo.ID_Cliente = cliente.ID_Cliente 
                        JOIN libro ON prestamo.ID_Libro = libro.ID_Libro 
                        WHERE cliente.ID_Cliente=%s OR cliente.Nombre=%s OR cliente.Apellido=%s 
                                OR libro.ID_Libro=%s OR libro.titulo=%s 
                                OR prestamo.ID_Prestamo=%s OR prestamo.ID_Usuario=%s""", 
                        (busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda))
                        resultados_prestamo = cursor.fetchall() 
                        for fila in resultados_prestamo:
                            if busqueda in fila:
                                 if self.prestamo_table.get_children():
                                     self.prestamo_table.item(self.prestamo_table.get_children()[-1], tags='match')
                            else:
                                if self.prestamo_table.get_children():
                                    self.prestamo_table.item(self.prestamo_table.get_children()[-1], tags='nomatch')
                        self.prestamo_table.tag_configure('match', background='green')
                        self.prestamo_table.tag_configure('nomatch', background='gray')
                        if resultados_prestamo:
                            messagebox.showinfo("Busqueda Éxitosa", "Resultados en pantalla.")
                        else:
                            messagebox.showinfo("Busqueda Fallida", "No se encontraron resultados.")
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
        finally:
            if mariadb_conexion:
                mariadb_conexion.close()
    
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

    def open_filter_window(self,parent):
        filter_window = tk.Toplevel(self)
        filter_window.title("Filtrar")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        filter_window.geometry("950x450")
        filter_window.config(bg="#042344")
        
        filter_window.resizable(False, False)
        filter_window.grab_set()
        filter_window.protocol("WM_DELETE_WINDOW", lambda:self.cancelar(filter_window))
        rectangulo_color = tk.Label(filter_window, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)
        
        tk.Label(filter_window, text="Tabla de Prestamos", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=250.0, y=20.0, width=450.0, height=35.0)
        tk.Label(filter_window, text="Ingrese el ID de Prestamo, Cliente y Libro Prestamo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=10.0, y=80.0, width=530.0, height=35.0)
        tk.Label(filter_window, text="ID Prestamo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=240.0, y=130.0, width=120.0, height=35.0)
        self.id_prestamos_entry = tk.Entry(filter_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.id_prestamos_entry.place(x=240.0, y=170.0, width=190.0, height=35.0)

        tk.Label(filter_window, text="ID Cliente", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=460.0, y=130.0, width=185.0, height=35.0)
        self.id_cliente_entry = tk.Entry(filter_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.id_cliente_entry.place(x=500.0, y=170.0, width=190.0, height=35.0)

        tk.Label(filter_window, text="ID Libro Prestamo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=240.0, y=230.0, width=180.0, height=35.0)
        self.id_libro_cliente_entry = tk.Entry(filter_window,  bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.id_libro_cliente_entry.place(x=240.0, y=270.0, width=190.0, height=35.0)

        
        self.images['boton_m'] = tk.PhotoImage(file=relative_to_assets("boton_filtrar.png"))

        self.boton_M = tk.Button(
            filter_window,
            image=self.images['boton_m'],
            borderwidth=0,
            highlightthickness=0,
            command=self.apply_filters,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_M.place(x=530.0, y=350.0, width=130.0, height=40.0)
        
        self.images['boton_c'] = tk.PhotoImage(file=relative_to_assets("L_cancelar.png"))

        self.boton_C = tk.Button(
            filter_window,
            image=self.images['boton_c'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.cancelar(filter_window),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_C.place(x=270.0, y=350.0, width=130.0, height=40.0)
         # Crear un estilo personalizado
        """style = ttk.Style()
        style.configure("Custom.TButton", background="#2E59A7", foreground="#ffffff", font=("Bold", 22))

        # Botón para filtrar
        self.filter_button = ttk.Button(filter_window, text="Filtrar", style="Custom.TButton", command=self.apply_filters)
        self.filter_button.place(x=250.0, y=480.0, width=140.0, height=50.0)#.pack(expand=True)#.place(x=390, y=400)

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.place(x=520.0, y=480.0, width=140.0, height=50.0)#.pack(pady=5, expand=False)"""
    
    def open_filter_window_modify(self,parent):
        filter_window = tk.Toplevel(self)
        filter_window.title("Modificar Préstamo")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        filter_window.geometry("950x550")
        filter_window.config(bg="#042344")
        filter_window.resizable(False, False)
        filter_window.grab_set()
        filter_window.protocol("WM_DELETE_WINDOW", lambda:self.cancelar(filter_window))
        rectangulo_color = tk.Label(filter_window, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)
        tk.Label(filter_window, text="Modificación De Préstamo", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=235.0, y=15.0, width=450.0, height=35.0)#.pack(pady=20,expand=False)#grid(row=0, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese los datos a modificar", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=10.0, y=80.0, width=330.0, height=35.0)#.pack(pady=10, expand=False)
        tk.Label(filter_window, text="Fecha Limite", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=227.0, y=140.0, width=130.0, height=35.0)#.pack(pady=10,expand=False)#grid(row=1, column=0, padx=10, pady=5)
        self.fecha_limite_entry = tk.Entry(filter_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.fecha_limite_entry.place(x=230.0, y=180.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="Cantidad", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=439.0, y=140.0, width=185.0, height=35.0)#.pack(pady=10,expand=False)#.grid(row=3, column=0, padx=10, pady=5)
        self.cantidad_entry = tk.Entry(filter_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.cantidad_entry.place(x=490.0, y=180.0, width=190.0, height=35.0)#pack(expand=False)#.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="ID del prestamo que será modificado", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=30.0, y=255.0, width=368.0, height=35.0)#.pack(pady=10, expand=False)
        tk.Label(filter_window, text="ID", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=315.0, y=315.0, width=120.0, height=35.0)#.pack(pady=10,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.id_prestamo_entry = tk.Entry(filter_window,  bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.id_prestamo_entry.place(x=365.0, y=355.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)

        # Crear un estilo personalizado
        self.images['boton_m'] = tk.PhotoImage(file=relative_to_assets("M_button_light_blue.png"))

        self.boton_M = tk.Button(
            filter_window,
            image=self.images['boton_m'],
            borderwidth=0,
            highlightthickness=0,
            command=self.apply_filters_modify,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_M.place(x=530.0, y=450.0, width=130.0, height=40.0)
        
        self.images['boton_c'] = tk.PhotoImage(file=relative_to_assets("L_cancelar.png"))

        self.boton_C = tk.Button(
            filter_window,
            image=self.images['boton_c'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.cancelar(filter_window),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_C.place(x=270.0, y=450.0, width=130.0, height=40.0)

        """self.filter_button = ttk.Button(filter_window, text="Modificar", style="Custom.TButton", command=self.apply_filters_modify)
        self.filter_button.place(x=250.0, y=480.0, width=140.0, height=50.0)

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.place(x=520.0, y=480.0, width=140.0, height=50.0)#.pack(expand=True)#.place(x=390, y=400)#.pack(pady=5, expand=False)"""

    def apply_filters_modify(self):
        id_prestamo= self.id_prestamo_entry.get() 
        cantidad = self.cantidad_entry.get()
        fecha_limite = self.fecha_limite_entry.get()
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
                    loans_validations.clear_entries_list(self)
                        #return True
                else:
                    messagebox.showinfo("Fallido", "La modificación del prestamo no pudo ejecutarse.")
                        #return False
            else:
                    messagebox.showinfo("Cancelado", "Modificación cancelada.")
        else:
                messagebox.showinfo("Error", "Por favor, proporciona una ID válida.")
    
    def save_modifications(self):
        fecha_registrar = loans_validations.format_date(self.fecha_registrar.get())
        fecha_limite = loans_validations.format_date(self.fecha_limite.get())
        #Cantidad = int(self.input_cantidad.get())
        ID_Prestamo = loans_validations.generate_alphanumeric_id()
        ID_Libro_Prestamo = loans_validations.generate_id_libro_prestamo(self)
        ID_Cliente = self.id_cliente.get()
                # Asegúrate de que ID_Libro esté definido
        if hasattr(self, 'ID_Libro'):
            ID_Libro = self.ID_Libro
        else:
            messagebox.showerror("Error", "Por favor, selecciona un libro de la lista.")
            return
            # Obtener ID_Usuario
        ID_Usuario = 1 or 2 or 3 or 4 or 5
        if ID_Usuario is None:
            messagebox.showerror("Error", "No se pudo obtener el ID de usuario.")
            return
        if create_loan(ID_Prestamo, fecha_registrar, fecha_limite):
            if create_libro_prestamo(ID_Libro_Prestamo, ID_Prestamo, ID_Libro):
                if update_prestamo_with_cliente(ID_Prestamo, ID_Cliente, ID_Libro_Prestamo):
                    if update_prestamo_and_libro(ID_Prestamo, ID_Cliente, ID_Libro, ID_Libro_Prestamo):
                            # Actualizar la tabla prestamo con ID_Usuario
                        if update_prestamo_with_usuario(ID_Prestamo, ID_Usuario):
                             if update_cliente_with_prestamo(ID_Cliente, ID_Prestamo):
                                messagebox.showinfo("Éxito", 
f"""
Registro éxitoso del préstamo. 
ID Préstamo: {ID_Prestamo}
ID Libro Préstamo: {ID_Libro_Prestamo}
""")
                        loans_validations.clear_entries_list(self)
            else:
                messagebox.showerror("Error", "Préstamo no pudo ser creado.")    
    #Boton de filtrado del Menú Lista-Prestamos
    def apply_filters(self):
        filter_books(self)
            
    def cancelar(self, window):
        if messagebox.askyesno("Advertencia", "¿Seguro que quieres cerrar esta ventana?"):
            window.destroy()  # Esto cerrará la ventana de filtro

    def on_treeview_select(self, event):
        # Obtener el elemento seleccionado
        selected_item = self.book_table_list.selection()[0]
        # Obtener los valores del elemento seleccionado
        item_values = self.book_table_list.item(selected_item, 'values')
        # Asumimos que el ID_Libro está en la primera columna
        self.ID_Libro = item_values[0]
    
    # def on_loans_double_click(self, event):
    #     try:
    #         selected_item = self.prestamo_table.selection()[0]
    #         prestamo_valores = self.prestamo_table.item(selected_item, 'values')

    #         self.prestamo_data = {
    #             "ID Prestamo": prestamo_valores[0],
    #             "ID Libro": prestamo_valores[1],
    #             "ID Cliente": prestamo_valores[2],
    #             "Nombre": prestamo_valores[3],
    #             "ID Libro Prestamo": prestamo_valores[4],
    #             "Titulo": prestamo_valores[5],
    #             "Cantidad": prestamo_valores[6],
    #             "F.Registro": prestamo_valores[7],
    #             "F.Limite": prestamo_valores[8],
    #             "Encargado": prestamo_valores[9]  # Asegúrate de que coincida con tu índice
    #         }

    #         mariadb_conexion = establecer_conexion()
    #         if mariadb_conexion:
    #             cursor = mariadb_conexion.cursor()

    #             cursor.execute('''
    #                 SELECT 
    #                 p.ID_Prestamo,
    #                 c.ID_Cliente,
    #                 c.Nombre
    #                 FROM cliente c
    #                 JOIN 
    #                     prestamo p ON p.ID_Cliente = c.ID_Cliente
    #                 WHERE  c.ID_Cliente = %s AND c.Nombre = %s
    #             ''', (self.prestamo_data["ID Cliente"], self.prestamo_data["Nombre"]))

    #             ejemplares = cursor.fetchall()

    #             if not ejemplares:
    #                 messagebox.showinfo("Información", "No se encontraron registros coincidentes.")
    #                 return

    #             self.prestamo_table.selection_remove(self.prestamo_table.selection())

    #             for ejemplar in ejemplares:
    #                 for row in self.prestamo_table.get_children():
    #                     if self.prestamo_table.item(row, 'values')[0] == str(ejemplar[0]):
    #                         self.prestamo_table.selection_add(row)

    #             mariadb_conexion.close()
    #     except mariadb.Error as ex:
    #         print("Error durante la conexión:", ex)
    #         messagebox.showerror("Error", f"Error durante la conexión: {ex}")
    #     except IndexError:
    #         print("No se ha seleccionado ningún préstamo.")
    #         messagebox.showerror("Error", "No se ha seleccionado ningún préstamo.")

    def on_loans_double_click(self, event):
        try:
            selected_item = self.prestamo_table.selection()[0]
            prestamo_valores = self.prestamo_table.item(selected_item, 'values')

            self.prestamo_data = {
                "ID Prestamo": prestamo_valores[0],
                "ID Libro": prestamo_valores[1],
                "ID Cliente": prestamo_valores[2],
                "Nombre": prestamo_valores[3],
                "ID Libro Prestamo": prestamo_valores[4],
                "Titulo": prestamo_valores[5],
                "Cantidad": prestamo_valores[6],
                "F.Registro": prestamo_valores[7],
                "F.Limite": prestamo_valores[8],
                "Encargado": prestamo_valores[9]  # Asegúrate de que coincida con tu índice
            }

            # Convertir las fechas al formato YYYY-MM-DD
            # self.prestamo_data["F.Registro"] = datetime.strptime(self.prestamo_data["F.Registro"], "%d/%m/%Y").strftime("%Y-%m-%d")
            # self.prestamo_data["F.Limite"] = datetime.strptime(self.prestamo_data["F.Limite"], "%d/%m/%Y").strftime("%Y-%m-%d")

            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()

                cursor.execute('''
                    SELECT 
                    p.ID_Prestamo,
                    c.ID_Cliente,
                    c.Nombre,
                    p.Fecha_Registro,
                    p.Fecha_Limite
                    FROM cliente c
                    JOIN 
                        prestamo p ON p.ID_Cliente = c.ID_Cliente
                    WHERE  c.ID_Cliente = %s AND c.Nombre = %s AND p.Fecha_Registro = %s AND p.Fecha_Limite = %s
                ''', (self.prestamo_data["ID Cliente"], self.prestamo_data["Nombre"], self.prestamo_data["F.Registro"], self.prestamo_data["F.Limite"]))

                ejemplares = cursor.fetchall()

                if not ejemplares:
                    messagebox.showinfo("Información", "No se encontraron registros coincidentes.")
                    return

                self.prestamo_table.selection_remove(self.prestamo_table.selection())

                for ejemplar in ejemplares:
                    for row in self.prestamo_table.get_children():
                        if self.prestamo_table.item(row, 'values')[0] == str(ejemplar[0]):
                            self.prestamo_table.selection_add(row)

                mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
            messagebox.showerror("Error", f"Error durante la conexión: {ex}")
        except IndexError:
            print("No se ha seleccionado ningún préstamo.")
            messagebox.showerror("Error", "No se ha seleccionado ningún préstamo.")

class ImprimirPrestamo:
    def __init__(self, selected_item):
        self.selected_item = {
            "ID_Prestamo": selected_item[0],
            "ID_Libro": selected_item[1],
            "ID_Cliente": selected_item[2],
            "Nombre": selected_item[3],
            "ID_Libro_Prestamo": selected_item[4],
            "Titulo": selected_item[5],
            "ejemplares": selected_item[6],
            "fecha_r": selected_item[7],
            "fecha_en": selected_item[8],
            "estado_prestamo": selected_item[9],
        }
        self.user_data = {}
        self.book_data = {}
        self.prestamo = {}
        self.datos_prestamos = self.selected_item.copy()
        print(self.datos_prestamos)

    def obtener_datos(self):
        cliente_id = self.datos_prestamos["ID_Cliente"]
        libro_id = self.datos_prestamos["ID_Libro"]
        print(f"Cliente ID: {cliente_id}, Libro ID: {libro_id}")  # Depuración

        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()

                # Obtener los datos del cliente
                cursor.execute('''
                    SELECT Cedula_Cliente, Nombre, Apellido, Telefono, Direccion
                    FROM cliente
                    WHERE ID_Cliente = %s
                ''', (cliente_id,))
                resultado_cliente = cursor.fetchone()
                print(f"Resultado Cliente: {resultado_cliente}")  # Depuración
                if resultado_cliente:
                    self.user_data = {
                        "Cedula": resultado_cliente[0],
                        "Nombre": resultado_cliente[1],
                        "Apellido": resultado_cliente[2],
                        "Telefono": resultado_cliente[3],
                        "Direccion": resultado_cliente[4]
                    }

                # Crear instancia de Cliente
                cliente = Cliente(
                    cedula=self.user_data["Cedula"],
                    nombre=self.user_data["Nombre"],
                    apellido=self.user_data["Apellido"],
                    telefono=self.user_data["Telefono"],
                    direccion=self.user_data["Direccion"]
                )

                # Obtener los datos del libro
                self.book_data = obtener_datos_libro(libro_id)
                if self.book_data:
                    # Crear instancia de Libro con el orden correcto de los parámetros
                    libro = Libro(
                        cota=self.book_data["Cota"],
                        categoria=self.book_data["ID_Categoria"],
                        sala=self.book_data["ID_Sala"],
                        asignatura=self.book_data["ID_Asignatura"],
                        numero_registro=self.book_data["n_registro"],
                        autor=self.book_data["autor"],
                        titulo=self.book_data["titulo"],
                        num_volumenes=self.book_data["n_volumenes"],
                        num_ejemplares=self.book_data["n_ejemplares"],
                        edicion=self.book_data["edicion"],
                        año=self.book_data["año"],
                        editorial=self.book_data["editorial"]
                    )

                    self.prestamo = {
                        "Cliente": self.user_data,
                        "Libro": self.book_data
                    }

                    print("Prestamo Data:", self.prestamo)

                    # Llamar a generar_reporte_pdf después de obtener los datos
                    fecha_actual = datetime.now().strftime("%d_%m_%Y")
                    nombre_corregido = self.user_data.get("Nombre", "").replace(" ", "_")
                    nombre_archivo_base = f"Reporte_de_prestamo_{nombre_corregido}_{fecha_actual}"
                    generar_pdf(cliente, libro, self.datos_prestamos["fecha_r"], self.datos_prestamos["fecha_en"], nombre_archivo_base)

        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
            messagebox.showerror("Error", f"Error durante la conexión")


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
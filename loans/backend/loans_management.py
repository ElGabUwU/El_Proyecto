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
from util.Reporte_PDF import generate_report_by_day,generate_report_by_month
from loans.backend.models import Cliente, Libro
from validations import loans_validations
from util.utilidades import resource_path
from validations.loans_validations import *
from loans.backend.db_loans import get_cliente_id_by_cedula,get_libro_id_by_registro
from loans.backend.db_loans import load_active_loans, es_novela
from util.ventana import centrar_ventana
from validations.clients_validations import limit_length
from books.backend.db_books import get_book_data,search_books
def validate_number_input(text):
        if text == "":
            return True
        try:
            int(text)
            return True
        except ValueError:
            return False



        
class P_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.parent = parent
        #validate_number = self.register(validate_number_input)
        self.images = {}
        self.id_usuario =self.parent.id_usuario
        self.left_frame2 = tk.Frame(self.canvas, bg="#FAFAFA")
        self.left_frame2.pack(expand=True, side="right", fill="both")
        self.left_frame2.place(x=215,y=218, height=470, width=1135)
        self.id_usuario = self.parent.id_usuario
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", expand=True, fill="both")
        self.data = []
        self.page_size = 19
        self.current_page = 0
        self.warned_about_overdue = False
        self.validate_number = self.register(validate_number_input)
        # Texto para el nombre

        self.label_nombre = self.canvas.create_text(245.0, 82.0, anchor="nw", text="Buscar por Cédula", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1175.0, 170.0, text="Renovar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1275.0, 170.0, text="Eliminar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1075.0, 170.0, text="Agregar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(975.0, 170.0, text="Refrescar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(840.0, 170.0, text="Generar PDF", fill="#031A33", font=("Bold", 17))

       # Títulos para los Treeviews
        bold_font = font.Font(family="Bold", size=15, weight="bold")
        self.label_prestamos = tk.Label(self.canvas, text="Tabla Prestamos", bg="#FAFAFA", fg="#031A33", font=bold_font)
        self.label_prestamos.place(x=665.0, y=185.0, width=237.0, height=35.0)


        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2,validate="key", validatecommand=(self.validate_number, "%P"))
        self.buscar.place(x=245.0, y=112.0, width=267.0, height=48.0)
        self.buscar.bind("<Return>", self.boton_buscar)
        self.buscar.bind("<KeyPress>",self.key_on_press_search)
        self.images['boton_imprimir'] = tk.PhotoImage(file=resource_path("assets_2/pdf-2.png"))#Logo_Imprimir
        
        # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_imprimir'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.show_report_window(),
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=800.0, y=60.0, width=90.0, height=100.0)
        # Cargar y almacenar las imágenes
        self.images['boton_agregar'] = tk.PhotoImage(file=resource_path("assets_2/5_agregar.png"))
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
        self.button_c.place(x=1030.0, y=60.0, width=90.0, height=100.0)

        self.images['boton_refrescar'] = tk.PhotoImage(file=resource_path("assets_2/16_refrescar.png"))
        # Cargar y almacenar la imagen del botón
        self.button_c = tk.Button(
            self,
            image=self.images['boton_refrescar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.refresh_loans_data(),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_c.place(x=930.0, y=60.0, width=90.0, height=100.0)

        #Boton Modificar
        # Cargar y almacenar las imágenes
        self.images['boton_renovar'] = tk.PhotoImage(file=resource_path("assets_2/renovar_12.png"))
        # Cargar y almacenar la imagen del botón
        self.button_m = tk.Button(
            self,
            image=self.images['boton_renovar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.update_selected_loan_due_date(),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_m.place(x=1130.0, y=60.0, width=90.0, height=100.0)

        self.images['boton_Eliminar_f'] = tk.PhotoImage(file=resource_path("assets_2/7_eliminar.png"))
        
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
        self.button_d.place(x=1230.0, y=60.0, width=90.0, height=100.0)
        self.setup_treeview()
        load_active_loans(self)

        
        self.display_page()
        
        
    def setup_treeview(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("RegisterLoanTreeview", 
                            background="#E5E1D7", 
                            foreground="black", 
                            rowheight=30, 
                            fieldbackground="#f0f0f0", 
                            bordercolor="blue", 
                            lightcolor="lightblue", 
                            darkcolor="darkblue")
        self.style.map('RegisterLoanTreeview', 
                    background=[('selected', '#347083')])
        self.style.configure("RegisterLoanTreeview.Heading", 
                            font=('Helvetica', 10, 'bold'), 
                            background="#2E59A7", 
                            foreground="#000000", 
                            borderwidth=0)

        columns2 = ("Cedula", "Cliente", "Nombre del Libro", "N° Registro", "F.Registro", "F.Limite", "Encargado", "ID_Prestamo", "ID_Usuario")
        self.cliente_prestamo_table = ttk.Treeview(self.left_frame2, columns=columns2, show='headings', style="Rounded.Treeview", selectmode="browse")

        for col2 in columns2:
            self.cliente_prestamo_table.heading(col2, text=col2)
            if col2 in ["ID_Prestamo", "ID_Usuario"]:
                self.cliente_prestamo_table.column(col2, width=0, stretch=False)  # Ocultar la columna
            else:
                self.cliente_prestamo_table.column(col2, width=90, anchor="center")
                
        self.cliente_prestamo_table.pack(expand=True, fill="both", padx=30, pady=5)
        scrollbar_pt = ttk.Scrollbar(self.cliente_prestamo_table, orient="vertical", command=self.cliente_prestamo_table.yview)
        self.cliente_prestamo_table.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
        self.images['boton_siguiente'] = tk.PhotoImage(file=resource_path("assets_2/siguiente.png"))
        self.images['boton_anterior'] = tk.PhotoImage(file=resource_path("assets_2/atras.png"))
        prev_button = tk.Button(
            self.left_frame2,
            image=self.images['boton_anterior'],
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#006ac2",   # Color del texto cuando el botón está activo
            command=self.previous_page)
        prev_button.pack(side=tk.LEFT, padx=25, pady=0)
        
        next_button = tk.Button(
            self.left_frame2, 
            image=self.images['boton_siguiente'],
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#006ac2",   # Color del texto cuando el botón está activo
            command=self.next_page)
        next_button.pack(side=tk.RIGHT, padx=25, pady=0)
        self.page_label = tk.Label(self.left_frame2, text=f"Página {self.current_page + 1}", bg="#FAFAFA", fg="#031A33", font=("Montserrat Regular", 13))
        self.page_label.pack(side=tk.BOTTOM, pady=15)
        
        
        
    def refresh_loans_data(self):
        load_active_loans(self)
        mostrar_mensaje_prestamos_vencidos()


    def get_data_page(self, offset, limit):
        return self.data[offset:offset + limit]
    def update_page_label(self):
        total_pages = (len(self.data) + self.page_size - 1) // self.page_size  # Calcular el total de páginas
        self.page_label.config(text=f"Página {self.current_page + 1} de {total_pages}")

    def display_page(self):
        page_data = self.get_data_page(self.current_page * self.page_size, self.page_size)
        hoy = datetime.now().date()
        for fila in page_data:
            # Verificar si la fila ya existe en la tabla
            exists = False
            for row in self.cliente_prestamo_table.get_children():
                if self.cliente_prestamo_table.item(row, 'values') == fila:
                    exists = True
                    break
            if not exists:
                # fecha_limite = datetime.strptime(fila[4], '%d-%m-%Y').strftime('%d-%m-%Y')
                # fecha_limite = datetime.strptime(fecha_limite, '%d-%m-%Y').date()
                # tag = 'vencido' if fecha_limite <= hoy - timedelta(days=3) else 'activo'
                self.cliente_prestamo_table.insert("", "end", values=fila)  # , tags=(tag,))
        # self.cliente_prestamo_table.tag_configure('vencido', background='red')
        # self.cliente_prestamo_table.tag_configure('activo', background='white')
        self.update_page_label()



    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.data):
            self.current_page += 1
            self.display_page()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()


        
        
    def verificar_eliminar(self):
        if self.parent.id_rol == 1:
            print("Sin permisos suficientes para eliminar!")
            messagebox.showinfo("AVISO", "Sin permisos suficientes para eliminar!")
        else:
            delete_selected_prestamo(self)
    
    def open_register_loan(self):
            Register_Loans(self, loans_validations)#loans_validations#client_values

    def key_on_press_search(self, event):
        current_text = self.buscar.get()
        limited_text = limit_length(current_text, 10)
        self.buscar.delete(0, 'end')
        self.buscar.insert(0, limited_text)

    def boton_buscar(self, event=None):  
        busqueda = self.buscar.get().strip()
        
        if not busqueda:
            messagebox.showinfo("Búsqueda Fallida de Préstamos", "No se ingresó ningún término de búsqueda. Por favor, ingrese una cédula para buscar.")
            return
        
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                query = """
                    SELECT c.Cedula, c.Nombre AS Nombre_Cliente, l.titulo AS Nombre_Libro, l.n_registro AS N_Registro, p.Fecha_Registro, p.Fecha_Limite, u.Nombre AS Nombre_Usuario, cp.ID_Prestamo, c.ID_Cliente
                    FROM cliente_prestamo cp 
                    JOIN cliente c ON cp.ID_Cliente = c.ID_Cliente 
                    JOIN libro l ON cp.ID_Libro = l.ID_Libro
                    JOIN prestamo p ON cp.ID_Prestamo = p.ID_Prestamo
                    JOIN usuarios u ON cp.ID_Usuario = u.ID_Usuario 
                    WHERE (c.Cedula=%s OR c.Nombre=%s OR l.titulo=%s OR p.Fecha_Registro=%s OR p.Fecha_Limite=%s OR u.Nombre=%s)
                    AND cp.estado_cliente_prestamo = 'activo'
                """
                cursor.execute(query, (busqueda, busqueda, busqueda, busqueda, busqueda, busqueda))
                resultados_prestamo = cursor.fetchall()

                if resultados_prestamo:
                    # Limpiar la tabla antes de insertar nuevos resultados
                    self.cliente_prestamo_table.delete(*self.cliente_prestamo_table.get_children())
                    
                    hoy = datetime.now().date()

                    prestamos_vencidos = 0

                    # Insertar los nuevos resultados
                    for fila in resultados_prestamo:
                        # Ajustar el formato de la fecha para DD-MM-YYYY
                        try:
                            fecha_limite = datetime.strptime(fila[5], '%d-%m-%Y').date()
                        except ValueError:
                            fecha_limite = datetime.strptime(fila[5], '%Y-%m-%d').date()

                        if fecha_limite <= hoy:
                            tag = 'vencido'
                            prestamos_vencidos += 1
                        else:
                            tag = 'activo'
                        self.cliente_prestamo_table.insert("", "end", values=tuple(fila), tags=(tag,))

                    # Configurar las etiquetas para los colores
                    self.cliente_prestamo_table.tag_configure('vencido', background='#FF4C4C')
                    self.cliente_prestamo_table.tag_configure('activo', background='white')

                    self.buscar.delete(0, 'end')  # Limpiar el Entry después de una búsqueda exitosa
                    total_prestamos = len(resultados_prestamo)
                    
                    # Obtener los datos del cliente
                    cliente_id = resultados_prestamo[0][8]
                    datos_cliente = obtener_datos_cliente(cliente_id)
                    
                    if datos_cliente:
                        nombre_cliente = datos_cliente["Nombre"]
                        apellido_cliente = datos_cliente["Apellido"]
                        mensaje_exito = f"""Préstamos del cliente: {nombre_cliente} {apellido_cliente}\n- Total de Préstamos: {total_prestamos}\n- Préstamos Vencidos: {prestamos_vencidos}"""

                        if prestamos_vencidos > 0:
                            mensaje_exito += """

    Por favor, contacte al cliente para renovar los préstamos vencidos o devolver los libros. Consulte el apartado de clientes para obtener más información sobre los datos del cliente.
    """

                        messagebox.showinfo("Búsqueda Exitosa de Préstamos", mensaje_exito)
                    else:
                        mensaje_exito = f"""
                        Búsqueda exitosa de préstamos:
                        - Total de Préstamos: {total_prestamos}
                        - Préstamos Vencidos: {prestamos_vencidos}
                        """
                        if prestamos_vencidos > 0:
                            mensaje_exito += """

    Por favor, contacte al cliente para renovar los préstamos vencidos o devolver los libros. Consulte el apartado de clientes para obtener más información sobre los datos del cliente.
    """
                        messagebox.showinfo("Búsqueda Exitosa de Préstamos", mensaje_exito)
                else:
                    self.buscar.delete(0, 'end')  # Limpiar el Entry si no se encontraron coincidencias
                    messagebox.showinfo("Búsqueda Fallida de Préstamos", f"No se encontraron préstamos asociados a la cédula '{busqueda}'. Por favor, verifique la cédula ingresada.")
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
        finally:
            if mariadb_conexion:
                mariadb_conexion.close()


    def update_selected_loan_due_date(self):
        selected_client = self.cliente_prestamo_table.selection()
        if selected_client:
            selected_client = selected_client[0]  # Obtener el primer elemento seleccionado
            client_values = self.cliente_prestamo_table.item(selected_client, 'values')
            id_prestamo = client_values[7]  # Asumiendo que ID_Prestamo es el octavo valor en la tupla
            print(f"Préstamo seleccionado: {client_values}")

            # Obtener el ID del cliente usando la cédula
            cedula_cliente = client_values[0]
            cliente_id = get_cliente_id_by_cedula(cedula_cliente)
            
            if cliente_id:
                # Obtener los datos del cliente usando el ID
                datos_cliente = obtener_datos_cliente(cliente_id)
                if datos_cliente:
                    nombre_cliente = datos_cliente["Nombre"]
                    apellido_cliente = datos_cliente["Apellido"]

                    # Mostrar mensaje de confirmación
                    mensaje_confirmacion = f"""¿Está seguro de que desea renovar el préstamo?
                    
    Detalles del Préstamo:
    - Título del Libro: {client_values[2]}
    - Fecha de Registro: {client_values[4]}
    - Fecha Límite Actual: {client_values[5]}
    - Nombre del Cliente: {nombre_cliente} {apellido_cliente}
    - Cédula del Cliente: {cedula_cliente}"""

                    if messagebox.askyesno("Confirmar Renovación", mensaje_confirmacion):
                        if renew_loan_due_date(id_prestamo):
                            messagebox.showinfo("Éxito", "La fecha límite del préstamo se ha actualizado correctamente.")
                        else:
                            messagebox.showerror("Error", "No se pudo actualizar la fecha límite del préstamo.")
                else:
                    messagebox.showerror("Error", "No se pudo obtener los datos del cliente.")
            else:
                messagebox.showerror("Error", "No se pudo obtener el ID del cliente.")
        else:
            messagebox.showwarning("Advertencia", "No hay ningún elemento seleccionado. Debe seleccionar un cliente para modificar el préstamo.")



    def on_treeview_select(self, event):
        # Obtener el elemento seleccionado
        selected_item = self.book_table_list.selection()[0]
        # Obtener los valores del elemento seleccionado
        item_values = self.book_table_list.item(selected_item, 'values')
        # Asumimos que el ID_Libro está en la primera columna
        self.ID_Libro = item_values[0]
    


    def show_report_window(self):
        GenerarReportePDF(self)



class GenerarReportePDF(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.client_data = {}
        self.books_data = []
        self.prestamos_data = []
        self.create_report_window()
    def cancelar(self, window):
        window.destroy()
    def create_report_window(self):
        # Definir las dimensiones de la ventana y centrarla antes de mostrarla
        self.geometry("463x330")
        centrar_ventana(self, 463, 330)
        
        self.canvas = tk.Canvas(self, bg="#031A33", width=463, height=330)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.iconbitmap(resource_path('assets_2/logo_biblioteca.ico'))
        self.resizable(False, False)
        self.grab_set()
        self.images = {}
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancelar(self))
        self.canvas.create_rectangle(0, 0, 570, 74, fill="#2E59A7")
        self.canvas.create_text(55.0, 21.0, anchor="nw", text="Generar Reporte PDF", fill="#ffffff", font=("Montserrat Medium", 28))


        # Diccionario para el combobox
        self.report_options = {"Reporte del Día Actual": "Reporte del Día Actual", "Reporte del Mes Actual": "Reporte del Mes Actual"}

        # Estilo del combobox
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                           fieldbackground="#2E59A7",  # Fondo del campo de entrada
                           background="#2E59A7",  # Fondo del desplegable
                           bordercolor="#041022",  # Color del borde
                           arrowcolor="#ffffff",  # Color de la flecha
                           padding="9",  # Padding para agrandar la altura del select
                           )

        # Crear el título del combobox
        tk.Label(self, text="Seleccionar Tipo de Reporte:", bg="#031A33", fg="#ffffff", font=("Montserrat Medium", 12)).place(x=61.0, y=110.0)
        
        # Crear el combobox
        self.report_combobox = ttk.Combobox(self, values=list(self.report_options.values()), state="readonly", width=30, font=("Bold", 10), style="TCombobox")
        self.report_combobox.place(x=61.0, y=151.5)
        self.report_combobox.set("Reporte del Día Actual")  # Establece el valor inicial a "Reporte del Día Actual"

        # Botón para generar el reporte
        self.images['boton_generar'] = tk.PhotoImage(file=resource_path("assets_2/G_boton.png"))
        boton_generar = self.images['boton_generar']
        tk.Button(
            self,
            image=boton_generar,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.generate_report(),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"  # Color del texto cuando el botón está activo
        ).place(x=61.0, y=265.0, width=130.0, height=40.0)

        # Botón para cancelar
        self.images['boton_cancelar'] = tk.PhotoImage(file=resource_path("assets_2/c_button_red1.png"))
        self.boton_cancelar = tk.Button(
            self,
            image=self.images['boton_cancelar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.cancelar(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_cancelar.place(x=250.0, y=265.0, width=130.0, height=40.0)

    def get_loans_by_day(self):
        prestamos_data = []
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                cursor.execute('''
                    SELECT
                        c.Cedula,
                        c.Nombre AS Nombre_Cliente,
                        l.titulo AS Nombre_Libro,
                        l.n_registro AS N_Registro,
                        p.Fecha_Registro,
                        p.Fecha_Limite,
                        u.Nombre AS Nombre_Usuario,
                        cp.ID_CP,
                        u.ID_Usuario
                    FROM 
                        cliente_prestamo cp
                    JOIN
                        prestamo p ON cp.ID_Prestamo = p.ID_Prestamo
                    JOIN 
                        cliente c ON cp.ID_Cliente = c.ID_Cliente
                    JOIN
                        libro l ON cp.ID_Libro = l.ID_Libro
                    JOIN 
                        usuarios u ON cp.ID_Usuario = u.ID_Usuario
                    WHERE 
                        DATE(STR_TO_DATE(p.Fecha_Registro, '%d-%m-%Y')) = CURDATE() AND cp.estado_cliente_prestamo = 'activo'
                ''')
                resultados = cursor.fetchall()
                for resultado in resultados:
                    prestamos_data.append({
                        "Cedula": resultado[0],
                        "Nombre_Cliente": resultado[1],
                        "Nombre_Libro": resultado[2],
                        "N_Registro": resultado[3],
                        "Fecha_Registro": resultado[4],
                        "Fecha_Limite": resultado[5],
                        "Nombre_Usuario": resultado[6],
                        "ID_CP": resultado[7],
                        "ID_Usuario": resultado[8]
                    })
                mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
        print(f"Préstamos del Día Actual: {prestamos_data}")
        return prestamos_data


    def get_loans_by_month(self):
        prestamos_data = []
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                cursor.execute('''
                    SELECT
                        c.Cedula,
                        c.Nombre AS Nombre_Cliente,
                        l.titulo AS Nombre_Libro,
                        l.n_registro AS N_Registro,
                        p.Fecha_Registro,
                        p.Fecha_Limite,
                        u.Nombre AS Nombre_Usuario,
                        cp.ID_CP,
                        u.ID_Usuario
                    FROM 
                        cliente_prestamo cp
                    JOIN
                        prestamo p ON cp.ID_Prestamo = p.ID_Prestamo
                    JOIN 
                        cliente c ON cp.ID_Cliente = c.ID_Cliente
                    JOIN
                        libro l ON cp.ID_Libro = l.ID_Libro
                    JOIN 
                        usuarios u ON cp.ID_Usuario = u.ID_Usuario
                    WHERE 
                        YEAR(STR_TO_DATE(p.Fecha_Registro, '%d-%m-%Y')) = YEAR(CURDATE()) AND MONTH(STR_TO_DATE(p.Fecha_Registro, '%d-%m-%Y')) = MONTH(CURDATE()) AND cp.estado_cliente_prestamo = 'activo'
                ''')
                resultados = cursor.fetchall()
                for resultado in resultados:
                    prestamos_data.append({
                        "Cedula": resultado[0],
                        "Nombre_Cliente": resultado[1],
                        "Nombre_Libro": resultado[2],
                        "N_Registro": resultado[3],
                        "Fecha_Registro": resultado[4],
                        "Fecha_Limite": resultado[5],
                        "Nombre_Usuario": resultado[6],
                        "ID_CP": resultado[7],
                        "ID_Usuario": resultado[8]
                    })
                mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
        print(f"Préstamos del Mes Actual: {prestamos_data}")
        return prestamos_data

    

    def obtener_datos(self):
        if not self.prestamos_data:
            messagebox.showwarning("Advertencia", "No se encontraron préstamos para el período seleccionado.", parent=self)
            return None, None, None

        books_data = []
        prestamos_formateados = []

        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                for prestamo in self.prestamos_data:
                    cliente_id = get_cliente_id_by_cedula(prestamo["Cedula"])
                    cursor.execute('''
                        SELECT Cedula, Nombre, Apellido, Telefono, Direccion
                        FROM cliente
                        WHERE ID_Cliente = %s
                    ''', (cliente_id,))
                    resultado_cliente = cursor.fetchone()
                    print(f"Resultado Cliente: {resultado_cliente}\n")
                    if resultado_cliente:
                        client_data = {
                            "Cedula": resultado_cliente[0],
                            "Nombre": resultado_cliente[1],
                            "Apellido": resultado_cliente[2],
                            "Telefono": resultado_cliente[3],
                            "Direccion": resultado_cliente[4]
                        }
                    cliente = Cliente(
                        cedula=client_data["Cedula"],
                        nombre=client_data["Nombre"],
                        apellido=client_data["Apellido"],
                        telefono=client_data["Telefono"],
                        direccion=client_data["Direccion"]
                    )
                    self.client_data[resultado_cliente[0]] = cliente

                    libro_id = get_libro_id_by_registro(prestamo["N_Registro"])
                    book_data = obtener_datos_libro(libro_id)
                    if book_data:
                        libro = Libro(
                            cota=book_data["Cota"],
                            categoria=book_data["ID_Categoria"],
                            sala=book_data["ID_Sala"],
                            asignatura=book_data["ID_Asignatura"],
                            numero_registro=book_data["n_registro"],
                            autor=book_data["autor"],
                            titulo=book_data["titulo"],
                            num_volumenes=book_data["n_volumenes"],
                            num_ejemplares=book_data["n_ejemplares"],
                            edicion=book_data["edicion"],
                            año=book_data["año"],
                            editorial=book_data["editorial"]
                        )
                        # Formatear fechas correctamente
                        try:
                            prestamo_fecha_registro = datetime.strptime(prestamo["Fecha_Registro"], '%d-%m-%Y')
                            fecha_r = prestamo_fecha_registro.strftime('%d-%m-%Y')
                        except ValueError:
                            print(f"Error: El formato de la fecha '{prestamo['Fecha_Registro']}' no es válido.\n")
                            fecha_r = prestamo["Fecha_Registro"]
                        try:
                            prestamo_fecha_limite = datetime.strptime(prestamo["Fecha_Limite"], '%d-%m-%Y')
                            fecha_en = prestamo_fecha_limite.strftime('%d-%m-%Y')
                        except ValueError:
                            print(f"Error: El formato de la fecha '{prestamo['Fecha_Limite']}' no es válido.\n")
                            fecha_en = prestamo["Fecha_Limite"]
                        prestamos_formateados.append({
                            "Cedula": prestamo["Cedula"],
                            "Nombre_Cliente": prestamo["Nombre_Cliente"],
                            "Nombre_Libro": prestamo["Nombre_Libro"],
                            "N_Registro": prestamo["N_Registro"],
                            "fecha_r": fecha_r,
                            "fecha_en": fecha_en,
                            "Nombre_Usuario": prestamo["Nombre_Usuario"],
                            "ID_CP": prestamo["ID_CP"]
                        })
                        books_data.append(libro)
                # Ordenar los préstamos y los libros por fecha
                prestamos_formateados, books_data = zip(*sorted(zip(prestamos_formateados, books_data), key=lambda x: datetime.strptime(x[0]["fecha_r"], '%d-%m-%Y')))
                prestamos_formateados = list(prestamos_formateados)
                books_data = list(books_data)
                print("Books Data:", books_data)
                print("Prestamos Formateados:", prestamos_formateados)
                return self.client_data, books_data, prestamos_formateados
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
            messagebox.showerror("Error", f"Error durante la conexión: {ex}", parent=self)
            return None, None, None

    def generate_report(self):
        report_type = self.report_combobox.get()
        if report_type == "Reporte del Día Actual":
            self.prestamos_data = self.get_loans_by_day()
            if not self.prestamos_data:
                messagebox.showinfo("Información", "No se han realizado préstamos hoy.", parent=self)
                return
            client_data, books_data, prestamos_formateados = self.obtener_datos()
            if client_data and books_data and prestamos_formateados:
                success = generate_report_by_day(client_data, books_data, prestamos_formateados, self)
        elif report_type == "Reporte del Mes Actual":
            self.prestamos_data = self.get_loans_by_month()
            if not self.prestamos_data:
                meses = {
                    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
                    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
                }
                fecha_actual = datetime.now()
                mes_actual = meses[fecha_actual.month]
                messagebox.showinfo("Información", f"No se han realizado préstamos en el mes de {mes_actual}.", parent=self)
                return
            client_data, books_data, prestamos_formateados = self.obtener_datos()
            if client_data and books_data and prestamos_formateados:
                success = generate_report_by_month(client_data, books_data, prestamos_formateados, self)
        else:
            messagebox.showwarning("Advertencia", "Seleccione un tipo de reporte válido.", parent=self)
            return

        if success:
            messagebox.showinfo("Éxito", "El reporte ha sido creado de forma exitosa.", parent=self)
        else:
            messagebox.showerror("Error", "Guardado cancelado.", parent=self)
        self.destroy()



# Asegúrate de que P_Listar está definido/importado correctamente
class Register_Loans():
    def __init__(self, parent, loans_validations):
        self.parent = parent
        self.loans_validations = loans_validations
        self.register_loan_window = tk.Toplevel(parent)
        self.validate_number = self.register_loan_window.register(validate_number_input)
        # Datos y paginación
        self.data = []
        #self.agarrar_datos()
        self.page_size = 19
   
        self.current_page = 0
        
        self.setup_window()

        # Llamada a la función para cargar los libros
        self.load_books()
        # Llamada a la función para mostrar la página actual
        self.display_page(self.data, self.current_page, self.page_size)
        self.mostrar_mensaje_prestamos_vencidos()

        
    def setup_window(self):
        self.register_loan_window.title("Registrar Préstamo")
        self.register_loan_window.iconbitmap(resource_path('assets_2/logo_biblioteca.ico'))
        self.register_loan_window.geometry("1355x600")
        self.register_loan_window.config(bg="#042344")
        self.register_loan_window.resizable(False, False)
        self.register_loan_window.grab_set()
        self.register_loan_window.protocol("WM_DELETE_WINDOW", lambda: self.cancelar(self.register_loan_window))
        self.images = {}          
        # Crear el marco izquierdo para el menú de navegación
        self.left_frame_list = tk.Frame(self.register_loan_window, bg="#042344")
        self.left_frame_list.place(x=170, y=160, height=430, width=1200)
        
        rectangulo_color = tk.Label(self.register_loan_window, bg="#2E59A7", width=200, height=3)
        rectangulo_color.place(x=0, y=0)
        tk.Label(self.register_loan_window, text="Tabla Prestamos", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=505.0, y=8.0, width=450.0, height=35.0)
        tk.Label(self.register_loan_window, text="Cedula del Cliente", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=628.0, y=70.0, width=185.0, height=35.0)
        self.cedula = tk.Entry(self.register_loan_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat", validate="key", validatecommand=(self.validate_number, "%P"))
        self.cedula.place(x=630.0, y=100.0, width=190.0, height=35.0)
        tk.Label(self.register_loan_window, text="Fecha Registrar", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=22.0, y=140.0, width=160.0, height=35.0)
        self.fecha_registrar = tk.Entry(self.register_loan_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.fecha_registrar.place(x=20.0, y=170.0, width=170.0, height=35.0)
        tk.Label(self.register_loan_window, text="Fecha Limite", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=7.0, y=240.0, width=160.0, height=35.0)
        self.fecha_limite = tk.Entry(self.register_loan_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.fecha_limite.place(x=20.0, y=270.0, width=170.0, height=35.0)

        # Establecer las fechas automáticamente
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        fecha_limite = (datetime.now() + timedelta(days=3)).strftime("%d/%m/%Y")
        self.fecha_registrar.insert(0, fecha_actual)
        self.fecha_limite.insert(0, fecha_limite)
        self.fecha_registrar.config(state='readonly')
        self.fecha_limite.config(state='readonly')

        # Configurar el Treeview
        tree = ("ID", "Sala", "Categoria", "Asignatura", "Cota", "N° Registro", "Titulo", "Autor", "Editorial", "Año", "Edición", "N° Volúmenes", "N° Ejemplares")
        self.book_table_list = ttk.Treeview(self.left_frame_list, columns=tree, show='headings', style="Rounded.Treeview")
        self.book_table_list.column("ID", width=40, anchor="center")
        self.book_table_list.column("Sala", width=40, anchor="center")
        self.book_table_list.column("Cota", width=30, anchor="center")
        self.book_table_list.column("N° Registro", width=50, anchor="center")
        self.book_table_list.column("Titulo", width=100, anchor="center")
        self.book_table_list.column("Año", width=30, anchor="center")
        self.book_table_list.column("Edición", width=30, anchor="center")
        self.book_table_list.column("N° Ejemplares", width=70, anchor="center")
        self.book_table_list.column("N° Volúmenes", width=70, anchor="center")
        for col in tree:
            if col not in ("ID", "Sala", "Cota", "N° Registro", "Titulo", "Año", "N° Ejemplares", "N° Volúmenes"):
                self.book_table_list.column(col, width=95, anchor="center")
            self.book_table_list.heading(col, text=col)
        self.book_table_list.pack(expand=True, fill="both", padx=30, pady=5)
        
        scrollbar_pt = ttk.Scrollbar(self.book_table_list, orient="vertical", command=self.book_table_list.yview)
        self.book_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
        self.book_table_list.bind('<<TreeviewSelect>>', self.on_treeview_select)
        self.images['boton_siguiente'] = tk.PhotoImage(file=resource_path("assets_2/siguie-inver.png"))
        self.images['boton_anterior'] = tk.PhotoImage(file=resource_path("assets_2/anteri-inver.png"))
        # Botones de navegación
        prev_button = tk.Button(
            self.left_frame_list,
            image=self.images['boton_anterior'],
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg="#042344",
            activebackground="#042344",
            activeforeground="#006ac2",
            command=self.previous_page
        )
        prev_button.pack(side=tk.LEFT, padx=25, pady=0)
        
        next_button = tk.Button(
            self.left_frame_list,
            image=self.images['boton_siguiente'],
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg="#042344",
            activebackground="#042344",
            activeforeground="#006ac2",
            command=self.next_page
        )
        next_button.pack(side=tk.RIGHT, padx=27, pady=0)

        # Etiqueta para mostrar la página actual
        # Define self.page_label antes de llamar a reading_books
        self.page_label = tk.Label(self.left_frame_list, text=f"Página {self.current_page + 1}", bg="#042344", fg="White", font=("Montserrat Regular", 13))
        self.page_label.pack(side=tk.BOTTOM, pady=15)
        # Llama a reading_books después de definir self.page_label
      
        
        self.images['boton_r'] = tk.PhotoImage(file=resource_path("assets_2/R_button_light_blue.png"))
        self.boton_R = tk.Button(
            self.register_loan_window,
            image=self.images['boton_r'],
            borderwidth=0,
            highlightthickness=0,
            command=self.save_modifications,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_R.place(x=24.0, y=800.0, width=130.0, height=40.0) #irrelevante por la funcion que lo hace aparecer luego
        self.boton_R.place_forget()
        self.cedula.bind("<KeyRelease>", lambda event: self.loans_validations.validate_entries(self, event))
        self.cedula.bind("<KeyPress>",self.key_on_press_search)
        #self.cedula.bind("<Return>", lambda event: self.save_modifications())
        

    def key_on_press_search(self, event):
        current_text = self.cedula.get()
        limited_text = limit_length(current_text, 10)
        self.cedula.delete(0, 'end')
        self.cedula.insert(0, limited_text)

    def on_treeview_select(self, event):
        # Obtener el elemento seleccionado
        selected_item = self.book_table_list.selection()[0]
        # Obtener los valores del elemento seleccionado
        item_values = self.book_table_list.item(selected_item, 'values')
        # Asumimos que el ID_Libro está en la primera columna
        self.ID_Libro = item_values[0]
    
    def boton_buscar(self, event):
        busqueda = self.buscar.get().strip()
        campo_seleccionado = self.campo_busqueda.get()  # Obtener el campo seleccionado
        campo_real = self.filter_options[campo_seleccionado]  # Traducir al nombre real de la columna
        
        if not busqueda:
            messagebox.showinfo("Búsqueda Fallida de Libro", f"No se ingresó ningún término de búsqueda. Por favor, ingrese un término para buscar en el campo '{campo_seleccionado}'.")
            return
        
        # Convertir la búsqueda a minúsculas y eliminar tildes
        busqueda_normalizada = unidecode.unidecode(busqueda).lower()
        
        try:
            self.search_data = search_books(campo_real, busqueda_normalizada)
            self.search_current_page = 0  # Resetear la página a la primera página
            self.is_search_active = True

            if self.search_data:
                # Limpiar la tabla antes de insertar nuevos resultados
                self.book_table_list.delete(*self.book_table_list.get_children())
                self.display_page(self.search_data, self.search_current_page, self.search_page_size, is_search=True)
                self.buscar.delete(0, 'end')  # Limpiar el Entry después de una búsqueda exitosa
                messagebox.showinfo("Búsqueda Exitosa de Libro", f"Se encontraron {len(self.search_data)} resultados para '{busqueda}' en el campo '{campo_seleccionado}'.")
            else:
                self.buscar.delete(0, 'end')  # Limpiar el Entry si no se encontraron coincidencias
                messagebox.showinfo("Búsqueda Fallida de Libro", f"No se encontraron resultados para '{busqueda}' en el campo '{campo_seleccionado}'.")
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)

    def display_page(self, data, current_page, page_size, is_search=False):
        # Limpiar la tabla antes de insertar nuevos resultados
        for row in self.book_table_list.get_children():
            self.book_table_list.delete(row)
        
        # Obtener los datos de la página actual
        offset = current_page * page_size
        page_data = data[offset:offset + page_size]
        
        # Insertar los nuevos resultados
        for row in page_data:
            n_ejemplares = row[12]
            tag = 'multiple' if n_ejemplares > 1 else 'single'
            self.book_table_list.insert("", "end", values=row, tags=(tag,))
        
        # Configurar las etiquetas para los colores
        self.book_table_list.tag_configure('multiple', background='lightblue')
        self.book_table_list.tag_configure('single', background='#E5E1D7')
        
        # Actualizar la etiqueta de la página
        self.update_page_label(len(data), current_page, page_size, is_search)


    def load_books(self):
        try:
            self.data = get_book_data()
            self.current_page = 0  # Resetear a la primera página
            self.is_search_active = False  # Asegurar que estamos en modo normal
            self.display_page(self.data, self.current_page, self.page_size)
        except Exception as ex:
            print("Error al cargar los libros:", ex)



    def next_page(self):
        if self.is_search_active:
            if (self.search_current_page + 1) * self.search_page_size < len(self.search_data):
                self.search_current_page += 1
                self.display_page(self.search_data, self.search_current_page, self.search_page_size, is_search=True)
        else:
            if (self.current_page + 1) * self.page_size < len(self.data):
                self.current_page += 1
                self.display_page(self.data, self.current_page, self.page_size)

    def previous_page(self):
        if self.is_search_active:
            if self.search_current_page > 0:
                self.search_current_page -= 1
                self.display_page(self.search_data, self.search_current_page, self.search_page_size, is_search=True)
        else:
            if self.current_page > 0:
                self.current_page -= 1
                self.display_page(self.data, self.current_page, self.page_size)


    def update_page_label(self, total_data, current_page, page_size, is_search=False):
        total_pages = (total_data + page_size - 1) // page_size  # Calcular el total de páginas
        self.page_label.config(text=f"Página {current_page + 1} de {total_pages}")

    def mostrar_mensaje_prestamos_vencidos(self):
        prestamos_vencidos = obtener_prestamos_vencidos()
        if prestamos_vencidos:
            mensaje_vencidos = "Hay préstamos vencidos asociados a los siguientes clientes:\n\n"
            for prestamo in prestamos_vencidos:
                id_cliente = prestamo[0]
                datos_cliente = obtener_datos_cliente(id_cliente)
                if datos_cliente:
                    mensaje_vencidos += f"Cliente: {datos_cliente['Nombre']} {datos_cliente['Apellido']}\nCédula: {datos_cliente['Cedula']}\nTeléfono: {datos_cliente['Telefono']}\nPréstamos Vencidos: {prestamo[1]}\n\n"           
            mensaje_vencidos += "Por favor, contacte a los clientes para renovar los préstamos vencidos o devolver los libros. Consulte el apartado de préstamos para obtener más información sobre los libros prestados."
            messagebox.showwarning("Préstamos Vencidos", mensaje_vencidos, parent=self.register_loan_window)

    def save_modifications(self):
        from users.backend.db_users import obtener_id_usuario_actual

        # Formatear las fechas
        fecha_registrar = loans_validations.format_date(self.fecha_registrar.get())
        Cedula = self.cedula.get()
        if hasattr(self, 'ID_Libro'):
            ID_Libro = self.ID_Libro
        else:
            messagebox.showerror("Error", "Por favor, selecciona un libro de la lista.", parent=self.register_loan_window)
            return

        # Obtener la información del libro
        datos_libro = obtener_datos_libro(ID_Libro)
        if not datos_libro:
            messagebox.showerror("Error", "No se pudo obtener la información del libro.", parent=self.register_loan_window)
            return

        n_registro = datos_libro["n_registro"]

        # Validar si el libro ya está prestado
        error_libro_prestado = validar_libro_no_prestado(n_registro, Cedula)
        if error_libro_prestado:
            messagebox.showerror("Error de Préstamo", error_libro_prestado, parent=self.register_loan_window)
            return

        # Obtener ID del Cliente
        ID_Cliente = get_cliente_id_by_cedula(Cedula)
        if ID_Cliente is None:
            messagebox.showerror("Error", "No se pudo obtener la ID del Cliente. Ingrese un N° de Cédula existente", parent=self.register_loan_window)
            return

        # Obtener ID del Usuario Logueado
        ID_Usuario = self.parent.id_usuario
        if ID_Usuario is None:
            messagebox.showerror("Error", "No se pudo obtener el ID de usuario.", parent=self.register_loan_window)
            return

        # Generar un nuevo ID_Prestamo
        ID_Prestamo = loans_validations.generate_alphanumeric_id()
        print(f"Nuevo ID_Prestamo generado: {ID_Prestamo}")

        # Generar ID de Libro Préstamo
        ID_Libro_Prestamo = generate_id_libro_prestamo(self)

        # Verificar si el libro es una novela
        if es_novela(ID_Libro):
            fecha_limite = (datetime.strptime(fecha_registrar, '%d-%m-%Y') + timedelta(days=8)).strftime('%d-%m-%Y')
        else:
            fecha_limite = (datetime.strptime(fecha_registrar, '%d-%m-%Y') + timedelta(days=3)).strftime('%d-%m-%Y')

        # Validar los campos
        errores = validar_campos_loans(
            Cedula,
            ID_Libro,
            None  # No hay ID de libro para registro
        )
        
        print(f"Errores: {errores}")  # Agregar esta línea para depuración

        if errores:        
            messagebox.showerror("Error al registrar", "Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"- {msg}" for msg in errores),parent=self)
            return

        # Depuración de los valores que se van a pasar a create_books
        print(f"Valores para registro: Cedula={Cedula}, ID_Libro={ID_Libro}, N° Registro={n_registro}")

        # Crear el préstamo y actualizar las tablas
        if create_loan(ID_Cliente, ID_Prestamo, fecha_registrar, fecha_limite):
            if update_all_tables(ID_Cliente, ID_Libro, ID_Libro_Prestamo, ID_Prestamo, ID_Usuario):
                messagebox.showinfo("Éxito", f"""Préstamo Registrado con Éxito

    Detalles del Préstamo:
    - Fecha de Registro: {fecha_registrar}
    - Fecha Límite: {fecha_limite}
    - Cédula del Cliente: {Cedula}

    Por favor, asegúrese de que el cliente devuelva el libro antes de la fecha límite.
    Consulte el apartado de préstamos para obtener más información sobre los libros prestados.
    """, parent=self.register_loan_window)
                loans_validations.clear_entries_list_register(self)
                reading_books(self)
            else:
                messagebox.showerror("Error", "No se pudo actualizar las tablas. Puede que no haya ejemplares disponibles.", parent=self.register_loan_window)
        else:
            messagebox.showerror("Error", "Préstamo no pudo ser creado.", parent=self.register_loan_window)





    def cancelar(self, window):
        if messagebox.askyesno(
                "Advertencia",
                "¿Seguro que quieres cerrar esta ventana? Perderás los datos del registro del préstamo.", parent=window):
            window.destroy()

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
# class ModifyLoans(P_Listar):
#     def __init__(self, parent, cedula, fecha_limite, loans_validations):
#         super().__init__(parent)  # Llamar al constructor de la clase base
#         self.parent = parent
#         self.loans_validations = loans_validations
#         self.modify_loan_window = tk.Toplevel(parent)
#         self.setup_window()

#         #Establecer la cédula y la fecha límite en los campos de entrada
#         self.cedula_entry.insert(0, cedula)
#         self.fecha_limite_entry.insert(0, fecha_limite)

#     def setup_window(self):
#         self.modify_loan_window.title("Renovación Préstamo")
#         self.modify_loan_window.iconbitmap(resource_path('assets_2/logo_biblioteca.ico'))
#         self.modify_loan_window.geometry("950x550")
#         self.modify_loan_window.config(bg="#042344")
#         self.modify_loan_window.resizable(False, False)
#         self.modify_loan_window.grab_set()
#         self.modify_loan_window.protocol("WM_DELETE_WINDOW", lambda: self.cancelar(self.modify_loan_window, "modificar"))

#         rectangulo_color = tk.Label(self.modify_loan_window, bg="#2E59A7", width=200, height=4)
#         rectangulo_color.place(x=0, y=0)
#         tk.Label(self.modify_loan_window, text="Modificación De Préstamo", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=235.0, y=15.0, width=450.0, height=35.0)
#         tk.Label(self.modify_loan_window, text="Ingrese los datos a modificar", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=10.0, y=80.0, width=330.0, height=35.0)
#         tk.Label(self.modify_loan_window, text="Fecha Limite", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=360.0, y=140.0, width=130.0, height=35.0)
#         self.fecha_limite_entry = tk.Entry(self.modify_loan_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         self.fecha_limite_entry.place(x=365.0, y=180.0, width=190.0, height=35.0)
#         # tk.Label(self.modify_loan_window, text="Cantidad", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=439.0, y=140.0, width=185.0, height=35.0)
#         # self.cantidad_entry = tk.Entry(self.modify_loan_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         # self.cantidad_entry.place(x=490.0, y=180.0, width=190.0, height=35.0)
#         tk.Label(self.modify_loan_window, text="Ingrese la cedula del cliente para modificar el prestamo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=35.0, y=255.0, width=540.0, height=35.0)
#         tk.Label(self.modify_loan_window, text="Cedula", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=335.0, y=315.0, width=120.0, height=35.0)
#         self.cedula_entry = tk.Entry(self.modify_loan_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         self.cedula_entry.place(x=365.0, y=355.0, width=190.0, height=35.0)
        
#         # Botones
#         self.images = {}
#         self.images['boton_m'] = tk.PhotoImage(file=resource_path("assets_2/M_button_light_blue.png"))
#         self.boton_M = tk.Button(
#             self.modify_loan_window,
#             image=self.images['boton_m'],
#             borderwidth=0,
#             highlightthickness=0,
#             command=self.apply_filters_modify,
#             relief="flat",
#             bg="#031A33",
#             activebackground="#031A33",
#             activeforeground="#FFFFFF"
#         )
#         self.boton_M.place(x=530.0, y=450.0, width=130.0, height=40.0)
        
#         self.images['boton_c'] = tk.PhotoImage(file=resource_path("assets_2/c_button_red1.png"))
#         self.boton_C = tk.Button(
#             self.modify_loan_window,
#             image=self.images['boton_c'],
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: self.cancelar(self.modify_loan_window, "modificar"),
#             relief="flat",
#             bg="#031A33",
#             activebackground="#031A33",
#             activeforeground="#FFFFFF"
#         )
#         self.boton_C.place(x=270.0, y=450.0, width=130.0, height=40.0)


#     def cancelar(self, window, ventana_llamante):
#         if ventana_llamante == "modificar":
#             if messagebox.askyesno(
#                     "Advertencia",
#                     "¿Seguro que quieres cerrar esta ventana? Perderás todos los cambios no guardados en el préstamo.",
#                     parent=self.modify_loan_window):
#                 window.destroy()
#         else:
#             pass

#     def apply_filters_modify(self):
#         cedula = self.cedula_entry.get()
#         fecha_limite = self.fecha_limite_entry.get()
#         print(f"cedula:{cedula}, fecha_limite:{fecha_limite}")
        
#         errores = validar_campos(
#             cedula=cedula,
#             fecha_limite=fecha_limite,
#             tipo_validacion="modificar",
#             #client_id=None
#         )
#         print(f"Errores: {errores}")  # Agregar esta línea para depuración
#         if errores:
#             messagebox.showerror("Error al modificar", "Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"- {msg}" for msg in errores), parent=self)
#             return
        
#         if fecha_limite:
#             is_valid, message = validate_fecha_limite(fecha_limite)
#             if not is_valid:
#                 messagebox.showinfo("Error", message, parent=self.modify_loan_window)
#                 return
#             try:
#                 fecha_limite = datetime.strptime(fecha_limite, '%d-%m-%Y')
#             except ValueError:
#                 messagebox.showinfo("Error", "Por favor, proporciona una fecha válida en el formato DD-MM-YYYY.", parent=self.modify_loan_window)
#                 return
        
#         if cedula:
#             respuesta = messagebox.askyesno("Confirmar modificación", "¿Desea modificar?")
#             if respuesta:
#                 if update_client_loans(cedula, fecha_limite):
#                     messagebox.showinfo("Éxito", "Modificación exitosa del préstamo del cliente", parent=self.modify_loan_window)
#                     loans_validations.clear_entries_list(self)
#                 else:
#                     messagebox.showinfo("Fallido", "La modificación del préstamo no pudo ejecutarse.", parent=self.modify_loan_window)
#             else:
#                 messagebox.showinfo("Cancelado", "Modificación cancelada.", parent=self.modify_loan_window)
#         else:
#             messagebox.showinfo("Error", "Por favor, proporciona una cédula válida.", parent=self.modify_loan_window)


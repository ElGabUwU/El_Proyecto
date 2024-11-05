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
from util.Reporte_PDF import generar_pdf,formatear_fecha,formatear_fecha_titulo
from loans.backend.models import Cliente, Libro
from validations import loans_validations
from util.utilidades import resource_path
from validations.loans_validations import *

def validate_number_input(text):
        if text == "":
            return True
        try:
            float(text)
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
        

        self.left_frame2 = tk.Frame(self.canvas, bg="#FAFAFA")
        self.left_frame2.pack(expand=True, side="right", fill="both")
        self.left_frame2.place(x=215,y=218, height=470, width=1135)
        
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", expand=True, fill="both")
        
        # Texto para el nombre

        self.label_nombre = self.canvas.create_text(245.0, 82.0, anchor="nw", text="Buscar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1175.0, 170.0, text="Editar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1275.0, 170.0, text="Eliminar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(875.0, 170.0, text="Imprimir", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(975.0, 170.0, text="Refrescar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1075.0, 170.0, text="Agregar", fill="#031A33", font=("Bold", 17))
        # self.canvas.create_text(1275.0, 170.0, text="Filtrar", fill="#031A33", font=("Bold", 17))

       # Títulos para los Treeviews
        bold_font = font.Font(family="Bold", size=15, weight="bold")
        self.label_prestamos = tk.Label(self.canvas, text="Tabla Prestamos", bg="#FAFAFA", fg="#031A33", font=bold_font)
        self.label_prestamos.place(x=665.0, y=185.0, width=237.0, height=35.0)


        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.buscar.place(x=245.0, y=112.0, width=267.0, height=48.0)
        self.buscar.bind("<Return>", self.boton_buscar)
        self.images['boton_imprimir'] = tk.PhotoImage(file=resource_path("assets_2/Logo_Imprimir.png"))
        
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
        self.button_e.place(x=830.0, y=60.0, width=90.0, height=100.0)
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
            command=lambda: self.lists_clients_loans(), #or lists_clients(self),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        )
        self.button_c.place(x=930.0, y=60.0, width=90.0, height=100.0)

        #Boton Filtrar
        # Cargar y almacenar las imágenes
        # self.images['boton_filtrar_f'] = tk.PhotoImage(file=resource_path("assets_2/14_filtrar.png"))
        # # Cargar y almacenar la imagen del botón
        # self.button_f = tk.Button(
        #     self,
        #     image=self.images['boton_filtrar_f'],
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: self.open_filter_loans_window(),
        #     relief="flat",
        #     bg="#FAFAFA",
        #     activebackground="#FAFAFA",  # Mismo color que el fondo del botón
        #     activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
        # )
        # self.button_f.place(x=1230.0, y=60.0, width=90.0, height=100.0)

        #Boton Modificar
        # Cargar y almacenar las imágenes
        self.images['boton_modificar'] = tk.PhotoImage(file=resource_path("assets_2/6_editar.png"))
        # Cargar y almacenar la imagen del botón
        self.button_m = tk.Button(
            self,
            image=self.images['boton_modificar'],
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

        # Crear un estilo específico para el Treeview listado de libros en esta ventana
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



        #Columnas Prestamo
        columns2 = ("Cedula", "Cliente", "Nombre del Libro", "N° Registro", "F.Registro", "F.Limite", "Encargado", "ID_Prestamo")
        self.cliente_prestamo_table = ttk.Treeview(self.left_frame2, columns=columns2, show='headings', style="Rounded.Treeview", selectmode="browse")

        for col2 in columns2:
            self.cliente_prestamo_table.heading(col2, text=col2)
            if col2 == "ID_Prestamo":
                self.cliente_prestamo_table.column(col2, width=0, stretch=False)  # Ocultar la columna
            else:
                self.cliente_prestamo_table.column(col2, width=90, anchor="center")

        self.cliente_prestamo_table.pack(expand=True, fill="both", padx=30, pady=5)

        self.cliente_prestamo_table.bind("<Double-1>", self.on_loans_double_click)  # SELECCION DE TODOS LOS EJEMPLARES CON DOBLE CLICK
        scrollbar_pt = ttk.Scrollbar(self.cliente_prestamo_table, orient="vertical", command=self.cliente_prestamo_table.yview)
        self.cliente_prestamo_table.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
        self.lists_clients_loans()
        
        


    def lists_clients_loans(self):
        try:
            mariadb_conexion = establecer_conexion()
            if not mariadb_conexion:
                print("Failed to establish connection.")
                return

            cursor = mariadb_conexion.cursor()

            query1 = '''
            SELECT
                c.Cedula,
                c.Nombre AS Nombre_Cliente,
                l.titulo AS Nombre_Libro,
                l.n_registro AS N_Registro,
                p.Fecha_Registro,
                p.Fecha_Limite,
                u.Nombre AS Nombre_Usuario,
                p.ID_Prestamo,
                cp.ID_CP
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
                cp.estado_cliente_prestamo = 'activo';
            '''

            cursor.execute(query1)
            resultados1 = cursor.fetchall()

            # Debugging: Print the results
            print("Query executed successfully. Results:")
            for resultado in resultados1:
                print(resultado)

            for row in self.cliente_prestamo_table.get_children():
                self.cliente_prestamo_table.delete(row)

            prestamos_vencidos = []
            hoy = datetime.now().date()

            for fila in resultados1:
                # Ajustar el formato de la fecha para DD-MM-YYYY
                fecha_limite = datetime.strptime(fila[4], '%d-%m-%Y').strftime('%d-%m-%Y')
                fecha_limite = datetime.strptime(fecha_limite, '%d-%m-%Y').date()
                if fecha_limite <= hoy - timedelta(days=3):
                    tag = 'vencido'
                    prestamos_vencidos.append(fila)
                else:
                    tag = 'activo'
                self.cliente_prestamo_table.insert("", "end", values=tuple(fila), tags=(tag,))

            # Configurar las etiquetas para los colores
            self.cliente_prestamo_table.tag_configure('vencido', background='red')
            self.cliente_prestamo_table.tag_configure('activo', background='white')

            if prestamos_vencidos:
                messagebox.showwarning("Préstamos Vencidos", "Hay préstamos que han pasado más de 3 días desde su fecha límite.")

        except mariadb.Error as ex:
            print(f"Error during query execution: {ex}")
        finally:
            if mariadb_conexion is not None:
                mariadb_conexion.close()
                print("Connection closed.")

    def imprimir_seleccionado(self):
        selected_items = self.cliente_prestamo_table.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún préstamo.")
            return

        prestamos_data = []
        for item in selected_items:
            prestamo_valores = self.cliente_prestamo_table.item(item, 'values')
            prestamo_data = {
                "ID Prestamo": prestamo_valores[0],
                "ID Libro": prestamo_valores[1],
                "ID Cliente": prestamo_valores[2],
                "Nombre": prestamo_valores[3],
                "ID Libro Prestamo": prestamo_valores[4],
                "Titulo": prestamo_valores[5],
                "F.Registro": prestamo_valores[6],
                "F.Limite": prestamo_valores[7],
                "Encargado": prestamo_valores[8]
            }
            prestamos_data.append(prestamo_data)

        if prestamos_data:
            imprimir = ImprimirPrestamo(prestamos_data)
            imprimir.obtener_datos()
        
    def verificar_eliminar(self):
        if self.parent.id_rol == 1:
            print("Sin permisos suficientes para eliminar!")
            messagebox.showinfo("AVISO", "Sin permisos suficientes para eliminar!")
        else:
            delete_selected_prestamo(self)
    
    def open_register_loan(self):
            Register_Loans(self, loans_validations)#loans_validations#client_values

    def boton_buscar(self, event=None):  
        busqueda = self.buscar.get()
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                self.cliente_prestamo_table.delete(*self.cliente_prestamo_table.get_children())
                # Ejecutar y procesar la consulta
                cursor.execute("""SELECT c.Cedula, c.Nombre AS Nombre_Cliente, l.titulo AS Nombre_Libro, p.Fecha_Registro, p.Fecha_Limite, u.Nombre AS Nombre_Usuario
                                FROM cliente_prestamo cp 
                                JOIN cliente c ON cp.ID_Cliente = c.ID_Cliente 
                                JOIN libro l ON cp.ID_Libro = l.ID_Libro
                                JOIN prestamo p ON cp.ID_Prestamo = p.ID_Prestamo
                                JOIN usuarios u ON cp.ID_Usuario = u.ID_Usuario 
                                WHERE c.Cedula=%s OR c.Nombre=%s OR l.titulo=%s 
                                OR p.Fecha_Registro=%s OR p.Fecha_Limite=%s OR u.Nombre=%s""", 
                            (busqueda, busqueda, busqueda, busqueda, busqueda, busqueda))
                resultados_prestamo = cursor.fetchall()
                
                for fila in resultados_prestamo:
                    if busqueda in map(str, fila):  # Convertir cada elemento de la fila a string para la comparación
                        self.cliente_prestamo_table.insert("", "end", values=tuple(fila))

                if resultados_prestamo:
                    messagebox.showinfo("Busqueda Éxitosa", "Resultados en pantalla.")
                else:
                    messagebox.showinfo("Busqueda Fallida", "No se encontraron resultados.")
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
        finally:
            if mariadb_conexion:
                mariadb_conexion.close()
    #FUNCION OPTIMIZADA Y MOVIDA a la clase Register_Loans a peticion de bing ya que alla es donde se usa, no aqui
    """def reading_books(self,book_table_list):
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

                                            # Insert new data into the Treeview
                                        for fila in resultados:
                                            book_table_list.insert("", "end", values=tuple(fila))
                                        mariadb_conexion.close()
                                except mariadb.Error as ex:
                                        print("Error durante la conexión:", ex)"""

    
    def update_selected_loan_due_date(self):
        selected_client = self.cliente_prestamo_table.selection()
        if selected_client:
            selected_client = selected_client[0]  # Obtener el primer elemento seleccionado
            client_values = self.cliente_prestamo_table.item(selected_client, "values")
            id_prestamo = client_values[7]  # Asumiendo que ID_Prestamo es el octavo valor en la tupla
            if update_loan_due_date(id_prestamo):
                messagebox.showinfo("Éxito", "La fecha límite del préstamo se ha actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar la fecha límite del préstamo.")
        else:
            messagebox.showwarning("Advertencia", "No hay ningún elemento seleccionado. Debe seleccionar un cliente para modificar el préstamo.")

    # def open_filter_loans_window(self):
    #     FilterLoansWindow(self, self.cliente_prestamo_table)


    # def open_modify_loans_window(self):
    #     selected_client= self.cliente_prestamo_table.selection()
    #     if selected_client:
    #         selected_client = selected_client[0]
    #         client_values = self.cliente_prestamo_table.item(selected_client, "values")
    #         #cedula = client_values[0]  # Asumiendo que la cédula es el primer valor en la tupla
    #         fecha_limite = client_values[4]  # Asumiendo que la fecha límite es el quinto valor en la tupla
    #         ModifyLoans(self, fecha_limite, loans_validations)
    #     else:
    #         messagebox.showwarning("Advertencia", "No hay ningún elemento seleccionado. Debe seleccionar un cliente para modificar el préstamo.")





    def on_treeview_select(self, event):
        # Obtener el elemento seleccionado
        selected_item = self.book_table_list.selection()[0]
        # Obtener los valores del elemento seleccionado
        item_values = self.book_table_list.item(selected_item, 'values')
        # Asumimos que el ID_Libro está en la primera columna
        self.ID_Libro = item_values[0]
    
    def on_loans_double_click(self, event):
        try:
            selected_item = self.cliente_prestamo_table.selection()[0]
            prestamo_valores = self.cliente_prestamo_table.item(selected_item, 'values')
            self.prestamo_data = {
                "ID Prestamo": prestamo_valores[0],
                "ID Libro": prestamo_valores[1],
                "ID Cliente": prestamo_valores[2],
                "Nombre": prestamo_valores[3],
                "ID Libro Prestamo": prestamo_valores[4],
                "Titulo": prestamo_valores[5],
                "F.Registro": prestamo_valores[6],
                "F.Limite": prestamo_valores[7],
                "Encargado": prestamo_valores[8]
            }
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                cursor.execute('''
                    SELECT 
                        p.ID_Prestamo
                    FROM prestamo p
                    JOIN cliente c ON p.ID_Cliente = c.ID_Cliente
                    WHERE p.ID_Cliente = %s AND c.Nombre = %s
                ''', (self.prestamo_data["ID Cliente"], self.prestamo_data["Nombre"]))
                ejemplares = cursor.fetchall()
                # Depuración: Mostrar cuántos préstamos coincidentes se encontraron
                print(f"Préstamos encontrados: {len(ejemplares)}")
                if not ejemplares:
                    print("No se encontraron registros coincidentes.")
                    return
                self.cliente_prestamo_table.selection_remove(self.cliente_prestamo_table.selection())
                for ejemplar in ejemplares:
                    for row in self.cliente_prestamo_table.get_children():
                        if self.cliente_prestamo_table.item(row, 'values')[0] == str(ejemplar[0]):
                            self.cliente_prestamo_table.selection_add(row)
                mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
            messagebox.showerror("Error", f"Error durante la conexión: {ex}")
        except IndexError:
            print("No se ha seleccionado ningún préstamo.")
            messagebox.showerror("Error", "No se ha seleccionado ningún préstamo.")


   
class ImprimirPrestamo:
    def __init__(self, selected_items):
        self.selected_items = selected_items
        self.user_data = {}
        self.books_data = []
        self.prestamos_data = self.selected_items.copy()

    def obtener_datos(self):
        cliente_id = self.prestamos_data[0]["ID Cliente"]
        print(f"Cliente ID: {cliente_id}")

        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                cursor.execute('''
                    SELECT Cedula_Cliente, Nombre, Apellido, Telefono, Direccion
                    FROM cliente
                    WHERE ID_Cliente = %s
                ''', (cliente_id,))
                resultado_cliente = cursor.fetchone()
                print(f"Resultado Cliente: {resultado_cliente}")
                if resultado_cliente:
                    self.user_data = {
                        "Cedula": resultado_cliente[0],
                        "Nombre": resultado_cliente[1],
                        "Apellido": resultado_cliente[2],
                        "Telefono": resultado_cliente[3],
                        "Direccion": resultado_cliente[4]
                    }

                cliente = Cliente(
                    cedula=self.user_data["Cedula"],
                    nombre=self.user_data["Nombre"],
                    apellido=self.user_data["Apellido"],
                    telefono=self.user_data["Telefono"],
                    direccion=self.user_data["Direccion"]
                )

                for prestamo in self.prestamos_data:
                    libro_id = prestamo["ID Libro"]
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
                        self.books_data.append(book_data)
                        prestamo.update({
                            "fecha_r": formatear_fecha(prestamo["F.Registro"]),
                            "fecha_en": formatear_fecha(prestamo["F.Limite"])
                        })

                print("Books Data:", self.books_data)
                print("Prestamos Data:", self.prestamos_data)

                fecha_actual = datetime.now().strftime("%d_%m_%Y")
                nombre_corregido = self.user_data.get("Nombre", "").replace(" ", "_")
                nombre_archivo_base = f"Reporte_de_prestamo_{nombre_corregido}_{fecha_actual}"
                generar_pdf(cliente, self.books_data, self.prestamos_data, nombre_archivo_base)

        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
            messagebox.showerror("Error", f"Error durante la conexión")

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta


# Asegúrate de que P_Listar está definido/importado correctamente
class Register_Loans(P_Listar):
    def __init__(self, parent, loans_validations):
        super().__init__(parent)  # Llamar al constructor de la clase base
        self.parent = parent
        self.loans_validations = loans_validations
        self.register_loan_window = tk.Toplevel(parent)
        self.validate_number = self.register(validate_number_input)
        # Datos y paginación
        self.data = []
        self.page_size = 19
        self.current_page = 0
        
        self.setup_window()

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
        self.cedula = tk.Entry(self.register_loan_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat",validate="key", validatecommand=(self.validate_number, "%P"))
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
        self.reading_books()
        
        
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
        #self.cedula.bind("<Return>", lambda event: self.save_modifications())
    def reading_books(self):
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                cursor.execute('SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, titulo, autor, editorial, año, edicion, n_volumenes, n_ejemplares, FROM libro')
                self.data = cursor.fetchall()  # Almacena los datos en self.data
                mariadb_conexion.close()
                self.display_page()  # Llama a display_page() para mostrar los datos paginados
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)

    def get_data_page(self, offset, limit):
        return self.data[offset:offset + limit]

    def display_page(self):
        for row in self.book_table_list.get_children():
            self.book_table_list.delete(row)
        page_data = self.get_data_page(self.current_page * self.page_size, self.page_size)
        for fila in page_data:
            n_ejemplares = fila[11]
            tag = 'multiple' if n_ejemplares > 1 else 'single'
            parent = self.book_table_list.insert("", "end", values=tuple(fila), tags=(tag,))
            if n_ejemplares > 1:
                for i in range(1, n_ejemplares + 1):
                    self.book_table_list.insert(parent, "end", text=f"Ejemplar {i}", values=tuple(fila), tags=('single',))
        self.book_table_list.tag_configure('multiple', background='lightblue')
        self.book_table_list.tag_configure('single', background='#E5E1D7')
        self.update_page_label()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.data):
            self.current_page += 1
            self.display_page()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def update_page_label(self):
        total_pages = (len(self.data) + self.page_size - 1) // self.page_size  # Calcular el total de páginas
        self.page_label.config(text=f"Página {self.current_page + 1} de {total_pages}")
        
    def save_modifications(self):
        fecha_registrar = loans_validations.format_date(self.fecha_registrar.get())
        fecha_limite = loans_validations.format_date(self.fecha_limite.get())

        ID_Libro_Prestamo = loans_validations.generate_id_libro_prestamo(self)
        Cedula = self.cedula.get()
        if hasattr(self, 'ID_Libro'):
            ID_Libro = self.ID_Libro
        else:
            messagebox.showerror("Error", "Por favor, selecciona un libro de la lista.", parent=self.register_loan_window)
            return
        ID_Cliente = loans_validations.get_cliente_id_by_cedula(Cedula)
        if ID_Cliente is None:
            messagebox.showerror("Error", "No se pudo obtener la ID del Cliente. Ingrese un N° de Cédula existente", parent=self.register_loan_window)
            return

        # Asignar ID de usuario (esto parece ser un valor fijo, podrías mejorarlo)
        ID_Usuario = 1 or 2 or 3 or 4 or 5
        if ID_Usuario is None:
            messagebox.showerror("Error", "No se pudo obtener el ID de usuario.", parent=self.register_loan_window)
            return

        # Generar un nuevo ID_Prestamo
        ID_Prestamo = loans_validations.generate_alphanumeric_id()
        print(f"Nuevo ID_Prestamo generado: {ID_Prestamo}")

        if create_loan(ID_Cliente, ID_Prestamo, fecha_registrar, fecha_limite):
            if update_all_tables(ID_Cliente, ID_Libro, ID_Libro_Prestamo, ID_Prestamo, ID_Usuario):
                messagebox.showinfo("Éxito", f"""DATOS
                Registro éxitoso del préstamo.
                ID Cliente_Prestamo: {ID_Prestamo}
                ID Libro Préstamo: {ID_Libro_Prestamo}
                """, parent=self.register_loan_window)
                loans_validations.clear_entries_list_register(self)
            else:
                messagebox.showerror("Error", "No se pudo actualizar las tablas. Puede que no haya ejemplares disponibles.", parent=self.register_loan_window)
        else:
            messagebox.showerror("Error", "Préstamo no pudo ser creado.", parent=self.register_loan_window)


    def cancelar(self, window):
            if messagebox.askyesno(
                    "Advertencia",
                    "¿Seguro que quieres cerrar esta ventana? Perderás los datos del registro del préstamo.",parent=window):
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

# class FilterLoansWindow:
#     def __init__(self, parent ,prestamo_table):
#         self.parent = parent
#         self.prestamo_table = prestamo_table
#         self.filter_window = tk.Toplevel(parent)
#         self.setup_window()

#     def setup_window(self):
#         self.filter_window.title("Filtrar")
#         self.filter_window.iconbitmap(resource_path('assets_2/logo_biblioteca.ico'))
#         self.filter_window.geometry("950x450")
#         self.filter_window.config(bg="#042344")
#         self.filter_window.resizable(False, False)
#         self.filter_window.grab_set()
#         self.filter_window.protocol("WM_DELETE_WINDOW", lambda: self.cancelar(self.filter_window))
        
#         rectangulo_color = tk.Label(self.filter_window, bg="#2E59A7", width=200, height=4)
#         rectangulo_color.place(x=0, y=0)
#         tk.Label(self.filter_window, text="Tabla de Prestamos", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=250.0, y=20.0, width=450.0, height=35.0)
#         tk.Label(self.filter_window, text="Ingrese el ID de Prestamo, Cliente y Libro Prestamo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=10.0, y=80.0, width=530.0, height=35.0)

#         tk.Label(self.filter_window, text="ID Prestamo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=240.0, y=130.0, width=120.0, height=35.0)
#         self.id_prestamos_entry = tk.Entry(self.filter_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         self.id_prestamos_entry.place(x=240.0, y=170.0, width=190.0, height=35.0)

#         tk.Label(self.filter_window, text="ID Cliente", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=460.0, y=130.0, width=185.0, height=35.0)
#         self.id_cliente_entry = tk.Entry(self.filter_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         self.id_cliente_entry.place(x=500.0, y=170.0, width=190.0, height=35.0)

#         tk.Label(self.filter_window, text="ID Libro Prestamo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=240.0, y=230.0, width=180.0, height=35.0)
#         self.id_libro_cliente_entry = tk.Entry(self.filter_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         self.id_libro_cliente_entry.place(x=240.0, y=270.0, width=190.0, height=35.0)

#         self.images = {}
#         self.images['boton_m'] = tk.PhotoImage(file=resource_path("assets_2/boton_filtrar.png"))
#         self.boton_M = tk.Button(
#             self.filter_window,
#             image=self.images['boton_m'],
#             borderwidth=0,
#             highlightthickness=0,
#             command=self.apply_filters,
#             relief="flat",
#             bg="#031A33",
#             activebackground="#031A33",
#             activeforeground="#FFFFFF"
#         )
#         self.boton_M.place(x=530.0, y=350.0, width=130.0, height=40.0)

#         self.images['boton_c'] = tk.PhotoImage(file=resource_path("assets_2/c_button_red1.png"))
#         self.boton_C = tk.Button(
#             self.filter_window,
#             image=self.images['boton_c'],
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: self.cancelar(self.filter_window),
#             relief="flat",
#             bg="#031A33",
#             activebackground="#031A33",
#             activeforeground="#FFFFFF"
#         )
#         self.boton_C.place(x=270.0, y=350.0, width=130.0, height=40.0)

    

#     def apply_filters(self):
#         # Suponiendo que filter_books es una función definida en algún lugar para filtrar los libros.
#         filter_books(self)
    
#     def cancelar(self, window):
#         if messagebox.askyesno("Advertencia", "¿Seguro que quieres cerrar esta ventana?", parent=self.filter_window):
#             window.destroy()
#             lists_clients_loans(self)

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
from db.conexion import establecer_conexion
mariadb_conexion = establecer_conexion()

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
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        self.canvas.create_text(840.0, 180.0, text="Refrescar", fill="black", font=("Bold", 17))
        self.canvas.create_text(940.0, 180.0, text="Imprimir", fill="black", font=("Bold", 17))
        self.canvas.create_text(1040.0, 180.0, text="Agregar", fill="black", font=("Bold", 17))
        self.canvas.create_text(1140.0, 180.0, text="Editar", fill="black", font=("Bold", 17))
        self.canvas.create_text(1240.0, 180.0, text="Eliminar", fill="black", font=("Bold", 17))

        self.right_frame_list_loans = tk.Frame(self.canvas, bg="#FAFAFA")
        self.right_frame_list_loans.pack(expand=True, side="right", fill="both") #padx=212, pady=150, ipady=80
        self.right_frame_list_loans.place(x=195,y=239, height=460, width=1180)

        bold_font = font.Font(family="Bold", size=15, weight="bold")
        self.label_clientes = tk.Label(self.canvas, text="Tabla Clientes", bg="#FAFAFA", fg="black", font=bold_font)
        self.label_clientes.place(x=655.0, y=205.0, width=237.0, height=38.0)

        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.buscar.place(x=265.0, y=130.0, width=267.0, height=48.0)
        
        self.label_nombre = self.canvas.create_text(265.0, 100.0, anchor="nw", text="Buscar", fill="black", font=("Bold", 17))
        self.buscar.bind("<Return>", self.boton_buscar)

        # Cargar y almacenar las imágenes
        self.images['boton_refrescar'] = tk.PhotoImage(file=relative_to_assets("16_refrescar.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_refrescar'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: reading_clients(self.clients_table_list_loans),
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=795.0, y=70.0, width=90.0, height=100.0)

        self.images['boton_imprimir'] = tk.PhotoImage(file=relative_to_assets("4_imprimir.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_imprimir'],
                borderwidth=0,
                highlightthickness=0,
                # command=lambda: self.reading_books(self.book_table_list),
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=895.0, y=70.0, width=90.0, height=100.0)

        self.images['boton_agregar'] = tk.PhotoImage(file=relative_to_assets("5_agregar.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_agregar'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.open_register_window(),
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=995.0, y=70.0, width=90.0, height=100.0)

        self.images['boton_Eliminar'] = tk.PhotoImage(file=relative_to_assets("7_eliminar.png"))
                    # Cargar y almacenar la imagen del botón
        self.button_dl = tk.Button(
            self,
            image=self.images['boton_Eliminar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: delete_client_loans(self),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_dl.place(x=1195.0, y=70.0, width=90.0, height=100.0)

        self.images['boton_modificar'] = tk.PhotoImage(file=relative_to_assets("6_editar.png"))
            # Cargar y almacenar la imagen del botón
        self.button_dl = tk.Button(
            self,
            image=self.images['boton_modificar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_modify_window(),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_dl.place(x=1095.0, y=70.0, width=90.0, height=100.0)

        styletrees = ttk.Style()
        styletrees.configure("Rounded.Treeview", 
                        borderwidth=2, 
                        relief="groove", 
                        bordercolor="blue", 
                        lightcolor="lightblue", 
                        darkcolor="darkblue",
                        rowheight=30,
                        background="#E5E1D7", 
                        fieldbackground="#f0f0f0")

        # Configurar estilo para las cabeceras
        styletrees.configure("Rounded.Treeview.Heading", 
                        font=('Helvetica', 10, 'bold'), 
                        background="#2E59A7", 
                        foreground="#000000",
                        borderwidth=0)

        columns = ("ID Cliente","ID Prestamo", "N° Cedula", "Nombre", "Apellido", "Teléfono", "Dirección")
        self.clients_table_list_loans= ttk.Treeview(self.right_frame_list_loans, columns=columns, show='headings', selectmode='extended', style="Rounded.Treeview")
        
        self.clients_table_list_loans.column("ID Cliente", width=20, anchor="center")
        self.clients_table_list_loans.column("ID Prestamo", width=20, anchor="center")

        for col in columns:
            if col not in ("ID Cliente", "ID Prestamo"):
                self.clients_table_list_loans.column(col, width=85, anchor="center")
            self.clients_table_list_loans.heading(col, text=col)
        self.clients_table_list_loans.pack(expand=True, fill="both", padx=30, pady=5)

        scrollbar_pt = ttk.Scrollbar(self.clients_table_list_loans, orient="vertical", command=self.clients_table_list_loans.yview)
        self.clients_table_list_loans.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")

        reading_clients (self.clients_table_list_loans)

    def open_register_window(self):
        filter_window = tk.Toplevel(self)
        filter_window.title("Registro")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        filter_window.geometry("950x400")
        filter_window.config(bg="#042344")
        
        tk.Label(filter_window, text="REGISTRO DE CLIENTES", fg="#ffffff", bg="#042344", font=("Bold", 25)).place(x=270.0, y=20.0, width=400.0, height=35.0)
        tk.Label(filter_window, text="Cedula", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=10.0, y=100.0, width=120.0, height=35.0)
        self.input_cedula = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_cedula.place(x=30.0, y=130.0, width=190.0, height=35.0)

        tk.Label(filter_window, text="Nombre", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=240.0, y=100.0, width=120.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.input_nombre = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_nombre.place(x=260.0, y=130.0, width=190.0, height=35.0)

        tk.Label(filter_window, text="Apellido", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=470.0, y=100.0, width=120.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=7, column=0, padx=10, pady=5)
        self.input_apellido = tk.Entry(filter_window,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_apellido.place(x=490.0, y=130.0, width=190.0, height=35.0)
        
        tk.Label(filter_window, text="Telefono", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=710.0, y=100.0, width=120.0, height=35.0)
        self.input_telefono = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_telefono.place(x=720.0, y=130.0, width=190.0, height=35.0)

        tk.Label(filter_window, text="Direccion", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=30.0, y=240.0, width=120.0, height=35.0)
        self.input_direccion = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_direccion.place(x=30.0, y=270.0, width=190.0, height=35.0)

                # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("R_Boton_registrar.png"))

        self.boton_R = tk.Button(
            filter_window,
            image=self.images['boton_R'],
            borderwidth=0,
            highlightthickness=0,
            command=self.register_client,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_R.place(x=265.0, y=450.0, width=130.0, height=40.0)
        self.boton_R.place_forget()  # Ocultar el botón inicialmente

        # Vincular la validación a los eventos de los campos de entrada
        self.input_cedula.bind("<KeyRelease>", self.validate_entries)
        self.input_nombre.bind("<KeyRelease>", self.validate_entries)
        self.input_apellido.bind("<KeyRelease>", self.validate_entries)
        self.input_telefono.bind("<KeyRelease>", self.validate_entries)
        self.input_direccion.bind("<KeyRelease>", self.validate_entries)

        # Crear un estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TButton", background="#2E59A7", foreground="#ffffff", font=("Bold", 22))

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.place(x=500.0, y=300.0, width=140.0, height=50.0)
    
    def open_modify_window(self):
        filter_window = tk.Toplevel(self)
        filter_window.title("Registro")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        filter_window.geometry("950x400")
        filter_window.config(bg="#042344")
        
        tk.Label(filter_window, text="MODIFICACIÓN DE CLIENTES", fg="#ffffff", bg="#042344", font=("Bold", 25)).place(x=270.0, y=20.0, width=420.0, height=35.0)
        tk.Label(filter_window, text="Cedula", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=10.0, y=100.0, width=120.0, height=35.0)
        self.input_cedula = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_cedula.place(x=30.0, y=130.0, width=190.0, height=35.0)

        tk.Label(filter_window, text="Nombre", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=240.0, y=100.0, width=120.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.input_nombre = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_nombre.place(x=260.0, y=130.0, width=190.0, height=35.0)

        tk.Label(filter_window, text="Apellido", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=470.0, y=100.0, width=120.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=7, column=0, padx=10, pady=5)
        self.input_apellido = tk.Entry(filter_window,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_apellido.place(x=490.0, y=130.0, width=190.0, height=35.0)
        
        tk.Label(filter_window, text="Telefono", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=710.0, y=100.0, width=120.0, height=35.0)
        self.input_telefono = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_telefono.place(x=720.0, y=130.0, width=190.0, height=35.0)

        tk.Label(filter_window, text="Direccion", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=30.0, y=240.0, width=120.0, height=35.0)
        self.input_direccion = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_direccion.place(x=30.0, y=270.0, width=190.0, height=35.0)

        self.modify_client()

                        # Cargar y almacenar las imágenes
        self.images['boton_m'] = tk.PhotoImage(file=relative_to_assets("M_Boton.png"))

        self.boton_R = tk.Button(
            filter_window,
            image=self.images['boton_m'],
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

        # Vincular la validación a los eventos de los campos de entrada
        self.input_cedula.bind("<KeyRelease>", self.validate_entries)
        self.input_nombre.bind("<KeyRelease>", self.validate_entries)
        self.input_apellido.bind("<KeyRelease>", self.validate_entries)
        self.input_telefono.bind("<KeyRelease>", self.validate_entries)
        self.input_direccion.bind("<KeyRelease>", self.validate_entries)

        # Crear un estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TButton", background="#2E59A7", foreground="#ffffff", font=("Bold", 22))

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.place(x=500.0, y=300.0, width=140.0, height=50.0)
        
    def cancelar(self, window):
        window.destroy()  # Esto cerrará la ventana de filtro

    def register_client(self):
        ID_Cedula= self.input_cedula.get() 
        nombre = self.input_nombre.get()
        apellido = self.input_apellido.get()
        telefono= str(self.input_telefono.get())
        direccion=self.input_direccion.get()
        if self.cedula_existe(ID_Cedula):
            messagebox.showinfo("Error", "La cédula ya está registrada.")
            return
        if create_client_loans(ID_Cedula, nombre, apellido, telefono, direccion):
            messagebox.showinfo("Éxito", "Registro éxitoso del cliente.")
            self.clear_entries_register_loans()
        else:
            messagebox.showinfo("Registro fallido", "Cliente no pudo ser registrado.")
    
    def modify_client(self):
        selected_item = self.clients_table_list_loans.selection()
        if selected_item:
            item_values = self.clients_table_list_loans.item(selected_item, 'values')
            self.input_cedula.delete(0, tk.END)
            self.input_cedula.insert(0, item_values[2])
            self.input_nombre.delete(0, tk.END)
            self.input_nombre.insert(0, item_values[3])
            self.input_apellido.delete(0, tk.END)
            self.input_apellido.insert(0, item_values[4])
            self.input_telefono.delete(0, tk.END)
            self.input_telefono.insert(0, item_values[5])
            self.input_direccion.delete(0, tk.END)
            self.input_direccion.insert(0, item_values[6])
            self.current_id_cliente = item_values[0]
        else:
            messagebox.showwarning("Selección vacía", "Por favor, seleccione un cliente de la tabla.")

    def save_modifications(self):
        new_cedula = self.input_cedula.get()  # Si la cédula se puede modificar, obtén el nuevo valor
        nombre = self.input_nombre.get()
        apellido = self.input_apellido.get()
        telefono = self.input_telefono.get()
        direccion = self.input_direccion.get()
        id_cliente = self.current_id_cliente
    
        if modify_client_loans(id_cliente, new_cedula, nombre, apellido, telefono, direccion):
            messagebox.showinfo("Éxito", "Modificación exitosa del cliente.")
            self.clear_entries_register_loans()
        else:
            messagebox.showerror("Error", "Cliente no pudo ser modificado.")

    def cedula_existe(self,cedula):
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            query = "SELECT COUNT(*) FROM cliente WHERE Cedula_Cliente = %s"
            cursor.execute(query, (cedula,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        
    def clear_entries_register_loans(self):
        self.input_cedula.delete(0, tk.END)
        self.input_nombre.delete(0, tk.END)
        self.input_apellido.delete(0, tk.END)
        self.input_telefono.delete(0, tk.END)
        self.input_direccion.delete(0, tk.END)
        #self.input_cantidad.delete(0, tk.END)
    
    def generate_alphanumeric_id(self, length=8):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))

    def validate_entries(self, event=None):
        # Comprobar si todos los campos están llenos
        if (self.input_cedula.get() and self.input_nombre.get() and self.input_apellido.get() and
                self.input_telefono.get() and self.input_direccion.get()):
                # self.fecha_registrar.get() and self.fecha_limite.get()):
            self.boton_R.place(x=740.0, y=300.0, width=130.0, height=40.0)  # Mostrar el botón
        else:
            self.boton_R.place_forget()  # Ocultar el botón si algún campo está vacío

    def boton_buscar(self, event):
        busqueda= self.buscar.get()
        try:
             mariadb_conexion = establecer_conexion()
             if mariadb_conexion:#.is_connected():
                        cursor = mariadb_conexion.cursor()
                        cursor.execute("""SELECT ID_Cliente, ID_Prestamo, Cedula_Cliente, Nombre, Apellido,
                                        Telefono, Direccion FROM cliente WHERE 
                                        ID_Cliente=%s OR ID_Prestamo=%s OR Cedula_Cliente=%s OR 
                                        Nombre=%s OR Apellido=%s OR Telefono=%s OR 
                                        Direccion=%s""", 
                           (busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda))
                        resultados = cursor.fetchall() 

                        self.clients_table_list_loans.delete(*self.clients_table_list_loans.get_children())
                        for fila in resultados:
                            self.clients_table_list_loans.insert("", "end", values=tuple(fila))
                            if busqueda in fila:
                                self.clients_table_list_loans.item(self.clients_table_list_loans.get_children()[-1], tags='match')
                            else:
                                self.clients_table_list_loans.item(self.clients_table_list_loans.get_children()[-1], tags='nomatch')
                        self.clients_table_list_loans.tag_configure('match', background='green')
                        self.clients_table_list_loans.tag_configure('nomatch', background='gray')
                        if resultados:
                            messagebox.showinfo("Busqueda Éxitosa", "Resultados en pantalla.")
                        else:
                            messagebox.showinfo("Busqueda Fallida", "No se encontraron resultados.")
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
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        #validate_number = self.register(validate_number_input)
        self.images = {}

        #Marco listado prestamo-clientes
        # self.left_frame2 = tk.Frame(self.canvas, bg="#FFFFFF")
        self.left_frame2 = tk.Frame(self.canvas, bg="#FAFAFA")
        self.left_frame2.pack(expand=True, side="right", fill="both")
        self.left_frame2.place(x=200,y=220, height=490, width=1180)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side="right", expand=True, fill="both")

        # Texto para el nombre

        self.label_nombre = self.canvas.create_text(265.0, 100.0, anchor="nw", text="Buscar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1035.0, 200.0, text="Editar", fill="#031A33", font=("Bold", 17))
        self.canvas.create_text(1135.0, 200.0, text="Eliminar", fill="#031A33", font=("Bold", 17))
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
            command=lambda: delete_selected_prestamo(self),
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


        scrollbar_pt = ttk.Scrollbar(self.prestamo_table, orient="vertical", command=self.prestamo_table.yview)
        self.prestamo_table.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
    
    def open_register_loan(self):
        filter_window = tk.Toplevel(self)
        filter_window.title("Registrar Préstamo")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        filter_window.geometry("1550x600")
        filter_window.config(bg="#042344")

        # Crear el marco izquierdo para el menú de navegación
        self.left_frame_list = tk.Frame(filter_window, bg="#042344")
        self.left_frame_list.place(x=170, y=160, height=400, width=1200)

        tk.Label(filter_window, text="TABLA PRESTAMOS", fg="#ffffff", bg="#042344", font=("Bold", 25)).place(x=505.0, y=20.0, width=450.0, height=35.0)
        tk.Label(filter_window, text="ID Cliente", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=600.0, y=70.0, width=160.0, height=35.0)
        self.id_cliente = tk.Entry(filter_window,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.id_cliente.place(x=630.0, y=100.0, width=190.0, height=35.0)

        tk.Label(filter_window, text="Fecha Registrar", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=20.0, y=140.0, width=160.0, height=35.0)
        self.fecha_registrar = tk.Entry(filter_window,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.fecha_registrar.place(x=20.0, y=170.0, width=170.0, height=35.0)
        
        tk.Label(filter_window, text="Fecha Limite", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=20.0, y=240.0, width=160.0, height=35.0)
        self.fecha_limite = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.fecha_limite.place(x=20.0, y=270.0, width=170.0, height=35.0)

        tk.Label(filter_window, text="Cantidad", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=25.0, y=340, width=105.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.input_cantidad = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.input_cantidad.place(x=20.0, y=370.0, width=170.0, height=35.0)#.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)

        # Establecer las fechas automáticamente
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        fecha_limite = (datetime.now() + timedelta(days=0)).strftime("%d/%m/%Y")

        self.fecha_registrar.insert(0, fecha_actual)
        self.fecha_limite.insert(0, fecha_limite)

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

        self.images['boton_r'] = tk.PhotoImage(file=relative_to_assets("R_Boton_registrar.png"))

        self.boton_R = tk.Button(
            filter_window,
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

        self.input_cantidad.bind("<KeyRelease>", self.validate_entries)

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
        filter_window.geometry("950x550")
        filter_window.config(bg="#042344")

        tk.Label(filter_window, text="TABLA PRESTAMOS", fg="#ffffff", bg="#042344", font=("Bold", 25)).place(x=250.0, y=20.0, width=450.0, height=35.0)#.pack(pady=20,expand=False)#.grid(row=4, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese el ID de Prestamo, Cliente y Libro Prestamo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=10.0, y=70.0, width=530.0, height=35.0)#.pack(pady=10, expand=False)
        tk.Label(filter_window, text="ID Prestamo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=210.0, y=130.0, width=120.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=5, column=0, padx=10, pady=5)
        self.id_prestamos_entry = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.id_prestamos_entry.place(x=240.0, y=170.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="ID Cliente", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=500.0, y=130.0, width=185.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.id_cliente_entry = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.id_cliente_entry.place(x=500.0, y=170.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="ID Libro Prestamo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=240.0, y=230.0, width=180.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=7, column=0, padx=10, pady=5)
        self.id_libro_cliente_entry = tk.Entry(filter_window,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.id_libro_cliente_entry.place(x=240.0, y=270.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=7, column=1, padx=10, pady=5)

         # Crear un estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TButton", background="#2E59A7", foreground="#ffffff", font=("Bold", 22))

        # Botón para filtrar
        self.filter_button = ttk.Button(filter_window, text="Filtrar", style="Custom.TButton", command=self.apply_filters)
        self.filter_button.place(x=250.0, y=480.0, width=140.0, height=50.0)#.pack(expand=True)#.place(x=390, y=400)

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.place(x=520.0, y=480.0, width=140.0, height=50.0)#.pack(pady=5, expand=False)
    
    def open_filter_window_modify(self,parent):
        filter_window = tk.Toplevel(self)
        filter_window.title("Modificar Préstamo")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        filter_window.geometry("950x550")
        filter_window.config(bg="#042344")

        tk.Label(filter_window, text="MODIFICACIÓN DE PRÉSTAMO", fg="#ffffff", bg="#042344", font=("Bold", 25)).place(x=250.0, y=20.0, width=450.0, height=35.0)#.pack(pady=20,expand=False)#grid(row=0, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese los datos a modificar", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=10.0, y=70.0, width=330.0, height=35.0)#.pack(pady=10, expand=False)
        tk.Label(filter_window, text="Fecha Limite", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=237.0, y=130.0, width=130.0, height=35.0)#.pack(pady=10,expand=False)#grid(row=1, column=0, padx=10, pady=5)
        self.fecha_limite_entry = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.fecha_limite_entry.place(x=240.0, y=170.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="Cantidad", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=449.0, y=130.0, width=185.0, height=35.0)#.pack(pady=10,expand=False)#.grid(row=3, column=0, padx=10, pady=5)
        self.cantidad_entry = tk.Entry(filter_window, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.cantidad_entry.place(x=500.0, y=170.0, width=190.0, height=35.0)#pack(expand=False)#.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="ID del prestamo que será modificado", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=30.0, y=320.0, width=350.0, height=35.0)#.pack(pady=10, expand=False)
        tk.Label(filter_window, text="ID", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=300.0, y=360.0, width=120.0, height=35.0)#.pack(pady=10,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.id_prestamo_entry = tk.Entry(filter_window,  bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="flat")
        self.id_prestamo_entry.place(x=350.0, y=400.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)

        # Crear un estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TButton", background="#2E59A7", foreground="#ffffff", font=("Bold", 22))

        self.filter_button = ttk.Button(filter_window, text="Modificar", style="Custom.TButton", command=self.apply_filters_modify)
        self.filter_button.place(x=250.0, y=480.0, width=140.0, height=50.0)

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.place(x=520.0, y=480.0, width=140.0, height=50.0)#.pack(expand=True)#.place(x=390, y=400)#.pack(pady=5, expand=False)

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
                    self.clear_entries_list()
                        #return True
                else:
                    messagebox.showinfo("Fallido", "La modificación del prestamo no pudo ejecutarse.")
                        #return False
            else:
                    messagebox.showinfo("Cancelado", "Modificación cancelada.")
        else:
                messagebox.showinfo("Error", "Por favor, proporciona una ID válida.")
    
    def save_modifications(self):
        fecha_registrar = self.format_date(self.fecha_registrar.get())
        fecha_limite = self.format_date(self.fecha_limite.get())
        Cantidad = int(self.input_cantidad.get())
        ID_Prestamo = self.generate_alphanumeric_id()
        ID_Libro_Prestamo = self.generate_id_libro_prestamo()
        ID_Cliente = self.id_cliente.get()
                # Asegúrate de que ID_Libro esté definido
        if hasattr(self, 'ID_Libro'):
            ID_Libro = self.ID_Libro
        else:
            messagebox.showerror("Error", "Por favor, selecciona un libro de la lista.")
            return
            # Obtener ID_Usuario
        ID_Usuario = 1 or 2 or 3
        if ID_Usuario is None:
            messagebox.showerror("Error", "No se pudo obtener el ID de usuario.")
            return
        if create_loan(ID_Prestamo, fecha_registrar, fecha_limite):
            if create_libro_prestamo(ID_Libro_Prestamo, ID_Prestamo, ID_Libro, Cantidad):
                if update_prestamo_with_cliente(ID_Prestamo, ID_Cliente, ID_Libro_Prestamo):
                    if update_prestamo_and_libro(ID_Prestamo, ID_Cliente, ID_Libro, ID_Libro_Prestamo, Cantidad):
                            # Actualizar la tabla prestamo con ID_Usuario
                        if update_prestamo_with_usuario(ID_Prestamo, ID_Usuario):
                             if update_cliente_with_prestamo(ID_Cliente, ID_Prestamo):
                                messagebox.showinfo("Éxito", 
f"""
Registro éxitoso del préstamo. 
ID Préstamo: {ID_Prestamo}
ID Libro Préstamo: {ID_Libro_Prestamo}
""")
                        self.clear_entries_list()
            else:
                messagebox.showerror("Error", "Préstamo no pudo ser creado.")    
    #Boton de filtrado del Menú Lista-Prestamos
    def apply_filters(self):
        filter_books_one(self)
        filter_books_two(self)
        filter_books_three(self)

    def clear_entries_list(self):
        # elf.id_prestamo_entry.delete(0, tk.END)
        self.input_cantidad.delete(0, tk.END)
        # self.fecha_limite_entry.delete(0, tk.END)
    
    def validate_entries(self, event=None):
        # Comprobar si todos los campos están llenos
        if (self.input_cantidad.get()):
            self.boton_R.place(x=40.0, y=450.0, width=130.0, height=40.0)  # Mostrar el botón
        else:
            self.boton_R.place_forget()  # Ocultar el botón si algún campo está vacío

    def generate_alphanumeric_id(self, length=6):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))
    
    def format_date(self, date_str):
        try:
            # Convertir la fecha del formato DD/MM/YYYY al formato YYYY-MM-DD
            formatted_date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            return formatted_date
        except ValueError as e:
            print(f"Error al formatear la fecha: {e}")
            return None

    def generate_id_libro_prestamo(self):
        while True:
            new_id = random.randint(1000, 9999)
            if not libro_prestamo_exists(new_id):
                return new_id
            
    def cancelar(self, window):
        window.destroy()  # Esto cerrará la ventana de filtro

    def on_treeview_select(self, event):
        # Obtener el elemento seleccionado
        selected_item = self.book_table_list.selection()[0]
        # Obtener los valores del elemento seleccionado
        item_values = self.book_table_list.item(selected_item, 'values')
        # Asumimos que el ID_Libro está en la primera columna
        self.ID_Libro = item_values[0]
        

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
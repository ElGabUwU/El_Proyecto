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
from tkinter import messagebox
from util.Reporte_PDF import generar_pdf
from loans.backend.models import Cliente, Libro
from validations import clients_validations

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

class C_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.parent=parent
        validate_number = self.register(validate_number_input)
        self.images = {}

        self.canvas.create_text(940.0, 180.0, text="Refrescar", fill="black", font=("Bold", 17))
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
            command=lambda: clients_validations.verificar_eliminar(self),
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
            command=lambda: self.verify_selected_item(), #verificar que halla un elemento seleccionado antes de abrir la ventana emergente
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
        register_window = tk.Toplevel(self)
        register_window.title("Registro")
        register_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        register_window.geometry("950x400")
        register_window.config(bg="#042344")
        register_window.resizable(False, False)
        self.register_window=register_window
        # ESTO ME SIRVE PARA LA VENTANA DE LIBROS!!!!
        #lienzo.create_rectangle(0, 0, 950, 74, fill="#2E59A7")
        
        rectangulo_color = tk.Label(register_window, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)  # Posición del rectángulo dentro de la ventana
        tk.Label(register_window, text="Registro de Clientes", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=270.0, y=13.0, width=400.0, height=40.0)
        tk.Label(register_window, text="Cedula", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=3.0, y=100.0, width=120.0, height=35.0)
        self.input_cedula = tk.Entry(register_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.input_cedula.place(x=33.0, y=130.0, width=190.0, height=35.0)
        #que es esto???

        tk.Label(register_window, text="Nombres", fg="#CCCED1", bg="#042344", font=("Montserrat Regular",15)).place(x=243.0, y=100.0, width=120.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.input_nombre = tk.Entry(register_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.input_nombre.place(x=263.0, y=130.0, width=190.0, height=35.0)

        tk.Label(register_window, text="Apellidos", fg="#CCCED1", bg="#042344", font=("Montserrat Regular",15)).place(x=474.0, y=100.0, width=120.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=7, column=0, padx=10, pady=5)
        self.input_apellido = tk.Entry(register_window,  bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.input_apellido.place(x=493.0, y=130.0, width=190.0, height=35.0)
        
        tk.Label(register_window, text="Teléfono", fg="#CCCED1", bg="#042344", font=("Montserrat Regular",15)).place(x=700.0, y=100.0, width=120.0, height=35.0)
        self.input_telefono = tk.Entry(register_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.input_telefono.place(x=723.0, y=130.0, width=190.0, height=35.0)

        tk.Label(register_window, text="Dirección", fg="#CCCED1", bg="#042344", font=("Montserrat Regular",15)).place(x=14.0, y=200.0, width=120.0, height=35.0)
        self.input_direccion = tk.Entry(register_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.input_direccion.place(x=33.0, y=230.0, width=190.0, height=35.0)

                # Cargar y almacenar las imágenes
                
        self.images['boton_C'] = tk.PhotoImage(file=relative_to_assets("L_cancelar.png"))

        self.boton_C = tk.Button(
            register_window,
            image=self.images['boton_C'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.cancelar(register_window),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_C.place(x=753.0, y=300.0, width=130.0, height=40.0)
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("R_button_light_blue.png"))

        self.boton_R = tk.Button(
            register_window,
            image=self.images['boton_R'],
            borderwidth=0,
            highlightthickness=0,
            command=self.register_client,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        
        # Configurar eventos para validar entradas
        self.input_cedula.bind("<KeyRelease>", lambda event: clients_validations.validate_entries(self, event))
        self.input_nombre.bind("<KeyRelease>", lambda event: clients_validations.validate_entries(self, event))
        self.input_apellido.bind("<KeyRelease>", lambda event: clients_validations.validate_entries(self, event))
        self.input_telefono.bind("<KeyRelease>", lambda event: clients_validations.validate_entries(self, event))
        self.input_direccion.bind("<KeyRelease>", lambda event: clients_validations.validate_entries(self, event))

        # Crear un estilo personalizado
        """style = ttk.Style()
        style.configure("Custom.TButton", background="#2E59A7", foreground="#ffffff", font=("Bold", 22))

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.place(x=500.0, y=300.0, width=140.0, height=50.0)"""
    def verify_selected_item(self):
        selected_item = self.clients_table_list_loans.selection()
        if selected_item:
            self.open_modify_window()
        else:
            messagebox.showwarning("Selección vacía", "Por favor, seleccione un cliente de la tabla.")
    def open_modify_window(self):
        selected_item = self.clients_table_list_loans.selection()
        
        modify_window = tk.Toplevel(self)
        modify_window.title("Modificar")
        modify_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        modify_window.geometry("950x400")
        modify_window.config(bg="#042344")
        modify_window.resizable(False, False)
        self.modify_window=modify_window
        rectangulo_color = tk.Label(modify_window, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)
        tk.Label(modify_window, text="Modificación de Clientes", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=270.0, y=20.0, width=420.0, height=35.0)
        tk.Label(modify_window, text="Cedula", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=3.0, y=100.0, width=120.0, height=35.0)
        self.input_cedula = tk.Entry(modify_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.input_cedula.place(x=33.0, y=130.0, width=190.0, height=35.0)
        


        tk.Label(modify_window, text="Nombres", fg="#CCCED1", bg="#042344", font=("Montserrat Regular",15)).place(x=243.0, y=100.0, width=120.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.input_nombre = tk.Entry(modify_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.input_nombre.place(x=263.0, y=130.0, width=190.0, height=35.0)

        tk.Label(modify_window, text="Apellidos", fg="#CCCED1", bg="#042344", font=("Montserrat Regular",15)).place(x=474.0, y=100.0, width=120.0, height=35.0)#.pack(pady=5,expand=False)#.grid(row=7, column=0, padx=10, pady=5)
        self.input_apellido = tk.Entry(modify_window,  bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.input_apellido.place(x=493.0, y=130.0, width=190.0, height=35.0)
        
        tk.Label(modify_window, text="Teléfono", fg="#CCCED1", bg="#042344", font=("Montserrat Regular",15)).place(x=700.0, y=100.0, width=120.0, height=35.0)
        self.input_telefono = tk.Entry(modify_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.input_telefono.place(x=723.0, y=130.0, width=190.0, height=35.0)

        tk.Label(modify_window, text="Dirección", fg="#CCCED1", bg="#042344", font=("Montserrat Regular",15)).place(x=14.0, y=200.0, width=120.0, height=35.0)
        self.input_direccion = tk.Entry(modify_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.input_direccion.place(x=33.0, y=230.0, width=190.0, height=35.0)

        self.modify_client()

        # Cargar y almacenar las imágenes
        self.images['boton_m'] = tk.PhotoImage(file=relative_to_assets("M_button_light_blue.png"))

        self.boton_R = tk.Button(
            modify_window,
            image=self.images['boton_m'],
            borderwidth=0,
            highlightthickness=0,
            command=self.save_modifications,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        #self.boton_R.place(x=265.0, y=450.0, width=130.0, height=40.0)
        #self.boton_R.place_forget()  # Ocultar el botón inicialmente

        
        self.images['boton_C'] = tk.PhotoImage(file=relative_to_assets("L_cancelar.png"))

        self.boton_C = tk.Button(
            modify_window,
            image=self.images['boton_C'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda:self.cancelar(modify_window),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_C.place(x=753.0, y=300.0, width=130.0, height=40.0)
        
        
        # Vincular la validación a los eventos de los campos de entrada
        self.input_cedula.bind("<KeyRelease>", lambda event: clients_validations.validate_entries(self, event))
        self.input_nombre.bind("<KeyRelease>", lambda event: clients_validations.validate_entries(self, event))
        self.input_apellido.bind("<KeyRelease>", lambda event: clients_validations.validate_entries(self, event))
        self.input_telefono.bind("<KeyRelease>", lambda event: clients_validations.validate_entries(self, event))
        self.input_direccion.bind("<KeyRelease>", lambda event: clients_validations.validate_entries(self, event))
        
    def cancelar(self, window):
        window.destroy()  # Esto cerrará la ventana de filtro

    def register_client(self):
        ID_Cedula= self.input_cedula.get() 
        nombre = self.input_nombre.get()
        apellido = self.input_apellido.get()
        telefono= str(self.input_telefono.get())
        direccion=self.input_direccion.get()
        if clients_validations.cedula_existe(self, ID_Cedula):
            messagebox.showinfo("Error", "La cédula ya está registrada.")
            self.clear_entries_register_loans()
            return
        if create_client_loans(ID_Cedula, nombre, apellido, telefono, direccion):
            messagebox.showinfo("Éxito", "Registro éxitoso del cliente.")
            self.clear_entries_register_loans()
            self.register_window.destroy()
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
        """else:
            messagebox.showwarning("Selección vacía", "Por favor, seleccione un cliente de la tabla.")"""

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
            self.modify_window.destroy()
        else:
            messagebox.showerror("Error", "Cliente no pudo ser modificado.")
        
    def clear_entries_register_loans(self):
        self.input_cedula.delete(0, tk.END)
        self.input_nombre.delete(0, tk.END)
        self.input_apellido.delete(0, tk.END)
        self.input_telefono.delete(0, tk.END)
        self.input_direccion.delete(0, tk.END)
        #self.input_cantidad.delete(0, tk.END)

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
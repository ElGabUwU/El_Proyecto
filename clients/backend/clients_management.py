import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import font
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from loans.backend.db_loans import *
from Library.bd_prestamo_listado_Frames2 import *
import random
import string
from backend.loans_filters import *
from db.conexion import establecer_conexion
from tkinter import messagebox
from validations import clients_validations
import re
import tkinter as tk
from tkinter import messagebox
from clients.backend.db_clients import *
from validations.clients_validations import capitalize_first_letter, limit_length, get_cliente_id_by_cedula
from validations.clients_validations import *
from util.utilidades import resource_path
from util.ventana import centrar_ventana
def validate_number_input(text):
        if text == "":
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False


class C_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.parent=parent
        self.validate_number = self.register(validate_number_input)
        self.images = {}
        
        


        self.canvas.create_text(980.0, 170.0, text="Refrescar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1080.0, 170.0, text="Agregar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1177.0, 170.0, text="Editar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1275.0, 170.0, text="Eliminar", fill="#040F21", font=("Bold", 17))

        self.right_frame_list_loans = tk.Frame(self.canvas, bg="#FAFAFA")
        self.right_frame_list_loans.pack(expand=True, side="right", fill="both") #padx=212, pady=150, ipady=80
        self.right_frame_list_loans.place(x=215,y=218, height=470, width=1135)

        bold_font = font.Font(family="Bold", size=15, weight="bold")
        self.label_clientes = tk.Label(self.canvas, text="Tabla Clientes", bg="#FAFAFA", fg="black", font=bold_font)
        self.label_clientes.place(x=665.0, y=180.0, width=225.0, height=35.0)

        self.label_nombre = self.canvas.create_text(245.0, 82.0, anchor="nw", text="Buscar por Cédula", fill="black", font=("Bold", 17))

        
        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2, validate="key", validatecommand=(self.validate_number, "%P"))
        self.buscar.place(x=245.0, y=112.0, width=267.0, height=48.0)
        self.buscar.bind("<Return>", self.boton_buscar)
        self.buscar.bind("<KeyPress>", self.key_on_press_search)

        # Cargar y almacenar las imágenes
        self.images['boton_refrescar'] = tk.PhotoImage(file=resource_path("assets_2/16_refrescar.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_refrescar'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.refresh_frame_clients(),
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=935.0, y=60.0, width=90.0, height=100.0)

        

        self.images['boton_agregar'] = tk.PhotoImage(file=resource_path("assets_2/5_agregar.png"))
            
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
        self.button_e.place(x=1035.0, y=60.0, width=90.0, height=100.0)

        self.images['boton_Eliminar'] = tk.PhotoImage(file=resource_path("assets_2/7_eliminar.png"))
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
        self.button_dl.place(x=1235.0, y=60.0, width=90.0, height=100.0)

        self.images['boton_modificar'] = tk.PhotoImage(file=resource_path("assets_2/6_editar.png"))
            # Cargar y almacenar la imagen del botón
        self.button_dl = tk.Button(
            self,
            image=self.images['boton_modificar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_modify_window(), #verificar que halla un elemento seleccionado antes de abrir la ventana emergente
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_dl.place(x=1135.0, y=60.0, width=90.0, height=100.0)
        
        self.data = []
        self.page_size = 19
        self.current_page = 0
        self.setup_treeview()
        self.load_clients()
        self.display_page()

    def setup_treeview(self):
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
        styletrees.configure("Rounded.Treeview.Heading",
                            font=('Helvetica', 10, 'bold'),
                            background="#2E59A7",
                            foreground="#000000",
                            borderwidth=0)
        columns = ("Cedula", "Nombre", "Apellido", "Teléfono", "Dirección")
        self.clients_table_list_loans = ttk.Treeview(self.right_frame_list_loans, columns=columns, show='headings', style="Rounded.Treeview", selectmode="browse")
        self.clients_table_list_loans.column("Cedula", width=20, anchor="center")
        for col in columns:
            self.clients_table_list_loans.heading(col, text=col)
            self.clients_table_list_loans.column(col, width=85, anchor="center")
        self.clients_table_list_loans.pack(expand=True, fill="both", padx=30, pady=5)
        scrollbar_pt = ttk.Scrollbar(self.clients_table_list_loans, orient="vertical", command=self.clients_table_list_loans.yview)
        self.clients_table_list_loans.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
        self.images['boton_siguiente'] = tk.PhotoImage(file=resource_path("assets_2/siguiente.png"))
        self.images['boton_anterior'] = tk.PhotoImage(file=resource_path("assets_2/atras.png"))
        prev_button = tk.Button(
            self.right_frame_list_loans,
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
            self.right_frame_list_loans, 
            image=self.images['boton_siguiente'],
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#006ac2",   # Color del texto cuando el botón está activo
            command=self.next_page)
        next_button.pack(side=tk.RIGHT, padx=25, pady=0)
        
        self.page_label = tk.Label(self.right_frame_list_loans, text=f"Página {self.current_page + 1}", bg="#FAFAFA", fg="#031A33", font=("Montserrat Regular", 13))
        self.page_label.pack(side=tk.BOTTOM, pady=15)


        #self.refresh_frame_clients()
        
    def get_data_page(self, offset, limit):
        return self.data[offset:offset + limit]

    def display_page(self):
        for row in self.clients_table_list_loans.get_children():
            self.clients_table_list_loans.delete(row)
        page_data = self.get_data_page(self.current_page * self.page_size, self.page_size)
        for fila in page_data:
            self.clients_table_list_loans.insert("", "end", values=fila)
        self.update_page_label()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.data):
            self.current_page += 1
            self.display_page()
            self.clients_table_list_loans.yview_moveto(0)  

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()
            self.clients_table_list_loans.yview_moveto(0)  

    def update_page_label(self):
        total_pages = (len(self.data) + self.page_size - 1) // self.page_size  # Calcular el total de páginas
        self.page_label.config(text=f"Página {self.current_page + 1} de {total_pages}")

    
    def load_clients(self):
        self.data = reading_clients(self.clients_table_list_loans)
        self.current_page = 0  # Resetear a la primera página
        self.display_page()


    def refresh_frame_clients(self):
        self.load_clients()

    
    def open_register_window(self):
        C_Register(self)

    def open_modify_window(self):
        selected_items = self.clients_table_list_loans.selection()
        if selected_items:
            selected_item = selected_items[0]
            item_values = self.clients_table_list_loans.item(selected_item, "values")
            C_Modify(self, item_values)
        else:
            messagebox.showwarning("Advertencia", "No hay ningún elemento seleccionado. Debe seleccionar un cliente para modificarlo.")

 
    def key_on_press_search(self, event):
        # Obtener el widget que disparó el evento
        widget = event.widget
        current_text = widget.get()

        # Permitir teclas de control como Backspace, Delete, Left, Right
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'):
            return

        # Verificar si el texto actual ya ha alcanzado el límite
        if len(current_text) >= 10:
            return "break"

        # Limitar la longitud del texto
        limited_text = limit_length(current_text, 10)

        # Actualizar el widget solo si el texto ha cambiado
        if current_text != limited_text:
            widget.delete(0, 'end')
            widget.insert(0, limited_text)

    def boton_buscar(self, event):
        busqueda = self.buscar.get().strip()
        
        if not busqueda:
            messagebox.showinfo("Búsqueda Fallida", "No se ingresó ningún término de búsqueda. Por favor, ingrese una cédula para buscar.")
            return
        
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                # Realizar la búsqueda exacta solo para la cédula
                cursor.execute("""
                    SELECT Cedula, Nombre, Apellido, Telefono, Direccion, ID_Cliente 
                    FROM cliente 
                    WHERE Cedula = %s
                """, (busqueda,))
                resultados = cursor.fetchall()

                if resultados:
                    # Limpiar la tabla antes de insertar nuevos resultados
                    self.clients_table_list_loans.delete(*self.clients_table_list_loans.get_children())
                    
                    # Insertar los nuevos resultados
                    for fila in resultados:
                        self.clients_table_list_loans.insert("", "end", values=tuple(fila))

                    self.buscar.delete(0, 'end')  # Limpiar el Entry después de una búsqueda exitosa
                    # Usar la opción seleccionada para el mensaje de éxito
                    messagebox.showinfo("Búsqueda Exitosa de Cliente", f"Cliente encontrado: {resultados[0][1]} {resultados[0][2]}.")
                else:
                    self.buscar.delete(0, 'end')  # Limpiar el Entry si no se encontraron coincidencias
                    # Usar la opción seleccionada para el mensaje de fallo
                    messagebox.showinfo("Búsqueda Fallida de Cliente", f"No se encontró ningún cliente con la cédula '{busqueda}'. Por favor, verifique la cédula ingresada.")
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
        finally:
            if mariadb_conexion:
                mariadb_conexion.close()


class C_Modify(tk.Toplevel):
    def __init__(self, parent, client_data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.withdraw()
        self.parent = parent
        self.title("Modificar")
        self.iconbitmap(resource_path('assets_2/logo_biblioteca.ico'))
        self.geometry("950x400")
        centrar_ventana(self, 950, 400)
        self.config(bg="#042344")
        self.resizable(False, False)
        self.validate_number = self.register(validate_number_input)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancelar())
        self.images = {}
        
        # Guardar los datos del cliente en un diccionario
        self.client_data = {
            "Cedula": client_data[0],
            "Nombre": client_data[1], 
            "Apellido": client_data[2],
            "Telefono" :client_data[3],
            "Direccion" : client_data[4]  
        }
        self.original_values_client = self.client_data.copy()
        print(self.client_data,"\n",self.original_values_client)
        
        #Initialize input fields and other elements
        self.create_widgets()
        self.crear_boton_modificar()
        self.crear_boton_modificar_inactivo()
        self.crear_boton_restaurar()
        self.crear_boton_cancelar()
        self.insert_values_client()
        self.deiconify()
        


            
        
    def create_widgets(self):
        rectangulo_color = tk.Label(self, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)
        tk.Label(self, text="Modificación de Clientes", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=270.0, y=20.0, width=420.0, height=35.0)

        tk.Label(self, text="Cedula", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=3.0, y=100.0, width=120.0, height=35.0)
        self.input_cedula = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(self.validate_number, "%P"))
        self.input_cedula.place(x=33.0, y=130.0, width=190.0, height=35.0)
        self.input_cedula.bind("<Return>", self.focus_next_widget)
        self.input_cedula.bind("<KeyPress>", self.on_key_press_modify)
        self.input_cedula.bind("<KeyRelease>", self.check_changes)

        tk.Label(self, text="Nombres", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=243.0, y=100.0, width=120.0, height=35.0)
        self.input_nombre = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_nombre.place(x=263.0, y=130.0, width=190.0, height=35.0)
        self.input_nombre.bind("<Return>", self.focus_next_widget)
        self.input_nombre.bind("<KeyPress>", self.on_key_press_modify)
        self.input_nombre.bind("<KeyRelease>", self.check_changes)

        tk.Label(self, text="Apellidos", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=474.0, y=100.0, width=120.0, height=35.0)
        self.input_apellido = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_apellido.place(x=493.0, y=130.0, width=190.0, height=35.0)
        self.input_apellido.bind("<Return>", self.focus_next_widget)
        self.input_apellido.bind("<KeyPress>", self.on_key_press_modify)
        self.input_apellido.bind("<KeyRelease>", self.check_changes)

        tk.Label(self, text="Teléfono", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=700.0, y=100.0, width=120.0, height=35.0)
        self.input_telefono = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(self.validate_number, "%P"))
        self.input_telefono.place(x=723.0, y=130.0, width=190.0, height=35.0)
        self.input_telefono.bind("<Return>", self.focus_next_widget)
        self.input_telefono.bind("<KeyPress>", self.on_key_press_modify)
        self.input_telefono.bind("<KeyRelease>", self.check_changes)

        tk.Label(self, text="Dirección", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=14.0, y=200.0, width=120.0, height=35.0)
        self.input_direccion = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_direccion.place(x=33.0, y=230.0, width=190.0, height=35.0)
        self.input_direccion.bind("<Return>", self.focus_next_widget)
        self.input_direccion.bind("<KeyPress>", self.on_key_press_modify)
        self.input_direccion.bind("<KeyRelease>", self.check_changes)


    def insert_values_client(self):
        self.clear_entries_modify_client()
        self.input_cedula.insert(0, self.original_values_client["Cedula"])
        self.input_nombre.insert(0, self.original_values_client["Nombre"])
        self.input_apellido.insert(0, self.original_values_client["Apellido"])
        self.input_telefono.insert(0, self.original_values_client["Telefono"])
        self.input_direccion.insert(0, self.original_values_client["Direccion"])
        print("Valores del cliente insertados:", self.original_values_client)
        self.check_changes()

    def clear_entries_modify_client(self):
        self.input_cedula.delete(0, tk.END)
        self.input_nombre.delete(0, tk.END)
        self.input_apellido.delete(0, tk.END)
        self.input_telefono.delete(0, tk.END)
        self.input_direccion.delete(0, tk.END)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"
    
    def on_key_press_modify(self, event):
        widget = event.widget
        current_text = widget.get()
        
        if widget == self.input_cedula:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isdigit():
                return "break"

            cursor_position = widget.index(tk.INSERT)
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            new_text = limit_length(new_text, 10)
            formatted_text = new_text
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            widget.icursor(cursor_position + 1)
            return "break"
        
        elif widget == self.input_nombre or widget == self.input_apellido:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isalpha() and event.char != " ":
                return "break"

            cursor_position = widget.index(tk.INSERT)
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            new_text = limit_length(new_text, 30)
            formatted_text = capitalize_first_letter(new_text)
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            widget.icursor(cursor_position + 1)
            return "break"
        
        elif widget == self.input_telefono:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isdigit():
                return "break"

            cursor_position = widget.index(tk.INSERT)
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            new_text = limit_length(new_text, 11)
            formatted_text = new_text
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            widget.icursor(cursor_position + 1)
            return "break"
        
        elif widget == self.input_direccion:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not allow_permitted_characters(event.char):
                return "break"
            
            cursor_position = widget.index(tk.INSERT)
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            new_text = limit_length(new_text, 100)
            formatted_text = validar_y_formatear_direccion(new_text)
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            widget.icursor(cursor_position + 1)
            return "break"

    def check_changes(self, *args):
        try:
            # Obtener los valores actuales de los campos de cliente
            current_values = {
                "Nombre": self.input_nombre.get(),
                "Apellido": self.input_apellido.get(),
                "Cedula": self.input_cedula.get().strip(),
                "Telefono": self.input_telefono.get().strip(),
                "Direccion": self.input_direccion.get(),
            }

            # Comparar valores clave por clave
            differences = []
            for key in current_values:
                if current_values[key] != self.original_values_client[key]:
                    differences.append(f"Diferencia en {key}: {current_values[key]} (actual) != {self.original_values_client[key]} (original)")

            if differences:
                for diff in differences:
                    print(diff)
                self.mostrar_boton_modificar()
                print("Se detectaron cambios. Botón 'Modificar' mostrado.")
            else:
                self.ocultar_boton_modificar()
                self.mostrar_boton_modificar_inactivo()
                print("No se detectaron cambios. Botón 'Modificar' inactivo mostrado.")
        except Exception as e:
            print(f"Error en check_changes: {e}")
            
    def modify_client(self):
        nuevos_valores = {
            "Nombre": self.input_nombre.get(),
            "Apellido": self.input_apellido.get(),
            "Cedula": self.input_cedula.get(),
            "Telefono": self.input_telefono.get(),
            "Direccion": self.input_direccion.get(),
        }
        
        cedula = self.original_values_client["Cedula"]
        print(f"Cedula: {cedula}")
        id_cliente = get_cliente_id_by_cedula(cedula)
        # Validar los campos incluyendo el ID del cliente
        errores = validar_campos(
            nombre=self.input_nombre.get(),
            apellido=self.input_apellido.get(),
            cedula=self.input_cedula.get(),
            telefono=self.input_telefono.get(),
            direccion=self.input_direccion.get(),
            tipo_validacion="modificar",
            client_id=id_cliente
        )
        
        print(f"Errores: {errores}")  # Agregar esta línea para depuración
        if errores:
            messagebox.showerror("Error al modificar", "Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"- {msg}" for msg in errores), parent=self)
            return
        
        print("Datos recogidos:")
        for key, value in nuevos_valores.items():
            print(f"{key}: {value}")

        # Actualizar el cliente con los nuevos valores
        client_data = {"cedula": cedula}
        if update_client(client_data, nuevos_valores):
            messagebox.showinfo("Éxito", "Modificación del cliente exitosa.", parent=self)
            self.clear_entries_modify_client()
            self.destroy()
        else:
            messagebox.showinfo("Modificación fallida", "Cliente mantiene sus valores.", parent=self)


    def crear_boton_modificar(self):
        try:
            self.images['boton_R'] = tk.PhotoImage(file=resource_path("assets_2/M_button_light_blue.png"))
            print("Imagen del botón 'Modificar' cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar la imagen del botón 'Modificar': {e}")
            return
        self.boton_modificar = tk.Button(
            self,
            image=self.images["boton_R"],
            borderwidth=0,
            highlightthickness=0,
            command=self.modify_client,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_modificar.place(x=33.0, y=280.0, width=130.0, height=40.0)
        self.boton_modificar.place_forget()
        print("Botón 'Modificar' creado y oculto inicialmente.")

    def crear_boton_modificar_inactivo(self):
        try:
            self.images['boton_R_inactivo'] = tk.PhotoImage(file=resource_path("assets_2/M_button_grey.png"))
            print("Imagen del botón 'Modificar' inactivo cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar la imagen del botón 'Modificar' inactivo: {e}")
            return
        self.boton_modificar_inactivo = tk.Button(
            self,
            image=self.images["boton_R_inactivo"],
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_modificar_inactivo.place(x=33.0, y=280.0, width=130.0, height=40.0)
        self.boton_modificar_inactivo.place_forget()
        print("Botón 'Modificar' inactivo creado y oculto inicialmente.")

    def mostrar_boton_modificar(self):
        self.boton_modificar.place(x=33.0, y=280.0, width=130.0, height=40.0)
        self.boton_modificar_inactivo.place_forget()
        print("Botón 'Modificar' mostrado.")

    def mostrar_boton_modificar_inactivo(self):
        self.boton_modificar_inactivo.place(x=33.0, y=280.0, width=130.0, height=40.0)
        self.boton_modificar.place_forget()
        print("Botón 'Modificar' inactivo mostrado.")

    def ocultar_boton_modificar(self):
        self.boton_modificar.place_forget()
        self.boton_modificar_inactivo.place_forget()
        print("Botón 'Modificar' oculto.")

    def crear_boton_cancelar(self):
        try:
            self.images['boton_C'] = tk.PhotoImage(file=resource_path("assets_2/c_button_red1.png"))
            print("Imagen del botón 'Cancelar' cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar la imagen del botón 'Cancelar': {e}")
            return
        self.boton_C = tk.Button(
            self,
            image=self.images["boton_C"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.cancelar(),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_C.place(x=178.0, y=280.0, width=130.0, height=40.0)
        print("Botón 'Cancelar' creado.")

    def crear_boton_restaurar(self):
        try:
            self.images['boton_r'] = tk.PhotoImage(file=resource_path("assets_2/rest_button_green.png"))
            print("Imagen del botón 'Restaurar' cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar la imagen del botón 'Restaurar': {e}")
            return
        self.boton_R = tk.Button(
            self,
            image=self.images['boton_r'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.insert_values_client(),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_R.place(x=323.0, y=280.0, width=130.0, height=40.0)
        print("Botón 'Restaurar' creado.")


    def cancelar(self):
        if messagebox.askyesno(
            "Advertencia",
            "¿Estás seguro de que quieres cerrar esta ventana? Todos los cambios no guardados se perderán.",parent=self
        ):
            self.destroy()  # Asegúrate de que 'self' se refiere a la ventana que quieres cerrar



class C_Register(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.withdraw()
        self.parent = parent
        self.title("Registro")
        self.iconbitmap(resource_path('assets_2/logo_biblioteca.ico'))
        self.geometry("950x380")
        
        centrar_ventana(self, 950, 380)
        self.config(bg="#042344")
        self.resizable(False, False)
        self.validate_number = self.register(validate_number_input)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancelar())
        self.images = {}
        
        
        #Initialize input fields and other elements
        self.create_widgets()
        self.crear_boton_register()
        self.crear_boton_cancelar()
        self.deiconify()
       
        


            
        
    def create_widgets(self):
        rectangulo_color = tk.Label(self, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)
        tk.Label(self, text="Registro de Clientes", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=270.0, y=15.0, width=400.0, height=40.0)

        tk.Label(self, text="Cedula", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=3.0, y=100.0, width=120.0, height=35.0)
        self.input_cedula = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(self.validate_number, "%P"))
        self.input_cedula.place(x=33.0, y=130.0, width=190.0, height=35.0)
        self.input_cedula.bind("<Return>", self.focus_next_widget)
        self.input_cedula.bind("<KeyPress>", self.on_key_press_register)

        tk.Label(self, text="Nombres", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=243.0, y=100.0, width=120.0, height=35.0)
        self.input_nombre = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_nombre.place(x=263.0, y=130.0, width=190.0, height=35.0)
        self.input_nombre.bind("<Return>", self.focus_next_widget)
        self.input_nombre.bind("<KeyPress>", self.on_key_press_register)
        

        tk.Label(self, text="Apellidos", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=474.0, y=100.0, width=120.0, height=35.0)
        self.input_apellido = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_apellido.place(x=493.0, y=130.0, width=190.0, height=35.0)
        self.input_apellido.bind("<Return>", self.focus_next_widget)
        self.input_apellido.bind("<KeyPress>", self.on_key_press_register)
        

        tk.Label(self, text="Teléfono", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=700.0, y=100.0, width=120.0, height=35.0)
        self.input_telefono = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(self.validate_number, "%P"))
        self.input_telefono.place(x=723.0, y=130.0, width=190.0, height=35.0)
        self.input_telefono.bind("<Return>", self.focus_next_widget)
        self.input_telefono.bind("<KeyPress>", self.on_key_press_register)
        

        tk.Label(self, text="Dirección", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=14.0, y=200.0, width=120.0, height=35.0)
        self.input_direccion = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_direccion.place(x=33.0, y=230.0, width=190.0, height=35.0)
        self.input_direccion.bind("<Return>",lambda event : self.register_client())
        self.input_direccion.bind("<KeyPress>", self.on_key_press_register)
        


    

    def clear_entries_register_client(self):
        self.input_cedula.delete(0, tk.END)
        self.input_nombre.delete(0, tk.END)
        self.input_apellido.delete(0, tk.END)
        self.input_telefono.delete(0, tk.END)
        self.input_direccion.delete(0, tk.END)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"
    
    def on_key_press_register(self, event):
        widget = event.widget
        current_text = widget.get()
        
        if widget == self.input_cedula:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isdigit():
                return "break"

            cursor_position = widget.index(tk.INSERT)
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            new_text = limit_length(new_text, 10)
            formatted_text = new_text
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            widget.icursor(cursor_position + 1)
            return "break"
        
        elif widget == self.input_nombre or widget == self.input_apellido:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isalpha() and event.char != " ":
                return "break"

            cursor_position = widget.index(tk.INSERT)
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            new_text = limit_length(new_text, 30)
            formatted_text = capitalize_first_letter(new_text)
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            widget.icursor(cursor_position + 1)
            return "break"
        
        elif widget == self.input_telefono:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isdigit():
                return "break"

            cursor_position = widget.index(tk.INSERT)
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            new_text = limit_length(new_text, 11)
            formatted_text = new_text
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            widget.icursor(cursor_position + 1)
            return "break"
        
        elif widget == self.input_direccion:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not allow_permitted_characters(event.char):
                return "break"
            
            cursor_position = widget.index(tk.INSERT)
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            new_text = limit_length(new_text, 100)
            formatted_text = validar_y_formatear_direccion(new_text)
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            widget.icursor(cursor_position + 1)
            return "break"


    def register_client(self):
        nombre = self.input_nombre.get()
        apellido = self.input_apellido.get()
        cedula = self.input_cedula.get()
        telefono = self.input_telefono.get()
        direccion = self.input_direccion.get()

        print(f"nombre: {nombre}, apellido: {apellido}, cedula: {cedula}")

        errores = validar_campos(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            telefono=telefono,
            direccion=direccion,
            tipo_validacion="registro",
            client_id=None
        )
        print(f"Errores: {errores}")  # Agregar esta línea para depuración
        if errores:
            messagebox.showerror("Error en el registro", "Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"- {msg}" for msg in errores), parent=self)
            return
        print(errores)
        if register_client_in_db(cedula, nombre, apellido, telefono, direccion):
            messagebox.showinfo("Éxito", "Registro exitoso del cliente.", parent=self)
            self.clear_entries_register_client()
        else:
            messagebox.showinfo("Registro fallido", "El cliente no pudo registrarse.", parent=self)
    

    def crear_boton_register(self):
        try:
            self.images['boton_register'] = tk.PhotoImage(file=resource_path("assets_2/R_button_light_blue.png"))
            print("Imagen del botón 'Restaurar' cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar la imagen del botón 'Restaurar': {e}")
            return
        self.boton_R = tk.Button(
            self,
            image=self.images['boton_register'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.register_client(),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_R.place(x=33.0, y=300.0, width=130.0, height=40.0)
        print("Botón 'Registrar' creado.")

    def crear_boton_cancelar(self):
        try:
            self.images['boton_C'] = tk.PhotoImage(file=resource_path("assets_2/c_button_red1.png"))
            print("Imagen del botón 'Cancelar' cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar la imagen del botón 'Cancelar': {e}")
            return
        self.boton_C = tk.Button(
            self,
            image=self.images["boton_C"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.cancelar(),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_C.place(x=225.0, y=300.0, width=130.0, height=40.0)
        print("Botón 'Cancelar' creado.")



    def cancelar(self):
        if messagebox.askyesno(
            "Advertencia",
            "¿Estás seguro de que quieres cerrar esta ventana? Todos los datos no guardados del cliente se perderán.",parent=self
        ):
            self.destroy()  # Asegúrate de que 'self' se refiere a la ventana que quieres cerrar

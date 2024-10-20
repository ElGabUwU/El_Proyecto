import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
#from Library.librerias import recoger_sesion, drop_sesion
from users.backend.db_users import *
#from Vistas.listas import *
import random
from db.conexion import establecer_conexion
from validations.user_validations import *
from users.backend.db_users import *

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

class U_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent=parent
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        self.cargos = {
            1: "Encargado de Servicio",
            2: "Asistente Bibliotecario"
        }
        # Crear el marco izquierdo para el menú de navegación

        self.user_frame_list = tk.Frame(self.canvas, bg="#FAFAFA")
        self.user_frame_list.pack(expand=True, side="left", fill="both") #padx=212, pady=150, ipady=80
        self.user_frame_list.place(x=215,y=205, height=480, width=1150)

        # # Texto para el nombre
        # self.label_nombre = self.canvas.create_text(265.0, 100.0, anchor="nw", text="Buscar", fill="#031A33", font=("Bold", 17))
        # self.canvas.create_text(1110.0, 170.0, text="Editar", fill="#031A33", font=("Bold", 17))
        # self.canvas.create_text(1240.0, 170.0, text="Eliminar", fill="#031A33", font=("Bold", 17))
        # self.canvas.create_text(980.0, 170.0, text="Refrescar", fill="#031A33", font=("Bold", 17))

        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.label_nombre = self.canvas.create_text(265.0, 100.0, anchor="nw", text="Buscar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1077.0, 170.0, text="Editar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1175.0, 170.0, text="Eliminar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(980.0, 170.0, text="Agregar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(880.0, 170.0, text="Refrescar", fill="#040F21", font=("Bold", 17))
        
        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.buscar.place(x=265.0, y=130.0, width=267.0, height=48.0)
        self.buscar.bind("<Return>", self.boton_buscar)

            
            # Cargar y almacenar las imágenes
        self.images['boton_cargar'] = tk.PhotoImage(file=relative_to_assets("16_refrescar.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_cargar'],
                borderwidth=0,
                highlightthickness=0,
                command=self.refresh_frame,
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=810.0, y=60.0, width=130.0, height=100.0)

                    # Cargar y almacenar las imágenes
        self.images['boton_agregar'] = tk.PhotoImage(file=relative_to_assets("5_agregar.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_agregar'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda:self.open_registrar_window(),
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=910.0, y=60.0, width=130.0, height=100.0)

            # Cargar y almacenar las imágenes
        self.images['boton_eliminar'] = tk.PhotoImage(file=relative_to_assets("7_eliminar.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
            self,
            image=self.images['boton_eliminar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: delete_selected_user(self) ,
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo 
            )
        self.button_e.place(x=1110.0, y=60.0, width=130.0, height=100.0)

        self.images['boton_modificar'] = tk.PhotoImage(file=relative_to_assets("6_editar.png"))
                    # Cargar y almacenar la imagen del botón
        self.button_m = tk.Button(
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
        self.button_m.place(x=1010.0, y=60.0, width=130.0, height=100.0)

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


        columns = ("ID Usuario", "Cargo", "ID Rol", "Nombre", "Apellido", "C.I", "Nombre Usuario")
        self.user_table_list= ttk.Treeview(self.user_frame_list, columns=columns, show='headings', style="Rounded.Treeview")
        for col in columns:
            self.user_table_list.heading(col, text=col)
            self.user_table_list.column(col, width=90, anchor="center")
        self.user_table_list.pack(expand=True, fill="both", padx=70, pady=5)

        scrollbar_pt = ttk.Scrollbar(self.user_table_list, orient="vertical", command=self.user_table_list.yview)
        self.user_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
        
        list_users_db(self.user_table_list,self.cargos)

    def refresh_frame(self):
        # Eliminar todos los widgets del frame
        for widget in self.user_frame_list.winfo_children():
            widget.destroy()

        # Estilo del Treeview
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

        # Estilo para las cabeceras
        style.configure("Rounded.Treeview.Heading",
                        font=('Helvetica', 10, 'bold'),
                        background="#2E59A7",
                        foreground="#000000",
                        borderwidth=0)

        # Crear y configurar el Treeview
        columns = ("ID Usuario", "Cargo", "ID Rol", "Nombre", "Apellido", "C.I", "Nombre Usuario")
        self.user_table_list = ttk.Treeview(self.user_frame_list, columns=columns, show='headings', style="Rounded.Treeview")

        for col in columns:
            self.user_table_list.heading(col, text=col)
            self.user_table_list.column(col, width=90, anchor="center")

        self.user_table_list.pack(expand=True, fill="both", padx=70, pady=5)

        # Scrollbar
        scrollbar_pt = ttk.Scrollbar(self.user_table_list, orient="vertical", command=self.user_table_list.yview)
        self.user_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")

        # Recargar los datos desde la base de datos
        list_users_db(self.user_table_list, self.cargos)


    
    def open_registrar_window(self):
        # Llamar directamente a la clase U_Registrar sin necesidad de seleccionar un elemento
            U_Registrar(self)

    def open_modify_window(self):
        selected_items = self.user_table_list.selection()
        if selected_items:
            selected_item = selected_items[0]
            item_values = self.user_table_list.item(selected_item, "values")
            U_Modificar(self, item_values)
        else:
            messagebox.showwarning("Advertencia", "No hay ningún elemento seleccionado. Debe seleccionar un usuario para modificarlo.")

            
    

    def boton_buscar(self, event):
        busqueda= self.buscar.get()
        try:
             mariadb_conexion = establecer_conexion()
             if mariadb_conexion:#.is_connected():
                        cursor = mariadb_conexion.cursor()
                        cursor.execute("""SELECT ID_Usuario, ID_Cargo, ID_Rol, Nombre, Apellido,
                                        Cedula, Nombre_Usuario FROM usuarios WHERE 
                                        ID_Usuario=%s OR ID_Cargo=%s OR ID_Rol=%s OR 
                                        Nombre=%s OR Apellido=%s OR Cedula=%s OR 
                                        Nombre_Usuario=%s""", 
                           (busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda))
                        resultados = cursor.fetchall() 

                        self.user_table_list.delete(*self.user_table_list.get_children())
                        for fila in resultados:
                            self.user_table_list.insert("", "end", values=tuple(fila))
                            if busqueda in fila:
                                self.user_table_list.item(self.user_table_list.get_children()[-1], tags='match')
                            else:
                                self.user_table_list.item(self.user_table_list.get_children()[-1], tags='nomatch')
                        self.user_table_list.tag_configure('match', background='green')
                        self.user_table_list.tag_configure('nomatch', background='gray')
                        if resultados:
                            messagebox.showinfo("Busqueda Éxitosa", "Resultados en pantalla.")
                        else:
                            messagebox.showinfo("Busqueda Fallida", "No se encontraron resultados.")
        except mariadb.Error as ex:
                print("Error durante la conexión:", ex)

    def cancelar(self, window):
        window.destroy()  # Esto cerrará la ventana de filtro

    def clear_entries_modify_window(self):
        self.nombre_entry.delete(0, tk.END)
        self.apellido_entry.delete(0, tk.END)
        self.id_cedula_entry.delete(0, tk.END)
        self.nombre_usuario_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)    

class U_Registrar(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__()
        self.parent = parent
        self.canvas = tk.Canvas(self, bg="#031A33", width=863, height=530)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.validate_number = self.register(validate_number_input)
        self.images = {}
        self.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        self.resizable(False, False)
        self.grab_set()
        self.canvas.create_rectangle(0, 0, 950, 74, fill="#2E59A7")
        """rectangulo_color = tk.Label(self, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)"""
        self.canvas.create_text(255.0, 21.0, anchor="nw", text="Registro de Usuarios", fill="#ffffff", font=("Montserrat Medium", 28))
        self.cargos = {
            1: "Encargado de Servicio",
            2: "Asistente Bibliotecario"
        }
        # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("R_button_light_blue.png"))

        # Crear el botón
        boton_R = self.images['boton_R']
        tk.Button(
            self,
            image=boton_R,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.register_user(),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"  # Color del texto cuando el botón está activo
        ).place(x=61.0, y=465.0, width=130.0, height=40.0)
        
        self.images['boton_c'] = tk.PhotoImage(file=relative_to_assets("L_cancelar.png"))
        self.boton_C = tk.Button(
            self,
            image=self.images['boton_c'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.cancelar(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_C.place(x=250.0, y=465.0, width=130.0, height=40.0)

                #REVISAR COMO SE SUBIERON LOS CARGOS A LA BD PARA HACER LAS VALIDACIONES 
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                fieldbackground="#2E59A7",  # Fondo del campo de entrada
                background="#2E59A7",  # Fondo del desplegable
                bordercolor="#041022",  # Color del borde
                arrowcolor="#ffffff",  # Color de la flecha
                padding= "9",
                ) # padding para agrandar la altura del select
        
        
            
        self.cargo_combobox = ttk.Combobox(self, values=list(self.cargos.values()), state="readonly", width=30, font=("Bold", 10), style="TCombobox")
        self.cargo_combobox.place(x=61.0, y=181.5)
        self.cargo_combobox.set("Encargado de Servicio")  # Establece el valor inicial a "1I" 

        # Crear y colocar los widgets
        #primera fila
        self.input_nombre = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_nombre.place(x=61.0, y=282.0, width=237.0, height=37.5)
        self.input_nombre.bind("<Return>",self.focus_next_widget)
        self.input_nombre.bind("<KeyPress>",self.on_key_press_register)
        
        self.input_apellido = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_apellido.place(x=318.0, y=282.0, width=237.0, height=38.0)
        self.input_apellido.bind("<Return>",self.focus_next_widget)
        self.input_apellido.bind("<KeyPress>",self.on_key_press_register)

        
        self.input_cedula = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(self.validate_number, "%P"))
        self.input_cedula.place(x=575.0, y=282.0, width=237.0, height=37.5)
        self.input_cedula.bind("<Return>",self.focus_next_widget)
        self.input_cedula.bind("<KeyPress>",self.on_key_press_register)

        #segunda fila
        self.input_username = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_username.place(x=61.0, y=382.0, width=237.0, height=37.5)
        self.input_username.bind("<Return>",self.focus_next_widget)
        self.input_username.bind("<KeyPress>",self.on_key_press_register)

        #tercera fila
        self.input_password = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_password.place(x=318.0, y=382.0, width=237.0, height=37.5)
        self.input_password.bind("<Return>",self.focus_next_widget)
        self.input_password.bind("<KeyPress>",self.on_key_press_register)

        self.input_verify_password = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_verify_password.place(x=575.0, y=382.0, width=237.0, height=37.5)
        self.input_verify_password.bind("<Return>",lambda event : self.register_user())
        self.input_verify_password.bind("<KeyPress>",self.on_key_press_register)

        self.inicializador_titulos()
        # self.register_user()
        # self.validacion_sala(None)
    def cancelar(self, window):
        window.destroy()
    def inicializador_titulos(self):
        # Titulos de los inputs
        self.canvas.create_text(61.0, 106.0, anchor="nw", text="Ingrese la información del nuevo usuario a agregar", fill="#a6a6a6", font=("Bold", 17))
        #fila 1
        self.canvas.create_text(61.0, 152.0, anchor="nw", text="Cargo", fill="#a6a6a6", font=("Bold", 17))

        #fila 2
        self.canvas.create_text(61.0, 252.0, anchor="nw", text="Nombres", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(318.0, 252.0, anchor="nw", text="Apellidos", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(575.0, 252.0, anchor="nw", text="Cedula", fill="#a6a6a6", font=("Bold", 17))
        
        #fila 3
        self.canvas.create_text(61.0, 352.0, anchor="nw", text="Nombre de usuario", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(318.0, 352.0, anchor="nw", text="Contraseña", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(575.0, 352.0, anchor="nw", text="Confirmar Contraseña", fill="#a6a6a6", font=("Bold", 17))
        #fila 4
        
    def register_user(self):
        cargo = self.cargo_combobox.get()
        cargo_id = None
        
        # Obtener el ID del cargo desde el diccionario
        for key, value in self.cargos.items():
            if value == cargo:
                cargo_id = key
                break
        nombre = self.input_nombre.get()
        apellido = self.input_apellido.get()
        cedula = self.input_cedula.get()
        username = self.input_username.get()
        password = self.input_password.get()
        verify_password = self.input_verify_password.get()  # Asumiendo que tienes este campo en tu formulario
        rol = 1
        
        print(f"cargo: {cargo_id}, nombre: {nombre}, apellido: {apellido}, cedula: {cedula}, username: {username}, password: {password}")
        print("\n")

        # Validar campos antes de crear el usuario
        error_messages = validar_campos(username, password, tipo_validacion="registro", nombre=nombre, apellido=apellido, cedula=cedula, cargo=cargo, verify_password=verify_password)
        
        if error_messages:
            messagebox.showerror("Error en el registro", "Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"- {msg}" for msg in error_messages),parent=self)
            
            return

        if create_user(cargo_id, rol, nombre, apellido, cedula, username, password):
            messagebox.showinfo("Éxito", "Registro exitoso del usuario.")
            self.clear_entries_register()
            self.destroy()
        else:
            messagebox.showinfo("Registro fallido", "El usuario no pudo registrarse.",parent=self)
    def clear_entries_register(self):
         # Limpiar los campos después del registro exitoso
            self.cargo_combobox.set('Encargado de Servicio')
            self.input_nombre.delete(0, tk.END)
            self.input_apellido.delete(0, tk.END)
            self.input_cedula.delete(0, tk.END)
            self.input_username.delete(0, tk.END)
            self.input_password.delete(0, tk.END)
            self.input_verify_password.delete(0, tk.END)

        #-------------------------------------------------------------------------------
    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"
    def on_key_press_register(self, event):
        widget = event.widget
        current_text = widget.get()

        if widget == self.input_username:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not allow_permitted_characters(event.char):
                return "break"

            cursor_position = widget.index(tk.INSERT)
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            new_text = limit_length(new_text, 12)
            formatted_text = new_text
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            widget.icursor(cursor_position + 1)
            return "break"

        elif widget == self.input_cedula:
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

        elif widget == self.input_password or widget == self.input_verify_password:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if event.char == ' ':
                return "break"

            cursor_position = widget.index(tk.INSERT)
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            new_text = limit_length(new_text, 16)
            formatted_text = new_text.replace(' ', '')
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

    


class U_Modificar(tk.Toplevel):
    def __init__(self, parent, item_values, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.validate_number = self.register(validate_number_input)
        self.images = {}
        self.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        self.geometry("950x450")
        self.config(bg="#042344")
        self.resizable(False, False)
        self.grab_set()

        # Guardar los datos del usuario en un diccionario
        self.user_data = {
            "id": item_values[0],
            "nombre": item_values[1],
            "cargo": item_values[2]
        }

        rectangulo_color = tk.Label(self, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)
        tk.Label(self, text="Modificación de Usuarios", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=225.0, y=20.0, width=450.0, height=35.0)
        tk.Label(self, text="Ingrese los datos a modificar", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=10.0, y=90.0, width=330.0, height=35.0)
        tk.Label(self, text="Cedula", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=210.0, y=150.0, width=120.0, height=35.0)
        self.id_cedula_entry = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.id_cedula_entry.place(x=240.0, y=190.0, width=190.0, height=35.0)

        tk.Label(self, text="Nombre de Usuario", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=493.0, y=150.0, width=185.0, height=35.0)
        self.nombre_usuario_entry = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.nombre_usuario_entry.place(x=500.0, y=190.0, width=190.0, height=35.0)

        tk.Label(self, text="Nombres", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=220.0, y=250.0, width=120.0, height=35.0)
        self.nombre_entry = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.nombre_entry.place(x=240.0, y=290.0, width=190.0, height=35.0)
        #esta mal la posicion!!!!!!!
        tk.Label(self, text="Apellidos", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=482.0, y=250.0, width=120.0, height=35.0)
        self.apellido_entry = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.apellido_entry.place(x=500.0, y=290.0, width=190.0, height=35.0)

        
        self.images['boton_m'] = tk.PhotoImage(file=relative_to_assets("M_button_light_blue.png"))
        self.boton_M = tk.Button(
            self,
            image=self.images['boton_m'],
            borderwidth=0,
            highlightthickness=0,
            command=self.apply_modify_users,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_M.place(x=530.0, y=380.0, width=130.0, height=40.0)

        self.images['boton_c'] = tk.PhotoImage(file=relative_to_assets("L_cancelar.png"))
        self.boton_C = tk.Button(
            self,
            image=self.images['boton_c'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.cancelar(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_C.place(x=270.0, y=380.0, width=130.0, height=40.0)

    def apply_modify_users(self):
        # Implementa la lógica para aplicar los cambios
        pass

    def cancelar(self, window):
        window.destroy()


# class U_Modificar(tk.Toplevel):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.title("Modificar Usuario")
#         self.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
#         self.geometry("950x550")
#         self.config(bg="#042344")
#         self.resizable(False, False)
#         self.images = {}
#         validate_number = self.register(validate_number_input)

#         self.create_labels()
#         self.create_entries()
#         self.create_buttons()

#     def create_labels(self):
#         tk.Label(self, bg="#2E59A7", width=200, height=4).place(x=0, y=0)
#         tk.Label(self, text="Modificación de Usuarios", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=225.0, y=20.0, width=450.0, height=35.0)
#         tk.Label(self, text="Ingrese los datos a modificar", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=10.0, y=100.0, width=330.0, height=35.0)
#         tk.Label(self, text="Cedula", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=210.0, y=130.0, width=120.0, height=35.0)
#         tk.Label(self, text="Nombre de Usuario", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=500.0, y=130.0, width=185.0, height=35.0)
#         tk.Label(self, text="Nombre", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=220.0, y=230.0, width=120.0, height=35.0)
#         tk.Label(self, text="Apellido", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=500.0, y=230.0, width=120.0, height=35.0)
#         tk.Label(self, text="ID del usuario que será modificado", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=30.0, y=320.0, width=350.0, height=35.0)
#         tk.Label(self, text="ID", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=300.0, y=360.0, width=120.0, height=35.0)

#     def create_entries(self):
#         self.id_cedula_entry = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         self.id_cedula_entry.place(x=240.0, y=170.0, width=190.0, height=35.0)

#         self.nombre_usuario_entry = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         self.nombre_usuario_entry.place(x=500.0, y=170.0, width=190.0, height=35.0)

#         self.nombre_entry = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         self.nombre_entry.place(x=240.0, y=270.0, width=190.0, height=35.0)

#         self.apellido_entry = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         self.apellido_entry.place(x=500.0, y=270.0, width=190.0, height=35.0)

#         self.id_entry = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
#         self.id_entry.place(x=350.0, y=400.0, width=190.0, height=35.0)

#     def create_buttons(self):
#         self.images['boton_m'] = tk.PhotoImage(file=relative_to_assets("M_button_light_blue.png"))
#         self.boton_M = tk.Button(
#             self,
#             image=self.images['boton_m'],
#             borderwidth=0,
#             highlightthickness=0,
#             command=self.apply_modify_users,
#             relief="flat",
#             bg="#031A33",
#             activebackground="#031A33",
#             activeforeground="#FFFFFF"
#         )
#         self.boton_M.place(x=530.0, y=480.0, width=130.0, height=40.0)

#         self.images['boton_c'] = tk.PhotoImage(file=relative_to_assets("L_cancelar.png"))
#         self.boton_C = tk.Button(
#             self,
#             image=self.images['boton_c'],
#             borderwidth=0,
#             highlightthickness=0,
#             command=self.cancelar,
#             relief="flat",
#             bg="#031A33",
#             activebackground="#031A33",
#             activeforeground="#FFFFFF"
#         )
#         self.boton_C.place(x=270.0, y=480.0, width=130.0, height=40.0)

#     def apply_modify_users(self):
#         id_cedula = self.id_cedula_entry.get()
#         name_user = self.nombre_usuario_entry.get()
#         nombre = self.nombre_entry.get()
#         apellido = self.apellido_entry.get()
#         id_usuario = self.id_entry.get()

#         if id_usuario:
#             respuesta = messagebox.askyesno("Confirmar modificación", "¿Desea modificar?")
#             if respuesta:
#                 if update_user_list(id_cedula, name_user, nombre, apellido, id_usuario):
#                     messagebox.showinfo("Éxito", "Modificación éxitosa del usuario")
#                 else:
#                     messagebox.showinfo("Fallido", "No se pudo modificar al usuario.")
#             else:
#                 messagebox.showinfo("Cancelado", "Modificación cancelada.")
#         else:
#             messagebox.showinfo("Error", "Por favor, proporciona una ID válida.")

#     def boton_buscar(self, event):
#         busqueda = self.buscar.get()
#         try:
#             mariadb_conexion = establecer_conexion()
#             if mariadb_conexion:
#                 cursor = mariadb_conexion.cursor()
#                 cursor.execute("""
#                     SELECT ID_Usuario, ID_Cargo, ID_Rol, Nombre, Apellido, Cedula, Nombre_Usuario
#                     FROM usuarios
#                     WHERE ID_Usuario=%s OR ID_Cargo=%s OR ID_Rol=%s OR Nombre=%s OR Apellido=%s OR Cedula=%s OR Nombre_Usuario=%s
#                 """, (busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda))
#                 resultados = cursor.fetchall()
                
#                 self.user_table_list.delete(*self.user_table_list.get_children())
#                 for fila in resultados:
#                     self.user_table_list.insert("", "end", values=tuple(fila))
#                     if busqueda in fila:
#                         self.user_table_list.item(self.user_table_list.get_children()[-1], tags='match')
#                     else:
#                         self.user_table_list.item(self.user_table_list.get_children()[-1], tags='nomatch')

#                 self.user_table_list.tag_configure('match', background='green')
#                 self.user_table_list.tag_configure('nomatch', background='gray')
                
#                 if resultados:
#                     messagebox.showinfo("Búsqueda Éxitosa", "Resultados en pantalla.")
#                 else:
#                     messagebox.showinfo("Búsqueda Fallida", "No se encontraron resultados.")
#         except mariadb.Error as ex:
#             print("Error durante la conexión:", ex)

#     def cancelar(self):
#         self.destroy()

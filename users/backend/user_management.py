import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import font
#from Library.librerias import recoger_sesion, drop_sesion
from users.backend.db_users import *
#from Vistas.listas import *
import random
from db.conexion import establecer_conexion
from validations.user_validations import *
from users.backend.db_users import *
from util.utilidades import resource_path
def validate_number_input(text):
        if text == "":
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False



class U_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent=parent
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.validate_number = self.register(validate_number_input)
        self.images = {}
        self.cargos = {
            1: "Encargado de Servicio",
            2: "Asistente Bibliotecario"
        }
        self.roles = {
            1: "Admin",
            2: "Super Admin"
        }
        
        self.data = []
        self.page_size = 15
        self.current_page = 0
        
        # Crear el marco izquierdo para el menú de navegación

        self.user_frame_list = tk.Frame(self.canvas, bg="#FAFAFA")
        self.user_frame_list.pack(expand=True, side="left", fill="both") #padx=212, pady=150, ipady=80
        self.user_frame_list.place(x=215,y=218, height=470, width=1135)
        # Títulos para los Treeviews
        bold_font = font.Font(family="Bold", size=15, weight="bold")
        self.label_prestamos = tk.Label(self.canvas, text="Tabla Usuarios", bg="#FAFAFA", fg="#031A33", font=bold_font)
        self.label_prestamos.place(x=665.0, y=180.0, width=225.0, height=35.0)

        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.label_nombre = self.canvas.create_text(245.0, 82.0, anchor="nw", text="Buscar por Cédula", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1177.0, 170.0, text="Editar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1275.0, 170.0, text="Eliminar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1080.0, 170.0, text="Agregar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(980.0, 170.0, text="Refrescar", fill="#040F21", font=("Bold", 17))
        # Configurar el Entry con validación
        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2, validate="key", validatecommand=(self.validate_number, "%P"))
        self.buscar.insert(0, "Ingrese cédula")
        self.buscar.place(x=245.0, y=112.0, width=267.0, height=48.0)
        self.buscar.bind("<Return>", self.boton_buscar)
        self.buscar.bind("<KeyPress>",self.key_on_press_search)
    
        
        
            
            # Cargar y almacenar las imágenes
        self.images['boton_cargar'] = tk.PhotoImage(file=resource_path("assets_2/16_refrescar.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_cargar'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.refresh_frame(),
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=915.0, y=60.0, width=130.0, height=100.0)

                    # Cargar y almacenar las imágenes
        self.images['boton_agregar'] = tk.PhotoImage(file=resource_path("assets_2/5_agregar.png"))
            
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
        self.button_e.place(x=1015.0, y=60.0, width=130.0, height=100.0)

            # Cargar y almacenar las imágenes
        self.images['boton_eliminar'] = tk.PhotoImage(file=resource_path("assets_2/7_eliminar.png"))
            
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
        self.button_e.place(x=1215.0, y=60.0, width=130.0, height=100.0)

        self.images['boton_modificar'] = tk.PhotoImage(file=resource_path("assets_2/6_editar.png"))
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
        self.button_m.place(x=1115.0, y=60.0, width=130.0, height=100.0)
        """
        prev_button = tk.Button(self.user_frame_list, text="< Anterior", borderwidth=0, highlightthickness=0, relief="flat", font=("Montserrat Regular", 15), bg="#FAFAFA", fg="#006ac2", activebackground="#FAFAFA", activeforeground="#006ac2", command=self.previous_page)
        prev_button.pack(side=tk.LEFT, padx=10, pady=10)

        next_button = tk.Button(self.user_frame_list, text="Siguiente >", borderwidth=0, highlightthickness=0, relief="flat", font=("Montserrat Regular", 15), bg="#FAFAFA", fg="#006ac2", activebackground="#FAFAFA", activeforeground="#006ac2", command=self.next_page)
        next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.page_label = tk.Label(self.user_frame_list, text=f"Página {self.current_page + 1}", bg="#FAFAFA", fg="#031A33", font=("Montserrat Regular", 13))
        self.page_label.pack(side=tk.BOTTOM, pady=15)"""
              
        self.setup_treeview()
        #self.load_users()
        
        self.display_page()
        self.refresh_frame()
         
     
        
    def setup_treeview(self):
        style = ttk.Style()
        style.configure("Rounded.Treeview", 
                        background="#E5E1D7",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="#f0f0f0",
                        bordercolor="blue",
                        lightcolor="lightblue",
                        darkcolor="darkblue")
        style.map('Rounded.Treeview', background=[('selected', '#347083')])
        style.configure("Rounded.Treeview.Heading",
                        font=('Helvetica', 10, 'bold'),
                        background="#2E59A7",
                        foreground="#000000",
                        borderwidth=0)
        columns = ("ID Usuario", "Cargo", "ID Rol", "Nombre", "Apellido", "C.I", "Nombre Usuario")
        self.user_table_list = ttk.Treeview(self.user_frame_list, columns=columns, show='headings', style="Rounded.Treeview", selectmode="browse")
        for col in columns:
            self.user_table_list.heading(col, text=col)
            self.user_table_list.column(col, width=90, anchor="center")
        self.user_table_list.pack(expand=True, fill="both", padx=30, pady=5)
        scrollbar_pt = ttk.Scrollbar(self.user_table_list, orient="vertical", command=self.user_table_list.yview)
        self.user_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
        self.images['boton_siguiente'] = tk.PhotoImage(file=resource_path("assets_2/siguiente.png"))
        self.images['boton_anterior'] = tk.PhotoImage(file=resource_path("assets_2/atras.png"))
        # Botones de navegación
        prev_button = tk.Button(
            self.user_frame_list, 
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
            self.user_frame_list, 
            image=self.images['boton_siguiente'],
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#006ac2",   # Color del texto cuando el botón está activo
            command=self.next_page)
        next_button.pack(side=tk.RIGHT, padx=25, pady=0)
        
        # Etiqueta para mostrar la página actual
        self.page_label = tk.Label(self.user_frame_list, text=f"Página {self.current_page + 1}", bg="#FAFAFA", fg="#031A33", font=("Montserrat Regular", 13))
        self.page_label.pack(side=tk.BOTTOM, pady=15)
        #list_users_db(self.user_table_list,self.cargos,self.roles)       
        
    def list_users_db(self, treeview, cargos, roles):
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            query = "SELECT * FROM usuarios WHERE estado_usuario = 'activo'"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            mariadb_conexion.close()
            
            # Almacenar los datos en self.data en lugar de insertarlos directamente en el Treeview
            self.data = []
            for row in rows:
                row = list(row)
                row[1] = cargos.get(row[1], "Desconocido")
                row[2] = roles.get(row[2], "Desconocido")
                self.data.append(tuple(row))

            # Mostrar la primera página de datos
            self.display_page()
    def get_data_page(self, offset, limit):
        return self.data[offset:offset + limit]

    def display_page(self):
        for row in self.user_table_list.get_children():
            self.user_table_list.delete(row)
        page_data = self.get_data_page(self.current_page * self.page_size, self.page_size)
        for fila in page_data:
            self.user_table_list.insert("", "end", values=fila)
        self.update_page_label()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.data):
            self.current_page += 1
            self.display_page()
            self.user_table_list.yview_moveto(0)  

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()
            self.user_table_list.yview_moveto(0)  

    def update_page_label(self):
        
        total_pages = (len(self.data) + self.page_size - 1) // self.page_size  # Calcular el total de páginas
        self.page_label.config(text=f"Página {self.current_page + 1} de {total_pages}")
        
        
    def refresh_frame(self):
        self.list_users_db(self.user_table_list, self.cargos,self.roles)


    
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

    def convertir_cargo_rol(self, cargo, rol):
        cargo_nombre = self.cargos.get(cargo, "Desconocido")
        rol_nombre = self.roles.get(rol, "Desconocido")
        return cargo_nombre, rol_nombre


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
                    SELECT ID_Usuario, ID_Cargo, ID_Rol, Nombre, Apellido, Cedula, Nombre_Usuario 
                    FROM usuarios 
                    WHERE Cedula = %s
                """, (busqueda,))
                resultados = cursor.fetchall()

                if resultados:
                    # Limpiar la tabla antes de insertar nuevos resultados
                    self.user_table_list.delete(*self.user_table_list.get_children())
                    
                    # Insertar los nuevos resultados con la conversión de cargo y rol
                    for fila in resultados:
                        id_usuario, id_cargo, id_rol, nombre, apellido, cedula, nombre_usuario = fila
                        cargo, rol = self.convertir_cargo_rol(id_cargo, id_rol)
                        self.user_table_list.insert("", "end", values=(id_usuario, cargo, rol, nombre, apellido, cedula, nombre_usuario))

                    self.buscar.delete(0, 'end')  # Limpiar el Entry después de una búsqueda exitosa
                    messagebox.showinfo("Búsqueda Exitosa de Usuario", f"Se encontró el usuario: {resultados[0][3]} {resultados[0][4]}.")
                else:
                    self.buscar.delete(0, 'end')  # Limpiar el Entry si no se encontraron coincidencias
                    messagebox.showinfo("Búsqueda Fallida de Usuario", f"No se encontró ningún usuario con la cédula '{busqueda}'. Por favor, verifique la cédula ingresada.")
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
        finally:
            if mariadb_conexion:
                mariadb_conexion.close()






    def cancelar(self, window):
        if messagebox.askyesno("Advertencia", "¿Seguro que quieres cerrar esta ventana?"):
            window.destroy()  # Esto cerrará la ventana de filtro

  

class U_Registrar(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__()
        self.withdraw()
        self.parent = parent
        self.canvas = tk.Canvas(self, bg="#031A33", width=863, height=530)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.validate_number = self.register(validate_number_input)
        self.images = {}
        self.iconbitmap(resource_path('assets_2/logo_biblioteca.ico'))
        self.resizable(False, False)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancelar(self))
        self.canvas.create_rectangle(0, 0, 950, 74, fill="#2E59A7")
        """rectangulo_color = tk.Label(self, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)"""
        self.canvas.create_text(255.0, 21.0, anchor="nw", text="Registro de Usuarios", fill="#ffffff", font=("Montserrat Medium", 28))
        self.cargos = {
            1: "Encargado de Servicio",
            2: "Asistente Bibliotecario"
        }
        self.roles = {
            1: "Admin",
            2: "Super Admin"
        }
        # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=resource_path("assets_2/R_button_light_blue.png"))

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
        
        self.images['boton_c'] = tk.PhotoImage(file=resource_path("assets_2/c_button_red1.png"))
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
        self.cargo_combobox.set("Encargado de Servicio")  # Establece el valor inicial a "Encargado de Servicio"

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
        self.after(500,self.deiconify)
    def cancelar(self, window):
        if messagebox.askyesno("Advertencia", "¿Seguro que quieres cerrar esta ventana? Los datos del nuevo usuario no se guardarán.", parent=self):
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
            messagebox.showinfo("Éxito", "Registro exitoso del usuario.",parent=self)
            self.clear_entries_register()
            #self.destroy()
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
    def __init__(self, parent, user_data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.withdraw()
        self.parent = parent
        self.validate_number = self.register(validate_number_input)
        self.images = {}
        self.iconbitmap(resource_path('assets_2/logo_biblioteca.ico'))
        self.geometry("863x530") 
        self.config(bg="#042344")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancelar(self))
        self.grab_set()
        self.cargos = {
            1: "Encargado de Servicio",
            2: "Asistente Bibliotecario"
        }
        self.roles = {
            1: "Admin",
            2: "Super Admin"
        }
        # Guardar los datos del usuario en un diccionario
        self.user_data = {
            "ID": user_data[0],
            "Cargo" : user_data[1],
            "ID_Rol" :user_data[2],
            "Nombre": user_data[3],
            "Apellido": user_data[4],
            "Cedula": user_data[5],
            "Username": user_data[6],
            "Password": user_data[7] # Este campo se actualizará al modificar
           # "Verify_Password": ""  # Este campo se actualizará al modificar
        }
        self.original_values_user = self.user_data.copy()
        print(self.user_data,"\n",self.original_values_user)
        # Crear los elementos de la interfaz
        
        self.create_widgets()
        self.crear_boton_modificar()
        self.crear_boton_modificar_inactivo()
        self.crear_boton_restaurar()
        self.crear_boton_cancelar()
        self.insert_values_user()
        self.after(500,self.deiconify)
    def create_widgets(self):
        rectangulo_color = tk.Label(self, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)

        tk.Label(self, text="Modificación de Usuarios", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=225.0, y=20.0, width=450.0, height=35.0)

        tk.Label(self, text="Ingrese los datos a modificar", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=10.0, y=100.0, width=330.0, height=35.0)
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                fieldbackground="#2E59A7",  # Fondo del campo de entrada
                background="#2E59A7",  # Fondo del desplegable
                bordercolor="#041022",  # Color del borde
                arrowcolor="#ffffff",  # Color de la flecha
                padding= "9",
                ) # padding para agrandar la altura del select
        # Crear y colocar los widgets
        # Primera fila
        self.cargo_combobox = ttk.Combobox(self, values=list(self.cargos.values()), state="readonly", width=30, font=("Bold", 10), style="TCombobox")
        self.cargo_combobox.place(x=61.0, y=185.5)
        self.cargo_combobox.bind("<<ComboboxSelected>>",self.check_changes)

        # Segunda fila
        self.input_nombre = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_nombre.place(x=61.0, y=285.0, width=237.0, height=37.5)
        self.input_nombre.bind("<Return>", self.focus_next_widget)  # Llamada a focus_next_widget
        self.input_nombre.bind("<KeyPress>", self.on_key_press_modify)  # Llamada a on_key_press_modify
        self.input_nombre.bind("<KeyRelease>", self.check_changes)

        self.input_apellido = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_apellido.place(x=318.0, y=285.0, width=237.0, height=38.0)
        self.input_apellido.bind("<Return>", self.focus_next_widget)  # Llamada a focus_next_widget
        self.input_apellido.bind("<KeyPress>", self.on_key_press_modify)  # Llamada a on_key_press_modify
        self.input_apellido.bind("<KeyRelease>", self.check_changes)

        self.input_cedula = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(self.validate_number, "%P"))
        self.input_cedula.place(x=575.0, y=285.0, width=237.0, height=37.5)
        self.input_cedula.bind("<Return>", self.focus_next_widget)  # Llamada a focus_next_widget
        self.input_cedula.bind("<KeyPress>", self.on_key_press_modify)  # Llamada a on_key_press_modify
        self.input_cedula.bind("<KeyRelease>", self.check_changes)

        # Tercera fila
        self.input_username = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_username.place(x=61.0, y=385.0, width=237.0, height=37.5)
        self.input_username.bind("<Return>", self.focus_next_widget)  # Llamada a focus_next_widget
        self.input_username.bind("<KeyPress>", self.on_key_press_modify)  # Llamada a on_key_press_modify
        self.input_username.bind("<KeyRelease>", self.check_changes)

        self.input_password = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.input_password.place(x=318.0, y=385.0, width=237.0, height=37.5)
        self.input_password.bind("<Return>", self.focus_next_widget)  # Llamada a focus_next_widget
        self.input_password.bind("<KeyPress>", self.on_key_press_modify)  # Llamada a on_key_press_modify
        self.input_password.bind("<KeyRelease>", self.check_changes)

        # self.input_verify_password = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        # self.input_verify_password.place(x=575.0, y=385.0, width=237.0, height=37.5)
        # self.input_verify_password.bind("<Return>", lambda event: self.modify_user)
        # self.input_verify_password.bind("<KeyPress>", self.on_key_press_modify)  # Llamada a on_key_press_modify
        

        self.inicializador_titulos()

 

    def inicializador_titulos(self):
        # Titulos de los inputs
        tk.Label(self, text="Cargo", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=61.0, y=152.0)
        tk.Label(self, text="Nombre", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=61.0, y=252.0)
        tk.Label(self, text="Apellido", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=318.0, y=252.0)
        tk.Label(self, text="Cedula", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=575.0, y=252.0)
        tk.Label(self, text="Nombre de usuario", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=61.0, y=352.0)
        tk.Label(self, text="Contraseña", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=318.0, y=352.0)
        #tk.Label(self, text="Confirmar Contraseña", fg="#a6a6a6", bg="#042344", font=("Bold", 17)).place(x=575.0, y=352.0)

    def insert_values_user(self):
        self.clear_entries_user_modify()
        self.cargo_combobox.insert(0,self.original_values_user["Cargo"])  
        self.input_nombre.insert(0, self.original_values_user['Nombre'])
        self.input_apellido.insert(0, self.original_values_user['Apellido'])
        self.input_cedula.insert(0, self.original_values_user['Cedula'])
        self.input_username.insert(0, self.original_values_user['Username'])
        self.input_password.insert(0, self.original_values_user["Password"])
        self.check_changes()

    def clear_entries_user_modify(self):
        self.cargo_combobox.set("Encargado de Servicio")  # Establece el valor inicial a "Encargado de Servicio"
        self.input_nombre.delete(0, tk.END)
        self.input_apellido.delete(0, tk.END)
        self.input_cedula.delete(0, tk.END)
        self.input_username.delete(0, tk.END)
        self.input_password.delete(0, tk.END)
        #self.input_verify_password.delete(0, tk.END)

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def on_key_press_modify(self, event):
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
    
    def check_changes(self, *args):
        try:
            # Obtener los valores actuales de los campos de usuario
            current_values = {
                "Cargo" : self.cargo_combobox.get().strip(),
                "Nombre": self.input_nombre.get().strip(),
                "Apellido": self.input_apellido.get().strip(),
                "Cedula": self.input_cedula.get().strip(),
                "Username": self.input_username.get().strip(),
                "Password": self.input_password.get().strip(),
                
            }

            # Comparar valores clave por clave
            differences = []
            for key in current_values:
                if current_values[key] != self.original_values_user[key]:
                    differences.append(f"Diferencia en {key}: {current_values[key]} (actual) != {self.original_values_user[key]} (original)")

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
        self.boton_modificar_inactivo.place(x=61.0, y=465.0, width=130.0, height=40.0)
        self.boton_modificar_inactivo.place_forget()
        print("Botón 'Modificar' inactivo creado y oculto inicialmente.")

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
            command=self.modify_user,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_modificar.place(x=61.0, y=465.0, width=130.0, height=40.0)
        self.boton_modificar.place_forget()
        print("Botón 'Modificar' creado y oculto inicialmente.")

    def mostrar_boton_modificar(self):
        self.boton_modificar.place(x=61.0, y=465.0, width=130.0, height=40.0)
        self.boton_modificar_inactivo.place_forget()
        print("Botón 'Modificar' mostrado.")

    def mostrar_boton_modificar_inactivo(self):
        self.boton_modificar_inactivo.place(x=61.0, y=465.0, width=130.0, height=40.0)
        self.boton_modificar.place_forget()
        print("Botón 'Modificar' inactivo mostrado.")

    def ocultar_boton_modificar(self):
        self.boton_modificar.place_forget()
        self.boton_modificar_inactivo.place_forget()
        print("Botón 'Modificar' oculto.")

    def crear_boton_restaurar(self):
        self.images['boton_r'] = tk.PhotoImage(file=resource_path("assets_2/rest_button_green.png"))
         
        self.boton_R = tk.Button(
            self,
            image=self.images['boton_r'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.insert_values_user(),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_R.place(x=220.0, y=465.0, width=130.0, height=40.0)

    def crear_boton_cancelar(self):
        self.images['boton_c'] = tk.PhotoImage(file=resource_path("assets_2/c_button_red1.png"))
 
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
        self.boton_C.place(x=380.0, y=465.0, width=130.0, height=40.0)


    def cancelar(self, window):
        
        if messagebox.askyesno("Advertencia", f'¿Seguro que quieres cerrar esta ventana? Todos los cambios no guardados en el usuario {self.original_values_user["Nombre"]} se perderán.', parent=self):
            window.destroy()




    def modify_user(self):
        cargo = self.cargo_combobox.get()
        cargo_id = None
        
        # Obtener el ID del cargo desde el diccionario
        for key, value in self.cargos.items():
            if value == cargo:
                cargo_id = key
                break
        nuevos_valores = {
            "Cargo": cargo_id,
            "Nombre": self.input_nombre.get(),
            "Apellido": self.input_apellido.get(),
            "Cedula": self.input_cedula.get(),
            "Username": self.input_username.get(),
            "Password": self.input_password.get(),
        }
        
        id_cliente = self.original_values_user["ID"]
        print(f"ID USUARIO : {id_cliente}")
        
        # Validar los campos incluyendo el ID del usuario
        errores = validar_campos(
            self.input_username.get().strip(),
            self.input_password.get().strip(),
            tipo_validacion="modificar",
            nombre=self.input_nombre.get().strip(),
            apellido=self.input_apellido.get().strip(),
            cedula=self.input_cedula.get().strip(),
            cargo=self.cargo_combobox.get().strip(),
            user_id=id_cliente
        )
        
        print(f"Errores: {errores}")  # Agregar esta línea para depuración
        if errores:
            messagebox.showerror("Error al modificar", "Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"- {msg}" for msg in errores), parent=self)
            return
        
        print("Datos recogidos:")
        for key, value in nuevos_valores.items():
            print(f"{key}: {value}")

        # Actualizar el usuario con los nuevos valores
        user_data = {"id": id_cliente}
        if update_user(user_data, nuevos_valores):
            messagebox.showinfo("Éxito", "Modificación del usuario exitosa.", parent=self)
            self.clear_entries_user_modify()
            self.destroy()
        else:
            messagebox.showinfo("Modificación fallida", "Usuario mantiene sus valores.", parent=self)

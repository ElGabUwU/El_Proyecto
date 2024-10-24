import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
#from Library.librerias import recoger_sesion, drop_sesion
from Library.fun_db_users import *
#from Vistas.listas import *
import random
from db.conexion import establecer_conexion

#ID_Rol?
#hacer que nombre y apellido sean un solo entry?
def campos_validacion(Cargo,Nombre,Apellido,Cedula,Nombre_Usuario,Clave):
    if not Cargo:
        messagebox.showerror("Error", "El campo 'Cargo' es obligatorio.")
        return True
    if not Nombre:
        messagebox.showerror("Error", "El campo 'Nombre' es obligatorio.")
        return True
    if not Apellido:
        messagebox.showerror("Error", "El campo 'Apellido' es obligatorio.")
        return True
    if not Cedula:
        messagebox.showerror("Error", "El campo 'Cedula' es obligatorio.")
        return True
    
    if not Nombre_Usuario:
        messagebox.showerror("Error", "El campo 'Nombre de Usuario' es obligatorio.")
        return True
    
    if not Clave:
        messagebox.showerror("Error", "El campo 'Contraseña' es obligatorio.")
        return True
    else:
        return False


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

class U_Registrar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        
        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del nuevo usuario a agregar", fill="#a6a6a6", font=("Bold", 17))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cargo", fill="#a6a6a6", font=("Bold", 17))

        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Nombre", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Apellido", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(779.0, 252.0, anchor="nw", text="Cedula", fill="#a6a6a6", font=("Bold", 17))
        
        
        #fila 3
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Nombre de usuario", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Contraseña", fill="#a6a6a6", font=("Bold", 17))
        
        
        #fila 4
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        #primera fila
        self.input_nombre = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_nombre.place(x=520.0, y=282.0, width=237.0, height=38.0)
 
        self.input_apellido = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_apellido.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.input_cedula = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_cedula.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        
        #segunda fila
        self.input_username = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_username.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.input_password = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_password.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        #tercera fila
        
        #Select tipo de pokemon
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                        fieldbackground="#2E59A7",  # Fondo del campo de entrada
                        background="#2E59A7",  # Fondo del desplegable
                        bordercolor="#041022",  # Color del borde
                        arrowcolor="#ffffff",  # Color de la flecha
                        padding= "9",
                        ) # padding para agrandar la altura del select
        
        cargos = {
        "Encargado de Servicio": 1, "Asistente Bibliotecario": 2
        
        }
        
        self.cargo_combobox = ttk.Combobox(self, values=list(cargos.keys()), state="readonly", width=30, font=("Bold", 10), style="TCombobox")
        self.cargo_combobox.place(x=263.0, y=181.5)
        
        def register_user():
            #REVISAR COMO SE SUBIERON LOS CARGOS A LA BD PARA HACER LAS VALIDACIONES    
            
            N_cargo = self.cargo_combobox.get() if self.cargo_combobox else None 
            
            if isinstance(N_cargo, str):
                cargo = cargos.get(N_cargo, None)
            else:
                cargo = None
            
            nombre= self.input_nombre.get()
            apellido=self.input_apellido.get()
            cedula=self.input_cedula.get()
            username=self.input_username.get()
            password=self.input_password.get()
            rol=1
            
            print("cargo ", {cargo},"nombre ", {nombre}, "apellido ", {apellido}, "cedula ", {cedula}, "username ", {username}, "password ", {password})
            print("\n")
            
            
            if campos_validacion(cargo,nombre,apellido,cedula,username,password) == True:
                return
            
            if self.cedula_existe(cedula):
                messagebox.showinfo("Error", "La cédula ya está registrada.")
                return
            
            
            if create_user(cargo, rol, nombre, apellido, cedula, username, password):
                messagebox.showinfo("Éxito", "Registro éxitoso del usuario.")
                self.cargo_combobox.set('')
                self.input_nombre.delete(0, tk.END)
                self.input_apellido.delete(0, tk.END)
                self.input_cedula.delete(0, tk.END)
                self.input_username.delete(0, tk.END)
                self.input_password.delete(0, tk.END)
            else:
                messagebox.showinfo("Registro fallido", "Usuario no pudo registrarse.")
                
        
        #-------------------------------------------------------------------------------
        # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("R_Boton_registrar.png"))

        # Crear el botón
        boton_R = self.images['boton_R']
        tk.Button(
            self,
            image=boton_R,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: register_user(),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"  # Color del texto cuando el botón está activo
        ).place(x=265.0, y=465.0, width=130.0, height=40.0)

    def cedula_existe(self, cedula):
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            query = "SELECT COUNT(*) FROM usuarios WHERE Cedula = %s"
            cursor.execute(query, (cedula,))
            result = cursor.fetchone()
            return result[0] > 0

class U_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Crear el marco izquierdo para el menú de navegación

        self.user_frame_list = tk.Frame(self.canvas, bg="#FAFAFA")
        self.user_frame_list.pack(expand=True, side="left", fill="both") #padx=212, pady=150, ipady=80
        self.user_frame_list.place(x=215,y=205, height=480, width=1150)

        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.label_nombre = self.canvas.create_text(265.0, 100.0, anchor="nw", text="Buscar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1077.0, 170.0, text="Editar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1175.0, 170.0, text="Eliminar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(980.0, 170.0, text="Agregar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(880.0, 170.0, text="Refrescar", fill="#040F21", font=("Bold", 17))
        
        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.buscar.place(x=265.0, y=130.0, width=267.0, height=48.0)
        self.buscar.bind("<Return>", self.boton_buscar)

            #Boton Cargar Libros
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
                #command=self.refresh_frame,
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
            command=lambda: self.open_modify_window(self),
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
        
        list_users_db(self.user_table_list)

    def refresh_frame(self):
        # Eliminar todos los widgets del frame
        for widget in self.user_frame_list.winfo_children():
            widget.destroy()

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

        # Volver a crear y configurar el Treeview
        columns = ("ID Usuario", "Cargo", "ID Rol", "Nombre", "Apellido", "C.I", "Nombre Usuario")
        self.user_table_list = ttk.Treeview(self.user_frame_list, columns=columns, show='headings', style="Rounded.Treeview")
        for col in columns:
            self.user_table_list.heading(col, text=col)
            self.user_table_list.column(col, width=90, anchor="center")
        self.user_table_list.pack(expand=True, fill="both", padx=70, pady=5)

        scrollbar_pt = ttk.Scrollbar(self.user_table_list, orient="vertical", command=self.user_table_list.yview)
        self.user_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")

        # Recargar los datos desde la base de datos
        list_users_db(self.user_table_list)
    
    def open_modify_window(self,parent):
        filter_window = tk.Toplevel(self)
        filter_window.title("Modificar Usuario")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))
        filter_window.geometry("950x550")
        filter_window.config(bg="#042344")
        filter_window.resizable(False, False)
        rectangulo_color = tk.Label(filter_window, bg="#2E59A7", width=200, height=4)
        rectangulo_color.place(x=0, y=0)
        tk.Label(filter_window, text="Modificación de Usuarios", fg="#ffffff", bg="#2E59A7", font=("Montserrat Medium", 28)).place(x=225.0, y=20.0, width=450.0, height=35.0)#.pack(pady=20,expand=False)#grid(row=0, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese los datos a modificar", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=10.0, y=100.0, width=330.0, height=35.0)#.pack(pady=10, expand=False)
        tk.Label(filter_window, text="Cedula", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=210.0, y=130.0, width=120.0, height=35.0)#.pack(pady=10,expand=False)#grid(row=1, column=0, padx=10, pady=5)
        self.id_cedula_entry = tk.Entry(filter_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.id_cedula_entry.place(x=240.0, y=170.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=1, column=1, padx=10, pady=5)

        #tk.Label(filter_window, text="Ingrese el nuevo nombre de usuario", fg="#a6a6a6", bg="#2E59A7", font=("Bold", 17)).place()#.pack(pady=10, expand=False)
        tk.Label(filter_window, text="Nombre de Usuario", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=500.0, y=130.0, width=185.0, height=35.0)#.pack(pady=10,expand=False)#.grid(row=3, column=0, padx=10, pady=5)
        self.nombre_usuario_entry = tk.Entry(filter_window, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.nombre_usuario_entry.place(x=500.0, y=170.0, width=190.0, height=35.0)#pack(expand=False)#.grid(row=3, column=1, padx=10, pady=5)

        #tk.Label(filter_window, text="Ingrese el nombre y apellido ", fg="#a6a6a6", bg="#2E59A7", font=("Bold", 17)).place()#.pack(pady=10, expand=False)
        tk.Label(filter_window, text="Nombre", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=220.0, y=230.0, width=120.0, height=35.0)#.pack(pady=10,expand=False)#.grid(row=5, column=0, padx=10, pady=5)
        self.nombre_entry = tk.Entry(filter_window,  bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.nombre_entry.place(x=240.0, y=270.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=5, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="Apellido", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=500.0, y=230.0, width=120.0, height=35.0)#.pack(pady=10,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.apellido_entry = tk.Entry(filter_window,  bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.apellido_entry.place(x=500.0, y=270.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="ID del usuario que será modificado", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=30.0, y=320.0, width=350.0, height=35.0)#.pack(pady=10, expand=False)
        tk.Label(filter_window, text="ID", fg="#CCCED1", bg="#042344", font=("Montserrat Regular", 15)).place(x=300.0, y=360.0, width=120.0, height=35.0)#.pack(pady=10,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.id_entry = tk.Entry(filter_window,  bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", relief="flat")
        self.id_entry.place(x=350.0, y=400.0, width=190.0, height=35.0)#.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)

        self.images['boton_m'] = tk.PhotoImage(file=relative_to_assets("M_button_light_blue.png"))

        self.boton_M = tk.Button(
            filter_window,
            image=self.images['boton_m'],
            borderwidth=0,
            highlightthickness=0,
            command=self.apply_modify_users,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_M.place(x=530.0, y=480.0, width=130.0, height=40.0)
        
        self.images['boton_c'] = tk.PhotoImage(file=relative_to_assets("c_button_red1.png"))

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
        self.boton_C.place(x=270.0, y=480.0, width=130.0, height=40.0)
        
        
        # Crear un estilo personalizado
        """style = ttk.Style()
        style.configure("Custom.TButton", background="#2E59A7", foreground="#ffffff", font=("Bold", 22))

        self.filter_button = ttk.Button(filter_window, text="Modificar", style="Custom.TButton", command=self.apply_modify_users)
        self.filter_button.place(x=250.0, y=480.0, width=140.0, height=50.0)

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.place(x=520.0, y=480.0, width=140.0, height=50.0)#.pack(expand=True)#.place(x=390, y=400)#.pack(pady=5, expand=False)"""
        
    def apply_modify_users(self):
            id_cedula= self.id_cedula_entry.get() #self.cota.get()
            name_user = self.nombre_usuario_entry.get()#self.combobox1.get()
            nombre = self.nombre_entry.get()#self.menu_actual.get() if self.menu_actual else None
            apellido = self.apellido_entry.get()
            id = self.id_entry.get()
            if id:
                respuesta = messagebox.askyesno("Confirmar modificación", "¿Desea modificar?")
                if respuesta:
                    if update_user_list(id_cedula, name_user, nombre, apellido, id):
                        messagebox.showinfo("Éxito", "Modificación éxitosa del usuario")
                            #return True
                    else:
                        messagebox.showinfo("Fallido", "No se pudo modificar al usuario.")
                            #return False
                else:
                        messagebox.showinfo("Cancelado", "Modificación cancelada.")
            else:
                    messagebox.showinfo("Error", "Por favor, proporciona una ID válida.")

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

class U_Modificar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#031A33", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        
        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del usuario a modificar", fill="#a6a6a6", font=("Bold", 17))
        
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="ID", fill="#a6a6a6", font=("Bold", 17))
        #fila 1
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Cargo", fill="#a6a6a6", font=("Bold", 17))

        #fila 2
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Nombre", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Apellido", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(779.0, 352.0, anchor="nw", text="Cedula", fill="#a6a6a6", font=("Bold", 17))
        
        
        #fila 3
        self.canvas.create_text(263.0, 452.0, anchor="nw", text="Nombre de usuario", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(520.0, 452.0, anchor="nw", text="Contraseña", fill="#a6a6a6", font=("Bold", 17))
        
        
    
        #primera fila
        self.input_ID = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_ID.place(x=263.0, y=182.0, width=237.0, height=37.5)
        #se deberia agregar un campo de id?
        
        #segunda fila
        self.input_nombre = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_nombre.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.input_apellido = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_apellido.place(x=520.0, y=382.0, width=237.0, height=38.0)
        
        self.input_cedula = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_cedula.place(x=779.0, y=382.0, width=237.0, height=37.5)
        
        
        #tercera fila
        self.input_username = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_username.place(x=263.0, y=482.0, width=237.0, height=37.5)
        
        self.input_password = tk.Entry(self, bd=0, bg="#031A33", fg="#a6a6a6", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", borderwidth=0.5, relief="solid")
        self.input_password.place(x=520.0, y=482.0, width=237.0, height=37.5)
        
        #Select tipo de pokemon
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox",
                        fieldbackground="#FFFFFF",  # Fondo del campo de entrada
                        background="#FF0000",  # Fondo del desplegable
                        bordercolor="#000716",  # Color del borde
                        arrowcolor="#FFFFFF",  # Color de la flecha
                        padding= "9",
                        ) # padding para agrandar la altura del select
        
        cargos = {
        "Encargado de Servicio": 1, "Asistente Bibliotecario": 2
        
        }
        
        self.cargo_combobox = ttk.Combobox(self, values=list(cargos.keys()), state="readonly", width=30, font=("Montserrat Medium", 10))
        self.cargo_combobox.place(x=263.0, y=281.5)
        
      
        

        #-------------------------------------------------------------------------------
        # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=relative_to_assets("M_Boton.png"))
        
        #MODIFICAR ESTO!!!!
        def modify_user():
            id_user= self.input_ID.get() 
            N_cargo = self.cargo_combobox.get() if self.cargo_combobox else None 
            
            if isinstance(N_cargo, str):
                cargo = cargos.get(N_cargo, None)
            else:
                cargo = None
            nombre= self.input_nombre.get()
            apellido=self.input_apellido.get()
            cedula=self.input_cedula.get()
            username=self.input_username.get()
            password=self.input_password.get()
            print("cargo ", {cargo}, "nombre ", {nombre}, "apellido ", {apellido}, "cedula ", {cedula}, "username ", {username}, "password ", {password})
        
            print("\n")
            if campos_validacion(cargo,nombre,apellido,cedula,username,password) == True:
                    return
            if not id_user:
                messagebox.showerror("Error", "El campo 'ID' es obligatorio.")
                return 
            if update_user(cargo,nombre,apellido,cedula,username,password,id_user):
                messagebox.showinfo("Éxito", "Modificación del libro éxitoso.")
                self.cargo_combobox.set('')
                self.input_nombre.delete(0, tk.END)
                self.input_apellido.delete(0, tk.END)
                self.input_cedula.delete(0, tk.END)
                self.input_username.delete(0, tk.END)
                self.input_password.delete(0, tk.END)
            else:
                messagebox.showinfo("Modificación fallida", "Libro no sufrio cambios.")

        # Crear el botón
        boton_R = self.images['boton_R']
        tk.Button(
            self,
            image=boton_R,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: modify_user(),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"  # Color del texto cuando el botón está activo
        ).place(x=265.0, y=565.0, width=130.0, height=40.0)
        
class U_Eliminar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#031A33", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Formulario para el eliminar
        self.label_info = self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del usuario a Eliminar", fill="#a6a6a6", font=("Bold", 17))
        
        # Texto para el nombre
        self.label_ID = self.canvas.create_text(263.0, 152.0, anchor="nw", text="ID", fill="#a6a6a6", font=("Bold", 17))
        
        self.input_ID = tk.Entry(
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
        self.input_ID.place(x=263.0, y=182.0, width=237.0, height=38.0)

        def delete_user(self):
            id=self.input_ID.get() if self.input_ID else None
            if id:
                # Confirmación antes de eliminar
                respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar este libro?")
                if respuesta:
                    if delete_user_db(id):
                        messagebox.showinfo("Éxito", "Eliminación exitosa del libro.")
                    else:
                        messagebox.showinfo("Falla en la Eliminación", "El libro no existe o ya fue eliminado.")
                else:
                    messagebox.showinfo("Cancelado", "Eliminación cancelada.")
            else:
                messagebox.showinfo("Error", "Por favor, proporciona un ID de libro válido.")
        
        # Cargar y almacenar las imágenes
        self.images['boton_Eliminar_f'] = tk.PhotoImage(file=relative_to_assets("Boton_eliminar.png"))
        
        # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
            self,
            image=self.images['boton_Eliminar_f'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda:delete_user(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"  # Color del texto cuando el botón está activo
        )
        self.button_e.place(x=265.0, y=264.0, width=130.0, height=40.0)
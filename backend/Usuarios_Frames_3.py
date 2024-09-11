import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
#from Library.librerias import recoger_sesion, drop_sesion
from Library.fun_db_users import *
#from Vistas.listas import *
import random

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
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        
        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del nuevo usuario a agregar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        #fila 1
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cargo", fill="#000000", font=("Montserrat Regular", 15))

        #fila 2
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Nombre", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 252.0, anchor="nw", text="Apellido", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 252.0, anchor="nw", text="Cedula", fill="#000000", font=("Montserrat Regular", 15))
        
        
        #fila 3
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Nombre de usuario", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Contraseña", fill="#000000", font=("Montserrat Regular", 15))
        
        
        #fila 4
        #-------------------------------------------------------------------------------------
        # Crear y colocar los widgets
        #primera fila
        self.input_nombre = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_nombre.place(x=520.0, y=282.0, width=237.0, height=38.0)
 
        self.input_apellido = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_apellido.place(x=263.0, y=282.0, width=237.0, height=37.5)
        
        self.input_cedula = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_cedula.place(x=779.0, y=282.0, width=237.0, height=37.5)
        
        
        #segunda fila
        self.input_username = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_username.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.input_password = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_password.place(x=520.0, y=382.0, width=237.0, height=37.5)
        
        #tercera fila
        
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
            
            
            if create_user(cargo, rol, nombre, apellido, cedula, username, password):
                messagebox.showinfo("Éxito", "Registro del libro éxitoso.")
                self.cargo_combobox.set('')
                self.input_nombre.delete(0, tk.END)
                self.input_apellido.delete(0, tk.END)
                self.input_cedula.delete(0, tk.END)
                self.input_username.delete(0, tk.END)
                self.input_password.delete(0, tk.END)
            else:
                messagebox.showinfo("Registro fallido", "Libro no sufrio cambios.")
                
        
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
        ).place(x=265.0, y=465.0, width=130.0, height=40.0)

class U_Listar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Crear el marco izquierdo para el menú de navegación
        self.user_frame_list = tk.Frame(self.canvas, bg="white")
        self.user_frame_list.pack(expand=True, side="left", fill="both") #padx=212, pady=150, ipady=80
        self.user_frame_list.place(x=215,y=155, height=550, width=1150)

        # Texto para el nombre
        self.label_nombre = self.canvas.create_text(635.0, 85.0, anchor="nw", text="Buscar", fill="#000000", font=("Montserrat Regular", 15))
        
        self.buscar = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key")
        self.buscar.place(x=635.0, y=110.0, width=237.0, height=38.0)

            #                 Boton Cargar Libros
            # Cargar y almacenar las imágenes
        self.images['boton_cargar'] = tk.PhotoImage(file=relative_to_assets("Cargar_rojo.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_cargar'],
                borderwidth=0,
                highlightthickness=0,
                command=self.refresh_frame,
                relief="flat"
            )
        self.button_e.place(x=415.0, y=110.0, width=140.0, height=40.0)

            # Cargar y almacenar las imágenes
        self.images['boton_eliminar'] = tk.PhotoImage(file=relative_to_assets("Boton_eliminar.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
            self,
            image=self.images['boton_eliminar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_delete_window(self) ,
            relief="flat"
            )
        self.button_e.place(x=915.0, y=110.0, width=130.0, height=40.0)

        self.images['boton_modificar'] = tk.PhotoImage(file=relative_to_assets("M_boton.png"))
                    # Cargar y almacenar la imagen del botón
        self.button_m = tk.Button(
            self,
            image=self.images['boton_modificar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_modify_window(self),
            relief="flat"
            )
        self.button_m.place(x=1095.0, y=110.0, width=130.0, height=40.0)

        columns = ("ID Usuario", "Cargo", "ID Rol", "Nombre", "Apellido", "C.I", "Nombre Usuario")
        self.user_table_list= ttk.Treeview(self.user_frame_list, columns=columns, show='headings')
        for col in columns:
            self.user_table_list.heading(col, text=col)
            self.user_table_list.column(col, width=90)
        self.user_table_list.pack(expand=True, fill="both", padx=70, pady=45)

        scrollbar_pt = ttk.Scrollbar(self.user_table_list, orient="vertical", command=self.user_table_list.yview)
        self.user_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
        
        list_users_db(self.user_table_list)

    def refresh_frame(self):
        # Eliminar todos los widgets del frame
        for widget in self.user_frame_list.winfo_children():
            widget.destroy()

        # Volver a crear y configurar el Treeview
        columns = ("ID Usuario", "Cargo", "ID Rol", "Nombre", "Apellido", "C.I", "Nombre Usuario")
        self.user_table_list = ttk.Treeview(self.user_frame_list, columns=columns, show='headings')
        for col in columns:
            self.user_table_list.heading(col, text=col)
            self.user_table_list.column(col, width=90)
        self.user_table_list.pack(expand=True, fill="both", padx=70, pady=45)

        scrollbar_pt = ttk.Scrollbar(self.user_table_list, orient="vertical", command=self.user_table_list.yview)
        self.user_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")

        # Recargar los datos desde la base de datos
        list_users_db(self.user_table_list)
    
    def open_modify_window(self,parent):
        filter_window = tk.Toplevel(self)
        filter_window.title("Filtrar")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))

        self.bg_image = tk.PhotoImage(file=relative_to_assets("logo_biblioteca.png"))
        # Crear un Label para la imagen de fondo
        bg_label = tk.Label(filter_window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(filter_window, text="MODIFICACIÓN DE USUARIOS", fg="black", bg="white", font=("Helvetica", 15)).pack(pady=20,expand=False)#grid(row=0, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese el nuevo número de cédula", fg="black", bg="white").pack(pady=10, expand=False)
        tk.Label(filter_window, text="Cedula", fg="black", bg="white").pack(pady=10,expand=False)#grid(row=1, column=0, padx=10, pady=5)
        self.id_cedula_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_cedula_entry.pack(expand=False)#.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="Ingrese el nuevo nombre de usuario", fg="black", bg="white").pack(pady=10, expand=False)
        tk.Label(filter_window, text="Nombre de Usuario", fg="black", bg="white").pack(pady=10,expand=False)#.grid(row=3, column=0, padx=10, pady=5)
        self.nombre_usuario_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.nombre_usuario_entry.pack(expand=False)#.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(filter_window, text="Ingrese el nombre y apellido ", fg="black", bg="white").pack(pady=10, expand=False)
        tk.Label(filter_window, text="Nombre", fg="black", bg="white").pack(pady=10,expand=False)#.grid(row=5, column=0, padx=10, pady=5)
        self.nombre_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.nombre_entry.pack(expand=False)#.grid(row=5, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="Apellido", fg="black", bg="white").pack(pady=10,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.apellido_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.apellido_entry.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese ID del usuario", fg="black", bg="white").pack(pady=10, expand=False)
        tk.Label(filter_window, text="ID", fg="black", bg="white").pack(pady=10,expand=False)#.grid(row=6, column=0, padx=10, pady=5)
        self.id_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_entry.pack(expand=False)#.grid(row=6, column=1, padx=10, pady=5)

        # Botón para filtrar
        self.filter_button = tk.Button(filter_window, text="Modificar", bg="#f80000" ,fg="black",command=self.apply_modify_users)
        self.filter_button.pack(expand=True)#.place(x=390, y=400)
        
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

    def open_delete_window(self,parent):
        filter_window = tk.Toplevel(self)
        filter_window.title("Filtrar")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))

        self.bg_image = tk.PhotoImage(file=relative_to_assets("logo_biblioteca.png"))
        # Crear un Label para la imagen de fondo
        bg_label = tk.Label(filter_window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(filter_window, text="Eliminación de Usuario", fg="black", bg="white", font=("Helvetica", 15)).pack(pady=20,expand=False)#grid(row=0, column=5, padx=10, pady=5)
        tk.Label(filter_window, text="Ingrese el ID del Usuario", fg="black", bg="white").pack(pady=10, expand=False)
        tk.Label(filter_window, text="Cedula", fg="black", bg="white").pack(pady=10,expand=False)#grid(row=1, column=0, padx=10, pady=5)
        self.id_usuario_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.id_usuario_entry.pack(expand=False)#.grid(row=1, column=1, padx=10, pady=5)

        # Botón para filtrar
        self.filter_button = tk.Button(filter_window, text="Eliminar", bg="#f80000" ,fg="black",command=self.apply_delete_user)
        self.filter_button.pack(expand=True)#.place(x=390, y=400)

    def apply_delete_user(self):
            id_usuario= self.id_usuario_entry.get() #self.cota.get()
            if id:
                respuesta = messagebox.askyesno("Confirmar modificación", "¿Desea eliminar al usuario?")
                if respuesta:
                    if delete_user_db(id_usuario):
                        messagebox.showinfo("Éxito", "Eliminación éxitosa del usuario")
                            #return True
                    else:
                        messagebox.showinfo("Fallido", "No se pudo eliminar al usuario.")
                            #return False
                else:
                        messagebox.showinfo("Cancelado", "Eliminación cancelada.")
            else:
                    messagebox.showinfo("Error", "Por favor, proporciona una ID válida.")        
class U_Modificar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}
        
        # Titulos de los inputs
        self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del usuario a modificar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        
        self.canvas.create_text(263.0, 152.0, anchor="nw", text="ID", fill="#000000", font=("Montserrat Regular", 15))
        #fila 1
        self.canvas.create_text(263.0, 252.0, anchor="nw", text="Cargo", fill="#000000", font=("Montserrat Regular", 15))

        #fila 2
        self.canvas.create_text(263.0, 352.0, anchor="nw", text="Nombre", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 352.0, anchor="nw", text="Apellido", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(779.0, 352.0, anchor="nw", text="Cedula", fill="#000000", font=("Montserrat Regular", 15))
        
        
        #fila 3
        self.canvas.create_text(263.0, 452.0, anchor="nw", text="Nombre de usuario", fill="#000000", font=("Montserrat Regular", 15))
        self.canvas.create_text(520.0, 452.0, anchor="nw", text="Contraseña", fill="#000000", font=("Montserrat Regular", 15))
        
        
    
        #primera fila
        self.input_ID = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_ID.place(x=263.0, y=182.0, width=237.0, height=37.5)
        #se deberia agregar un campo de id?
        
        #segunda fila
        self.input_nombre = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_nombre.place(x=263.0, y=382.0, width=237.0, height=37.5)
        
        self.input_apellido = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_apellido.place(x=520.0, y=382.0, width=237.0, height=38.0)
        
        self.input_cedula = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.input_cedula.place(x=779.0, y=382.0, width=237.0, height=37.5)
        
        
        #tercera fila
        self.input_username = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
        self.input_username.place(x=263.0, y=482.0, width=237.0, height=37.5)
        
        self.input_password = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
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
        ).place(x=265.0, y=565.0, width=130.0, height=40.0)
        
      
        
        
        
class U_Eliminar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        validate_number = self.register(validate_number_input)
        self.images = {}

        # Formulario para el eliminar
        self.label_info = self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingrese la información del usuario a Eliminar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        
        # Texto para el nombre
        self.label_ID = self.canvas.create_text(263.0, 152.0, anchor="nw", text="ID", fill="#000000", font=("Montserrat Regular", 15))
        
        self.input_ID = tk.Entry(
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
        self.input_ID.place(x=263.0, y=182.0, width=237.0, height=38.0)
        #Y ESTO TAMBIEN!!!!!
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
            relief="flat"
        )
        self.button_e.place(x=265.0, y=264.0, width=130.0, height=40.0)
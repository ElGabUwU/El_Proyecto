import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from Library.librerias import recoger_sesion, drop_sesion
from backend.fun_db_users import *
from Vistas.listas import *
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
        self.cargo_combobox.place(x=263.0, y=281.5)
        
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
            
            print("cargo ", {cargo}, "nombre ", {nombre}, "apellido ", {apellido}, "cedula ", {cedula}, "username ", {username}, "password ", {password})
            print("\n")
            
            
            if campos_validacion(cargo,nombre,apellido,cedula,username,password) == True:
                return
            
            
            if create_user(cargo, nombre, apellido, cedula, username, password):
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
                    if delete_user(id):
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
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
from Library.librerias import *
from Books.backend.db_books import *
import random
import subprocess
from Books.backend.Libros_Frames_2 import *
from backend.Usuarios_Frames_3 import *
from backend.Prestamos_Frames_2 import *
import tkinter as tk



#relleno_menu


class Bienvenida(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.images = {}
        self.canvas.create_text(
                600.0,
                141.0,
                anchor="nw",
                text="Bienvenido",
                fill="#040F21",
                font=("Inter", 64 * -1)
            )
        self.images["bienvenida"] = tk.PhotoImage(file=relative_to_assets("logo-biblioteca-red-2.png"))
        self.images["bienvenida"]= self.images["bienvenida"].subsample(2, 2)
        self.canvas.create_image(760.0, 360.0, image=self.images["bienvenida"])
        

class Menu(tk.Frame):
    def __init__(self, parent, mostrar_frame,frame_header):
        super().__init__(parent)
        self.pack(side="left", fill="both", expand=True)
        self.frame_header=frame_header
        self.images = {}
        self.canvas = tk.Canvas(
            self,
            bg="#041022",
            height=768,
            width=217,  
            bd=1,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0) 
         
        #iconos
        
        imagen_salir = Image.open("assets_2/icono_libros.png")
        nueva_imagen = imagen_salir.resize((30, 30), Image.Resampling.LANCZOS)

        self.images["icono_libros"] = ImageTk.PhotoImage(nueva_imagen)
        
        imagen_salir = Image.open("assets_2/icono_usuarios.png")
        nueva_imagen = imagen_salir.resize((30, 30), Image.Resampling.LANCZOS)

        self.images["icono_usuarios"] = ImageTk.PhotoImage(nueva_imagen)
        
        imagen_salir = Image.open("assets_2/icono_prestamos.png")
        nueva_imagen = imagen_salir.resize((25, 25), Image.Resampling.LANCZOS)

        self.images["icono_prestamos"] = ImageTk.PhotoImage(nueva_imagen)
        
        imagen_salir = Image.open("assets_2/icono_perfil.png")
        nueva_imagen = imagen_salir.resize((30, 30), Image.Resampling.LANCZOS)

        self.images["icono_perfil"] = ImageTk.PhotoImage(nueva_imagen)
        
        imagen_salir = Image.open("assets_2/logo_salir.png")
        nueva_imagen = imagen_salir.resize((20, 20), Image.Resampling.LANCZOS)

        self.images["logo_salir"] = ImageTk.PhotoImage(nueva_imagen)
        
        
        
        # Crear el botón que abrirá el menú desplegable
        self.L_menu_button = tk.Button(self, text="Libros",image=self.images["icono_libros"],compound="left", bg="#041022", fg="#a6a6a6", font=("Inter", 21), relief="flat", command=lambda:self.show_menu(self.L_dropdown_menu,self.L_menu_button), anchor="w", padx=10)
        self.L_menu_button.place(x=0.0, y=0, width=213.0, height=58.0)
        
        self.U_menu_button = tk.Button(self, text="Usuarios",image=self.images["icono_usuarios"],compound="left", bg="#041022", fg="#a6a6a6", font=("Inter", 21), relief="flat", command=lambda:self.show_menu(self.U_dropdown_menu,self.U_menu_button), anchor="w", padx=10)
        self.U_menu_button.place(x=0.0, y=58.0, width=213.0, height=58.0)
        
        self.P_menu_button = tk.Button(self, text="Prestamos ▾",image=self.images["icono_prestamos"],compound="left", bg="#041022", fg="#a6a6a6", font=("Inter", 21), relief="flat", command=lambda:self.show_menu(self.P_dropdown_menu,self.P_menu_button), anchor="w", padx=10)
        self.P_menu_button.place(x=0.0, y=116.0, width=213.0, height=58.0)
        
        self.perfil_button = tk.Button(self, text="Mi Perfil",image=self.images["icono_perfil"],compound="left", bg="#041022", fg="#a6a6a6", font=("Inter", 21), relief="flat",anchor="w", padx=10, command=lambda:{mostrar_frame(app.frame_perfil), self.frame_header.update_header_text("Mi Perfil")})
        self.perfil_button.place(x=0.0, y=174.0, width=213.0, height=58.0)

        self.Salir = tk.Button(self, text="Cerrar Sesión", image=self.images["logo_salir"],compound="left", bg="#041022", fg="#a6a6a6", font=("Inter", 20), relief="flat", padx=10, command=lambda: self.salir())
        self.Salir.place(x=1.0, y=600.0, width=213.0, height=58.0)
        
        
        #tk.Button(self, text="Presionar", image=self.images["logo_salir"], compound="left")

        

        # Crear la imagen en el canvas
        #self.canvas.create_image(15.0, 610.0, image=self.images["logo_salir"], tags="logo_salir")

        # Asegurarse de que la imagen esté por encima del botón
        #self.canvas.tag_raise("logo_salir")
        #self.Salir.lift()
        #self.canvas.create_text(15.0, 590.0, anchor="nw", text="Cedula: V31242538", fill="White", font=("Montserrat Regular", 15))
        



        # menú desplegable de Libros
        self.L_dropdown_menu = tk.Menu(self, tearoff=0, bg="#041022", fg="#a6a6a6", font=("Inter", 20),
                                     activebackground="#2E59A7", activeforeground="#A6A6A6")
        self.L_dropdown_menu.add_command(
            label="Registrar",
            #command=lambda: {self.frame_header.update_header_text("Registrar"), mostrar_frame(app.L_frame_registrar)}
        )
        self.L_dropdown_menu.add_command(
            label="Listado",
            command=lambda: {self.frame_header.update_header_text("Listado"),mostrar_frame(app.L_frame_listar)}
        )
        self.L_dropdown_menu.add_command(
            label="Modificar",
            #command=lambda: {self.frame_header.update_header_text("Modificar"),mostrar_frame(app.L_frame_modificar)}
        )
        self.L_dropdown_menu.add_command(
            label="Eliminar",
            command=lambda: {self.frame_header.update_header_text("Eliminar"),mostrar_frame(app.L_frame_eliminar)}
        )
        
        # menú desplegable de Usuarios
        self.U_dropdown_menu = tk.Menu(self, tearoff=0, bg="#041022", fg="#a6a6a6", font=("Inter", 20),
                                     activebackground="#2E59A7", activeforeground="white")
        self.U_dropdown_menu.add_command(
            label="Registrar",
            command=lambda: {self.frame_header.update_header_text("Registrar"), mostrar_frame(app.U_frame_registrar)}
        )
        self.U_dropdown_menu.add_command(
            label="Listado",
            command=lambda: {self.frame_header.update_header_text("Listado"), mostrar_frame(app.U_frame_listar)}
        )
        self.U_dropdown_menu.add_command(
            label="Modificar",
            command=lambda: {self.frame_header.update_header_text("Modificar"),mostrar_frame(app.U_frame_modificar)}
        )
        self.U_dropdown_menu.add_command(
            label="Eliminar",
            command=lambda: {self.frame_header.update_header_text("Eliminar"),mostrar_frame(app.U_frame_eliminar)}
        )
        
        # menú desplegable de Prestamos
        
        self.P_dropdown_menu = tk.Menu(self, tearoff=0, bg="#041022", fg="#a6a6a6", font=("Inter", 20),activebackground="#2E59A7", activeforeground="white")
        self.P_dropdown_menu.add_command(
            label="Registrar",
            command=lambda: {self.frame_header.update_header_text("Registrar"), mostrar_frame(app.P_frame_registrar)}
        )
        self.P_dropdown_menu.add_command(
            label="Listado",
            command=lambda: {self.frame_header.update_header_text("Listado"), mostrar_frame(app.P_frame_listar)}
        )
        self.P_dropdown_menu.add_command(
            label="Modificar",
            command=lambda: {self.frame_header.update_header_text("Modificar"),mostrar_frame(app.P_frame_modificar)}
        )
        self.P_dropdown_menu.add_command(
            label="Eliminar",
            command=lambda: {self.frame_header.update_header_text("Eliminar"),mostrar_frame(app.P_frame_eliminar)}
        )


        # Ajustar el padding de los elementos del menú
        self.L_dropdown_menu.entryconfig("Registrar", font=("Helvetica", 20), accelerator=" ")
        self.U_dropdown_menu.entryconfig("Listado", font=("Helvetica", 20), accelerator=" "*1)
        self.P_dropdown_menu.entryconfig("Registrar", font=("Helvetica", 20), accelerator=" ")

    def show_menu(self,dropdown_menu,button):
        
        dropdown_menu.post(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())
    def salir(self):
        app.destroy()
        self.show_login()
    def show_login(self):
        import tkinter as tk
        from pathlib import Path
        import sys
        from tkinter import ttk, messagebox
        from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
        sys.path.append(str(Path(__file__).resolve().parent))
        from Login.backend.form_login import FormLogin
        from Login.frontend.form_master import MasterPanel
        from Login.frontend.from_login_designer import FormLoginDesigner
        import util.ventana as utl
        
        # Crear una instancia de MasterPanel y pasar el callback iniciar_starter
        master_panel = MasterPanel(on_close_callback=self.iniciar_login)
        
        app.after(1500, master_panel.on_close)  # Esperar 1500 milisegundos antes de iniciar Starter
        master_panel.show()
    def iniciar_login(self):
        from Login.backend.form_login import FormLogin, FormLoginDesigner
        from Login.frontend.form_master import MasterPanel
        
        app = FormLogin()
        
        
        
    
class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.var_text="Sistema de Inventario"
        self.images = {}
        self.canvas = tk.Canvas(self, bg="#2E59A7")
        self.canvas.pack(side="left", fill="both", expand= False)
        
        self.canvas.place(x=0.0, y=0.0, width=1366.0, height=60.0)
        self.images["logo_header"] = tk.PhotoImage(file=relative_to_assets("logo_header.png"))
        self.canvas.create_image(185.0, 26.0, image=self.images["logo_header"])
        
        
        #self.images["image_3"] = tk.PhotoImage(file=relative_to_assets("header.png"))
        #self.canvas.create_image(682.0, 29.0, image=self.images["image_3"])
        
        self.header_var_text=self.canvas.create_text(
            1250.0,
            12.0,
            anchor="ne",
            text="Sistema de Inventario",
            fill="#ffffff",
            font=("Inter", 25 * -1)
        )
        self.canvas.create_text(
            15.0,
            8.0,
            anchor="nw",
            text="Pedro Perez", #cuando el login este listo se nesita imprimir el nombre del usuario con algo asi como: self.usuario
            fill="#a6a6a6",
            font=("Inter", 22 * -1)
        )
        self.canvas.create_text(
            15.0,
            30.0,
            anchor="nw",
            text="admin", #cuando el login este listo se nesita imprimir el rol del usuario con algo asi como: self.rol_usuario
            fill="#a6a6a6",
            font=("Inter", 14 * -1)
        )
    def update_header_text(self, new_text):
        self.canvas.itemconfig(self.header_var_text, text=new_text)
        
# Definir la clase Perfil
class Perfil(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.images = {}
        
        # Titulos de los inputs
        self.canvas.create_text(263.0, 95.0, anchor="nw", text="Tu información", fill="#040F21", font=("Montserrat Medium", 24))
        
        # Sección de información de cuenta
        self.canvas.create_text(263.0, 166.0, anchor="nw", text="Información de la cuenta", fill="#042344", font=("Montserrat Regular", 18))
        
        self.username_text = self.canvas.create_text(263.0, 215.0, anchor="nw", text="Nombre de usuario:", fill="#a6a6a6", font=("Montserrat Regular", 15))
        self.password_text = self.canvas.create_text(263.0, 264.0, anchor="nw", text="Contraseña:", fill="#042344", font=("Montserrat Regular", 15))
        self.role_text = self.canvas.create_text(263.0, 313.0, anchor="nw", text="Rol:", fill="#042344", font=("Montserrat Regular", 15))
        
        # Sección de información del usuario
        self.canvas.create_text(263.0, 370.0, anchor="nw", text="Información del Usuario", fill="#040F21", font=("Montserrat Regular", 18))
        self.first_name_text = self.canvas.create_text(263.0, 418.0, anchor="nw", text="Nombres:", fill="#042344", font=("Montserrat Regular", 15))
        self.last_name_text = self.canvas.create_text(263.0, 467.0, anchor="nw", text="Apellidos:", fill="#042344", font=("Montserrat Regular", 15))
        self.position_text = self.canvas.create_text(263.0, 516.0, anchor="nw", text="Cargo:", fill="#042344", font=("Montserrat Regular", 15))
        self.id_text = self.canvas.create_text(263.0, 565.0, anchor="nw", text="Cédula:", fill="#042344", font=("Montserrat Regular", 15))
        
        self.update_user_info()

    def update_user_info(self):
        """Método para actualizar la información del usuario en el perfil"""
        usuario = app_state.usuario
        if usuario:
            self.canvas.itemconfig(self.username_text, text=f"Nombre de usuario: {usuario.nombre_usuario}")
            self.canvas.itemconfig(self.password_text, text=f"Contraseña: {usuario.clave}")
            self.canvas.itemconfig(self.role_text, text=f"Rol: {usuario.id_rol}")
            self.canvas.itemconfig(self.first_name_text, text=f"Nombres: {usuario.nombre}")
            self.canvas.itemconfig(self.last_name_text, text=f"Apellidos: {usuario.apellido}")
            self.canvas.itemconfig(self.position_text, text=f"Cargo: {usuario.id_cargo}")
            self.canvas.itemconfig(self.id_text, text=f"Cédula: {usuario.cedula}")
       

# Definir la clase AppState y crear una instancia global
class AppState:
    def __init__(self):
        self.usuario = None

    def iniciar_sesion(self,usuario):
        self.usuario = usuario

app_state = AppState()

# Definir la clase Usuario
class Usuario:
    def __init__(self, user_data):
        self.id_usuario = user_data[0]
        self.id_cargo = user_data[1]
        self.id_rol = user_data[2]
        self.nombre = user_data[3]
        self.apellido = user_data[4]
        self.cedula = user_data[5]
        self.nombre_usuario = user_data[6]
        self.clave = user_data[7]

    def mostrar_informacion(self):
        print(f"ID Usuario: {self.id_usuario}")
        print(f"ID Cargo: {self.id_cargo}")
        print(f"ID Rol: {self.id_rol}")
        print(f"Nombre: {self.nombre}")
        print(f"Apellido: {self.apellido}")
        print(f"Cédula: {self.cedula}")
        print(f"Nombre de Usuario: {self.nombre_usuario}")

class Starter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_state = app_state
        self.geometry("1366x768")
        self.title("Arcanum Library")
        self.iconbitmap(relative_to_assets('logo_biblioteca.ico'))  
        self.L_frame_eliminar = L_Eliminar(self)
        #self.L_frame_modificar = L_Modificar(self)
        self.L_frame_listar = L_Listar(self)
        #self.L_frame_registrar = L_Registrar(self)
        self.U_frame_eliminar = U_Eliminar(self)
        self.U_frame_modificar = U_Modificar(self)
        self.U_frame_listar = U_Listar(self)
        self.U_frame_registrar = U_Registrar(self)
        self.P_frame_eliminar = P_Eliminar(self)
        self.P_frame_modificar = P_Modificar(self)
        self.P_frame_listar = P_Listar(self)
        self.P_frame_registrar = P_Registrar(self)
        self.frame_perfil = Perfil(self)

        self.frame_bienvenida = Bienvenida(self)
        self.frame_bienvenida.place(x=0, y=0)

        self.frame_header = Header(self)
        self.frame_header.place(x=0, y=0, width=1366, height=54)

        self.frame_menu = Menu(self, lambda frame: self.mostrar_frame(frame), self.frame_header)
        self.frame_menu.place(x=0, y=53, width=215, height=714)
    
    def mostrar_frame(self, frame):
        frames = [
            self.frame_bienvenida, self.L_frame_listar, 
            self.L_frame_eliminar, self.U_frame_eliminar, self.U_frame_modificar, self.U_frame_listar,
            self.U_frame_registrar, self.P_frame_eliminar, self.P_frame_modificar, self.P_frame_listar,
            self.P_frame_registrar, self.frame_perfil
        ]
        
        for f in frames:
            f.place_forget()# De esta forma se ocultan todos los frames antes de mostrar el frame deseado
        
        frame.place(x=0, y=0)# Hace que el frame sea visible
        #De esta forma se deja siempre visible tanto el header como el menu
        self.frame_menu.lift()
        self.frame_header.lift()

    def show(self):
        self.mainloop()

def start_starter():
    global app# De esta forma permite que se pueda acceder a la instancia Starter
    app = Starter()
    app.mainloop()



if __name__ == "__main__":
    start_starter()

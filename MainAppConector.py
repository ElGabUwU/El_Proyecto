import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
from Library.librerias import *
from Books.backend.db_books import *
import random
from Books.backend.books_management import *
from users.backend.user_management import *
from loans.backend.loans_management import *
from clients.backend.clients_management import *
import tkinter as tk



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
        self.parent = parent
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
        
        """def mostrar_nombre_usuario(self):
            global U_nombre  # Declarar que usaremos la variable global
            if U_nombre:
                print(f"Nombre de Usuario: {U_nombre}")
            else:
                print("No hay nombre de usuario disponible")
        mostrar_nombre_usuario(self)"""
        
        # Crear el botón que abrirá el menú desplegable
        
        
        self.L_menu_button = tk.Button(self, text="Libros",image=self.images["icono_libros"],compound="left", bg="#041022", fg="#a6a6a6", font=("Inter", 21), relief="flat", command=lambda:{self.frame_header.update_header_text("Libros"),mostrar_frame(app.L_frame_listar)}, anchor="w", padx=10)
        self.L_menu_button.place(x=0.0, y=0, width=213.0, height=58.0)
        self.L_menu_button.bind("<Enter>", lambda event: self.on_enter(self.L_menu_button))
        self.L_menu_button.bind("<Leave>", lambda event: self.on_leave(self.L_menu_button))
        
        self.Salir = tk.Button(self, text="Cerrar Sesión", image=self.images["logo_salir"],compound="left", bg="#041022", fg="#a6a6a6", font=("Inter", 20), relief="flat", padx=10, command=lambda: self.salir())
        self.Salir.place(x=1.0, y=600.0, width=213.0, height=58.0)
        self.Salir.bind("<Enter>", lambda event: self.on_enter(self.Salir))
        self.Salir.bind("<Leave>", lambda event: self.on_leave(self.Salir))
        
        self.U_menu_button = tk.Button(self, text="Usuarios",image=self.images["icono_usuarios"],compound="left", bg="#041022", fg="#a6a6a6", font=("Inter", 21), relief="flat", command=lambda:{self.frame_header.update_header_text("Usuarios"), mostrar_frame(app.U_frame_listar)}, anchor="w", padx=10)
        self.U_menu_button.bind("<Enter>", lambda event: self.on_enter(self.U_menu_button))
        self.U_menu_button.bind("<Leave>", lambda event: self.on_leave(self.U_menu_button))
        
        self.P_menu_button = tk.Button(self, text="Prestamos ▾",image=self.images["icono_prestamos"],compound="left", bg="#041022", fg="#a6a6a6", font=("Inter", 21), relief="flat", command=lambda:self.show_menu(self.P_dropdown_menu,self.P_menu_button), anchor="w", padx=10)
        self.P_menu_button.bind("<Enter>", lambda event: self.on_enter(self.P_menu_button))
        self.P_menu_button.bind("<Leave>", lambda event: self.on_leave(self.P_menu_button))
        
        self.perfil_button = tk.Button(self, text="Mi Perfil",image=self.images["icono_perfil"],compound="left", bg="#041022", fg="#a6a6a6", font=("Inter", 21), relief="flat",anchor="w", padx=10, command=lambda:{mostrar_frame(app.frame_perfil), self.frame_header.update_header_text("Mi Perfil")})
        self.perfil_button.bind("<Enter>", lambda event: self.on_enter(self.perfil_button))
        self.perfil_button.bind("<Leave>", lambda event: self.on_leave(self.perfil_button))
        
        
        # Crear el botón que abrirá el menú desplegable
        if self.parent.id_rol == 1:
            self.P_menu_button.place(x=0.0, y=58.0, width=213.0, height=58.0)
            
            self.perfil_button.place(x=0.0, y=116.0, width=213.0, height=58.0)
            
        else: 
            self.U_menu_button.place(x=0.0, y=58.0, width=213.0, height=58.0)
            
            self.P_menu_button.place(x=0.0, y=116.0, width=213.0, height=58.0)
            
            self.perfil_button.place(x=0.0, y=174.0, width=213.0, height=58.0)
        
        
        #tk.Button(self, text="Presionar", image=self.images["logo_salir"], compound="left")

        


        # menú desplegable de Prestamos
        
        self.P_dropdown_menu = tk.Menu(self, tearoff=0, bg="#041022", fg="#a6a6a6", font=("Inter", 20),activebackground="#2E59A7", activeforeground="white")
        self.P_dropdown_menu.add_command(
            label="Clientes",
            command=lambda: {self.frame_header.update_header_text("Prestamos-Clientes"), mostrar_frame(app.P_frame_registrar)}
        )
        self.P_dropdown_menu.add_command(
            label="Libros",
            command=lambda: {self.frame_header.update_header_text("Prestamos-Libros"), mostrar_frame(app.P_frame_listar)}
        )
        
        

        # Ajustar el padding de los elementos del menú
        self.P_dropdown_menu.entryconfig("Clientes", font=("Helvetica", 20), accelerator=" "*6)

    def on_enter(self, button):
        button['background'] = "#2E59A7"

    def on_leave(self, button):
        button['background'] = '#041022'
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
        from users.backend.form_login import FormLogin
        from users.frontend.form_master import MasterPanel
        from users.frontend.from_login_designer import FormLoginDesigner
        import util.ventana as utl
        
        # Crear una instancia de MasterPanel y pasar el callback iniciar_starter
        master_panel = MasterPanel(on_close_callback=self.iniciar_login)
        
        app.after(1500, master_panel.on_close)  # Esperar 1500 milisegundos antes de iniciar Starter
        master_panel.show()
    def iniciar_login(self):
        from users.backend.form_login import FormLogin, FormLoginDesigner
        from users.frontend.form_master import MasterPanel
        
        app = FormLogin()
        
        
        
    
class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.var_text="Sistema de Inventario"
        self.parent = parent
        self.images = {}
        self.canvas = tk.Canvas(self, bg="#2E59A7")
        self.canvas.pack(side="left", fill="both", expand= False)
        
        self.canvas.place(x=0.0, y=0.0, width=1366.0, height=60.0)
        self.images["logo_header"] = tk.PhotoImage(file=relative_to_assets("logo_header.png"))
        self.canvas.create_image(185.0, 26.0, image=self.images["logo_header"])
        
        
        #self.images["image_3"] = tk.PhotoImage(file=relative_to_assets("header.png"))
        #self.canvas.create_image(682.0, 29.0, image=self.images["image_3"])
        
        if self.parent.id_rol == 1:
            self.rol="Admin"
        else:
            self.rol="Super Admin"
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
            text=self.parent.U_nombre, #cuando el login este listo se nesita imprimir el nombre del usuario con algo asi como: self.usuario
            fill="#a6a6a6", 
            font=("Inter", 22 * -1)
        )
        self.canvas.create_text(
            15.0,
            30.0,
            anchor="nw",
            text=self.rol, #cuando el login este listo se nesita imprimir el rol del usuario con algo asi como: self.rol_usuario
            fill="#a6a6a6",
            font=("Inter", 14 * -1)
        )
    def update_header_text(self, new_text):
        self.canvas.itemconfig(self.header_var_text, text=new_text)
        
class Perfil(tk.Frame):        
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        #validate_number = self.register(validate_number_input)
        self.parent = parent
        self.images = {}
        
        if self.parent.id_rol == 1:
            self.rol="Admin"
        else:
            self.rol="Super Admin"
            
        if self.parent.id_cargo == 1:
            self.cargo="Encargado de Servicio"
        else:
            self.cargo="Asistente Bibliotecario"
        
        # Titulos de los inputs #310 x
        self.canvas.create_text(263.0, 95.0, anchor="nw", text="Tu información", fill="#040F21", font=("Montserrat Medium", 24))
        
        #seccion de informacion de cuenta
        self.canvas.create_text(263.0, 166.0, anchor="nw", text="Información de la cuenta", fill="#042344", font=("Montserrat Regular", 18))
        


        self.canvas.create_text(263.0, 215.0, anchor="nw", text=f"Nombre de usuario: {self.parent.U_nombre}", fill="#042344", font=("Montserrat Regular", 15))

        
        self.canvas.create_text(263.0, 264.0, anchor="nw", text="Contraseña: ******", fill="#042344", font=("Montserrat Regular", 15))

        self.canvas.create_text(263.0, 313.0, anchor="nw", text=f"Rol: {self.rol}", fill="#042344", font=("Montserrat Regular", 15))
        
        #seccion de informacion del usuario
        self.canvas.create_text(263.0, 370.0, anchor="nw", text="Información del Usuario", fill="#040F21", font=("Montserrat Regular", 18))
        
        self.canvas.create_text(263.0, 418.0, anchor="nw", text=f"Nombres: {self.parent.nombre}", fill="#042344", font=("Montserrat Regular", 15))
        
        self.canvas.create_text(263.0, 467.0, anchor="nw", text=f"Apellidos: {self.parent.apellido}", fill="#042344", font=("Montserrat Regular", 15))

        self.canvas.create_text(263.0, 516.0, anchor="nw", text=f"Cargo: {self.cargo}", fill="#042344", font=("Montserrat Regular", 15))
        
        self.canvas.create_text(263.0, 565.0, anchor="nw", text=f"Cedula: {self.parent.cedula}", fill="#042344", font=("Montserrat Regular", 15))

        """self.parent.U_nombre
        self.parent.id_usuario
        self.parent.id_cargo
        self.parent.id_rol
        self.parent.nombre
        self.parent.apellido
        self.parent.cedula"""



class Starter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.title("Arcanum Library")
        self.iconbitmap(relative_to_assets('logo_biblioteca.ico')) 
        self.U_nombre = self.id_usuario = self.id_cargo = self.id_rol = self.nombre = self.apellido = self.cedula = None
        self.agarrar_datos()
        print("funciono?")
        print(self.U_nombre)
        #self.L_frame_eliminar = L_Eliminar(self)
        #self.L_frame_modificar = L_Modificar(self)
        self.L_frame_listar = L_Listar(self)
        #self.L_frame_registrar = L_Registrar(self)
        #self.U_frame_eliminar = U_Eliminar(self)
        #self.U_frame_modificar = U_Modificar()
        self.U_frame_listar = U_Listar(self)
        #self.U_frame_registrar = U_Registrar(self)
#        self.P_frame_eliminar = P_Eliminar(self)
        #self.P_frame_modificar = Pdificar(self)
        self.P_frame_listar = P_Listar(self)
        self.P_frame_registrar = C_Listar(self)#CLIENTES
        self.frame_perfil = Perfil(self)

        self.frame_bienvenida = Bienvenida(self)
        self.frame_bienvenida.place(x=0, y=0)

        self.frame_header = Header(self)
        self.frame_header.place(x=0, y=0, width=1366, height=54)

        self.frame_menu = Menu(self, lambda frame: self.mostrar_frame(frame), self.frame_header)
        self.frame_menu.place(x=0, y=53, width=215, height=714)
        
        #if usuario_actual:
        
        #self.id_usuario = usuario_actual.id_usuario if usuario_actual else None
        #print(self.id_usuario)
            
        """id_cargo=usuario_actual.id_cargo
        id_rol=usuario_actual.id_rol
        nombre=usuario_actual.nombre
        apellido=usuario_actual.apellido
        cedula=usuario_actual.cedula
        nombre_usuario=usuario_actual.nombre_usuario
        print("dato recivido")
        print(id_usuario)
    else:
        print("error")"""
        
        
    def agarrar_datos(self):
        from users.backend.db_users import Usuario,usuario_actual
        if usuario_actual:
            print("usuario logueado!!!!!")
            print(f"ID Usuario: {usuario_actual.id_usuario}")
            print(f"ID Cargo: {usuario_actual.id_cargo}")
            print(f"ID Rol: {usuario_actual.id_rol}")
            print(f"Nombre: {usuario_actual.nombre}")
            print(f"Apellido: {usuario_actual.apellido}")
            print(f"Cédula: {usuario_actual.cedula}")
            print(f"Nombre de Usuario: {usuario_actual.nombre_usuario}")
            #global id_usuario,id_cargo,id_rol,nombre,apellido,cedula,U_nombre
            self.U_nombre=usuario_actual.nombre_usuario
            self.id_usuario=usuario_actual.id_usuario
            self.id_cargo=usuario_actual.id_cargo
            self.id_rol=usuario_actual.id_rol
            self.nombre=usuario_actual.nombre
            self.apellido=usuario_actual.apellido
            self.cedula=usuario_actual.cedula
            print(self.U_nombre)
        else:
            print("No hay usuario logueado")
    
        
    
    
        
    def mostrar_frame(self, frame):
        frames = [
            self.frame_bienvenida, self.L_frame_listar, 
            self.U_frame_listar,
            self.P_frame_listar, 
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


#hola
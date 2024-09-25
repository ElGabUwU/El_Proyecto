import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from Library.librerias import *
from Library.db_pokimon import *
import random
import subprocess
from backend.Libros_Frames_2 import *
from backend.Usuarios_Frames_3 import *
from backend.Prestamos_Frames_2 import *

#relleno_menu

class Bienvenida(tk.Frame):
    def __init__(self, parent): 
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#031A33", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.images = {}
        self.canvas.create_text(
                600.0,
                141.0,
                anchor="nw",
                text="Bienvenido",
                fill="#A6A6A6",
                font=("Inter", 64 * -1)
            )
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
        #relleno menu
        
        
        
        # Crear el botón que abrirá el menú desplegable
        self.L_menu_button = tk.Button(self, text="Libros          ▾", bg="#041022", fg="#a6a6a6", font=("Inter", 22), relief="flat", command=lambda:self.show_menu(self.L_dropdown_menu,self.L_menu_button), anchor="w", padx=10)
        self.L_menu_button.place(x=1.0, y=0, width=213.0, height=58.0)
        
        self.U_menu_button = tk.Button(self, text="Usuarios     ▾", bg="#041022", fg="#a6a6a6", font=("Inter", 22), relief="flat", command=lambda:self.show_menu(self.U_dropdown_menu,self.U_menu_button), anchor="w", padx=10)
        self.U_menu_button.place(x=1.0, y=58.0, width=213.0, height=58.0)
        
        self.P_menu_button = tk.Button(self, text="Prestamos  ▾", bg="#041022", fg="#a6a6a6", font=("Inter", 22), relief="flat", command=lambda:self.show_menu(self.P_dropdown_menu,self.P_menu_button), anchor="w", padx=10)
        self.P_menu_button.place(x=1.0, y=116.0, width=213.0, height=58.0)
        
        self.perfil_button = tk.Button(self, text="Mi Perfil", bg="#041022", fg="#a6a6a6", font=("Inter", 22), relief="flat",anchor="w", padx=10, command=lambda:{mostrar_frame(app.frame_perfil), self.frame_header.update_header_text("Mi Perfil")})
        self.perfil_button.place(x=1.0, y=174.0, width=213.0, height=58.0)

        # menú desplegable de Libros
        self.L_dropdown_menu = tk.Menu(self, tearoff=0, bg="#041022", fg="#a6a6a6", font=("Inter", 20),
                                     activebackground="#2E59A7", activeforeground="#A6A6A6")
        self.L_dropdown_menu.add_command(
            label="Registrar",
            command=lambda: {self.frame_header.update_header_text("Registrar"), mostrar_frame(app.L_frame_registrar)}
        )
        self.L_dropdown_menu.add_command(
            label="Listado",
            command=lambda: {self.frame_header.update_header_text("Listado"),mostrar_frame(app.L_frame_listar)}
        )
        self.L_dropdown_menu.add_command(
            label="Modificar",
            command=lambda: {self.frame_header.update_header_text("Modificar"),mostrar_frame(app.L_frame_modificar)}
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
    
class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.var_text="Sistema de Inventario"
        self.images = {}
        self.canvas = tk.Canvas(self, bg="#2E59A7")
        self.canvas.pack(side="left", fill="both", expand= False)
        
        self.canvas.place(x=0.0, y=0.0, width=1366.0, height=54.0)
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
        
class Perfil(tk.Frame):        
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="#042344", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        #validate_number = self.register(validate_number_input)
        self.images = {}
        
        # Titulos de los inputs #310 x
        self.canvas.create_text(263.0, 95.0, anchor="nw", text="Tu información", fill="#ffffff", font=("Montserrat Medium", 24))
        
        #seccion de informacion de cuenta
        self.canvas.create_text(263.0, 166.0, anchor="nw", text="Información de la cuenta", fill="#a6a6a6", font=("Montserrat Regular", 18))
        
        self.canvas.create_text(263.0, 215.0, anchor="nw", text="Nombre de usuario: El Gabo", fill="#a6a6a6", font=("Montserrat Regular", 15))
        
        self.canvas.create_text(263.0, 264.0, anchor="nw", text="Contraseña: 1234", fill="#a6a6a6", font=("Montserrat Regular", 15))

        self.canvas.create_text(263.0, 313.0, anchor="nw", text="Rol: Admin", fill="#a6a6a6", font=("Montserrat Regular", 15))
        
        #seccion de informacion del usuario
        self.canvas.create_text(263.0, 370.0, anchor="nw", text="Información del Usuario", fill="white", font=("Montserrat Regular", 18))
        
        self.canvas.create_text(263.0, 418.0, anchor="nw", text="Nombres: Pineda Benitez", fill="#a6a6a6", font=("Montserrat Regular", 15))
        
        self.canvas.create_text(263.0, 467.0, anchor="nw", text="Apellidos: Gabriel Ernesto", fill="#a6a6a6", font=("Montserrat Regular", 15))

        self.canvas.create_text(263.0, 516.0, anchor="nw", text="Cargo: Administrador", fill="#a6a6a6", font=("Montserrat Regular", 15))
        
        self.canvas.create_text(263.0, 565.0, anchor="nw", text="Cedula: V31242538", fill="#a6a6a6", font=("Montserrat Regular", 15))

#los place_forget se podrian optimizar

# def mostrar_frame(frame):
#     app.frame_bienvenida.place_forget()
#     app.L_frame_modificar.place_forget()
#     app.L_frame_listar.place_forget()
#     app.L_frame_registrar.place_forget()
#     app.L_frame_eliminar.place_forget()
#     app.U_frame_eliminar.place_forget()
#     app.U_frame_modificar.place_forget()
#     app.U_frame_listar.place_forget()
#     app.U_frame_registrar.place_forget()
#     app.P_frame_eliminar.place_forget()
#     app.P_frame_modificar.place_forget()
#     app.P_frame_listar.place_forget()
#     #app.P_frame_registrar2.place_forget()
#     app.P_frame_registrar.place_forget()
#     app.frame_perfil.place_forget()
#     frame.place(x=0, y=0)
#     app.frame_menu.lift()
#     app.frame_header.lift()

# class Starter(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("1366x768")
#         self.title("Arcanum Library")
#         self.iconbitmap(relative_to_assets('logo_biblioteca.ico')) #aqui iria el icono de la app
#         self.L_frame_eliminar = L_Eliminar(self)
#         self.L_frame_modificar = L_Modificar(self)
#         self.L_frame_listar = L_Listar(self)
#         self.L_frame_registrar = L_Registrar(self)
#         self.U_frame_eliminar = U_Eliminar(self)
#         self.U_frame_modificar = U_Modificar(self)
#         self.U_frame_listar = U_Listar(self)
#         self.U_frame_registrar = U_Registrar(self)
#         #self.P_frame_registrar2= P_Registrar2(self)
#         self.P_frame_eliminar = P_Eliminar(self)
#         self.P_frame_modificar = P_Modificar(self)
#         self.P_frame_listar = P_Listar(self)
#         self.P_frame_registrar = P_Registrar(self)
#         self.frame_perfil = Perfil(self)

#         self.frame_bienvenida = Bienvenida(self)
#         self.frame_bienvenida.place(x=0, y=0)

#         self.frame_header = Header(self)
#         self.frame_header.place(x=0, y=0, width=1366, height=54)

#         self.frame_menu = Menu(self, mostrar_frame, self.frame_header)
#         self.frame_menu.place(x=0, y=53, width=215, height=714)
    
#     def show(self):
#         self.mainloop()





import tkinter as tk

class Starter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.title("Arcanum Library")
        self.iconbitmap(relative_to_assets('logo_biblioteca.ico'))  
        self.L_frame_eliminar = L_Eliminar(self)
        self.L_frame_modificar = L_Modificar(self)
        self.L_frame_listar = L_Listar(self)
        self.L_frame_registrar = L_Registrar(self)
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
            self.frame_bienvenida, self.L_frame_modificar, self.L_frame_listar, self.L_frame_registrar,
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

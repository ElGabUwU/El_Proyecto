import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from Library.librerias import recoger_sesion, drop_sesion
from Library.db_pokimon import  create_pokemon,delete_pokemon,update_pokemon
from Vistas.listas import *
import random

from Libros_Frames import *
from Usuarios_Frames import *
from Prestamos_Frames import *

#relleno_menu


def relative_to_assets(path: str) -> str:
    return f"./assets_2/{path}"

class Bienvenida(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white", width=1366, height=768)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.images = {}
        self.canvas.create_text(
                600.0,
                141.0,
                anchor="nw",
                text="Bienvenido",
                fill="#191919",
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
            bg="#FFFFFF",
            height=768,
            width=215,  
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)  
        #relleno menu
        
        self.images["relleno_menu"] = tk.PhotoImage(file=relative_to_assets("relleno_menu.png"))
        self.canvas.create_image(107.0, 400.0, image=self.images["relleno_menu"])
        
        # Crear el botón que abrirá el menú desplegable
        self.L_menu_button = tk.Button(self, text="Libros ▼", bg="#75C99A", fg="#333333", font=("Inter", 24), relief="raised", command=lambda:self.show_menu(self.L_dropdown_menu,self.L_menu_button), anchor="w", padx=10)
        self.L_menu_button.place(x=1.0, y=0, width=213.0, height=58.0)
        
        self.U_menu_button = tk.Button(self, text="Usuarios ▼", bg="#75C99A", fg="#333333", font=("Inter", 24), relief="raised", command=lambda:self.show_menu(self.U_dropdown_menu,self.U_menu_button), anchor="w", padx=10)
        self.U_menu_button.place(x=1.0, y=58.0, width=213.0, height=58.0)
        
        self.P_menu_button=tk.Button(self, text="Prestamos ▼", bg="#75C99A", fg="#333333", font=("Inter", 24), relief="raised", command=lambda:self.show_menu(self.P_dropdown_menu,self.P_menu_button), anchor="w", padx=10)
        self.P_menu_button.place(x=1.0, y=116.0, width=213.0, height=58.0)

        # menú desplegable de Libros
        self.L_dropdown_menu = tk.Menu(self, tearoff=0, bg="#7CE98D", fg="#333333", font=("Inter", 24),
                                     activebackground="blue", activeforeground="white")
        self.L_dropdown_menu.add_command(
            label="Registrar",
            command=lambda: {self.frame_header.update_header_text("Registrar"), mostrar_frame(app.L_frame_registrar)}
        )
        self.L_dropdown_menu.add_command(
            label="Listado",
            command=lambda: self.frame_header.update_header_text("Listado")
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
        self.U_dropdown_menu = tk.Menu(self, tearoff=0, bg="#7CE98D", fg="#333333", font=("Inter", 24),
                                     activebackground="blue", activeforeground="white")
        self.U_dropdown_menu.add_command(
            label="Registrar",
            command=lambda: {self.frame_header.update_header_text("Registrar"), mostrar_frame(app.U_frame_registrar)}
        )
        self.U_dropdown_menu.add_command(
            label="Listado",
            command=lambda: self.frame_header.update_header_text("Listado")
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
        
        self.P_dropdown_menu = tk.Menu(self, tearoff=0, bg="#7CE98D", fg="#333333", font=("Inter", 24),
                                     activebackground="blue", activeforeground="white")
        self.P_dropdown_menu.add_command(
            label="Registrar",
            command=lambda: {self.frame_header.update_header_text("Registrar"), mostrar_frame(app.P_frame_registrar)}
        )
        self.P_dropdown_menu.add_command(
            label="Listado",
            command=lambda: self.frame_header.update_header_text("Listado")
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
        self.L_dropdown_menu.entryconfig("Registrar", font=("Helvetica", 24), accelerator=" ")
        self.U_dropdown_menu.entryconfig("Listado", font=("Helvetica", 24), accelerator=" "*1)
        self.P_dropdown_menu.entryconfig("Registrar", font=("Helvetica", 24), accelerator=" ")

    def show_menu(self,dropdown_menu,button):
        
        dropdown_menu.post(button.winfo_rootx(), button.winfo_rooty() + button.winfo_height())
        
        
    

        
        
    
class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.var_text="Sistema de Inventario"
        self.images = {}
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(side="left", fill="both", expand=False)
        
        self.canvas.place(x=1.0, y=0.0, width=1366.0, height=54.0)
        self.images["image_3"] = tk.PhotoImage(file=relative_to_assets("header.png"))
        self.canvas.create_image(682.0, 29.0, image=self.images["image_3"])
        
        self.header_var_text=self.canvas.create_text(
            226.0,
            5.0,
            anchor="nw",
            text="Sistema de Inventario",
            fill="#000000",
            font=("Inter", 40 * -1)
        )
        self.canvas.create_text(
            26.0,
            9.0,
            anchor="nw",
            text="pepe", #cuando el login este listo se nesita imprimir el nombre del usuario con algo asi como: self.usuario
            fill="#000000",
            font=("Inter", 18 * -1)
        )
        self.canvas.create_text(
            26.0,
            31.0,
            anchor="nw",
            text="admistrador", #cuando el login este listo se nesita imprimir el rol del usuario con algo asi como: self.rol_usuario
            fill="#000000",
            font=("Inter", 14 * -1)
        )
    def update_header_text(self, new_text):
        self.canvas.itemconfig(self.header_var_text, text=new_text)
        
#los place_forget se podrian optimizar        
import tkinter as tk

def mostrar_frame(frame):
    app.frame_bienvenida.place_forget()
    app.L_frame_modificar.place_forget()
    app.L_frame_registrar.place_forget()
    app.L_frame_eliminar.place_forget()
    app.U_frame_eliminar.place_forget()
    app.U_frame_modificar.place_forget()
    app.U_frame_registrar.place_forget()
    app.P_frame_eliminar.place_forget()
    app.P_frame_modificar.place_forget()
    app.P_frame_registrar.place_forget()
    frame.place(x=0, y=0)
    app.frame_menu.lift()
    app.frame_header.lift()

class Starter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.title("Arcanum Library")
        #self.iconbitmap(relative_to_assets('PokeBall.ico')) aqui iria el icono de la app
        self.L_frame_eliminar = L_Eliminar(self)
        self.L_frame_modificar = L_Modificar(self)
        self.L_frame_registrar = L_Registrar(self)
        self.U_frame_eliminar = U_Eliminar(self)
        self.U_frame_modificar = U_Modificar(self)
        self.U_frame_registrar = U_Registrar(self)
        self.P_frame_eliminar = P_Eliminar(self)
        self.P_frame_modificar = P_Modificar(self)
        self.P_frame_registrar = P_Registrar(self)

        self.frame_bienvenida = Bienvenida(self)
        self.frame_bienvenida.place(x=0, y=0)

        self.frame_header = Header(self)
        self.frame_header.place(x=0, y=0, width=1366, height=54)

        self.frame_menu = Menu(self, mostrar_frame, self.frame_header)
        self.frame_menu.place(x=0, y=54, width=215, height=714)

if __name__ == "__main__":
    app = Starter()
    app.mainloop()



#cambiar nombres variables, faltan algunos combobox

#menu mi perfil
#adaptar el codigo de henry
#agregar las opciones correctas al combobox de cargo en los frames de usuarios
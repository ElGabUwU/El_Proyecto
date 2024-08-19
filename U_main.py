# from pathlib import Path
# import tkinter as tk
# from tkinter import ttk
# from tkinter import Tk, Canvas, Button, PhotoImage,messagebox
# from Vistas.users_lista import show_users
# from Library.librerias import update_users,delete_users

# # Rutas relativas para las imagenes
# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"C:\El_Proyecto\assets")

# def relative_to_assets(path: str) -> Path:
#     return ASSETS_PATH / Path(path)

# # Clase principal de la aplicación
# class Users(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Pokedex")
#         self.geometry("1366x768")
#         self.resizable(False, False)  # No permitir cambiar el tamaño de la ventana
#         self.container = tk.Frame(self)
#         self.iconbitmap(relative_to_assets('PokeBall.ico'))
#         self.container.pack(fill="both", expand=True)
#         self.current_frame = None
#         self.show_frame(SecondaryPage)

#     def show_frame(self, page_class):
#         if self.current_frame is not None:
#             self.current_frame.pack_forget()
#         self.current_frame = page_class(self.container, self)
#         self.current_frame.pack(fill="both", expand=True)

#     def open(self):
#         self.mainloop()

# class SecondaryPage(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         main_page = M_Usuarios(self, controller)
#         main_page.pack(fill="both", expand=True)

# class M_Usuarios(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.config(bg="#FFFFFF")
#         self.create_widgets()

#     def create_widgets(self):
#         self.images = {}
#         canvas = tk.Canvas(
#             self,
#             bg="#FFFFFF",
#             height=768,
#             width=1366,
#             bd=0,
#             highlightthickness=0,
#             relief="ridge"
#         )
#         canvas.place(x=0, y=0)
#         self.image_image_1 = PhotoImage(
#             file=relative_to_assets("U_relleno_vertical.png"))
#         canvas.create_image(
#             107.0,
#             412.0,
#             image=self.image_image_1
#         )

#         self.image_image_2 = PhotoImage(
#             file=relative_to_assets("U_relleno_general.png"))
#         canvas.create_image(
#             789.0,
#             413.0,
#             image=self.image_image_2
#         )

#         self.image_image_3 = PhotoImage(
#             file=relative_to_assets("U_barra.png"))
#         canvas.create_image(
#             682.0,
#             29.0,
#             image=self.image_image_3
#         )
        
#         # Texto del navbar
#         canvas.create_text(
#             26.0,
#             9.0,
#             anchor="nw",
#             text="Cesar Maldonado",
#             fill="#000000",
#             font=("Inter", 18 * -1)
#         )

#         # Texto del navbar
#         canvas.create_text(
#             26.0,
#             31.0,
#             anchor="nw",
#             text="Admin",
#             fill="#000000",
#             font=("Inter", 14 * -1)
#         )
        
#         # Texto del navbar
#         canvas.create_text(
#             600.0,
#             141.0,
#             anchor="nw",
#             text="Bienvenido",
#             fill="#191919",
#             font=("Inter", 64 * -1)
#         )
        
#         # Texto del navbar
#         canvas.create_text(
#             226.0,
#             5.0,
#             anchor="nw",
#             text="Gestion de Usuarios",
#             fill="#000000",
#             font=("Inter", 40 * -1)
#         )

#         # Boton para regresar a la seleccion
#         self.images["button_volver"] = tk.PhotoImage(file=relative_to_assets("U_volver.png"))
#         tk.Button(
#             image=self.images["button_volver"],
#             borderwidth=0,
#             highlightthickness=0,
#             relief="raised",
#             bg="#6D6CFA",
#             activebackground="#6D6CFA",
#             command=lambda: self.open_seleccion(),

#         ).place(x=1135.0, y=15.0, width=208.0, height=29.0)
        
#         # Boton listar para ver a los usuarios
#         self.images["button_listado"] = tk.PhotoImage(file=relative_to_assets("U_listado.png"))
#         tk.Button(
#             self,
#             image=self.images["button_listado"],
#             borderwidth=0,
#             highlightthickness=0,
#             relief="flat",
#             command=show_users
#         ).place(x=1.0, y=57.0, width=213.0, height=58.0)
        
#         # Boton para modicar el usuario
#         self.images["button_modificar"] = tk.PhotoImage(file=relative_to_assets("U_modificar.png"))
#         tk.Button(
#             self,
#             image=self.images["button_modificar"],
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: self.controller.show_frame(Modificar),
#             relief="flat"
#         ).place(x=1.0,y=115.0,width=213.0,height=58.0)
        
#         # Boton para enviar a la accion de eliminar al usuario
#         self.images["button_eliminar"] = tk.PhotoImage(file=relative_to_assets("U_eliminar.png"))
#         tk.Button(
#             self,
#             image=self.images["button_eliminar"],
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: self.controller.show_frame(Eliminar),
#             relief="flat"
#         ).place(x=1.0, y=173.0, width=213.0, height=58.0)
#     def open_seleccion(self):
#         self.controller.destroy()  ##### Cierra solo la ventana  actual
#         from Vistas.R_selection import selection
#         selection().open() 

# #Clase para el Eliminar
# class Eliminar(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.config(bg="#FFFFFF")
#         self.create_widgets()

#     def create_widgets(self):
#         self.images = {}
#         self.canvas = tk.Canvas(
#             self,
#             bg="#FFFFFF",
#             height=768,
#             width=1366,
#             bd=0,
#             highlightthickness=0,
#             relief="ridge"
#         )
#         self.canvas.place(x=0, y=0)
        
#         #Imagenes generales para el relleno
#         self.image_image_1 = PhotoImage(
#             file=relative_to_assets("U_relleno_vertical.png"))
#         self.canvas.create_image(
#             107.0,
#             412.0,
#             image=self.image_image_1
#         )

#         self.image_image_2 = PhotoImage(
#             file=relative_to_assets("U_relleno_general.png"))
#         self.canvas.create_image(
#             789.0,
#             413.0,
#             image=self.image_image_2
#         )

#         self.image_image_3 = PhotoImage(
#             file=relative_to_assets("U_barra.png"))
#         self.canvas.create_image(
#             682.0,
#             29.0,
#             image=self.image_image_3
#         )
#         #----------------------------------------------------
#         # Texto del navbar
#         self.navbar_title = self.canvas.create_text(
#             26.0,
#             9.0,
#             anchor="nw",
#             text="Leito-Kun",
#             fill="#000000",
#             font=("Inter", 18 * -1)
#         )

#         # Texto del navbar
#         self.navbar_subtitle_1 = self.canvas.create_text(
#             26.0,
#             31.0,
#             anchor="nw",
#             text="Admin",
#             fill="#000000",
#             font=("Inter", 14 * -1)
#         )
        
#         # Texto del navbar
#         self.navbar_subtitle_2 = self.canvas.create_text(
#             226.0,
#             5.0,
#             anchor="nw",
#             text="Gestion de Usuarios",
#             fill="#000000",
#             font=("Inter", 40 * -1)
#         )

#         # Boton para regresar a la seleccion
#         self.images["button_volver"] = tk.PhotoImage(file=relative_to_assets("U_volver.png"))
#         self.button_volver = tk.Button(
#             self,
#             image=self.images["button_volver"],
#             borderwidth=0,
#             highlightthickness=0,
#             relief="raised",
#             bg="#6D6CFA",
#             activebackground="#6D6CFA"
#         )
#         self.button_volver.place(x=1135.0, y=15.0, width=208.0, height=29.0)
        
#         # Boton listar para ver a los usuarios
#         self.images["button_listado"] = tk.PhotoImage(file=relative_to_assets("U_listado.png"))
#         self.button_listado = tk.Button(
#             self,
#             image=self.images["button_listado"],
#             borderwidth=0,
#             highlightthickness=0,
#             relief="flat",
#             command=show_users
#         )
#         self.button_listado.place(x=1.0, y=57.0, width=213.0, height=58.0)
        
#         # Boton para modicar el usuario
#         self.images["button_modificar"] = tk.PhotoImage(file=relative_to_assets("U_modificar.png"))
#         self.button_modificar = tk.Button(
#             self,
#             image=self.images["button_modificar"],
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: {self.hide_widgets(), self.controller.show_frame(Modificar)},
#             relief="flat"
#         )
#         self.button_modificar.place(x=1.0, y=115.0, width=213.0, height=58.0)
        
#         # Boton para enviar a la accion de eliminar al usuario
#         self.images["button_eliminar"] = tk.PhotoImage(file=relative_to_assets("U_eliminar.png"))
#         self.button_eliminar = tk.Button(
#             self,
#             image=self.images["button_eliminar"],
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: self.controller.show_frame(Eliminar),
#             relief="flat"
#         )
#         self.button_eliminar.place(x=1.0, y=173.0, width=213.0, height=58.0)
        
#         # Formulario para eliminar al usuario
#         self.label_info = self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingresa la cedula del usuario a eliminar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        
#         self.label_cedula = self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cedula", fill="#000000", font=("Montserrat Regular", 15))
        
#         self.input_cedula = tk.Entry(
#             self,
#             bd=0,
#             bg="#FFFFFF",
#             fg="#000716",
#             highlightthickness=0, 
#             borderwidth=0.5, 
#             relief="solid"
#         )
#         self.input_cedula.place(x=263.0, y=182.0, width=237.0, height=38.0)
        
#         #Boton para eliminar el registro
#         self.images["button_eliminar_usuario"] = tk.PhotoImage(file=relative_to_assets("U_boton_E.png")) 
#         self.button_volver = tk.Button(
#             self,
#             image=self.images["button_eliminar_usuario"],
#             borderwidth=0,
#             highlightthickness=0,
#             relief="flat",
#             command=lambda:self.deleteuser()
#         )
#         self.button_volver.place(x=265.0, y=264.0, width=130.0, height=40.0)

#     def hide_widgets(self):
#         self.button_volver.place_forget()
#         self.button_modificar.place_forget()
#         self.button_listado.place_forget()
#         self.button_eliminar.place_forget()
#         self.input_cedula.place_forget()
#         self.canvas.itemconfigure(self.label_info, state='hidden')
#         self.canvas.itemconfigure(self.label_cedula, state='hidden')
#         self.canvas.itemconfigure(self.navbar_title, state='hidden')
#         self.canvas.itemconfigure(self.navbar_subtitle_1, state='hidden')
#         self.canvas.itemconfigure(self.navbar_subtitle_2, state='hidden')

#     def deleteuser(self):
#         usuario=self.input_cedula.get()
#         if delete_users(usuario):
#             messagebox.showinfo("Éxito", "Usuario Eliminado Satisfactoriamente.")
#         else:
#             messagebox.showerror("Error", "Usuario no en la Base de datos por favor Verifique.")

    
        
# #Clase para modificar
# class Modificar(tk.Frame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.config(bg="#FFFFFF")
#         self.create_widgets()


#     def validate_number_input(self,text):
#         if text == "":
#             return True
#         try:
#             float(text)
#             return True
#         except ValueError:
#             return False

#     def create_widgets(self):
#         self.images = {}
#         self.canvas = tk.Canvas(
#             self,
#             bg="#FFFFFF",
#             height=768,
#             width=1366,
#             bd=0,
#             highlightthickness=0,
#             relief="ridge"
#         )
#         self.canvas.place(x=0, y=0)

#         validate_number = self.register(self.validate_number_input)
        
#         #Imagenes generales para el relleno
#         self.image_image_1 = PhotoImage(
#             file=relative_to_assets("U_relleno_vertical.png"))
#         self.canvas.create_image(
#             107.0,
#             412.0,
#             image=self.image_image_1
#         )

#         self.image_image_2 = PhotoImage(
#             file=relative_to_assets("U_relleno_general.png"))
#         self.canvas.create_image(
#             789.0,
#             413.0,
#             image=self.image_image_2
#         )

#         self.image_image_3 = PhotoImage(
#             file=relative_to_assets("U_barra.png"))
#         self.canvas.create_image(
#             682.0,
#             29.0,
#             image=self.image_image_3
#         )
#         #----------------------------------------------------
#         # Texto del navbar
#         self.navbar_title = self.canvas.create_text(
#             26.0,
#             9.0,
#             anchor="nw",
#             text="Leito-Kun",
#             fill="#000000",
#             font=("Inter", 18 * -1)
#         )

#         # Texto del navbar
#         self.navbar_subtitle_1 = self.canvas.create_text(
#             26.0,
#             31.0,
#             anchor="nw",
#             text="Admin",
#             fill="#000000",
#             font=("Inter", 14 * -1)
#         )
        
#         # Texto del navbar
#         self.navbar_subtitle_2 = self.canvas.create_text(
#             226.0,
#             5.0,
#             anchor="nw",
#             text="Gestion de Usuarios",
#             fill="#000000",
#             font=("Inter", 40 * -1)
#         )

#         # Boton para regresar a la seleccion
#         self.images["button_volver"] = tk.PhotoImage(file=relative_to_assets("U_volver.png"))
#         self.button_volver = tk.Button(
#             self,
#             image=self.images["button_volver"],
#             borderwidth=0,
#             highlightthickness=0,
#             relief="raised",
#             bg="#6D6CFA",
#             activebackground="#6D6CFA"
#         )
#         self.button_volver.place(x=1135.0, y=15.0, width=208.0, height=29.0)
        
#         # Boton listar para ver a los usuarios
#         self.images["button_listado"] = tk.PhotoImage(file=relative_to_assets("U_listado.png"))
#         self.button_listado = tk.Button(
#             self,
#             image=self.images["button_listado"],
#             borderwidth=0,
#             highlightthickness=0,
#             relief="flat",
#             command=show_users
#         )
#         self.button_listado.place(x=1.0, y=57.0, width=213.0, height=58.0)
        
#         # Boton para modicar el usuario
#         self.images["button_modificar"] = tk.PhotoImage(file=relative_to_assets("U_modificar.png"))
#         self.button_modificar = tk.Button(
#             self,
#             image=self.images["button_modificar"],
#             borderwidth=0,
#             highlightthickness=0,
#             relief="flat"
#         )
#         self.button_modificar.place(x=1.0, y=115.0, width=213.0, height=58.0)
        
#         # Boton para enviar a la accion de eliminar al usuario
#         self.images["button_eliminar"] = tk.PhotoImage(file=relative_to_assets("U_eliminar.png"))
#         self.button_eliminar = tk.Button(
#             self,
#             image=self.images["button_eliminar"],
#             borderwidth=0,
#             highlightthickness=0,
#             command=lambda: self.controller.show_frame(Eliminar),
#             relief="flat"
#         )
#         self.button_eliminar.place(x=1.0, y=173.0, width=213.0, height=58.0)
        
#         # Formulario para eliminar al usuario
#         self.label_info = self.canvas.create_text(263.0, 106.0, anchor="nw", text="Ingresa los campos del usuario a modificar", fill="#4C4C4C", font=("Montserrat Medium", 15))
        
#         self.label_cedula = self.canvas.create_text(263.0, 152.0, anchor="nw", text="Cedula", fill="#000000", font=("Montserrat Regular", 15))
#         self.input_cedula = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
#         self.input_cedula.place(x=263.0, y=182.0, width=237.0, height=38.0)
        
#         # Input para ingresar el nombre del usuario
#         self.label_nombre = self.canvas.create_text(263.0, 230.0, anchor="nw", text="Nombre", fill="#000000", font=("Montserrat Regular", 15))
#         self.input_nombre = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
#         self.input_nombre.place(x=263.0, y=260.0, width=237.0, height=38.0)
        
#         # Input para ingresar la contraseña del usuario
#         self.label_password = self.canvas.create_text(263.0, 308.0, anchor="nw", text="Contraseña", fill="#000000", font=("Montserrat Regular", 15))
#         self.input_password = tk.Entry(self, show='*', bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, borderwidth=0.5, relief="solid")
#         self.input_password.place(x=263.0, y=338.0, width=237.0, height=38.0)
        
#         #Boton para eliminar el registro
#         self.images["button_modificar_usuario"] = tk.PhotoImage(file=relative_to_assets("U_boton_M.png")) 
#         self.button_volver = tk.Button(
#             self,
#             image=self.images["button_modificar_usuario"],
#             borderwidth=0,
#             highlightthickness=0,
#             relief="flat",
#             command=lambda:self.modify_user()
#         )
#         self.button_volver.place(x=263.0, y=403.0, width=130.0, height=40.0)

#     def modify_user(self):
#         dni=self.input_cedula.get()
#         nombre=self.input_nombre.get()
#         password=self.input_password.get()

#         if update_users(dni,nombre,password):
#             messagebox.showinfo("Éxito", "Usuario actualizado exitosamente.")
#         else:
#             messagebox.showerror("Error", "Error al actualizar el Usuario verifique Datos.")
#             pass
        

# # Ejecutar la aplicación
# if __name__ == "__main__":
#     app = Users()
#     app.mainloop()
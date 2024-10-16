from pathlib import Path

from Vistas.Main_PWindow import *
from Vistas.U_main import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
from Library.librerias import search_users
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\El_Proyecto\assets")
           
class selection():
    def __init__(self, usuario=None):
        self.usuario = usuario
        self.window = None
        
    def open_new(self, rol_usuario):
        self.window.destroy()
        Balls(rol_usuario).open()
        
    def open_U_main(self):
        self.window.destroy()
        Users().open()
        
    def open(self):
        #Obtener valores del usuario
        if self.usuario != None:
            type_rol = search_users(self.usuario)
            rol_usuario = type_rol[0][1]
        else:
            rol_usuario = "Administrador"
        
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        

        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.window = Tk()

        self.window.geometry("1366x768")
        self.window.configure(bg = "#FFFFFF")
        #Configuramos el icono de la aplicación
        self.window.iconbitmap(relative_to_assets('Arcanum.ico'))

        #Main_PW=Main_PW()

        canvas = Canvas(
            self.window,
            bg = "#FFFFFF",
            height = 768,
            width = 1366,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_text(
            210.0,
            79.0,
            anchor="nw",
            text="Seleccione el área a gestionar",
            fill="#000000",
            font=("Press Start 2P", 32 * -1)
        )
        
          #Funcion para evaluar el rol del usuario
        def isAdministrator(rol_usuario):
            return rol_usuario == "Administrador"
        
        # Función para manejar el clic del botón
        def handle_button_click():
            if isAdministrator(rol_usuario):
                self.open_U_main()
            else:
                messagebox.showerror("Permisos insuficientes", "No tienes los permisos requeridos para ingresar a esta sesión.")

        #boton1= Pokemones
        image_image_1 = PhotoImage(
            file=relative_to_assets("charmander.png"))
        canvas.create_image(
            280.0,
            459.0,
            image=image_image_1
        )

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_pokemones.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_new(rol_usuario),
            relief="flat"
        )
        button_1.place(
            x=245.0,
            y=230.0,
            width=130.0,
            height=40.0
        )

        image_image_2 = PhotoImage(
            file=relative_to_assets("entrenador.png"))
        resized_image = image_image_2.subsample(4,4)
        canvas.create_image(
            1057.0,
            469.0,
            image=resized_image
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets("button_usuarios.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=handle_button_click,
            relief="flat"
        )
        button_2.place(
            x=991.0,
            y=230.0,
            width=130.0,
            height=40.0
        )
        
        self.window.resizable(False, False)
        self.window.mainloop()
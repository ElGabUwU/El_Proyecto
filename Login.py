from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from Library.librerias import *
from Vistas.R_selection import *
from Register import show_registrar_window

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\El_Proyecto\assets")

#Ruta reltiva que conecta las imagenes con el archivo Login
def open_new(usuario):
    selection(usuario).open()

def recoger_datos():
    usuario = username.get()
    contrasena = password.get()
    if login(usuario, contrasena):
        window.destroy()
        open_new(usuario)

    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#Creamos un objeto usando la clase TK
#Se crea la instancia de esta clase TK
window = Tk()
#Cambiamos el nombre de la ventana
window.title("Login")
# Modificacamos el tamaño de la ventana (pixeles)
window.geometry("1366x768")
#Fondo de pantalla de la ventana
window.configure(bg = "#042344")
#Configuramos el icono de la aplicación.
window.iconbitmap(relative_to_assets('PokeBall.ico'))

#Estilos globales de la ventana
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 768,
    width = 1366,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
#---------------------------------------
#Imagen superior de la pokebola
image_image_1 = PhotoImage(
    file=relative_to_assets("pokebola.png"))
image_1 = canvas.create_image(
    678.0,
    234.0,
    image=image_image_1
)
#---------------------------------------
#Frase superior
canvas.create_text(
    530.0,
    446.0,
    anchor="nw",
    text="Inicio de sesión",
    fill="#FFFFFF",
    font=("Press Start 2P", 20 * -1)
)
#---------------------------------------
#Estilos de la imagen para el input (Usuario)
canvas.place(x = 0, y = 0)
entry_image_1 = PhotoImage(
    file=relative_to_assets("input_usuario.png"))
entry_bg_1 = canvas.create_image(
    683.0,
    525.0,
    image=entry_image_1
)
# ---------------------------------------
# Estilos del input (Usuario)
username = Entry(
    window,
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    relief="flat"
)
username.place(
    x=436.0,
    y=505.0,
    width=494.0,
    height=38.0
)
canvas.create_text(
    445.0,
    492.0,
    anchor="nw",
    text="Usuario",
    fill="#000000",
    font=("Press Start 2P", 15 * -1)
)
# ---------------------------------------
# Estilos del input (Contraseña)
password = Entry(
    window,
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    show="*",
    highlightthickness=0,
    relief="flat"
)
password.place(
    x=436.0,
    y=585.0,
    width=494.0,
    height=38.0
)
canvas.create_text(
    445.0,
    570.0,
    anchor="nw",
    text="Contraseña",
    fill="#000000",
    font=("Press Start 2P", 15 * -1)
)

# Dibuja una línea debajo del campo de contraseña
canvas.create_line(
    436.0, 623.0,  # Coordenadas x, y del inicio de la línea
    930.0, 623.0,  # Coordenadas x, y del final de la línea
    fill="#888480",# Color de la línea
    width=0.5      # Grosor de la línea
)
#---------------------------------------
#Boton para iniciar sesión
button_image_1 = PhotoImage(
    file=relative_to_assets("Login_button.png"))

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:recoger_datos(),
    relief="flat"
)
button_1.place(x=728.0, y=665.0, width=130.0, height=40.0)

button_image_2 = tk.PhotoImage(file=relative_to_assets("L_registrar.png"))

button_2 = tk.Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: {window.destroy(), show_registrar_window()},
    relief="flat"
)

button_2.place(x=512.0, y=666.0, width=130.0, height=46.0)

#---------------------------------------
# Deshabilitar la capacidad de redimensionar la ventana
window.resizable(False, False)
#---------------------------------------
window.mainloop()

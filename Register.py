from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from Library.librerias import signup

# Rutas relativas de las imágenes
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Pokedex_by_Venezuelan\assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Función para evaluar los inputs que solo permitan números
def validate_number_input(text):
    return text.isdigit() or text == ""

def show_registrar_window():
    registrar_window = Tk()
    registrar_window.title("Registrar")
    registrar_window.geometry("1366x768")
    registrar_window.configure(bg="#FFFFFF")
    registrar_window.iconbitmap(relative_to_assets('PokeBall.ico'))
    
    canvas = Canvas(
        registrar_window,
        bg="#FFFFFF",
        height=768,
        width=1366,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Cargar y mostrar las imágenes
    images = {}
    images["Bordes"] = PhotoImage(file=relative_to_assets("Bordes.png"))
    canvas.create_image(683.0, 389.0, image=images["Bordes"])

    # Registrar la función de validación
    validate_command = registrar_window.register(validate_number_input)

    # Entradas
    cedula = Entry(
        registrar_window,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        borderwidth=0.5,
        relief="solid",
        validate="key",
        validatecommand=(validate_command, "%P")
    )
    cedula.place(x=507.0, y=349.0, width=352.0, height=38.0)

    nombre = Entry(
        registrar_window,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        borderwidth=0.5,
        relief="solid"
    )
    nombre.place(x=507.0, y=249.0, width=352.0, height=38.0)

    clave = Entry(
        registrar_window,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        borderwidth=0.5,
        relief="solid"
    )
    clave.place(x=507.0, y=449.0, width=352.0, height=38.0)

    canvas.create_text(
        507.0,
        319.0,
        anchor="nw",
        text="Cedula",
        fill="#000000",
        font=("Montserrat Regular", 15 * -1)
    )

    canvas.create_text(
        507.0,
        219.0,
        anchor="nw",
        text="Nombre",
        fill="#000000",
        font=("Montserrat Regular", 15 * -1)
    )

    canvas.create_text(
        507.0,
        419.0,
        anchor="nw",
        text="Contraseña",
        fill="#000000",
        font=("Montserrat Regular", 15 * -1)
    )

    canvas.create_text(
        627.0,
        163.0,
        anchor="nw",
        text="Registrarse",
        fill="#4C4C4C",
        font=("Montserrat Medium", 20 * -1)
    )

    # Botón Cancelar
    button_image_1 = PhotoImage(file=relative_to_assets("L_cancelar.png"))
    Button(
        registrar_window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: registrar_window.destroy(),  # Simplemente cierra la ventana actual
        relief="flat"
    ).place(x=497.0, y=565.0, width=130.0, height=40.0)

    # Botón Registrar
    button_image_2 = PhotoImage(file=relative_to_assets("L_registrar.png"))
    Button(
        registrar_window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: register_user(),  # Aquí se puede agregar la funcionalidad para registrar
        relief="flat"
    ).place(x=739.0, y=565.0, width=130.0, height=40.0)

    def register_user():
        nuser = nombre.get()
        dni = cedula.get()
        pw = clave.get()
        rol = 1
        if signup(nuser, pw, rol, dni):
            messagebox.showinfo("Éxito", "Registro de usuario Exitoso")
        else:
            messagebox.showinfo("Éxito", "Registro Fallido usuario ya registrado")
    
    registrar_window.resizable(False, False)
    registrar_window.mainloop()

# Para probar la ventana de registro
if __name__ == "__main__":
    show_registrar_window()
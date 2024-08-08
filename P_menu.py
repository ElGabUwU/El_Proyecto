import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage




# Rutas relativas de las imágenes
ASSETS_PATH = Path(r"C:\El_Proyecto\assets_3")

# Función para asignar la ruta a las imágenes
def relative_to_assets(path: str) -> Path:
    
    full_path = ASSETS_PATH / Path(path)
    if not full_path.exists():
        raise FileNotFoundError(f"Image not found: {full_path}")
    return full_path
        
# Clase principal de la aplicación
class Balls(tk.Tk):
    def __init__(self, rol_usuario = None):
        self.rol_usuario = "administrador"
        super().__init__()
        self.title("Pokedex")
        self.geometry("1366x768")
        self.container = tk.Frame(self)
        self.resizable(False, False)  # No permitir cambiar el tamaño de la ventana
        self.container.pack(fill="both", expand=True)
        self.current_frame = None
        self.iconbitmap(relative_to_assets('PokeBall.ico'))
        self.show_frame(SecondaryPage)
        
        # Vincula la función on_closing al evento de cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        #drop_sesion()
        self.destroy()

    def show_frame(self, page_class):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        self.current_frame = page_class(self.container, self, self.rol_usuario)
        self.current_frame.pack(fill="both", expand=True)

    def open(self):
        self.mainloop()

class SecondaryPage(tk.Frame):
    def __init__(self, parent, controller, rol_usuario):
        super().__init__(parent)
        self.controller = controller
        self.rol_usuario = rol_usuario
        main_page = Main_PW(self, controller, rol_usuario)
        main_page.pack(fill="both", expand=True)

class Main_PW(tk.Frame):
    def __init__(self, parent, controller, rol_usuario):
        super().__init__(parent)
        self.controller = controller
        self.rol_usuario = rol_usuario
        usuario="admin"
        self.usuario=usuario
        self.config(bg="#FFFFFF")
        self.create_widgets()

    def create_widgets(self):
        self.images = {}
        canvas = tk.Canvas(
            self,
            bg="#FFFFFF",
            height=768,
            width=1366,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        self.image_image_1 = tk.PhotoImage(
            file=relative_to_assets("image_1.png"))
        canvas.create_image(
            107.0,
            412.0,
            image=self.image_image_1
        )

        self.image_image_2 = tk.PhotoImage(
            file=relative_to_assets("image_2.png"))
        canvas.create_image(
            682.0,
            29.0,
            image=self.image_image_2
        )

        canvas.create_text(
            1164.0,
            15.0,
            anchor="nw",
            text="Cerrar Sesión",
            fill="#4D4D4D",
            font=("Inter", 24 * -1)
        )

        self.button_image_1 = tk.PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_1.place(
            x=1.0,
            y=404.0,
            width=213.0,
            height=85.0
        )

        self.button_image_2 = tk.PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = tk.Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            x=1.0,
            y=229.0,
            width=213.0,
            height=58.5
        )

        self.button_image_3 = tk.PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = tk.Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_3.place(
            x=1.0,
            y=604.0,
            width=213.0,
            height=58.5
        )

        self.button_image_4 = tk.PhotoImage(
            file=relative_to_assets("button_4.png"))
        self.button_4 = tk.Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self.button_4.place(
            x=1.0,
            y=115.0,
            width=213.0,
            height=58.0
        )

        self.button_image_5 = tk.PhotoImage(
            file=relative_to_assets("button_5.png"))
        self.button_5 = tk.Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        self.button_5.place(
            x=1.0,
            y=287.0,
            width=213.0,
            height=58.0
        )

        self.button_image_6 = tk.PhotoImage(
            file=relative_to_assets("button_6.png"))
        self.button_6 = tk.Button(
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )
        self.button_6.place(
            x=1.0,
            y=487.0,
            width=213.0,
            height=58.0
        )

        self.button_image_7 = PhotoImage(
            file=relative_to_assets("button_7.png"))
        self.button_7 = tk.Button(
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            relief="flat"
        )
        self.button_7.place(
            x=1.0,
            y=173.0,
            width=213.0,
            height=58.5
        )

        self.button_image_8 = tk.PhotoImage(
            file=relative_to_assets("button_8.png"))
        self.button_8 = tk.Button(
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_8 clicked"),
            relief="flat"
        )
        self.button_8.place(
            x=1.0,
            y=345.0,
            width=213.0,
            height=58.5
        )

        self.button_image_9 = tk.PhotoImage(
            file=relative_to_assets("button_9.png"))
        self.button_9 = tk.Button(
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_9 clicked"),
            relief="flat"
        )
        self.button_9.place(
            x=1.0,
            y=545.0,
            width=213.0,
            height=58.5
        )

        self.button_image_10 = tk.PhotoImage(
            file=relative_to_assets("button_10.png"))
        self.button_10 = tk.Button(
            image=self.button_image_10,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_10 clicked"),
            relief="flat"
        )
        self.button_10.place(
            x=1.0,
            y=58.0,
            width=213.0,
            height=58.0
        )

        canvas.create_text(
            26.0,
            32.0,
            anchor="nw",
            text="Admin",
            fill="#000000",
            font=("Inter", 14 * -1)
        )

        canvas.create_text(
            26.0,
            10.0,
            anchor="nw",
            text="Henry Ferrer",
            fill="#000000",
            font=("Inter", 18 * -1)
        )
    
if __name__ == "__main__":
    app = Balls()
    app.mainloop()
    
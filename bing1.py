import tkinter as tk

def mostrar_frame(frame):
    # Aquí va tu lógica para mostrar el frame
    pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú Desplegable Personalizado")
        self.geometry("400x300")

        

        # Crear el botón que abrirá el menú desplegable
        self.menu_button = tk.Button(self, text="Opciones", bg="yellow", fg="red", font=("Helvetica", 12), relief="raised", command=self.show_menu)
        self.menu_button.place(x=10, y=10)

        # Crear el menú desplegable
        self.dropdown_menu = tk.Menu(self, tearoff=0, bg="lightblue", fg="black", font=("Helvetica", 12),
                                     activebackground="blue", activeforeground="white")
        self.dropdown_menu.add_command(
            label="Modificar",
            command=lambda: {self.update_header_text("Modificar"), mostrar_frame("frame_modificar")}
        )
        self.dropdown_menu.add_command(
            label="Eliminar",
            command=lambda: {self.update_header_text("Eliminar"), mostrar_frame("frame_eliminar")}
        )
        self.dropdown_menu.add_command(
            label="Agregar",
            command=lambda: {self.update_header_text("Agregar"), mostrar_frame("frame_agregar")}
        )
        self.dropdown_menu.add_command(
            label="Ver",
            command=lambda: {self.update_header_text("Ver"), mostrar_frame("frame_ver")}
        )

    def show_menu(self):
        self.dropdown_menu.post(self.menu_button.winfo_rootx(), self.menu_button.winfo_rooty() + self.menu_button.winfo_height())

    def update_header_text(self, text):
        # Aquí va tu lógica para actualizar el texto del header
        print(f"Header actualizado a: {text}")

if __name__ == "__main__":
    app = App()
    app.mainloop()

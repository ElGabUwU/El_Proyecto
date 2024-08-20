import tkinter as tk
from tkinter import ttk

def mostrar_frame(frame):
    # Aquí va tu lógica para mostrar el frame
    pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú Desplegable Personalizado")
        self.geometry("400x300")

        

        # Crear un estilo personalizado para el Combobox
        style = ttk.Style()
        style.configure("TCombobox", fieldbackground="yellow", background="yellow", foreground="red")

        # Crear el Combobox en modo readonly
        self.combobox = ttk.Combobox(self, values=["Modificar", "Eliminar", "Agregar", "Ver"], style="TCombobox", state="readonly")
        self.combobox.set("Opciones")  # Establecer el valor por defecto
        self.combobox.place(x=10, y=10)
        self.combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

    def on_combobox_select(self, event):
        selected_option = self.combobox.get()
        if selected_option == "Modificar":
            self.update_header_text("Modificar")
            mostrar_frame("frame_modificar")
        elif selected_option == "Eliminar":
            self.update_header_text("Eliminar")
            mostrar_frame("frame_eliminar")
        elif selected_option == "Agregar":
            self.update_header_text("Agregar")
            mostrar_frame("frame_agregar")
        elif selected_option == "Ver":
            self.update_header_text("Ver")
            mostrar_frame("frame_ver")

    def update_header_text(self, text):
        # Aquí va tu lógica para actualizar el texto del header
        print(f"Header actualizado a: {text}")

if __name__ == "__main__":
    app = App()
    app.mainloop()

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Pokédex")

# Cargar imagen de Charmander
imagen_charmander = Image.open("C:\\Pokedex_by_Venezuelan\\Library\\j.jpg")
render = ImageTk.PhotoImage(imagen_charmander)

# Crear canvas para la imagen (lado izquierdo)
canvas_imagen = tk.Canvas(ventana, width=imagen_charmander.width, height=imagen_charmander.height)
canvas_imagen.pack(side="left", padx=10, pady=10)

# Mostrar la imagen en el canvas
canvas_imagen.create_image(0, 0, anchor="nw", image=render)

# Crear etiqueta para el nombre del Pokémon (superpuesta en el canvas)
nombre_pokemon = "Charmander"
etiqueta_nombre = tk.Label(canvas_imagen, text=nombre_pokemon, font=("Helvetica", 14, "bold"), bg="white")
etiqueta_nombre.place(x=10, y=10)  # Ajusta las coordenadas según tu preferencia

# Crear marco para la información (lado derecho)
marco_info = ttk.Frame(ventana)
marco_info.pack(side="right", padx=10, pady=10)

canvas_descripcion = tk.Canvas(ventana, width=300, height=100)  # Ajusta las dimensiones
canvas_descripcion.pack(side="right", padx=10, pady=10)

# Crear etiqueta para la descripción
descripcion = "Charmander es un Pokémon de tipo Fuego. Es el número 004 en la Pokédex."
etiqueta_descripcion = tk.Label(canvas_descripcion, text=descripcion)
etiqueta_descripcion.pack(side="left", padx=10, pady=10)

# Crear lista desplazable en el lado derecho
lista_pokemon = ttk.Treeview(marco_info, columns=("Número"))
lista_pokemon.heading("#1", text="Número")
lista_pokemon.insert("", "end", text="Bulbasaur", values=("001"))
lista_pokemon.insert("", "end", text="Ivysaur", values=("002"))
# Agrega más Pokémon a la lista aquí...

# Configurar scrollbar para la lista
scrollbar = ttk.Scrollbar(marco_info, orient="vertical", command=lista_pokemon.yview)
lista_pokemon.configure(yscrollcommand=scrollbar.set)

# Empaquetar la lista y el scrollbar
lista_pokemon.pack(side="right", padx=10, pady=10)
scrollbar.pack(side="right", fill="y")

# Iniciar el bucle principal de Tkinter
ventana.mainloop()

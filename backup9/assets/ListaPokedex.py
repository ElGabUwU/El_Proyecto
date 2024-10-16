import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
import sqlite3
global tree

import random

#Cambios al canva pokemon
def mostrar_texto_aleatorio():
    tipo = "planta"
    altura = "1.6"
    peso = "20"
    sexo = "femenino"
    pokemon = Image.open("j.png")
    render = ImageTk.PhotoImage(pokemon)
    # Borra el contenido actual del Canvas
    canvas.delete("all")

    canvas.create_image(0, 0, anchor="nw", image=render)

    # Crea las etiquetas
    nombre_pokemon = "Charmander"
    etiqueta_nombre = tk.Label(canvas, text=nombre_pokemon, font=("Helvetica", 14, "bold"), bg="white")
    etiqueta_nombre.place(x=10, y=10)  # Ajusta las coordenadas según tu preferencia

    # Crea las etiquetas de información
    canvas.create_text(100, 100, text="Seen:", anchor="w", font=("Arial", 12))
    canvas.create_text(200, 100, text="12", anchor="w", font=("Arial", 12))
    canvas.create_text(100, 150, text="Owned:", anchor="w", font=("Arial", 12))
    canvas.create_text(200, 150, text="9", anchor="w", font=("Arial", 12))

    



#funcion sql para buscar datos del pokemon especifico
def search_pk(pokemon):
    bd = sqlite3.connect("pokimons.db")
    cursor = bd.cursor()
    if pokemon:
        for pk in pokemon:
            cursor.execute("""
                SELECT p.pkId,p.pkNombre,t.tipoNombre,p.pkPeso,p.pkAltura,s.sexoNombre,p.pkDesc FROM pokemons as p
                INNER JOIN tipos as t ON pkTipo == tipoId
                INNER JOIN sexo as s ON pkSexo == sexoId
                WHERE p.pkNombre == ?
                """,(pk,))
            search=(cursor.fetchall())
        return search
    else:
        search=[]
        return search
    bd.close()

#funcion sql para recoger info de todos los pokemons
def search_all_pk():
    bd = sqlite3.connect("pokimons.db")
    cursor = bd.cursor()
    cursor.execute("""
        SELECT p.pkId,p.pkNombre,t.tipoNombre,p.pkPeso,p.pkAltura,s.sexoNombre,p.pkDesc FROM pokemons as p
        INNER JOIN tipos as t ON pkTipo == tipoId
        INNER JOIN sexo as s ON pkSexo == sexoId
        ORDER BY p.pkId ASC
        """)
    search=cursor.fetchall()
    bd.close()
    return search

# Funcion para guardar la lista personal 
def favorite_items():
    def get_all_items_with_values(tree):
        items = tree.get_children()
        all_items = []
        for item in items:
            all_items.append((item, tree.item(item, 'values'),tree.item(item, 'tags')[0]))
        return all_items

    #guardar solo los nombres de los pokemons
    def get_favorite_items(tree):
        all_items = get_all_items_with_values(tree)
        favorite_items = []
        for item in all_items:
            if item[2] == 'checked':
                favorite_items.append(item[1][0])
        return favorite_items

    favorite_list = get_favorite_items(tree)
    return favorite_list

# Convertir el id al imprimir en treeview
def get_pk_id(id):
    if id <10:
        return '00'+str(id)
    elif id<100:
        return '0'+str(id)
    else:
        return str(id)


#funcion para mostrar todo en treeview
def update_treeview_favs(pkinfo):
    global tree
    try:
        tree.delete(*tree.get_children())
        info = pkinfo
        for row in info:
            id = get_pk_id(row[0])
            tree.insert('', 'end', text=id, values=row[1], tags=('row'))
    except ValueError as error:
        print(f"Error al actualizar los datos: {error}")
def command_to_search_all():
    search = search_all_pk()
    update_treeview_all(search)


#funcion para mostrar solo los favs en treeview
def update_treeview_all(pkinfo):
    global tree
    try:
        tree.delete(*tree.get_children())
        info = pkinfo
        for row in info:
            id = get_pk_id(row[0])
            tree.insert('', 'end', text=id, values=row[1], tags=('unchecked','row'))
    except ValueError as error:
        print(f"Error al actualizar los datos: {error}")
def command_to_search_favs():
    fav = favorite_items()  
    search = search_pk(fav)
    update_treeview_favs(search)

#funcion para recoger valores del item seleccionado
def select_item(event):
    try:
        itemSeleccionado = tree.focus()
        if itemSeleccionado:
            values = tree.item(itemSeleccionado)['values']
    except ValueError as error:
        print(f"Error al seleccionar el registro: {error}")

#acomodar imagenes
def resize_image(path, size):
    image = Image.open(path)
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)

#funcion para cambiar el tag en cada click
def box_click(event):
    item = tree.identify_row(event.y)
    if not item:
        return
    tags = tree.item(item, 'tags')
    if 'unchecked' in tags:
        tree.item(item, tags=('checked',))
    elif 'checked' in tags:
        tree.item(item, tags=('unchecked',))

#Crear pestaña
root = tk.Tk()
root.geometry("1366x768")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill='both')

# Agregar la cabecera
header = tk.Label(frame, text="Pokimons", font=("PressStart2P", 16))
header.pack(pady=10)

# Cargar imagenes en variables
im_checked = resize_image('checked.png', (15, 15))
im_unchecked = resize_image('unchecked.png', (15, 15))
im_tristate = resize_image('tristate.png', (15, 15))

# Crear el estilo para el Treeview y el scrollbar
style = ttk.Style()
style.theme_use('alt')
style.configure("mystyle.Treeview", 
                highlightthickness=0, 
                bd=0, 
                font=('PressStart2P', 11),  
                background="#D3D3D3",  
                foreground="black",    
                rowheight=25)
          
style.configure("mystyle.Treeview.Heading", 
                font=('PressStart2P', 13,),  
                background="#DF3535",          
                foreground="black") 
           
style.map("mystyle.Treeview.Heading", 
            background=[("active", "#DF3535")], 
            foreground=[("active", "black")])

style.map("mystyle.Treeview", 
            background=[("selected", "#F5A89A")],  
            foreground=[("selected", "black")])  
  
style.configure("mystyle.Vertical.TScrollbar",
                gripcount=0,
                background="#DF3535",
                arrowcolor="black")

style.map("mystyle.Vertical.TScrollbar",
            background=[("active", "#DF3535"), ("pressed", "#DF3535")],
            arrowcolor=[("active", "black"), ("pressed", "black")])

# Crear el Treeview
treeview_canvas = tk.Canvas(frame)
treeview_canvas.pack(side="top", fill="both", expand=True)


tree = ttk.Treeview(treeview_canvas, columns=('col1'),height=5, style="mystyle.Treeview")
tree.heading('#0', text="ID")
tree.column('#0', width=60)
tree.heading('col1', text="Pokimons")
tree.column('col1', width=100)

# Crear el Scrollbar
scrollbar = ttk.Scrollbar(treeview_canvas, orient="vertical", command=tree.yview, style="mystyle.Vertical.TScrollbar")
scrollbar.pack(side='right', fill='both')
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side='right', fill='both')

# asignar las imagenes a los tags
tree.tag_configure('unchecked', image=im_unchecked)
tree.tag_configure('tristate', image=im_tristate)
tree.tag_configure('checked', image=im_checked)

# asignar las acciones al treeview
tree.bind('<Button-1>', box_click, True)
tree.bind("<<TreeviewSelect>>",select_item)

# rellenar treeview
command_to_search_all()

#canva lateral para detalles pokemon
canvas = tk.Canvas(treeview_canvas, bg="white")
canvas.pack(side="top",fill="both", expand=True)
# Carga una imagen (reemplaza 'ruta_de_la_imagen.png' con la ruta correcta)

 



#canvas botones
buttons_canvas = tk.Canvas(root)
buttons_canvas.pack(side="bottom", fill="x")

# Crear botones
Button1 = tk.Button(buttons_canvas, text="Pokedex", width=10,command=command_to_search_all)
Button2 = tk.Button(buttons_canvas, text="Favoritos", width=10,command=command_to_search_favs)
boton_ejecutar = tk.Button(buttons_canvas, text="Mostrar 'hola'", command=mostrar_texto_aleatorio)

# Posicionar los botones debajo del Treeview
Button1.pack(side="bottom", anchor="se")
Button2.pack(side="bottom", anchor="se")
boton_ejecutar.pack(side="bottom", anchor="se")

root.mainloop()


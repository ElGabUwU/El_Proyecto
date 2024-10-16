import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
import sqlite3
import random
from pathlib import Path
from Library.librerias import *

def show_pokemons():  
    global tree
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Pokedex_by_Venezuelan\assets")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Global image reference to prevent garbage collection
    global_image_ref = None

    # Global image reference to prevent garbage collection
    global_image_ref = None

    # Changes to the Canvas Pokemon

    def resize_image_aspect_ratio(path, base_height):
        """
        Redimensiona la imagen a una altura base, preservando la relación de aspecto.

        :param path: Ruta de la imagen
        :param base_height: Altura base deseada
        :return: Objeto PhotoImage redimensionado
        """
        
        image = Image.open(path)
        aspect_ratio = base_height / float(image.size[1])  # Calcula la proporción del alto
        base_width = int(float(image.size[0]) * float(aspect_ratio))  # Calcula el nuevo ancho manteniendo la relación de aspecto
        image = image.resize((base_width, base_height), Image.LANCZOS)  # Redimensiona la imagen
        return ImageTk.PhotoImage(image)  # Convierte a un objeto PhotoImage para usar en Tkinter

#funcion para recoger valores del item seleccionado
    def return_selection(event):
        values = tree.focus()
        pokemon = tree.item(values,'values')
        search = search_pk(pokemon)
        def mostrar_texto_aleatorio(search):
            global global_image_ref  # Asegúrate de que la imagen no sea recolectada por el garbage collector
            values = search[0]
            nombre = values[1]
            tipo = values[2]
            altura = values[4]
            peso = values[3]
            sexo = values[5]
            descripcion = values[6]

            # Redimensionar la imagen a 300 píxeles de altura manteniendo la proporción
            render = resize_image_aspect_ratio(relative_to_assets("j.png"), 500)

            # Guarda la referencia global de la imagen
            global_image_ref = render

            # Borra el contenido actual del Canvas
            canvas.delete("all")

            # Mostrar la imagen redimensionada en el Canvas
            canvas.create_image(0, 60, anchor="nw", image=render)

            canvas.create_rectangle(500, 10, 1100, 600, fill="lightblue")

            # Crear etiquetas de información
            
            canvas.create_text(30,30,anchor="nw",text=nombre,fill="#000000",font=("Montserrat Medium", 25 ))          
            canvas.create_text(510, 100, text="Tipo:"+ tipo, anchor="w", font=("Arial", 28))
            canvas.create_text(800, 100, text="Altura:"+ str(altura), anchor="w", font=("Arial", 28))
            canvas.create_text(510, 150, text="Peso:"+ str(peso), anchor="w", font=("Arial", 28))
            canvas.create_text(800, 150, text="Sexo:"+ sexo, anchor="w", font=("Arial", 28))
            text_area = tk.Text(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, wrap=tk.WORD,)
            text_area.place(x=535.0, y=382.0, width=550.0, height=238.0)  
            text_area.insert(tk.END,descripcion)
            text_area.config(font=("Montserrat Medium", 15), padx=10, pady=10, borderwidth=0.5, relief="solid",state="disabled")
        if search:
            mostrar_texto_aleatorio(search)
        else:
            pass
        
    # Convertir el id al imprimir en treeview
    def get_pk_id(id):
        if id <10:
            return '00'+str(id)
        elif id<100:
            return '0'+str(id)
        else:
            return str(id)
    def cadena_a_lista(cadena):
        # Utiliza el método split() para dividir la cadena en una lista
        if cadena:
            return cadena.split(',')
        else:
            pass
    
    def lista_a_cadena(lista):
        # Utiliza la función join() para unir los elementos de la lista con comas
        if lista:
            return ','.join(lista)
        else:
            pass

    # Funcion para guardar la lista personal 
    def command_to_search_favs():
        # Funcion para guardar la lista personal 
        def save_favorites():
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
    
            fav = favorite_items()
            if fav:
                value = lista_a_cadena(fav)
                save_pk('Rafita-kun',value)
            else:
                pass
        save_favorites()

        def update_treeview_favs(pkinfo):
            global tree
            try:
                tree.delete(*tree.get_children())
                for info in pkinfo:
                    for row in info:
                        id = get_pk_id(row[0])
                        tree.insert('', 'end', text=id, values=row[1], tags=('row'))
            except ValueError as error:
                print(f"Error al actualizar los datos: {error}")
        pkfav = search_favorite_pk('Rafita-kun')
        value = cadena_a_lista(pkfav[0])
        search = search_pk_fav(value)
        update_treeview_favs(search)
        
    #Recargar treeview con los tags cambiados 
    def command_to_recharge():
        def return_items():
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
                    favorite_items.append(item[1][0])
                return favorite_items

            favorite_list = get_favorite_items(tree)
            return favorite_list 
        def recharge_treeview(pkinfo,checked):
            global tree
            try:
                tree.delete(*tree.get_children())
                for row in pkinfo:
                    if row[1] in checked:
                        id = get_pk_id(row[0])
                        tree.insert('', 'end', text=id, values=row[1], tags=('checked','row'))
                    else:
                        id = get_pk_id(row[0])
                        tree.insert('', 'end', text=id, values=row[1], tags=('unchecked','row'))
            except ValueError as error:
                print(f"Error al actualizar los datos: {error}")

        fav = return_items()
        search = search_all_pk()
        recharge_treeview(search,fav)
        
    #Guardar lista de favoritos
    def save_favorites():
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

        def save_pk(username,pks):
            db = sqlite3.connect('..pokimons.db')
            cursor = db.cursor()
            cursor.execute("UPDATE usuarios SET pkFavs == ? WHERE usuarioNombre == ?",(pks,username))
            db.commit()
            db.close()
            
        fav = favorite_items()
        value = lista_a_cadena(fav)
        save_pk('Rafita-kun',value)

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

        
    # Create window
    root = tk.Tk()
    root.geometry("1366x768")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill='both', expand=True)

    # Add header
    header = tk.Label(frame, text="Pokemons", font=("PressStart2P", 16))
    header.pack(pady=10)

    # Load images into variables
    im_checked = resize_image(relative_to_assets('checked.png'), (15, 15))
    im_unchecked = resize_image(relative_to_assets('unchecked.png'), (15, 15))
    im_tristate = resize_image(relative_to_assets('tristate.png'), (15, 15))

    # Create style for Treeview and scrollbar
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

    # Create Treeview
    treeview_canvas = tk.Canvas(frame)
    treeview_canvas.pack(side="top", fill="both", expand=True)

    tree = ttk.Treeview(treeview_canvas, columns=('col1'), height=5, style="mystyle.Treeview")
    tree.heading('#0', text="ID")
    tree.column('#0', width=60)
    tree.heading('col1', text="Pokemons")
    tree.column('col1', width=100)

    # Create Scrollbar
    scrollbar = ttk.Scrollbar(treeview_canvas, orient="vertical", command=tree.yview, style="mystyle.Vertical.TScrollbar")
    scrollbar.pack(side='right', fill='both')
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side='right', fill='both')

    # Assign images to tags
    tree.tag_configure('unchecked', image=im_unchecked)
    tree.tag_configure('tristate', image=im_tristate)
    tree.tag_configure('checked', image=im_checked)

    # Assign actions to Treeview
    tree.bind('<Button-1>', box_click, True)
    tree.bind("<<TreeviewSelect>>", return_selection)

    # Fill Treeview
    command_to_search_favs()

    # Side canvas for Pokemon details
    canvas = tk.Canvas(treeview_canvas, bg="white", height=300)  # Added height for better layout
    canvas.pack(side="top", fill="both", expand=True)


    # Canvas for buttons
    buttons_canvas = tk.Canvas(root)
    buttons_canvas.pack(side="bottom", fill="x")

    # Create buttons
    Button1 = tk.Button(buttons_canvas, text="Pokedex", width=10, command=command_to_recharge)
    Button2 = tk.Button(buttons_canvas, text="Favoritos", width=10, command=command_to_search_favs)
    boton_ejecutar = tk.Button(buttons_canvas, text="Mostrar 'hola'")

    # Position buttons below Treeview
    Button1.pack(side="right", anchor="se", padx=5)
    Button2.pack(side="right", anchor="se", padx=5)
    boton_ejecutar.pack(side="right", anchor="se", padx=5)

    root.mainloop()

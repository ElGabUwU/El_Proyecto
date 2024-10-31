import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import font
from Books.backend.db_books import *
from validations.books_validations import *
from PIL import Image,ImageTk
import random
from db.conexion import establecer_conexion
from util.utilidades import resource_path
def validate_number_input(text):
        if text == "":
            return True
        try:
            float(text)
            return True
        except ValueError:
            return False



class L_Listar(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.canvas = tk.Canvas(self, bg="#FAFAFA", width=1366, height=768)
        self.canvas.pack(side="right", fill="both", expand=True)
        self.images = {}
        self.book_data = {}  # Inicializar como un diccionario
        
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                            fieldbackground="#2E59A7",
                            background="#2E59A7",
                            bordercolor="#041022",
                            arrowcolor="#ffffff",
                            padding="9")

        self.campo_mapeo = {
        "Cota": "Cota",
        "N.registro": "n_registro",
        "Título": "titulo",
        "Autor": "autor"
        }
        # Añadir un Combobox para seleccionar el campo de búsqueda
        
        
        stylebotn = ttk.Style()
        stylebotn.configure("Rounded.TEntry", 
                            fieldbackground="#031A33", 
                            foreground="#a6a6a6", 
                            borderwidth=0.5, 
                            relief="solid", 
                            padding=5)
        stylebotn.map("Rounded.TEntry",
                      focuscolor=[('focus', '#FFFFFF')],
                      bordercolor=[('focus', '#000716')])

        self.left_frame_list = tk.Frame(self.canvas, bg="#FAFAFA")
        self.left_frame_list.pack(expand=True, side="left", fill="both") #padx=212, pady=150, ipady=80
        self.left_frame_list.place(x=215,y=218, height=470, width=1135)


        """"self.cota = tk.Entry(self, bd=0, bg="WHITE", fg="#031A33", highlightthickness=2, highlightbackground="#ffffff", highlightcolor="#ffffff", relief="solid" , borderwidth=0.5)
        self.cota.place(x=263.0, y=282.0, width=237.0, height=37.5)"""
        
        self.buscar = tk.Entry(self, bg="#FFFFFF", fg="#000000", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.buscar.place(x=245.0, y=112.0, width=267.0, height=48.0)
        


        self.campo_busqueda = ttk.Combobox(self, values=list(self.campo_mapeo.keys()), state="readonly", width=13, font=("Montserrat Medium", 13))
        self.campo_busqueda.place(x=535.0, y=112,height=48)
        self.campo_busqueda.set("Cota")  # Valor por defecto
        


        # Crear textos en el canvas
        self.canvas.create_text(535.0, 89.0, anchor="nw", text="Filtrado de Busqueda", fill="#040F21", font=("Bold", 12))
        self.label_nombre = self.canvas.create_text(245.0, 82.0, anchor="nw", text="Buscar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1177.0, 170.0, text="Editar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1275.0, 170.0, text="Eliminar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(980.0, 170.0, text="Refrescar", fill="#040F21", font=("Bold", 17))
        self.canvas.create_text(1080.0, 170.0, text="Agregar", fill="#040F21", font=("Bold", 17))

        # Títulos para los Treeviews
        bold_font = font.Font(family="Bold", size=15, weight="bold")
        self.label_prestamos = tk.Label(self.canvas, text="Tabla Libros", bg="#FAFAFA", fg="#031A33", font=bold_font)
        self.label_prestamos.place(x=665.0, y=180.0, width=225.0, height=35.0)

        # Para llamar a read_books cuando se presiona Enter
        self.buscar.bind("<Return>", self.boton_buscar)

            # Cargar y almacenar las imágenes
        self.images['boton_agregar'] = tk.PhotoImage(file=resource_path("assets_2/5_agregar.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_agregar'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.open_registrar_window(),
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=1015.0, y=60.0, width=130.0, height=100.0)
        
                    #Boton Cargar Libros
            # Cargar y almacenar las imágenes
        self.images['boton_refrescar'] = tk.PhotoImage(file=resource_path("assets_2/16_refrescar.png"))
            
            # Cargar y almacenar la imagen del botón
        self.button_e = tk.Button(
                self,
                image=self.images['boton_refrescar'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.reading_books(),
                relief="flat",
                bg="#FAFAFA",
                activebackground="#FAFAFA",  # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_e.place(x=915.0, y=60.0, width=130.0, height=100.0)
        
        

        self.images['boton_Eliminar'] = tk.PhotoImage(file=resource_path("assets_2/7_eliminar.png"))
                    # Cargar y almacenar la imagen del botón
        self.button_dl = tk.Button(
            self,
            image=self.images['boton_Eliminar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.verificar_eliminar(),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_dl.place(x=1215.0, y=60.0, width=130.0, height=100.0)

        self.images['boton_modificar'] = tk.PhotoImage(file=resource_path("assets_2/6_editar.png"))
            # Cargar y almacenar la imagen del botón
        self.button_dl = tk.Button(
            self,
            image=self.images['boton_modificar'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_modificar_window(),
            relief="flat",
            bg="#FAFAFA",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#FFFFFF"   # Color del texto cuando el botón está activo
            )
        self.button_dl.place(x=1115.0, y=60.0, width=130.0, height=100.0)

        # Datos y paginación
        self.data = []
        self.page_size = 19
        self.current_page = 0

        self.setup_treeview()
        self.reading_books()
        self.display_page()

    def setup_treeview(self):
        style = ttk.Style()
        style.configure("Rounded.Treeview",
                        borderwidth=2,
                        relief="groove",
                        bordercolor="blue",
                        lightcolor="lightblue",
                        darkcolor="darkblue",
                        rowheight=30,
                        background="#FFFFFF",
                        fieldbackground="#f0f0f0")
        style.configure("Rounded.Treeview.Heading",
                        font=('Helvetica', 10, 'bold'),
                        background="#2E59A7",
                        foreground="#000000",
                        borderwidth=0)
        columns = ("ID", "Sala", "Categoria", "Asignatura", "Cota", "N. Registro", "Título", "Autor", "Editorial", "Año", "Edición", "N° Volúmenes", "N° Ejemplares")
        self.book_table_list = ttk.Treeview(self.left_frame_list, columns=columns, show='headings', style="Rounded.Treeview", selectmode="browse")
        self.book_table_list.column("ID", width=50, anchor="center")
        self.book_table_list.column("Sala", width=50, anchor="center")
        for col in columns:
            if col not in ("ID", "Sala"):
                self.book_table_list.column(col, width=85, anchor="center")
            self.book_table_list.heading(col, text=col)
        self.book_table_list.pack(expand=True, fill="both", padx=30, pady=5)
        scrollbar_pt = ttk.Scrollbar(self.book_table_list, orient="vertical", command=self.book_table_list.yview)
        self.book_table_list.configure(yscrollcommand=scrollbar_pt.set)
        scrollbar_pt.pack(side="right", fill="y")
        self.book_table_list.bind("<Double-1>", self.on_book_double_click)

        prev_button = tk.Button(
            self.left_frame_list,
            text="< Anterior",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            font=("Montserrat Regular", 15),
            bg="#FAFAFA",
            fg="#006ac2",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#006ac2",   # Color del texto cuando el botón está activo
            command=self.previous_page
            )
        prev_button.pack(side=tk.LEFT, padx=10, pady=10)
        next_button = tk.Button(
            self.left_frame_list,
            text="Siguiente >",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            font=("Montserrat Regular", 15),
            bg="#FAFAFA",
            fg="#006ac2",
            activebackground="#FAFAFA",  # Mismo color que el fondo del botón
            activeforeground="#006ac2",
            command=self.next_page)
        next_button.pack(side=tk.RIGHT, padx=10, pady=10)
        # Etiqueta para mostrar la página actual
        self.page_label = tk.Label(self.left_frame_list, text=f"Página {self.current_page + 1}", bg="#FAFAFA", fg="#031A33",font=("Montserrat Regular", 13))
        self.page_label.pack(side=tk.BOTTOM, pady=15)
    def get_data_page(self, offset, limit):
        return self.data[offset:offset + limit]

    def display_page(self):
        for row in self.book_table_list.get_children():
            self.book_table_list.delete(row)
        page_data = self.get_data_page(self.current_page * self.page_size, self.page_size)
        for fila in page_data:
            n_ejemplares = fila[12]
            tag = 'multiple' if n_ejemplares > 1 else 'single'
            self.book_table_list.insert("", "end", values=fila, tags=(tag,))
        self.book_table_list.tag_configure('multiple', background='lightblue')
        self.book_table_list.tag_configure('single', background='#E5E1D7')
        self.update_page_label()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.data):
            self.current_page += 1
            self.display_page()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()
    def update_page_label(self):
        self.page_label.config(text=f"Página {self.current_page + 1}")
    def verificar_eliminar(self):
        if self.parent.id_rol == 1:
            print("Sin permisos suficientes para eliminar!")
            messagebox.showinfo("AVISO", "Sin permisos suficientes para eliminar!")
        
        else:
            delete_selected(self)
    def open_registrar_window(self):
        # Llamar directamente a la clase L_Registrar sin necesidad de seleccionar un elemento
        L_Registrar(self.parent)

    def open_modificar_window(self):
         selected_items = self.book_table_list.selection()
         if selected_items:
             selected_item = selected_items[0]
             item_values = self.book_table_list.item(selected_item, "values")
             L_Modificar(item_values)
         else:
             messagebox.showwarning("Advertencia", "No hay ningún elemento seleccionado. Debe seleccionar un libro para modificarlo.")
    
    def boton_buscar(self, event):
        busqueda = self.buscar.get()
        campo_seleccionado = self.campo_busqueda.get()  # Obtener el campo seleccionado
        campo_real = self.campo_mapeo[campo_seleccionado]  # Traducir al nombre real de la columna
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                query = f"SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, titulo, autor, editorial, año, edicion FROM libro WHERE {campo_real}=%s"
                cursor.execute(query, (busqueda,))
                resultados = cursor.fetchall()
                self.book_table_list.delete(*self.book_table_list.get_children())
                for fila in resultados:
                    if busqueda in map(str, fila):
                        self.book_table_list.insert("", "end", values=tuple(fila))
                if resultados:
                    messagebox.showinfo("Búsqueda Éxitosa", "Resultados en pantalla.")
                else:
                    messagebox.showinfo("Búsqueda Fallida", "No se encontraron resultados.")
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)


   

    # def boton_buscar(self, event):
    #     busqueda= self.buscar.get()
    #     try:
    #          mariadb_conexion = establecer_conexion()
    #          if mariadb_conexion:#.is_connected():
    #                     cursor = mariadb_conexion.cursor()
    #                     cursor.execute("""SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota,
    #                                     n_registro, titulo, autor, editorial, año, edicion FROM libro WHERE 
    #                                     ID_Libro=%s OR ID_Sala=%s OR ID_Categoria=%s OR 
    #                                     ID_Asignatura=%s OR Cota=%s OR n_registro=%s OR 
    #                                     titulo=%s OR autor=%s OR editorial=%s OR 
    #                                     año=%s OR edicion=%s""", 
    #                        (busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda, busqueda))
    #                     resultados = cursor.fetchall() 

    #                     self.book_table_list.delete(*self.book_table_list.get_children())
    #                     for fila in resultados:
    #                         self.book_table_list.insert("", "end", values=tuple(fila))
    #                         if busqueda in fila:
    #                             self.book_table_list.item(self.book_table_list.get_children()[-1], tags='match')
    #                         else:
    #                             self.book_table_list.item(self.book_table_list.get_children()[-1], tags='nomatch')
    #                     self.book_table_list.tag_configure('match', background='green')
    #                     self.book_table_list.tag_configure('nomatch', background='gray')
    #                     if resultados:
    #                         messagebox.showinfo("Busqueda Éxitosa", "Resultados en pantalla.")
    #                     else:
    #                         messagebox.showinfo("Busqueda Fallida", "No se encontraron resultados.")
    #     except mariadb.Error as ex:
    #             print("Error durante la conexión:", ex)
        
    def on_book_double_click(self, event):
        try:
            selected_item = self.book_table_list.selection()[0]
            libro_valores = self.book_table_list.item(selected_item, 'values')

            self.book_data = {
                "ID": libro_valores[0],
                "ID_Sala": libro_valores[1],
                "ID_Categoria": libro_valores[2],
                "ID_Asignatura": libro_valores[3],
                "Cota": libro_valores[4],
                "n_registro": libro_valores[5],
                "Titulo": libro_valores[6],
                "Autor": libro_valores[7],
                "Editorial": libro_valores[8],
                "Año": libro_valores[9],
                "Edicion": libro_valores[10],
                "n_volumenes": libro_valores[11],
                "n_ejemplares": libro_valores[12]  # Asegúrate de que coincida con tu índice
            }

            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()

                cursor.execute('''
                    SELECT ID_Libro
                    FROM libro
                    WHERE autor = %s AND editorial = %s AND titulo = %s AND año = %s
                ''', (self.book_data["Autor"], self.book_data["Editorial"], self.book_data["Titulo"], self.book_data["Año"]))

                ejemplares = cursor.fetchall()

                for ejemplar in ejemplares:
                    # Encuentra el ID_Libro en el Treeview y selecciónalo
                    for row in self.book_table_list.get_children():
                        if self.book_table_list.item(row, 'values')[0] == str(ejemplar[0]):
                            self.book_table_list.selection_add(row)

                mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
            messagebox.showerror("Error", f"Error durante la conexión: {ex}")
        except IndexError:
            print("No se ha seleccionado ningún libro.")
            messagebox.showerror("Error", "No se ha seleccionado ningún libro.")

    def open_filter_window(self):
        filter_window = tk.Toplevel(self)
        filter_window.title("Filtrar")
        filter_window.iconbitmap(relative_to_assets('logo_biblioteca.ico'))

        self.bg_image = tk.PhotoImage(file=relative_to_assets("Fondo Botones V1.png"))
        # Crear un Label para la imagen de fondo
        bg_label = tk.Label(filter_window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(filter_window, text="Sala", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=0, column=0, padx=10, pady=5)
        self.sala_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.sala_entry.pack(expand=False)

        tk.Label(filter_window, text="Categoria", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=0, column=2, padx=10, pady=5)
        self.categoria_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.categoria_entry.pack(expand=False)

        tk.Label(filter_window, text="Asignatura", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=0, column=4, padx=10, pady=5)
        self.asignatura_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.asignatura_entry.pack(expand=False)

        tk.Label(filter_window, text="Cota", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=0, column=6, padx=10, pady=5)
        self.cota_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.cota_entry.pack(expand=False)

        tk.Label(filter_window, text="Autor", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=1, column=0, padx=10, pady=5)
        self.autor_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.autor_entry.pack(expand=False)

        tk.Label(filter_window, text="Titulo", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=1, column=2, padx=10, pady=5)
        self.titulo_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.titulo_entry.pack(expand=False)

        tk.Label(filter_window, text="N° Registro", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=1, column=4, padx=10, pady=5)
        self.n_registro_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.n_registro_entry.pack(expand=False)

        tk.Label(filter_window, text="Año", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=2, column=0, padx=10, pady=5)
        self.año_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.año_entry.pack(expand=False)

        tk.Label(filter_window, text="Edicion", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=2, column=2, padx=10, pady=5)
        self.edicion_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.edicion_entry.pack(expand=False)

        tk.Label(filter_window, text="Editorial", fg="black", bg="white").pack(pady=5,expand=False)#.grid(row=2, column=4, padx=10, pady=5)
        self.editorial_entry = tk.Entry(filter_window, fg="black", bg="lightgray", relief="flat", highlightthickness=2)
        self.editorial_entry.pack(expand=False)
        
        # Crear un estilo personalizado
        style = ttk.Style()
        style.configure("Custom.TButton", background="#f80000", foreground="black")

        search_button = ttk.Button(filter_window, text="Buscar", command=self.filter_books, style="Custom.TButton")
        search_button.pack(pady=5, expand=False)

        button_cancel = ttk.Button(filter_window, text="Cancelar", command=lambda: self.cancelar(filter_window), style="Custom.TButton")
        button_cancel.pack(pady=5, expand=False)

        # Vincular el evento de escritura
        self.n_registro_entry.bind("<KeyRelease>", lambda event: self.format_n_registro(event))

    def format_n_registro(self, event):
        # Obtener el texto actual del campo de entrada
        text = self.n_registro_entry.get().replace(".", "")
        
        # Formatear el texto para insertar un punto después de las tres primeras cifras
        if len(text)> 1:
            formatted_text = text[:1] + "." + text[1:]
        else:
            formatted_text = text

        # Actualizar el campo de entrada con el texto formateado
        self.n_registro_entry.delete(0, tk.END)
        self.n_registro_entry.insert(0, formatted_text)

    def filter_books(self):
        sala = self.sala_entry.get().lower() or self.sala_entry.get().upper()
        categoria = self.categoria_entry.get().lower() or self.sala_entry.get().upper()
        asignatura = self.asignatura_entry.get().lower() or self.sala_entry.get().upper()
        cota = self.cota_entry.get().lower() or self.sala_entry.get().upper()
        autor = self.autor_entry.get().lower() or self.sala_entry.get().upper()
        titulo = self.titulo_entry.get().lower() or self.sala_entry.get().upper()
        n_registro = self.n_registro_entry.get().lower() or self.sala_entry.get().upper()
        año = self.año_entry.get().lower() or self.sala_entry.get().upper()
        edicion = self.edicion_entry.get().lower() or self.sala_entry.get().upper()
        editorial = self.editorial_entry.get().lower() or self.sala_entry.get().upper()
        self.salas_types = [
        "3G", "2E", "1I","3g","2e","1i"
        ]
        for row in self.book_table_list.get_children():
            values = self.book_table_list.item(row, "values")
              # Convertir los valores a enteros si es posible, de lo contrario mantenerlos como cadenas
            converted_values = []
            for value in values:
                try:
                    converted_values.append(int(value))
                except ValueError:
                    converted_values.append(value)
            values = [str(value) for value in values]
            if (sala in self.salas_types and
                categoria in values[2].lower() and values[2].upper() and
                asignatura in values[3].lower() and values[3].upper() and
                cota in values[4].lower() and values[4].upper() and
                autor in values[7].lower() and values[7].upper() and
                titulo in values[6].lower() and values[6].upper() and
                n_registro in values[5].lower() and values[5].upper() and
                año in values[9].lower() and values[9].upper() and
                edicion in values[10].lower() and values[10].upper() and
                editorial in values[8].lower() and values[8].upper()):
                self.book_table_list.item(row, tags='match')
            else:
                self.book_table_list.item(row, tags='nomatch')

        self.book_table_list.tag_configure('match', background='green')
        self.book_table_list.tag_configure('nomatch', background='gray')
    def reading_books(self):
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                cursor.execute('''
                    SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, titulo, autor, editorial, año, edicion, n_volumenes, n_ejemplares
                    FROM libro WHERE estado_libro='activo'
                ''')
                self.data = cursor.fetchall()
                mariadb_conexion.close()
                self.display_page()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
        except subprocess.CalledProcessError as e:
            print("Error al importar el archivo SQL:", e)
            
            #CARGAR LIBROS FUNCION ANTIGUA!
    """def reading_books(self, book_table_list):
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                cursor.execute('''
                    SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, titulo, autor, editorial, año, edicion, n_volumenes, n_ejemplares
                    FROM libro WHERE estado_libro='activo'
                ''')
                resultados = cursor.fetchall()
                
                # Limpiar la tabla antes de insertar nuevos datos
                for row in book_table_list.get_children():
                    book_table_list.delete(row)
                
                # Configurar las etiquetas para los colores
                book_table_list.tag_configure('multiple', background='lightblue')
                book_table_list.tag_configure('single', background='#E5E1D7')
                
                # Insertar los datos en el Treeview
                for fila in resultados:
                    book_id = fila[0]
                    n_ejemplares = fila[12]
                    tag = 'multiple' if n_ejemplares > 1 else 'single'
                    book_table_list.insert("", "end", values=tuple(fila), tags=(tag,))
                    
                
                mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
        except subprocess.CalledProcessError as e:
            print("Error al importar el archivo SQL:", e)"""
   

    def cancelar(self, window):
        if messagebox.askyesno("Advertencia", "¿Seguro que quieres cerrar esta ventana?"):
            window.destroy()  

from validations.books_validations import *

class L_Registrar(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.grab_set()
        self.canvas = tk.Canvas(self, bg="#031A33", width=1356, height=530)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.resizable(False, False)
        self.iconbitmap(resource_path('assets_2/logo_biblioteca.ico'))
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancelar(self))
       # validate_number = self.register(validat e_number_input)
        self.images = {}
        self.salas_types = ["1I", "2E", "3G"]
        self.categoria_types_general=["Ciencias de la Computación, Información y Obras Generales", "Filosofía y Psicología", "Religión-Teología", "Ciencias Sociales","Lenguas",
        "Ciencias Básicas","Tecnología y Ciencias Aplicadas","Artes y recreación","Literatura","Historia y Geografía"]
        self.asignature_type_general= ["Almanaques Mundiales","Computacion","Enciclopedia","Enciclopedia y Diccionarios","Filosofía","Filosofía-Diccionarios",
        "Informática","Metodología de la Investigación","Periodismo","Psicología","Psicología-Diccioanrios","Religión",
        "Educación Familiar y Ciudadana","Sociología","Medios de Comunicación","Mujer y Familia","Estadística Social",
        "Ciencias Políticas", "Economía Venezolana","Geografía Económica","Microeconomía","Macroeconomía","Derecho",
        "Derecho Constitucional","Derecho Laboral","Derecho Penal","Límites y Fronteras","Administración Pública","Premilitar",                                  "Servicios Sociales", "Filosofía de la Educación","Educación","Educación Rural","Pedagogía","Técnicas de Estudio",
        "Orientación", "Educación Preescolar","Educación Superior","Medios de Transporte","Currículo","Educación Básica",                                  "Publicaciones Oficiales-Folklore","Lenguaje","Linguística-Diccionarios","Lengua y Comunicación","Castellano y Literatura",
        "Inglés","Castellano","Química-Física-Diccionarios","Botánica-Zoología-Diccionarios","Matemática","Ciencia",
        "Estudios de la Naturaleza", "Álgebra","Matemática Financiera","Cálculo","Geometría","Astronomía","Física","Electricidad",
        "Electrónica", "Química","Fisioquímica","Química Orgánica","Ciencias de la Tierra","Biología","Medicina-Diccionarios",
        "Agricultura-Diccionarios","Biología Celular","Zoología","Ecología","Bioquímica","Enfermería","Anatomía Humana",
        "Contaminación Ambiental","Seguridad Industrial","Naturismo","Drogar","Enfermedades Varias","Pediatría","Ingeniería","Reciclaje",
        "Agricultura","Fertilizantes","Cultivos","Fruticultura","Ganadería","Comercio","Contabilidad","Administración",
        "Administración de Emperesa","Avicultura","Nutrición","Ganadería","Zootecnia","Administración de Personal","Mercadotecnia",
        "Historial del Arte","Dibujo","Arte y Recreación-Diccionarios","Artística","Artes Plásticas y Escultura","Pintura","Música",
        "Educación Física","Deportes","Literatura-Diccioanrios","Literatura","Novelas","Novelas Venezolanas","Poesías","Historia Universal",
        "Geografía General","Geografía de Venezuela","Historia","Historia de América","Historia Europea","Historia-Diccionarios"]
        self.categoria_types_state=["Estadal-B"]
        self.asignature_types_state= ["Bibliografia-Estadal","Historia Local-Rubio-Junin","Publicaciones Periódicas"]
        self.categoria_types_children=["Infantil-X"]
        self.asignature_types_children= ["Matemáticas","Castellano y Literatura","Ciencias Naturales","Petróleo","Agricultura","Cuentos Venezolanos",
        "Fábulas","Novelas Históricas","Sección de los más pequeños","Cuentos de Animales","Novelas de Aventuras",
        "Cuentos de Hadas y Fantasía","Cuentos Realistas","Poesías y Canciones Venezolanas","Cuentos de Aventuras",
        "Teatro","Teatro Venezolano","Fábulas Venezolanas","Mitos y Leyendas Venezolanas"]
        
        # Cargar y almacenar las imágenes
        self.images['boton_R'] = tk.PhotoImage(file=resource_path("assets_2/R_button_light_blue.png"))

            # Crear el botón con la imagen inicial

            # Crear el botón
        boton_R = self.images['boton_R']
        tk.Button(
                self,
                image=boton_R,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.register_book(),
                relief="flat",
                bg="#031A33",
                activebackground="#031A33", # Mismo color que el fondo del botón
                activeforeground="#FFFFFF"  # Color del texto cuando el botón está activo
            ).place(x=61.0, y=465.0, width=130.0, height=40.0)
        
        self.images['boton_c'] = tk.PhotoImage(file=resource_path("assets_2/c_button_red1.png"))
        self.boton_C = tk.Button(
            self,
            image=self.images['boton_c'],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.cancelar(self),
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_C.place(x=250.0, y=465.0, width=130.0, height=40.0)
          
            
        
        self.inicializar_titulos()
        self.inicializar_campos_y_widgets()
        self.validacion_sala(None)
    #def are_u_sure(self):
    
    def cancelar(self, window):
        if messagebox.askyesno("Advertencia", "¿Seguro que quieres cerrar esta ventana? Perderás todos los datos del libro que estás registrando.", parent=self):
            window.destroy()

    def inicializar_titulos(self):
        
        self.canvas.create_rectangle(0, 0, 1356, 74, fill="#2E59A7")
        # Títulos de los inputs
        self.canvas.create_text(535.0, 21.0, anchor="nw", text="Registro de Libros", fill="#ffffff", font=("Montserrat Medium", 28))
        self.canvas.create_text(61.0, 106.0, anchor="nw", text="Ingrese la información del libro a registrar", fill="#a6a6a6", font=("Bold", 17))
        
        # Fila 1
        self.canvas.create_text(61.0, 152.0, anchor="nw", text="Sala", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(378.0, 152.0, anchor="nw", text="Categoría", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(695.0, 152.0, anchor="nw", text="Asignatura", fill="#a6a6a6", font=("Bold", 17))
        
        # Fila 2
        self.canvas.create_text(61.0, 252.0, anchor="nw", text="Cota", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(378.0, 252.0, anchor="nw", text="Número de registro", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(695.0, 252.0, anchor="nw", text="Edición", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1016.0, 252.0, anchor="nw", text="N° volumen", fill="#a6a6a6", font=("Bold", 17))
        
        # Fila 3
        self.canvas.create_text(61.0, 352.0, anchor="nw", text="Título", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(378.0, 352.0, anchor="nw", text="Autor", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(695.0, 352.0, anchor="nw", text="Editorial", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1016.0, 352.0, anchor="nw", text="Año", fill="#a6a6a6", font=("Bold", 17))
    def inicializar_campos_y_widgets(self):
        validate_number = self.register(validate_number_input)
        # Configuración del estilo de los Combobox
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                            fieldbackground="#2E59A7",
                            background="#2E59A7",
                            bordercolor="#041022",
                            arrowcolor="#ffffff",
                            padding="9")

        # Combobox para Sala
        self.combobox1 = ttk.Combobox(self, values=self.salas_types, state="readonly", width=37, font=("Montserrat Medium", 10))
        self.combobox1.place(x=61.0, y=181.5)
        self.combobox1.set("1I")  # Establece el valor inicial a "1I"
        self.combobox1.bind("<<ComboboxSelected>>", self.validacion_sala)

        # Combobox para Categoría
        self.categoria_cb = ttk.Combobox(self, state="readonly", width=37, font=("Montserrat Medium", 10))
        self.categoria_cb.place(x=378.0, y=181.5)
        self.categoria_cb.set("No se ha seleccionado una categoría")
        # Combobox para Asignatura
        self.asignatura_cb = ttk.Combobox(self, state="readonly", width=37, font=("Montserrat Medium", 10))
        self.asignatura_cb.place(x=695.0, y=181.5)
        self.asignatura_cb.set("No se ha seleccionado una asignatura")
        

        # Crear y colocar los widgets
        # Primera fila
        self.cota = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.cota.place(x=61.0, y=282.0, width=297.0, height=37.5)
        self.cota.bind("<Return>", self.focus_next_widget)
        self.cota.bind("<KeyPress>",self.on_key_press)
        

        self.registro_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.registro_m.place(x=378.0, y=282.0, width=297.0, height=38.0)
        self.registro_m.bind("<Return>", self.focus_next_widget)
        self.registro_m.bind("<KeyPress>",self.on_key_press)

        self.edicion_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.edicion_m.place(x=695.0, y=282.0, width=297.0, height=37.5)
        self.edicion_m.bind("<Return>", self.focus_next_widget)
        self.edicion_m.bind("<KeyPress>",self.on_key_press)

        self.volumen_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.volumen_m.place(x=1016.0, y=282.0, width=297.0, height=37.5)
        self.volumen_m.bind("<Return>", self.focus_next_widget)
        self.volumen_m.bind("<KeyPress>",self.on_key_press)

        # Segunda fila
        self.titulo_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.titulo_m.place(x=61.0, y=382.0, width=297.0, height=37.5)
        self.titulo_m.bind("<Return>", self.focus_next_widget)
        self.titulo_m.bind("<KeyPress>", self.on_key_press)  # Formatear al perder el foco

        self.autor_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key")
        self.autor_m.place(x=378.0, y=382.0, width=297.0, height=37.5)
        self.autor_m.bind("<Return>", self.focus_next_widget)
        self.autor_m.bind("<KeyPress>", self.on_key_press)
        

        self.editorial_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key")
        self.editorial_m.place(x=695.0, y=382.0, width=297.0, height=37.5)
        self.editorial_m.bind("<Return>", self.focus_next_widget)
        self.editorial_m.bind("<KeyPress>", self.on_key_press)

        self.ano_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.ano_m.place(x=1016.0, y=382.0, width=297.0, height=37.5)
        self.ano_m.bind("<Return>",lambda event : self.register_book())
        self.ano_m.bind("<KeyPress>",self.on_key_press)
    
    def on_key_press(self, event):
        widget = event.widget
        current_text = widget.get()
        
        if widget == self.cota:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not allow_only_letters_numbers_dots(event.char):
                return "break"
            
            # Guardar la posición del cursor antes de añadir el nuevo carácter
            cursor_position = widget.index(tk.INSERT)
            
            # Añadir el nuevo carácter al texto actual en la posición del cursor
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            
            # Limitar la longitud y convertir a mayúsculas antes de actualizar el widget
            new_text = limitar_longitud_cota(new_text)
            formatted_text = convert_to_uppercase(new_text)

            # Actualizar el campo de entrada
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            
            # Restaurar la posición del cursor
            widget.icursor(cursor_position + 1)

            return "break"
        elif widget == self.registro_m:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not allow_only_numbers_and_dot_at_thousands(current_text + event.char):
                return "break"
            formatted_text = current_text + event.char
            formatted_text = current_text
        elif widget == self.titulo_m:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isalpha() and event.char not in " áéíóúÁÉÍÓÚñÑ.,;:!?¿¡-":
                return "break"
            current_text = longitud_titulo(current_text)
            current_text = format_title(current_text)
            formatted_text = validate_and_format_title(current_text)
        elif widget == self.autor_m:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isalpha() and event.char != " ":
                return "break"
            current_text = longitud_autor(current_text)
            formatted_text = validar_y_formatear_texto(current_text)
            
        elif widget == self.editorial_m:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isalpha() and event.char != " ":
                return "break"
            current_text = longitud_editorial(current_text)
            formatted_text = validar_y_formatear_texto(current_text)
        elif widget == self.ano_m:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isdigit():
                return "break"
            current_text = widget.get()  # Obtener texto actual sin añadir el nuevo carácter aún
            if len(current_text) >= 4:
                return "break"
            # Permitir añadir el nuevo carácter si no excede la longitud
            formatted_text = current_text[:widget.index(tk.INSERT)] + event.char + + current_text[widget.index(tk.INSERT):]
        elif widget == self.edicion_m:
            resultado = validar_digitos(event, longitud_nro_edicion)
            if resultado == "break":
                return "break"
            formatted_text = resultado

        elif widget == self.volumen_m:
            resultado = validar_digitos(event, longitud_volumen)
            if resultado == "break":
                return "break"
            formatted_text = resultado

        # Guardar la posición del cursor
        cursor_position = widget.index(tk.INSERT)

        # Actualizar el campo de entrada
        widget.delete(0, tk.END)
        widget.insert(0, formatted_text)

        # Restaurar la posición del cursor
        widget.icursor(cursor_position)
        event.widget.after(1,formatted_text)
    
    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    
        
        
    def actualizar_opciones(self, combobox, values):
        combobox['values'] = values

    def mostrar_opciones(self, categoria_values, asignatura_values):
        self.actualizar_opciones(self.categoria_cb, categoria_values)
        self.actualizar_opciones(self.asignatura_cb, asignatura_values)

    def validacion_sala(self, event):
        sala_seleccionada = self.combobox1.get()

        # Establecer los valores por defecto
        if sala_seleccionada == "1I":
            self.categoria_cb.set("No se ha seleccionado una categoría")
            self.asignatura_cb.set("No se ha seleccionado una asignatura")
            self.mostrar_opciones(self.categoria_types_children, self.asignature_types_children)
        elif sala_seleccionada == "2E":
            self.categoria_cb.set("No se ha seleccionado una categoría")
            self.asignatura_cb.set("No se ha seleccionado una asignatura")
            self.mostrar_opciones(self.categoria_types_state, self.asignature_types_state)
        elif sala_seleccionada == "3G":
            self.categoria_cb.set("No se ha seleccionado una categoría")
            self.asignatura_cb.set("No se ha seleccionado una asignatura")
            self.mostrar_opciones(self.categoria_types_general, self.asignature_type_general)
        else:
            messagebox.showwarning("Validación", "Por favor, seleccione una opción válida.")

    
        #-------------------------------------------------------------------------------
            
        
    def register_book(self):
        ID_Sala = self.combobox1.get()
        ID_Categoria = self.categoria_cb.get() if self.categoria_cb else None
        ID_Asignatura = self.asignatura_cb.get() if self.asignatura_cb else None
        Cota = self.cota.get()
        n_registro = self.registro_m.get()
        edicion = self.edicion_m.get()
        n_volumenes = self.volumen_m.get()
        titulo = self.titulo_m.get()
        autor = self.autor_m.get()
        editorial = self.editorial_m.get()
        año = self.ano_m.get()

        # Validar los campos
        errores = validar_campos(
            ID_Categoria,
            ID_Asignatura,
            Cota,
            titulo,
            autor,
            editorial,
            n_registro,
            n_volumenes,
            edicion,
            año,
            None  # No hay ID de libro para registro
        )
        print(f"Errores: {errores}")  # Agregar esta línea para depuración

        if errores:        
            messagebox.showerror("Error al registrar", "Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"- {msg}" for msg in errores),parent=self)
            return

        # Depuración de los valores que se van a pasar a create_books
        print(f"Valores para registro: ID_Sala={ID_Sala}, ID_Categoria={ID_Categoria}, ID_Asignatura={ID_Asignatura}, Cota={Cota}, n_registro={n_registro}, edicion={edicion}, n_volumenes={n_volumenes}, titulo={titulo}, autor={autor}, editorial={editorial}, año={año}")

        if create_books(ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año):
            messagebox.showinfo("Éxito", "Registro del libro éxitoso.",parent=self)
            self.clear_entries_register()
            
        # else:
        #     messagebox.showinfo("Registro fallido", "Libro mantiene sus valores.",parent=self)

    
    def clear_entries_register(self):
        self.combobox1.set("1I")
        self.categoria_cb.set("No se ha seleccionado una categoría")
        self.asignatura_cb.set("No se ha seleccionado una asignatura")
        self.cota.delete(0, tk.END)
        self.registro_m.delete(0, tk.END)
        self.edicion_m.delete(0, tk.END)
        self.volumen_m.delete(0, tk.END)
        self.titulo_m.delete(0, tk.END)
        self.autor_m.delete(0, tk.END)
        self.editorial_m.delete(0, tk.END)
        self.ano_m.delete(0, tk.END)

    



class L_Modificar(tk.Toplevel):      
    def __init__(self,book_data, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.title("Modificar")
        self.book_data = book_data
        self.protocol("WM_DELETE_WINDOW", lambda: self.cancelar(self))
        
        self.grab_set()
        
        """self.geometry("1366x768")
        longitudes = obtener_longitudes_min_max()
        if longitudes:
            for campo, valores in longitudes.items():
                print(f"{campo.capitalize()}: Longitud mínima = {valores['min']}, Longitud máxima = {valores['max']}")"""
        #validate_volumenes = self.register(self.validar_numero_volumenes_edicion)
        #validate_volumenes = self.register(self.validar_numero_volumenes_edicion)
        
        self.images = {}
        
        
        self.salas_types = ["1I", "2E", "3G"]
        self.categoria_types_general=["Ciencias de la Computación, Información y Obras Generales", "Filosofía y Psicología", "Religión-Teología", "Ciencias Sociales","Lenguas",
        "Ciencias Básicas","Tecnología y Ciencias Aplicadas","Artes y recreación","Literatura","Historia y Geografía"]
        self.asignature_type_general= ["Almanaques Mundiales","Computacion","Enciclopedia","Enciclopedia y Diccionarios","Filosofía","Filosofía-Diccionarios",
        "Informática","Metodología de la Investigación","Periodismo","Psicología","Psicología-Diccioanrios","Religión",
        "Educación Familiar y Ciudadana","Sociología","Medios de Comunicación","Mujer y Familia","Estadística Social",
        "Ciencias Políticas", "Economía Venezolana","Geografía Económica","Microeconomía","Macroeconomía","Derecho",
        "Derecho Constitucional","Derecho Laboral","Derecho Penal","Límites y Fronteras","Administración Pública","Premilitar",                                  "Servicios Sociales", "Filosofía de la Educación","Educación","Educación Rural","Pedagogía","Técnicas de Estudio",
        "Orientación", "Educación Preescolar","Educación Superior","Medios de Transporte","Currículo","Educación Básica",                                  "Publicaciones Oficiales-Folklore","Lenguaje","Linguística-Diccionarios","Lengua y Comunicación","Castellano y Literatura",
        "Inglés","Castellano","Química-Física-Diccionarios","Botánica-Zoología-Diccionarios","Matemática","Ciencia",
        "Estudios de la Naturaleza", "Álgebra","Matemática Financiera","Cálculo","Geometría","Astronomía","Física","Electricidad",
        "Electrónica", "Química","Fisioquímica","Química Orgánica","Ciencias de la Tierra","Biología","Medicina-Diccionarios",
        "Agricultura-Diccionarios","Biología Celular","Zoología","Ecología","Bioquímica","Enfermería","Anatomía Humana",
        "Contaminación Ambiental","Seguridad Industrial","Naturismo","Drogar","Enfermedades Varias","Pediatría","Ingeniería","Reciclaje",
        "Agricultura","Fertilizantes","Cultivos","Fruticultura","Ganadería","Comercio","Contabilidad","Administración",
        "Administración de Emperesa","Avicultura","Nutrición","Ganadería","Zootecnia","Administración de Personal","Mercadotecnia",
        "Historial del Arte","Dibujo","Arte y Recreación-Diccionarios","Artística","Artes Plásticas y Escultura","Pintura","Música",
        "Educación Física","Deportes","Literatura-Diccioanrios","Literatura","Novelas","Novelas Venezolanas","Poesías","Historia Universal",
        "Geografía General","Geografía de Venezuela","Historia","Historia de América","Historia Europea","Historia-Diccionarios"]
        self.categoria_types_state=["Estadal-B"]
        self.asignature_types_state= ["Bibliografia-Estadal","Historia Local-Rubio-Junin","Publicaciones Periódicas"]
        self.categoria_types_children=["Infantil-X"]
        self.asignature_types_children= ["Matemáticas","Castellano y Literatura","Ciencias Naturales","Petróleo","Agricultura","Cuentos Venezolanos",
        "Fábulas","Novelas Históricas","Sección de los más pequeños","Cuentos de Animales","Novelas de Aventuras",
        "Cuentos de Hadas y Fantasía","Cuentos Realistas","Poesías y Canciones Venezolanas","Cuentos de Aventuras",
        "Teatro","Teatro Venezolano","Fábulas Venezolanas","Mitos y Leyendas Venezolanas"]



        # Convertir book_data en un diccionario manteniendo los índices originales
        self.book_data = {
            "ID": book_data[0],
            "ID_Sala": book_data[1],
            "ID_Categoria": book_data[2],
            "ID_Asignatura": book_data[3],
            "Cota": book_data[4],
            "n_registro": book_data[5],
            "Titulo": book_data[6],
            "Autor": book_data[7],
            "Editorial": book_data[8],
            "Año": book_data[9],
            "Edicion": book_data[10],
            "Volumen": book_data[11],  # Repetido intencionalmente
            "Ejemplares": book_data[12]  # Repetido intencionalmente
        }
        
        self.original_values = self.book_data.copy()  # Copia el diccionario


        self.canvas = tk.Canvas(self, bg="#031A33", width=1356, height=530)
        self.canvas.pack(side="left", fill="both", expand=False)
        self.resizable(False, False)
        self.iconbitmap(resource_path('assets_2/logo_biblioteca.ico'))
        
        
        self.inicializar_titulos()
        self.inicializar_campos_y_widgets()
        self.crear_boton_modificar()
        self.crear_boton_modificar_inactivo()
        self.crear_boton_restaurar()
        self.crear_boton_cancelar()
        self.insert_values_book()

        
        
      
        # Validar y actualizar comboboxes basados en los datos iniciales
        self.validacion_sala(None)

    
    def inicializar_titulos(self):
        self.canvas.create_rectangle(0, 0, 1356, 74, fill="#2E59A7")
        
        self.canvas.create_text(535.0, 21.0, anchor="nw", text="Modificacion de Libros", fill="#ffffff", font=("Montserrat Medium", 28))
        # Títulos de los inputs
        self.canvas.create_text(61.0, 106.0, anchor="nw", text=f"Modificación del libro con el ID:{self.book_data['ID']}", fill="#a6a6a6", font=("Bold", 17))
        
        # Fila 1
        self.canvas.create_text(61.0, 152.0, anchor="nw", text="Sala", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(378.0, 152.0, anchor="nw", text="Categoría", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(695.0, 152.0, anchor="nw", text="Asignatura", fill="#a6a6a6", font=("Bold", 17))
        
        # Fila 2
        self.canvas.create_text(61.0, 252.0, anchor="nw", text="Cota", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(378.0, 252.0, anchor="nw", text="Número de registro", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(695.0, 252.0, anchor="nw", text="Edición", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1016.0, 252.0, anchor="nw", text="N° volumen", fill="#a6a6a6", font=("Bold", 17))
        
        # Fila 3
        self.canvas.create_text(61.0, 352.0, anchor="nw", text="Título", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(378.0, 352.0, anchor="nw", text="Autor", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(695.0, 352.0, anchor="nw", text="Editorial", fill="#a6a6a6", font=("Bold", 17))
        self.canvas.create_text(1016.0, 352.0, anchor="nw", text="Año", fill="#a6a6a6", font=("Bold", 17))

        
    
        
    def inicializar_campos_y_widgets(self):
        validate_number = self.register(validate_number_input)
        # Configuración del estilo de los Combobox
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                            fieldbackground="#2E59A7",
                            background="#2E59A7",
                            bordercolor="#041022",
                            arrowcolor="#ffffff",
                            padding="9")

        # Combobox para Sala
        self.combobox1 = ttk.Combobox(self, values=self.salas_types, state="readonly", width=37, font=("Montserrat Medium", 10))
        self.combobox1.place(x=61.0, y=181.5)
        self.combobox1.bind("<<ComboboxSelected>>", self.validacion_sala)
        
        
        # Combobox para Categoría
        self.categoria_cb = ttk.Combobox(self, values=self.categoria_types_general, state="readonly", width=37, font=("Montserrat Medium", 10))
        self.categoria_cb.place(x=378.0, y=181.5)
        self.categoria_cb.bind("<<ComboboxSelected>>", self.check_changes)

        # Combobox para Asignatura
        self.asignatura_cb = ttk.Combobox(self, values=self.asignature_type_general, state="readonly", width=37, font=("Montserrat Medium", 10))
        self.asignatura_cb.place(x=695.0, y=181.5)
        self.asignatura_cb.bind("<<ComboboxSelected>>", self.check_changes)

        # Crear y colocar los widgets
        # Primera fila
        self.cota = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.cota.place(x=61.0, y=282.0, width=297.0, height=37.5)
        self.cota.bind("<Return>", self.focus_next_widget)
        self.cota.bind("<KeyPress>",self.on_key_press)
        self.cota.bind("<KeyRelease>", self.check_changes)

        self.registro_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.registro_m.place(x=378.0, y=282.0, width=297.0, height=38.0)
        self.registro_m.bind("<Return>", self.focus_next_widget)
        self.registro_m.bind("<KeyPress>",self.on_key_press)
        self.registro_m.bind("<KeyRelease>", self.check_changes)

        self.edicion_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.edicion_m.place(x=695.0, y=282.0, width=297.0, height=37.5)
        self.edicion_m.bind("<Return>", self.focus_next_widget)
        self.edicion_m.bind("<KeyPress>",self.on_key_press)
        self.edicion_m.bind("<KeyRelease>", self.check_changes)

        self.volumen_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.volumen_m.place(x=1016.0, y=282.0, width=297.0, height=37.5)
        self.volumen_m.bind("<Return>", self.focus_next_widget)
        self.volumen_m.bind("<KeyPress>",self.on_key_press)
        self.volumen_m.bind("<KeyRelease>", self.check_changes)

        # Segunda fila
        self.titulo_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid")
        self.titulo_m.place(x=61.0, y=382.0, width=297.0, height=37.5)
        self.titulo_m.bind("<Return>", self.focus_next_widget)
        self.titulo_m.bind("<KeyPress>", self.on_key_press)  
        self.titulo_m.bind("<KeyRelease>", self.check_changes)
        


        self.autor_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key")
        self.autor_m.place(x=378.0, y=382.0, width=297.0, height=37.5)
        self.autor_m.bind("<Return>", self.focus_next_widget)
        self.autor_m.bind("<KeyPress>", self.on_key_press)
        self.autor_m.bind("<KeyRelease>", self.check_changes)

        self.editorial_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key")
        self.editorial_m.place(x=695.0, y=382.0, width=297.0, height=37.5)
        self.editorial_m.bind("<Return>", self.focus_next_widget)
        self.editorial_m.bind("<KeyPress>", self.on_key_press)
        self.editorial_m.bind("<KeyRelease>", self.check_changes)

        self.ano_m = tk.Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=2, highlightbackground="grey", highlightcolor="grey", borderwidth=0.5, relief="solid", validate="key", validatecommand=(validate_number, "%P"))
        self.ano_m.place(x=1016.0, y=382.0, width=297.0, height=37.5)
        self.ano_m.bind("<Return>", self.focus_next_widget)
        self.ano_m.bind("<KeyPress>",self.on_key_press)
        self.ano_m.bind("<KeyRelease>", self.check_changes)
    
    def insert_values_book(self):
        self.clear_entries_modify()
        self.combobox1.set(self.book_data["ID_Sala"])
        self.categoria_cb.set(self.book_data["ID_Categoria"])
        self.asignatura_cb.set(self.book_data["ID_Asignatura"])
        self.cota.insert(0, self.book_data["Cota"])
        self.registro_m.insert(0, self.book_data["n_registro"])
        self.edicion_m.insert(0, self.book_data["Edicion"])
        self.volumen_m.insert(0, self.book_data["Volumen"])
        self.titulo_m.insert(0, self.book_data["Titulo"])
        self.autor_m.insert(0, self.book_data["Autor"])
        self.editorial_m.insert(0, self.book_data["Editorial"])
        self.ano_m.insert(0, self.book_data["Año"])
        self.check_changes()
    def on_key_press(self, event):
        widget = event.widget
        current_text = widget.get()
        
        if widget == self.cota:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not allow_only_letters_numbers_dots(event.char):
                return "break"
            
            # Guardar la posición del cursor antes de añadir el nuevo carácter
            cursor_position = widget.index(tk.INSERT)
            
            # Añadir el nuevo carácter al texto actual en la posición del cursor
            new_text = current_text[:cursor_position] + event.char + current_text[cursor_position:]
            
            # Limitar la longitud y convertir a mayúsculas antes de actualizar el widget
            new_text = limitar_longitud_cota(new_text)
            formatted_text = convert_to_uppercase(new_text)

            # Actualizar el campo de entrada
            widget.delete(0, tk.END)
            widget.insert(0, formatted_text)
            
            # Restaurar la posición del cursor
            widget.icursor(cursor_position + 1)

            return "break"
        elif widget == self.registro_m:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not allow_only_numbers_and_dot_at_thousands(current_text + event.char):
                return "break"
            formatted_text = current_text + event.char
            formatted_text = current_text
        elif widget == self.titulo_m:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isalpha() and event.char not in " áéíóúÁÉÍÓÚñÑ.,;:!?¿¡-":
                return "break"
            current_text = longitud_titulo(current_text)
            current_text = format_title(current_text)
            formatted_text = validate_and_format_title(current_text)
        elif widget == self.autor_m:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isalpha() and event.char != " ":
                return "break"
            current_text = longitud_autor(current_text)
            formatted_text = validar_y_formatear_texto(current_text)
            
        elif widget == self.editorial_m:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isalpha() and event.char != " ":
                return "break"
            current_text = longitud_editorial(current_text)
            formatted_text = validar_y_formatear_texto(current_text)
        elif widget == self.ano_m:
            if event.keysym in ('BackSpace', 'Delete', "Left", "Right"):
                return
            if not event.char.isdigit():
                return "break"
            current_text = widget.get()  # Obtener texto actual sin añadir el nuevo carácter aún
            if len(current_text) >= 4:
                return "break"
            # Permitir añadir el nuevo carácter si no excede la longitud
            formatted_text = current_text[:widget.index(tk.INSERT)] + event.char + + current_text[widget.index(tk.INSERT):]
        elif widget == self.edicion_m:
            resultado = validar_digitos(event, longitud_nro_edicion)
            if resultado == "break":
                return "break"
            formatted_text = resultado

        elif widget == self.volumen_m:
            resultado = validar_digitos(event, longitud_volumen)
            if resultado == "break":
                return "break"
            formatted_text = resultado

        # Guardar la posición del cursor
        cursor_position = widget.index(tk.INSERT)

        # Actualizar el campo de entrada
        widget.delete(0, tk.END)
        widget.insert(0, formatted_text)

        # Restaurar la posición del cursor
        widget.icursor(cursor_position)
        event.widget.after(1,formatted_text)


    def mostrar_opciones(self, categoria_values, asignatura_values):

        self.categoria_cb['values'] = categoria_values
        self.asignatura_cb['values'] = asignatura_values
        self.check_changes()
        
    def actualizar_opciones(self, combobox, values):
        combobox['values'] = values
        combobox.set('')
        self.check_changes()

    def validacion_sala(self, event):
        stylebox = ttk.Style()
        stylebox.theme_use('clam')
        stylebox.configure("TCombobox",
                            fieldbackground="#2E59A7",  # Fondo del campo de entrada
                            background="#2E59A7",  # Fondo del desplegable
                            bordercolor="#041022",  # Color del borde
                            arrowcolor="#ffffff",  # Color de la flecha
                            padding="9",
                            )  # padding para agrandar la altura del select
        sala_seleccionada = self.combobox1.get()
        
        if sala_seleccionada == self.book_data["ID_Sala"]:
            self.categoria_cb.set(self.book_data["ID_Categoria"])
            self.asignatura_cb.set(self.book_data["ID_Asignatura"])
        else:
            self.categoria_cb.set("No se ha seleccionado una categoría")
            self.asignatura_cb.set("No se ha seleccionado una asignatura")

        if sala_seleccionada == "1I":
            self.mostrar_opciones(self.categoria_types_children, self.asignature_types_children)
            
        elif sala_seleccionada == "2E":
            self.mostrar_opciones(self.categoria_types_state, self.asignature_types_state)
            
        elif sala_seleccionada == "3G":
            self.mostrar_opciones(self.categoria_types_general, self.asignature_type_general)
        
        self.check_changes()
        
    def check_changes(self, *args):
     try:
        current_values = {
            "ID_Sala": self.combobox1.get().strip(),
            "ID_Categoria": self.categoria_cb.get().strip(),
            "ID_Asignatura": self.asignatura_cb.get().strip(),
            "Cota": self.cota.get().strip(),
            "n_registro": self.registro_m.get().strip(),
            "Titulo": self.titulo_m.get(),
            "Autor": self.autor_m.get(),
            "Editorial": self.editorial_m.get(),
            "Año": self.ano_m.get().strip(),
            "Edicion": self.edicion_m.get().strip(),
            "Volumen": self.volumen_m.get().strip(),
        }


        # Comparar valores clave por clave
        differences = []
        for key in current_values:
            if current_values[key] != self.original_values[key]:
                differences.append(f"Diferencia en {key}: {current_values[key]} (actual) != {self.original_values[key]} (original)")

        if differences:
            for diff in differences:
                print(diff)
            self.mostrar_boton_modificar()
            print("Se detectaron cambios. Botón 'Modificar' mostrado.")
        else:
            self.ocultar_boton_modificar()
            self.mostrar_boton_modificar_inactivo()
            print("No se detectaron cambios. Botón 'Modificar' inactivo mostrado.")
     except Exception as e:
        print(f"Error en check_changes: {e}")

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def modify_book(self):    
        # Recoger los valores de los campos    
        nuevos_valores = {        
            "ID_Sala": self.combobox1.get(),        
            "ID_Categoria": self.categoria_cb.get(),        
            "ID_Asignatura": self.asignatura_cb.get(),        
            "Cota": self.cota.get(),        
            "n_registro": self.registro_m.get(),        
            "Edicion": self.edicion_m.get(),        
            "n_volumenes": self.volumen_m.get(),        
            "Titulo": self.titulo_m.get(),        
            "Autor": self.autor_m.get(),        
            "Editorial": self.editorial_m.get(),        
            "Año": self.ano_m.get()    
        }

        # 
        # Obtener el ID del libro desde los valores originales    
        id_libro = self.original_values["ID"]    
        print(f"ID del libro: {id_libro}")

        # Validar los campos incluyendo el ID del libro    
        errores = validar_campos(
            self.categoria_cb.get(),        
            self.asignatura_cb.get(),
            self.cota.get(),        
            self.titulo_m.get(),        
            self.autor_m.get(),        
            self.editorial_m.get(),        
            self.registro_m.get(),        
            self.volumen_m.get(),        
            self.edicion_m.get(),        
            self.ano_m.get(),
            id_libro              # Pasar el ID del libro aquí    
        )    
        print(f"Errores: {errores}")  # Agregar esta línea para depuración
        if errores:        
            messagebox.showerror("Error al modificar", "Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"- {msg}" for msg in errores),parent=self)
            return
        print("Datos recogidos:")    
        for key, value in nuevos_valores.items():        
            print(f"{key}: {value}")

        # Actualizar los libros con los nuevos valores    
        if update_books(self.book_data, nuevos_valores): 
            messagebox.showinfo("Éxito", "Modificación del libro exitosa.",parent=self)        
            self.clear_entries_modify()  
            self.destroy()         
        else:        
            messagebox.showinfo("Modificación fallida", "Libro mantiene sus valores.",parent=self)

    def crear_boton_modificar_inactivo(self):
        try:
            self.images['boton_R_inactivo'] = tk.PhotoImage(file=resource_path("assets_2/M_button_grey.png"))
            print("Imagen del botón 'Modificar' inactivo cargada correctamente.")
        except Exception as e:
            print(f"Error al cargar la imagen del botón 'Modificar' inactivo: {e}")
            return

        self.boton_modificar_inactivo = tk.Button(
            self,
            image=self.images["boton_R_inactivo"],
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_modificar_inactivo.place(x=61.0, y=465.0, width=130.0, height=40.0)
        self.boton_modificar_inactivo.place_forget()
        print("Botón 'Modificar' inactivo creado y oculto inicialmente.")

    def crear_boton_modificar(self):
        self.images['boton_R'] = tk.PhotoImage(file=resource_path("assets_2/M_button_light_blue.png"))

        self.boton_modificar = tk.Button(
            self,
            image=self.images["boton_R"],
            borderwidth=0,
            highlightthickness=0,
            command=self.modify_book,
            relief="flat",
            bg="#031A33",
            activebackground="#031A33",
            activeforeground="#FFFFFF"
        )
        self.boton_modificar.place(x=61.0, y=465.0, width=130.0, height=40.0)
        self.boton_modificar.place_forget()
        print("Botón 'Modificar' creado y oculto inicialmente.")

    def mostrar_boton_modificar(self):
        self.boton_modificar.place(x=61.0, y=465.0, width=130.0, height=40.0)
        self.boton_modificar_inactivo.place_forget()
        print("Botón 'Modificar' mostrado.")

    def mostrar_boton_modificar_inactivo(self):
        self.boton_modificar_inactivo.place(x=61.0, y=465.0, width=130.0, height=40.0)
        self.boton_modificar.place_forget()
        print("Botón 'Modificar' inactivo mostrado.")

    def ocultar_boton_modificar(self):
        self.boton_modificar.place_forget()
        self.boton_modificar_inactivo.place_forget()
        print("Botón 'Modificar' oculto.")

    
    def crear_boton_restaurar(self):
        try:
            self.images['boton_r'] = tk.PhotoImage(file=resource_path("assets_2/rest_button_green.png"))
            self.boton_R = tk.Button(
                self,
                image=self.images['boton_r'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.insert_values_book(),
                relief="flat",
                bg="#031A33",
                activebackground="#031A33",
                activeforeground="#FFFFFF"
            )
            self.boton_R.place(x=220.0, y=465.0, width=130.0, height=40.0)
        except Exception as e:
            print(f"Error al cargar la imagen del botón 'Restaurar': {e}")

    def crear_boton_cancelar(self):
        try:
            self.images['boton_c'] = tk.PhotoImage(file=resource_path("assets_2/c_button_red1.png"))
            self.boton_C = tk.Button(
                self,
                image=self.images['boton_c'],
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.cancelar(self),
                relief="flat",
                bg="#031A33",
                activebackground="#031A33",
                activeforeground="#FFFFFF"
            )
            self.boton_C.place(x=380.0, y=465.0, width=130.0, height=40.0)
        except Exception as e:
            print(f"Error al cargar la imagen del botón 'Cancelar': {e}")

    def cancelar(self, window):
        if messagebox.askyesno("Advertencia", "¿Seguro que quieres cerrar esta ventana? Todos los cambios no guardados en el libro se perderán.", parent=self):
            window.destroy()



    def clear_entries_modify(self):
        self.combobox1.delete(0, tk.END)
        #self.menu_actual.delete(0, tk.END)
        self.combobox1.delete(0, tk.END)
        self.cota.delete(0, tk.END)
        self.registro_m.delete(0, tk.END)
        self.edicion_m.delete(0, tk.END)
        self.volumen_m.delete(0, tk.END)
        self.titulo_m.delete(0, tk.END)
        self.autor_m.delete(0, tk.END)
        self.editorial_m.delete(0, tk.END)
        self.registro_m.delete(0, tk.END)
        self.ano_m.delete(0, tk.END)
        
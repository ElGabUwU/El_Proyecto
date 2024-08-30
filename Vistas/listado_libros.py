import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
import mysql.connector as mariadb
import random
from pathlib import Path

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Listado de Libros")
        self.geometry("1000x600")
        
        # Crear el marco izquierdo para el menú de navegación
        self.right_frame = tk.Frame(self, bg="lightgray")
        self.right_frame.pack(side="right", fill="y")
        
        # Botones del menú de navegación
        buttons = ["Eliminar", "Modificar"]
        for button in buttons:
            tk.Button(self.right_frame, text=button, bg="lightgray").pack(fill="x", padx=5, pady=5)
        
        # Crear el marco derecho para el área principal de contenido
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side="left", expand=True, fill="both")
        
        # Barra de búsqueda en la parte superior
        search_frame = tk.Frame(self.left_frame)
        search_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(search_frame, text="Buscar:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", fill="x", expand=True)
        tk.Button(search_frame, text="Filtrar", command=self.filter_books).pack(side="left", padx=5)
        
        # Tabla de libros usando Treeview
        columns = ("ID", "Título", "Cota", "Autor", "Editorial", "N. Registro", "Edición", "Año", "Categoria/Asignatura")
        self.book_table = ttk.Treeview(self.left_frame, columns=columns, show='headings')
        for col in columns:
            self.book_table.heading(col, text=col)
            self.book_table.column(col, width=100)
        self.book_table.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Controles de paginación en la parte inferior
        pagination_frame = tk.Frame(self.left_frame)
        pagination_frame.pack(fill="x", padx=10, pady=10)
        tk.Button(pagination_frame, text="<").pack(side="left")
        tk.Label(pagination_frame, text="Página 1 de 10").pack(side="left", padx=5)
        tk.Button(pagination_frame, text=">").pack(side="left")
        
        # Datos de ejemplo
        self.books = [
            (1, "Libro A", "C001", "Autor A", "Editorial A", "R001", "1ª", "2020", "Ficción"),
            (2, "Libro B", "C002", "Autor B", "Editorial B", "R002", "2ª", "2019", "No Ficción"),
            # Agrega más libros según sea necesario
        ]
        self.load_books(self.books)
    
    def load_books(self, books):
        for book in books:
            self.book_table.insert("", "end", values=book)
    
    def filter_books(self):
        query = self.search_entry.get().lower()
        filtered_books = [book for book in self.books if query in book[1].lower()]
        self.book_table.delete(*self.book_table.get_children())
        self.load_books(filtered_books)

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()


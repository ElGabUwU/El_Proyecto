import mysql.connector
from mysql.connector import Error
from db.conexion import establecer_conexion
from tkinter import ttk, messagebox

# Tabla Cliente
def lists_clients(self):
    conexion = establecer_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT ID_Cliente, Cedula_Cliente, Nombre, Apellido, Telefono, Direccion FROM cliente")
            resultados = cursor.fetchall()
            for row in self.book_table.get_children():
                self.book_table.delete(row)
            for fila in resultados:
                self.book_table.insert("", "end", values=tuple(fila))
        except Error as e:
            messagebox.showerror(message=f"Error durante la consulta: {e}", title="Error de Consulta")
        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()

# Tabla Libros Prestamos
def lists_books_loans(self):
    conexion = establecer_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute('SELECT ID_Libro_Prestamo, ID_Libro, ID_Prestamo, Cantidad FROM libros_prestamo')
            resultados = cursor.fetchall()
            for row in self.libro_prestamo_table.get_children():
                self.libro_prestamo_table.delete(row)
            for fila in resultados:
                self.libro_prestamo_table.insert("", "end", values=tuple(fila))
        except Error as e:
            messagebox.showerror(message=f"Error durante la consulta: {e}", title="Error de Consulta")
        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()

# Tabla Prestamos
def lists_clients_loans(self):
    conexion = establecer_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute('SELECT ID_Prestamo, ID_Cliente, ID_Usuario, ID_Libro_Prestamo, Fecha_Registro, Fecha_Limite FROM prestamo')
            resultados = cursor.fetchall()
            for row in self.prestamo_table.get_children():
                self.prestamo_table.delete(row)
            for fila in resultados:
                self.prestamo_table.insert("", "end", values=tuple(fila))
        except Error as e:
            messagebox.showerror(message=f"Error durante la consulta: {e}", title="Error de Consulta")
        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()

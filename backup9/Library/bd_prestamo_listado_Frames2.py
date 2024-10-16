import mysql.connector as mariadb
from mysql.connector import Error
from db.conexion import establecer_conexion
from tkinter import ttk, messagebox
from datetime import datetime

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

def format_date(self, date_obj):
    try:
        # Si date_obj ya es un objeto datetime.date, conviértelo a cadena en formato YYYY-MM-DD
        if isinstance(date_obj, datetime):
            formatted_date = date_obj.strftime("%Y-%m-%d")
        elif isinstance(date_obj, str):
            # Convertir la fecha del formato DD/MM/YYYY al formato YYYY-MM-DD
            formatted_date = datetime.strptime(date_obj, "%d/%m/%Y").strftime("%Y-%m-%d")
        else:
            print(f"Tipo de dato inesperado: {type(date_obj)}")
            return None
        return formatted_date
    except ValueError as e:
        print(f"Error al formatear la fecha: {e}")
        return None

def lists_clients_loans(self):
    try:
        mariadb_conexion = establecer_conexion()
        if not mariadb_conexion:
            print("Failed to establish connection.")
            return

        cursor = mariadb_conexion.cursor()

        query1 = '''
        SELECT 
            p.ID_Prestamo,
            l.ID_Libro,
            c.ID_Cliente,
            c.Nombre AS Nombre_Cliente,
            lp.ID_Libro_Prestamo,
            l.titulo,
            l.n_ejemplares,
            p.Fecha_Registro,
            p.Fecha_Limite,
            u.Nombre AS Nombre_Usuario
        FROM 
            prestamo p
        JOIN 
            cliente c ON p.ID_Cliente = c.ID_Cliente
        JOIN 
            libros_prestamo lp ON p.ID_Libro_Prestamo = lp.ID_Libro_Prestamo
        JOIN
            libro l ON p.ID_Libro=l.ID_Libro
        JOIN 
            usuarios u ON p.ID_Usuario = u.ID_Usuario
        WHERE 
            p.estado = 'activo';
        '''

        cursor.execute(query1)
        resultados1 = cursor.fetchall()

        # Debugging: Print the results
        print("Query executed successfully. Results:")
        for resultado in resultados1:
            print(resultado)

        for row in self.prestamo_table.get_children():
            self.prestamo_table.delete(row)

        for fila in resultados1:
            fecha_limite = fila[8]  # Asumimos que fila[8] es un objeto datetime.date
            if fecha_limite < datetime.now().date():
                self.prestamo_table.insert("", "end", values=tuple(fila), tags=('vencido',))
            else:
                self.prestamo_table.insert("", "end", values=tuple(fila))

        # Configurar el estilo para las filas vencidas
        self.prestamo_table.tag_configure('vencido', background='red')

    except mariadb.Error as ex:
        print(f"Error during query execution: {ex}")
    finally:
        if mariadb_conexion is not None:
            mariadb_conexion.close()
            print("Connection closed.")
import mysql.connector as mariadb
from mysql.connector import Error
from db.conexion import establecer_conexion
from datetime import datetime, timedelta
from tkinter import ttk, messagebox



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

        prestamos_vencidos = []
        hoy = datetime.now().date()

        for fila in resultados1:
            fecha_limite = fila[7]
            if fecha_limite <= hoy - timedelta(days=20):
                tag = 'vencido'
                prestamos_vencidos.append(fila)
            else:
                tag = 'activo'
            self.prestamo_table.insert("", "end", values=tuple(fila), tags=(tag,))

        # Configurar las etiquetas para los colores
        self.prestamo_table.tag_configure('vencido', background='red')
        self.prestamo_table.tag_configure('activo', background='white')

        if prestamos_vencidos:
            messagebox.showwarning("Préstamos Vencidos", "Hay préstamos que han pasado más de 20 días desde su fecha límite.")

    except mariadb.Error as ex:
        print(f"Error during query execution: {ex}")
    finally:
        if mariadb_conexion is not None:
            mariadb_conexion.close()
            print("Connection closed.")
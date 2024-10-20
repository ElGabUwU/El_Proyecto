import mysql.connector as mariadb
from mysql.connector import Error
from db.conexion import establecer_conexion
from tkinter import ttk, messagebox

#OBTENCION DE DATOS PARA REPORTE DE PDF
def obtener_datos_libro(libro_id):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            cursor.execute('''
                SELECT ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares
                FROM libro
                WHERE ID_Libro = %s
            ''', (libro_id,))
            resultado_libro = cursor.fetchone()
            if resultado_libro:
                book_data = {
                    "ID_Sala": resultado_libro[0],
                    "ID_Categoria": resultado_libro[1],
                    "ID_Asignatura": resultado_libro[2],
                    "Cota": resultado_libro[3],
                    "n_registro": resultado_libro[4],
                    "edicion": resultado_libro[5],
                    "n_volumenes": resultado_libro[6],
                    "titulo": resultado_libro[7],
                    "autor": resultado_libro[8],
                    "editorial": resultado_libro[9],
                    "año": resultado_libro[10],
                    "n_ejemplares": resultado_libro[11]
                }
                print("Book Data:", book_data)
                return book_data
            else:
                print("No se encontró información del libro.")
            mariadb_conexion.close()
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
    return None

def obtener_datos_cliente(cliente_id):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            cursor.execute('''
                SELECT Cedula_Cliente, Nombre, Apellido, Telefono, Direccion
                FROM cliente
                WHERE ID_Cliente = %s
            ''', (cliente_id,))
            resultado_cliente = cursor.fetchone()
            print(f"Resultado Cliente: {resultado_cliente}")  # Depuración
            if resultado_cliente:
                user_data = {
                    "Cedula": resultado_cliente[0],
                    "Nombre": resultado_cliente[1],
                    "Apellido": resultado_cliente[2],
                    "Telefono": resultado_cliente[3],
                    "Direccion": resultado_cliente[4]
                }
                print("User Data:", user_data)  # Depuración
                return user_data
            else:
                print("No se encontró información del cliente.")
            mariadb_conexion.close()
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
    return None

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
            self.prestamo_table.insert("", "end", values=tuple(fila))

    except mariadb.Error as ex:
        print(f"Error during query execution: {ex}")
    finally:
        if mariadb_conexion is not None:
            mariadb_conexion.close()
            print("Connection closed.")
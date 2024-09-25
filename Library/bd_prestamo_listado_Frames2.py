import mysql.connector as mariadb
from db.conexion import *
#Tabla Cliente
def lists_clients(self):
        try:

            mariadb_conexion = mariadb.connect(
                                        host='localhost',
                                        port='3306',
                                        password='2525',
                                        database='basedatosbiblioteca'
            )
            if mariadb_conexion.is_connected():
                cursor = mariadb_conexion.cursor()
                cursor.execute('SELECT ID_Cliente, Cedula_Cliente, Nombre, Apellido, Telefono, Direccion FROM cliente')
                resultados = cursor.fetchall() 
                for row in self.book_table.get_children():
                    self.book_table.delete(row)
                    
                    # Insertar los datos en el Treeview
                for fila in resultados:
                    self.book_table.insert("", "end", values=tuple(fila))
                mariadb_conexion.close()
        except mariadb.Error as ex:
                print("Error durante la conexión:", ex)
#Tabla Libros Prestamos
def lists_books_loans(self):
        try:
            mariadb_conexion = mariadb.connect(
                                        host='localhost',
                                        port='3306',
                                        password='2525',
                                        database='basedatosbiblioteca'
            )
            if mariadb_conexion.is_connected():
                cursor = mariadb_conexion.cursor()
                cursor.execute('SELECT ID_Libro_Prestamo, ID_Libro, ID_Prestamo, Cantidad FROM libros_prestamo')
                resultados = cursor.fetchall() 
                for row in self.libro_prestamo_table.get_children():
                    self.libro_prestamo_table.delete(row)
                    
                    # Insertar los datos en el Treeview
                for fila in resultados:
                    self.libro_prestamo_table.insert("", "end", values=tuple(fila))
                mariadb_conexion.close()
        except mariadb.Error as ex:
                print("Error durante la conexión:", ex)
#Tabla Prestamos
def lists_clients_loans(self):
    try:
        mariadb_conexion = mariadb.connect(
            host='localhost',
            port='3306',
            password='2525',
            database='basedatosbiblioteca'
        )
        if mariadb_conexion.is_connected():
            cursor = mariadb_conexion.cursor()
        else:
            print("Failed to establish connection.")
            return

        query = '''
            SELECT p.ID_Prestamo, p.ID_Cliente, c.Nombre, p.ID_Libro_Prestamo, l.titulo, l.n_ejemplares, p.Fecha_Registro, p.Fecha_Limite, u.ID_Usuario AS Encargado
            FROM prestamo p
            JOIN cliente c ON p.ID_Cliente = c.ID_Cliente
            JOIN libro l ON p.ID_Libro_Prestamo = l.ID_Libro
            JOIN usuarios u ON p.ID_Usuario = u.ID_Usuario
        '''
        cursor.execute(query)
        resultados = cursor.fetchall()

        # Debugging: Print the results
        print("Query executed successfully. Results:")
        for resultado in resultados:
            print(resultado)

        for row in self.prestamo_table.get_children():
            self.prestamo_table.delete(row)

        for fila in resultados:
            self.prestamo_table.insert("", "end", values=tuple(fila))

    except mariadb.Error as ex:
        print(f"Error during query execution: {ex}")
    finally:
        if mariadb_conexion is not None and mariadb_conexion.is_connected():
            mariadb_conexion.close()
            print("Connection closed.")
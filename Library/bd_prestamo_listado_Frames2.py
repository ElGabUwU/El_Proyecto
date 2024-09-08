import mysql.connector as mariadb
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
                cursor.execute('SELECT ID_Prestamo, ID_Cliente, ID_Usuario, ID_Libro_Prestamo, Fecha_Registro, Fecha_Limite FROM prestamo')
                resultados = cursor.fetchall() 
                for row in self.prestamo_table.get_children():
                    self.prestamo_table.delete(row)
                    
                    # Insertar los datos en el Treeview
                for fila in resultados:
                    self.prestamo_table.insert("", "end", values=tuple(fila))
                mariadb_conexion.close()
        except mariadb.Error as ex:
                print("Error durante la conexión:", ex)

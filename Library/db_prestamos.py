import mysql.connector as mariadb
from colorama import init, Fore, Back, Style
from db.conexion import establecer_conexion
init(autoreset=True)
# Conectar a la base de datos
mariadb_conexion = establecer_conexion()

# Crear un nuevo cliente-prestamo
def create_client_loans(ID_Cedula, nombre, apellido, telefono, direccion, ID_Prestamo):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            # Consulta SQL para insertar un nuevo cliente
            sql_insert_query = """INSERT INTO cliente (Cedula_Cliente, Nombre, Apellido, Telefono, Direccion, ID_Prestamo) VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_insert_query, (ID_Cedula, nombre, apellido, telefono, direccion, ID_Prestamo))
            mariadb_conexion.commit()
            ID_Cliente = cursor.lastrowid  # Obtener el ID del cliente recién creado
            return ID_Cliente

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

    finally:
        
        if mariadb_conexion:#.is_connected():
            cursor.close()
            mariadb_conexion.close()

import mysql.connector
from mysql.connector import Error

def create_loan(ID_Prestamo, fecha_registrar, fecha_limite):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            # Consulta SQL para insertar un nuevo préstamo
            sql_insert_query = """INSERT INTO prestamo (ID_Prestamo, Fecha_Registro, Fecha_Limite) VALUES (%s, %s, %s)"""
            cursor.execute(sql_insert_query, (ID_Prestamo, fecha_registrar, fecha_limite))
            mariadb_conexion.commit()
            return ID_Prestamo
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False

    finally:
        if mariadb_conexion:#.is_connected():
            cursor.close()
            mariadb_conexion.close()

def update_prestamo_with_cliente(ID_Prestamo, ID_Cliente, ID_Libro_Prestamo):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            # Consulta SQL para actualizar el préstamo con el ID del cliente y el ID del libro
            sql_update_query = """UPDATE prestamo SET ID_Cliente = %s, ID_Libro_Prestamo = %s WHERE ID_Prestamo = %s"""
            cursor.execute(sql_update_query, (ID_Cliente, ID_Libro_Prestamo, ID_Prestamo))
            mariadb_conexion.commit()
            return True

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        if mariadb_conexion:
            mariadb_conexion.rollback()
        return False
    finally:
        if mariadb_conexion:#.is_connected():
            cursor.close()
            mariadb_conexion.close()

def create_libro_prestamo(ID_Libro_Prestamo, ID_Prestamo, Cantidad):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            # Consulta SQL para insertar un nuevo registro en libros_prestamo
            sql_insert_query = """INSERT INTO libros_prestamo (ID_Libro_Prestamo, ID_Prestamo, Cantidad) VALUES (%s, %s, %s)"""
            cursor.execute(sql_insert_query, (ID_Libro_Prestamo, ID_Prestamo, Cantidad))
            mariadb_conexion.commit()
            return True

    except mariadb.Error as e:
        if mariadb_conexion:
            mariadb_conexion.rollback()
        return False
    finally:
        if mariadb_conexion:#.is_connected():
            cursor.close()
            mariadb_conexion.close()

def update_libros_prestamo(ID_Libro_Prestamo, ID_Libro, ID_Prestamo, Cantidad):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            # Consulta SQL para actualizar la tabla libros_prestamo
            sql_update_query = """UPDATE libros_prestamo SET ID_Libro = %s, ID_Prestamo = %s, Cantidad = %s WHERE ID_Libro_Prestamo = %s"""
            cursor.execute(sql_update_query, (ID_Libro, ID_Prestamo, Cantidad, ID_Libro_Prestamo))
            mariadb_conexion.commit()
            return True

    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        if mariadb_conexion:
            mariadb_conexion.rollback()
        return False

    finally:
        if mariadb_conexion:#.is_connected():
            cursor.close()
            mariadb_conexion.close()

def libro_prestamo_exists(ID_Libro_Prestamo):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            sql_check_query = "SELECT 1 FROM libros_prestamo WHERE ID_Libro_Prestamo = %s"
            cursor.execute(sql_check_query, (ID_Libro_Prestamo,))
            result = cursor.fetchone()
            return result is not None

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False

    finally:
        if mariadb_conexion:#.is_connected():
            cursor.close()
            mariadb_conexion.close()

# Leer todos los prestamos
def read_client_loans():
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor=mariadb_conexion.cursor()
            cursor.execute('''
                SELECT * FROM cliente''')
            resultados=cursor.fetchall()
            print("\t\t\t\t\t===================LEYENDA========================")
            print("\n")
            print(f"\t\t\t\t\t\t ||{Fore.BLUE}ID_Cliente{Fore.LIGHTWHITE_EX}--{Fore.BLUE}ID_Prestamo{Fore.LIGHTWHITE_EX}--{Fore.BLUE}Cedula_Cliente{Fore.LIGHTWHITE_EX}||")
            print("\n")
            print(f"\t\t\t\t\t    ||{Fore.GREEN}Nombre{Fore.LIGHTWHITE_EX}--{Fore.GREEN}Apellido{Fore.LIGHTWHITE_EX}--{Fore.GREEN}Teléfono{Fore.LIGHTWHITE_EX}||")
            print("\n")
            print(f"\t\t\t\t\t\t||{Fore.RED}Dirección{Fore.LIGHTWHITE_EX}")
            print("\t\t\t\t\t===================================================")
            for fila in resultados:
                print(f"""
    ||===================================================================================||
    |||{Fore.BLUE}{fila[0]}--{fila[1]}--{fila[2]}{Fore.LIGHTWHITE_EX}
    |||{Fore.GREEN}{fila[3]}--{fila[4]}--{fila[5]}{Fore.LIGHTWHITE_EX}
    |||{Fore.RED}{fila[6]}
    ||===================================================================================||
                    """)
            mariadb_conexion.close()
            return resultados
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)

# Actualizar un prestamo
def update_client_loans(id_prestamo, cantidad, fecha_limite):
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        cursor.execute("SELECT ID_Prestamo FROM prestamo WHERE ID_Prestamo = %s", (id_prestamo,))
        busqueda=()
        busqueda=cursor.fetchone()
        print(busqueda)
        if busqueda is None:
            mariadb_conexion.close()
            print("No se encontró al cliente y su préstamo.")
            return False
        else:
            # Actualizar la fecha límite del préstamo
            cursor.execute('''
                UPDATE prestamo
                SET Fecha_Limite = %s
                WHERE ID_Prestamo = %s
            ''', (fecha_limite, id_prestamo))
        
        # Actualizar la cantidad de libros prestados
        cursor.execute('''
            UPDATE libros_prestamo
            SET Cantidad = %s
            WHERE ID_Prestamo = %s
        ''', (cantidad, id_prestamo))
        print("Actualización éxitosa.")
        mariadb_conexion.commit()
        mariadb_conexion.close()
        return True

# Eliminar prestamo del cliente
def delete_client_loans(ID_Cedula):
    try:
        # Establishing the connection using a context manager
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            # Executing the delete statement
            cursor.execute('DELETE FROM Cliente WHERE Cedula_Cliente=%s', (ID_Cedula,))
            if cursor.rowcount == 0:
                print("No se encontró al cliente y su préstamo.")
                return False
            # Committing the transaction
            mariadb_conexion.commit()
        return True
    except mariadb.Error as err:
        # Handling any database errors
        print(f"Error: {err}")
        return False

def delete_selected_cliente(self):
    selected_items = self.book_table.selection()
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            
            cursor = mariadb_conexion.cursor()
            for item in selected_items:
                item_id = self.book_table.item(item, 'values')[0]
                
                # Obtener los ID_Prestamo asociados al cliente
                cursor.execute('SELECT ID_Prestamo FROM prestamo WHERE ID_Cliente = %s', (item_id,))
                prestamos = cursor.fetchall()
                for prestamo in prestamos:
                    id_prestamo = prestamo[0]
                    # Eliminar filas dependientes en libros_prestamo
                    cursor.execute('DELETE FROM libros_prestamo WHERE ID_Prestamo = %s', (id_prestamo,))
                    # Eliminar filas en prestamo
                    cursor.execute('DELETE FROM prestamo WHERE ID_Prestamo = %s', (id_prestamo,))
                # Eliminar el cliente
                cursor.execute('DELETE FROM cliente WHERE ID_Cliente = %s', (item_id,))
                self.book_table.delete(item)
            mariadb_conexion.commit()
            mariadb_conexion.close()
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)

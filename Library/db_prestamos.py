import mysql.connector as mariadb
from colorama import init, Fore, Back, Style
from db.conexion import establecer_conexion
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

init(autoreset=True)
# Conectar a la base de datos
mariadb_conexion = establecer_conexion()

# Crear un nuevo cliente-prestamo
def create_client_loans(ID_Cedula, nombre, apellido, telefono, direccion):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            # Consulta SQL para insertar un nuevo cliente
            sql_insert_query = """INSERT INTO cliente (Cedula_Cliente, Nombre, Apellido, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql_insert_query, (ID_Cedula, nombre, apellido, telefono, direccion))
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

def modify_client_loans(id_cliente, new_cedula, nombre, apellido, telefono, direccion):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            # Consulta SQL para actualizar un cliente existente
            sql_update_query = """UPDATE cliente SET Cedula_Cliente = %s, Nombre = %s, Apellido = %s, Telefono = %s, Direccion = %s WHERE ID_Cliente = %s"""
            cursor.execute(sql_update_query, (new_cedula, nombre, apellido, telefono, direccion, id_cliente))
            mariadb_conexion.commit()
            return cursor.rowcount  # Devuelve el número de filas afectadas
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()

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
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            # Iniciar transacción
            mariadb_conexion.start_transaction()
            
            # Actualizar la tabla prestamo con ID_Cliente y ID_Libro_Prestamo
            sql_update_prestamo = """UPDATE prestamo SET ID_Cliente = %s, ID_Libro_Prestamo = %s WHERE ID_Prestamo = %s"""
            cursor.execute(sql_update_prestamo, (ID_Cliente, ID_Libro_Prestamo, ID_Prestamo))
            
            # Actualizar la tabla cliente con ID_Prestamo
            sql_update_cliente = """UPDATE cliente SET ID_Prestamo = %s WHERE ID_Cliente = %s"""
            cursor.execute(sql_update_cliente, (ID_Prestamo, ID_Cliente))
            
            # Confirmar transacción
            mariadb_conexion.commit()
            return True
    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        if mariadb_conexion:
            mariadb_conexion.rollback()
        return False
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()

# def get_id_usuario(ID_Usuario):
#     try:
#         mariadb_conexion = establecer_conexion()
#         if mariadb_conexion:
#             cursor = mariadb_conexion.cursor()
#             sql_select_usuario = """SELECT ID_Usuario FROM usuarios WHERE ID_Usuario = %s"""
#             cursor.execute(sql_select_usuario, (ID_Usuario,))
#             result = cursor.fetchone()
#             if result:
#                 return result[0]
#             else:
#                 print("Error: No se encontró el usuario con el ID_Cliente proporcionado.")
#                 return None
#     except mariadb.Error as e:
#         print(f"Error al conectar a la base de datos: {e}")
#         return None
#     finally:
#         if mariadb_conexion:
#             cursor.close()
#             mariadb_conexion.close()

def update_prestamo_with_usuario(ID_Prestamo, ID_Usuario):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            sql_update_prestamo = """UPDATE prestamo SET ID_Usuario = %s WHERE ID_Prestamo = %s"""
            cursor.execute(sql_update_prestamo, (ID_Usuario, ID_Prestamo))
            mariadb_conexion.commit()
            return True
    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        if mariadb_conexion:
            mariadb_conexion.rollback()
        return False
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()
def create_libro_prestamo(ID_Libro_Prestamo, ID_Prestamo, ID_Libro, Cantidad):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            # Verificar si el ID_Libro_Prestamo ya existe
            cursor.execute('SELECT COUNT(*) FROM libros_prestamo WHERE ID_Libro_Prestamo = %s', (ID_Libro_Prestamo,))
            if cursor.fetchone()[0] == 0:
                # Consulta SQL para insertar un nuevo registro en libros_prestamo
                sql_insert_query = """INSERT INTO libros_prestamo (ID_Libro_Prestamo, ID_Prestamo, ID_Libro, Cantidad) VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql_insert_query, (ID_Libro_Prestamo, ID_Prestamo, ID_Libro, Cantidad))
                mariadb_conexion.commit()
                return True
            else:
                print("ID_Libro_Prestamo ya existe.")
                return False
    except mariadb.Error as e:
        print(f"Error al conectar con MariaDB: {e}")
        if mariadb_conexion:
            mariadb_conexion.rollback()
        return False
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()

def update_prestamo_and_libro(ID_Prestamo, ID_Cliente, ID_Libro, ID_Libro_Prestamo, Cantidad):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            # Iniciar transacción
            mariadb_conexion.start_transaction()
            
            # Verificar si ID_Libro_Prestamo existe en libros_prestamo
            cursor.execute("SELECT 1 FROM libros_prestamo WHERE ID_Libro_Prestamo = %s", (ID_Libro_Prestamo,))
            if cursor.fetchone() is None:
                # Insertar en libros_prestamo si no existe
                sql_insert_libro_prestamo = """INSERT INTO libros_prestamo (ID_Libro_Prestamo, ID_Prestamo, Cantidad) VALUES (%s, %s, %s)"""
                cursor.execute(sql_insert_libro_prestamo, (ID_Libro_Prestamo, ID_Prestamo, Cantidad))
            
            # Actualizar prestamo con ID_Cliente, ID_Libro y ID_Libro_Prestamo
            sql_update_prestamo = """UPDATE prestamo SET ID_Cliente = %s, ID_Libro = %s, ID_Libro_Prestamo = %s WHERE ID_Prestamo = %s"""
            cursor.execute(sql_update_prestamo, (ID_Cliente, ID_Libro, ID_Libro_Prestamo, ID_Prestamo))
            
            # Actualizar libro con ID_Libro_Prestamo
            sql_update_libro = """UPDATE libro SET ID_Libro_Prestamo = %s WHERE ID_Libro = %s"""
            cursor.execute(sql_update_libro, (ID_Libro_Prestamo, ID_Libro))
            
            # Confirmar transacción
            mariadb_conexion.commit()
            return True

    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        if mariadb_conexion:
            mariadb_conexion.rollback()
        return False
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()

def libro_prestamo_exists(new_id):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            # Verificar si el ID_Libro_Prestamo existe en la tabla libros_prestamo
            cursor.execute("SELECT 1 FROM libros_prestamo WHERE ID_Libro_Prestamo = %s", (new_id,))
            result = cursor.fetchone()
            return result is not None
    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False
    finally:
        if mariadb_conexion:
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
def delete_client_loans(self):
    selected_clients = self.clients_table_list_loans.selection()
    if not selected_clients:
        messagebox.showwarning("Selección vacía", "Por favor, seleccione un cliente de la tabla.")
        return

    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            for cliente in selected_clients:
                item_id = self.clients_table_list_loans.item(cliente, 'values')[0]
                cursor.execute('DELETE FROM cliente WHERE ID_Cliente = %s', (item_id,))
                self.clients_table_list_loans.delete(cliente)
            mariadb_conexion.commit()
            mariadb_conexion.close()
            messagebox.showinfo("Éxito", "Eliminación exitosa del cliente.")
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        messagebox.showerror("Error", f"Error durante la conexión: {ex}")

def reading_clients(client_table_list_loans):
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:#.is_connected():
                cursor = mariadb_conexion.cursor()
                cursor.execute('SELECT ID_Cliente, ID_Prestamo, Cedula_Cliente, Nombre, Apellido, Telefono, Direccion FROM cliente')
                resultados = cursor.fetchall() 
                for row in client_table_list_loans.get_children():
                    client_table_list_loans.delete(row)
                    # Insertar los datos en el Treeview
                for fila in resultados:
                    client_table_list_loans.insert("", "end", values=tuple(fila))
                mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)

def delete_selected_cliente(self):
    selected_items = self.prestamo_table.selection()
    if not selected_items:
        messagebox.showwarning("Selección vacía", "Por favor, seleccione un préstamo de la tabla.")
        return
    selected_items = self.prestamo_table.selection()
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            for item in selected_items:
                item_values = self.prestamo_table.item(item, 'values')
                item_id = item_values[0]
                
                # Marcar el registro como eliminado en lugar de eliminarlo
                cursor.execute('UPDATE prestamo SET estado = "eliminado" WHERE ID_Prestamo = %s', (item_id,))
                
                # Eliminar la fila del Treeview
                self.prestamo_table.delete(item)
            
            mariadb_conexion.commit()
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
    finally:
        if mariadb_conexion:
            mariadb_conexion.close()


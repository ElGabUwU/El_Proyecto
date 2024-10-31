import mysql.connector as mariadb
from colorama import init, Fore, Back, Style
from db.conexion import establecer_conexion
from tkinter import messagebox
from mysql.connector import Error
from validations.loans_validations import generate_alphanumeric_id
from datetime import datetime
from validations.loans_validations import get_cliente_id_by_cedula
from loans.backend.sql_functions_db_loans import *

init(autoreset=True)
# Conectar a la base de datos
mariadb_conexion = establecer_conexion()

# Función para crear un préstamo para cada cliente
def create_loan(ID_Cliente, ID_Prestamo, fecha_registrar, fecha_limite):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor(buffered=True)
            print("Conexión a la base de datos establecida.")

            # Insertar un nuevo préstamo
            insert_new_loan(cursor, ID_Prestamo, fecha_registrar, fecha_limite)
            print(f"Nuevo préstamo insertado: {ID_Prestamo}, {fecha_registrar}, {fecha_limite}")
            mariadb_conexion.commit()

            # Asociar el préstamo con el cliente
            associate_loan_with_client(cursor, ID_Cliente, ID_Prestamo)
            print(f"Préstamo asociado con el cliente: {ID_Cliente}, {ID_Prestamo}")
            mariadb_conexion.commit()

            get_new_id_cp(cursor, ID_Cliente, ID_Prestamo)
            print(f"ID_CP que se obtuve de: {ID_Cliente}, {ID_Prestamo}")
            mariadb_conexion.commit()
            """
            OJO get new id cp
            """
            cursor.close()
            mariadb_conexion.close()
            print("Conexión a la base de datos cerrada.")
            return True
    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False
    finally:
        if mariadb_conexion and mariadb_conexion.is_connected():
            cursor.close()
            mariadb_conexion.close()
            print("Conexión a la base de datos cerrada en finally.")

#Función para actualizar/insertar datos en las columnas de tabla cliente_prestamos e igualmente en las tablas cliente y libro

def update_all_tables(ID_Cliente, ID_Libro, ID_Libro_Prestamo, ID_Prestamo, ID_Usuario):
    try:
        # Establecer conexión a la base de datos
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor(buffered=True)
            print("Conexión a la base de datos establecida.")

            # Iniciar transacción
            iniciar_transaccion(mariadb_conexion)

            # Verificar la cantidad de ejemplares disponibles
            cursor.execute("SELECT n_ejemplares FROM libro WHERE ID_Libro = %s", (ID_Libro,))
            ejemplares_disponibles = cursor.fetchone()[0]
            print(f"Ejemplares disponibles para el libro {ID_Libro}: {ejemplares_disponibles}")

            if ejemplares_disponibles <= 1:
                print("No hay ejemplares disponibles para prestar.")
                messagebox.showerror("Error", "No hay ejemplares disponibles para prestar.")
                return False

            # Restar 1 a la cantidad de ejemplares
            cursor.execute("UPDATE libro SET n_ejemplares = n_ejemplares - 1 WHERE ID_Libro = %s", (ID_Libro,))
            print(f"Ejemplar prestado. Nuevos ejemplares disponibles: {ejemplares_disponibles - 1}")

            # Verificar e insertar en libros_prestamo
            verificar_e_insertar_libro_prestamo(cursor, ID_Libro_Prestamo, ID_Prestamo, ID_Libro)

            # Insertar en cliente_prestamo
            cursor.execute("""
                INSERT INTO cliente_prestamo (ID_Cliente, ID_Prestamo, ID_Usuario, ID_Libro, ID_Libro_Prestamo)
                VALUES (%s, %s, %s, %s, %s)
            """, (ID_Cliente, ID_Prestamo, ID_Usuario, ID_Libro, ID_Libro_Prestamo))
            print(f"Registro insertado en cliente_prestamo: ID_Cliente={ID_Cliente}, ID_Prestamo={ID_Prestamo}, ID_Usuario={ID_Usuario}, ID_Libro={ID_Libro}, ID_Libro_Prestamo={ID_Libro_Prestamo}")

            # Obtener el ID_CP generado
            cursor.execute("SELECT LAST_INSERT_ID()")
            ID_CP = cursor.fetchone()[0]
            print(f"ID_CP obtenido: {ID_CP}")

            # Actualizar la tabla cliente con el ID_CP
            cursor.execute("""
                UPDATE cliente
                SET ID_CP = %s
                WHERE ID_Cliente = %s
            """, (ID_CP, ID_Cliente))
            print(f"Tabla cliente actualizada con ID_CP={ID_CP} para ID_Cliente={ID_Cliente}")

            # Actualizar la tabla prestamo con el ID_CP
            cursor.execute("""
                UPDATE prestamo
                SET ID_CP = %s
                WHERE ID_Prestamo = %s
            """, (ID_CP, ID_Prestamo))
            print(f"Tabla prestamo actualizada con ID_CP={ID_CP} para ID_Prestamo={ID_Prestamo}")

            # Confirmar transacción
            mariadb_conexion.commit()
            print("Transacción confirmada.")

            return True
    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        if mariadb_conexion:
            mariadb_conexion.rollback()
            print("Transacción revertida.")
        return False
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()
            print("Conexión a la base de datos cerrada.")



# Modificación y actualización un prestamo
def update_client_loans(cedula, fecha_limite):
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        try:
            # Obtener el ID_Cliente por cédula
            id_cliente = get_cliente_id_by_cedula(cedula)
            if id_cliente is None:
                print("No se encontró al cliente con la cédula proporcionada.")
                return False

            # Verificar si el cliente tiene un préstamo activo
            cursor.execute("SELECT ID_Prestamo FROM prestamo WHERE ID_CP = %s", (id_cliente,))
            busqueda = cursor.fetchone()
            print(f"Resultado: {busqueda}")
            if busqueda is None:
                print("No se encontró al cliente y su préstamo.")
                return False
            else:
                id_prestamo = busqueda[0]  # Asegúrate de que estás accediendo al índice correcto

                # Convertir fecha_limite al formato dd-mm-yyyy
                fecha_limite_formateada = fecha_limite.strftime('%Y-%m-%d')

                # Actualizar la fecha límite del préstamo
                cursor.execute('''
                    UPDATE prestamo
                    SET Fecha_Limite = %s
                    WHERE ID_Prestamo = %s
                ''', (fecha_limite_formateada, id_prestamo))
                
                # Confirmar la transacción
                mariadb_conexion.commit()
                print("Actualización exitosa.")
                return True
        except mariadb.Error as ex:
            print(f"Error durante la ejecución de la consulta: {ex}")
            return False
        finally:
            cursor.close()
            mariadb_conexion.close()
    else:
        print("No se pudo establecer la conexión con la base de datos.")
        return False

# Eliminar cliente
def delete_client_loans(self):
    selected_clients = self.clients_table_list_loans.selection()
    if not selected_clients:
        messagebox.showwarning("Selección vacía", "Por favor, seleccione un cliente de la tabla.")
        return
    
    respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar los clientes seleccionados?")
    if not respuesta:
        messagebox.showinfo("Cancelado", "Eliminación cancelada.")
        return

    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            clients_deleted = False
            for cliente in selected_clients:
                item_cliente = self.clients_table_list_loans.item(cliente, 'values')
                item_client = item_cliente[5]
                
                # Verificar si el cliente tiene préstamos relacionados
                cursor.execute('SELECT ID_CP FROM cliente_prestamo WHERE ID_Cliente = %s AND estado_cliente_prestamo = "activo"', (item_client,))
                prestamos_relacionados = cursor.fetchall()
                
                if prestamos_relacionados:
                    respuesta_prestamos = messagebox.askyesno(
                        "Confirmar Eliminación",
                        f"El cliente {item_client, 1} tiene préstamos relacionados. ¿Deseas eliminar todos los préstamos relacionados?"
                    )
                    if not respuesta_prestamos:
                        messagebox.showinfo("Cancelado", "Eliminación cancelada.")
                        return

                    # Marcar los préstamos relacionados como eliminados
                    cursor.execute('UPDATE cliente_prestamo SET estado_cliente_prestamo = "eliminado" WHERE ID_Cliente = %s', (item_client,))

                    # Marcar el cliente como eliminado
                cursor.execute('DELETE FROM cliente WHERE ID_Cliente= %s', (item_client,))
                # # Marcar el cliente como eliminado de forma eliminación lógica
                # cursor.execute('UPDATE cliente SET estado_cliente = "eliminado" WHERE ID_Cliente= %s', (item_client,))
                
                # Eliminar la fila del Treeview
                self.clients_table_list_loans.delete(cliente)
                clients_deleted = True

            if clients_deleted:
                mariadb_conexion.commit()
                messagebox.showinfo("Éxito", "El cliente y sus préstamos relacionados han sido eliminados.")
                print(f"Cliente con ID {item_client} y sus préstamos relacionados eliminados.")
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        messagebox.showerror("Error", f"Error durante la conexión: {ex}")
    finally:
        if mariadb_conexion:
            mariadb_conexion.close()


#Trae al treeview todos el listado de cliente 'activos'
def reading_clients(client_table_list_loans):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            cursor.execute('SELECT Cedula, Nombre, Apellido, Telefono, Direccion, ID_Cliente FROM cliente WHERE estado_cliente != "eliminado"')
            resultados = cursor.fetchall()
            cursor.close()
            mariadb_conexion.close()
            return resultados
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        return []



# Eliminar prestamo del cliente
def delete_selected_prestamo(self):
    selected_items = self.cliente_prestamo_table.selection()
    if not selected_items:
        messagebox.showwarning("Selección vacía", "Por favor, seleccione un préstamo de la tabla.")
        return
    
    respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar los préstamos seleccionados?")
    if not respuesta:
        messagebox.showinfo("Cancelado", "Eliminación cancelada.")
        return

    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            cliente_prestamo_table_deleted = False
            for item in selected_items:
                item_values = self.cliente_prestamo_table.item(item, 'values')
                item_id = item_values[7]

                # Marcar el registro como eliminado en lugar de eliminarlo
                cursor.execute('UPDATE cliente_prestamo SET estado_cliente_prestamo = "eliminado" WHERE ID_CP = %s', (item_id,))
                
                # Verificar si la actualización fue exitosa
                if cursor.rowcount == 0:
                    print(f"No se encontró el préstamo con ID_CP={item_id} o ya estaba eliminado.")
                    continue

                # Eliminar la fila del Treeview
                self.cliente_prestamo_table.delete(item)
                cliente_prestamo_table_deleted = True

            if cliente_prestamo_table_deleted:
                mariadb_conexion.commit()
                messagebox.showinfo("Éxito", "El préstamo ha sido marcado como eliminado.")
            else:
                messagebox.showwarning("Advertencia", "No se pudo eliminar ningún préstamo.")
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        messagebox.showerror("Error", f"Error durante la conexión: {ex}")
    finally:
        if mariadb_conexion:
            mariadb_conexion.close()


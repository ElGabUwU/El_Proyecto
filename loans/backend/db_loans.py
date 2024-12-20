import mysql.connector as mariadb
from colorama import init, Fore, Back, Style
from db.conexion import establecer_conexion
from tkinter import messagebox
from mysql.connector import Error
from validations.loans_validations import generate_alphanumeric_id
from datetime import datetime, timedelta
from loans.backend.sql_functions_db_loans import *

init(autoreset=True)
# Conectar a la base de datos
mariadb_conexion = establecer_conexion()

# Carga los prestamos activos
def load_active_loans(self):
    try:
        print("Intentando establecer conexión con la base de datos...")
        mariadb_conexion = establecer_conexion()
        if not mariadb_conexion:
            print("Failed to establish connection.")
            return

        cursor = mariadb_conexion.cursor()
        print("Conexión establecida. Ejecutando consulta para obtener préstamos activos...")

        query1 = '''
        SELECT
            c.Cedula,
            c.Nombre AS Nombre_Cliente,
            l.titulo AS Nombre_Libro,
            l.n_registro AS N_Registro,
            p.Fecha_Registro,
            p.Fecha_Limite,
            u.Nombre AS Nombre_Usuario,
            cp.ID_Prestamo
        FROM 
            cliente_prestamo cp
        JOIN
            prestamo p ON cp.ID_Prestamo = p.ID_Prestamo
        JOIN 
            cliente c ON cp.ID_Cliente = c.ID_Cliente
        JOIN
            libro l ON cp.ID_Libro = l.ID_Libro
        JOIN 
            usuarios u ON cp.ID_Usuario = u.ID_Usuario
        WHERE 
            cp.estado_cliente_prestamo = 'activo';
        '''

        cursor.execute(query1)
        resultados1 = cursor.fetchall()
        self.search_data = resultados1  # Almacenar los datos en self.search_data
        mariadb_conexion.close()
        self.search_current_page = 0  # Resetear a la primera página
        self.is_search_active = False
        self.display_page()
        
        # Debugging: Print the results
        print("Query executed successfully. Results:")
        for resultado in resultados1:
            print(resultado)

        # Verificar y establecer etiquetas para los colores de las filas
        hoy = datetime.now().date()
        prestamos_vencidos = []
        for fila in resultados1:
            # Ajustar el formato de la fecha para DD-MM-YYYY
            try:
                fecha_limite = datetime.strptime(fila[5], '%d-%m-%Y').date()
            except ValueError:
                fecha_limite = datetime.strptime(fila[5], '%Y-%m-%d').date()

            if fecha_limite <= hoy:
                tag = 'vencido'
                prestamos_vencidos.append(fila)
            else:
                tag = 'activo'

        # Configurar las etiquetas para los colores (no se inserta nada aquí)
        self.cliente_prestamo_table.tag_configure('vencido', background='#FF4C4C')
        self.cliente_prestamo_table.tag_configure('activo', background='white')
        
    except mariadb.Error as ex:
        print(f"Error during query execution: {ex}")
    finally:
        if mariadb_conexion is not None:
            cursor.close()
            mariadb_conexion.close()
            print("Connection closed.")




from datetime import datetime

def obtener_prestamos_vencidos():
    try:
        mariadb_conexion = establecer_conexion()
        if not mariadb_conexion:
            print("Failed to establish connection.")
            return []

        cursor = mariadb_conexion.cursor()

        query = '''
        SELECT
            cp.ID_Cliente
        FROM 
            cliente_prestamo cp
        JOIN
            prestamo p ON cp.ID_Prestamo = p.ID_Prestamo
        WHERE 
            cp.estado_cliente_prestamo = 'activo' AND
            p.Fecha_Limite <= CURDATE() AND
            cp.ID_Cliente IS NOT NULL AND
            cp.ID_Libro IS NOT NULL
        GROUP BY
            cp.ID_Cliente
        '''

        cursor.execute(query)
        clientes_con_prestamos_vencidos = cursor.fetchall()

        prestamos_vencidos = []

        # Depuración: Mostrar cuántos clientes con préstamos vencidos se encontraron
        print(f"Clientes con préstamos vencidos encontrados: {len(clientes_con_prestamos_vencidos)}")
        for cliente in clientes_con_prestamos_vencidos:
            id_cliente = cliente[0]
            print(f"ID Cliente: {id_cliente}")

            # Obtener y mostrar los datos de los préstamos de cada cliente
            cursor.execute('''
                SELECT 
                    c.Cedula, 
                    c.Nombre AS Nombre_Cliente, 
                    l.titulo AS Nombre_Libro, 
                    l.n_registro AS N_Registro, 
                    p.Fecha_Registro, 
                    p.Fecha_Limite, 
                    u.Nombre AS Nombre_Usuario, 
                    cp.ID_CP
                FROM 
                    cliente_prestamo cp
                JOIN 
                    prestamo p ON cp.ID_Prestamo = p.ID_Prestamo
                JOIN 
                    cliente c ON cp.ID_Cliente = c.ID_Cliente
                JOIN 
                    libro l ON cp.ID_Libro = l.ID_Libro
                JOIN 
                    usuarios u ON cp.ID_Usuario = u.ID_Usuario
                WHERE 
                    cp.ID_Cliente = %s AND
                    cp.estado_cliente_prestamo = 'activo' AND
                    p.Fecha_Limite <= CURDATE()
            ''', (id_cliente,))
            prestamos_cliente = cursor.fetchall()

            contador_prestamos_vencidos = 0
            for prestamo_cliente in prestamos_cliente:
                fecha_limite = datetime.strptime(prestamo_cliente[5], '%d-%m-%Y').date()
                if fecha_limite <= datetime.now().date():
                    contador_prestamos_vencidos += 1
                    print(f"Préstamo: {prestamo_cliente}")

            if contador_prestamos_vencidos > 0:
                prestamos_vencidos.append((id_cliente, contador_prestamos_vencidos))

        # Depuración: Mostrar cuántos préstamos vencidos tiene cada cliente
        for prestamo in prestamos_vencidos:
            print(f"ID Cliente: {prestamo[0]}, Préstamos Vencidos: {prestamo[1]}")

        return prestamos_vencidos

    except mariadb.Error as ex:
        print(f"Error during query execution: {ex}")
        return []
    finally:
        if mariadb_conexion is not None:
            cursor.close()
            mariadb_conexion.close()
            print("Connection closed.")

def mostrar_mensaje_prestamos_vencidos():
    prestamos_vencidos = obtener_prestamos_vencidos()
    if prestamos_vencidos:
        mensaje_vencidos = "Hay préstamos vencidos asociados a los siguientes clientes:\n\n"
        detalles_vencidos = ""
        for i, prestamo in enumerate(prestamos_vencidos):
            id_cliente = prestamo[0]
            datos_cliente = obtener_datos_cliente(id_cliente)
            if datos_cliente:
                if i < 2:
                    mensaje_vencidos += f"Cliente: {datos_cliente['Nombre']} {datos_cliente['Apellido']}\nCédula: {datos_cliente['Cedula']}\nTeléfono: {datos_cliente['Telefono']}\nPréstamos Vencidos: {prestamo[1]}\n\n"
                detalles_vencidos += f"Cliente: {datos_cliente['Nombre']} {datos_cliente['Apellido']}\nCédula: {datos_cliente['Cedula']}\nTeléfono: {datos_cliente['Telefono']}\nPréstamos Vencidos: {prestamo[1]}\n\n"
        
        mensaje_vencidos += "Por favor, contacte a los clientes para renovar los préstamos vencidos o devolver los libros. Consulte el apartado de préstamos para obtener más información sobre los libros prestados."
        detalles_vencidos += "Por favor, contacte a los clientes para renovar los préstamos vencidos o devolver los libros. Consulte el apartado de préstamos para obtener más información sobre los libros prestados."
        
        # Mostrar mensaje inicial con opción de ver más
        if len(prestamos_vencidos) > 2:
            if messagebox.askyesno("Préstamos Vencidos", f"{mensaje_vencidos}\n\n¿Desea ver más detalles?"):
                messagebox.showwarning("Detalles de Préstamos Vencidos", f"Hay préstamos vencidos asociados a los siguientes clientes:\n\n{detalles_vencidos}")
        else:
            messagebox.showwarning("Préstamos Vencidos", mensaje_vencidos)



#Función para actualizar/insertar datos en las columnas de tabla cliente_prestamos e igualmente en las tablas cliente y libro

def update_all_tables(ID_Cliente, ID_Libro, ID_Libro_Prestamo, ID_Prestamo, ID_Usuario, fecha_registrar, fecha_limite):
    try:
        # Establecer conexión a la base de datos
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor(buffered=True)
            print("Conexión a la base de datos establecida.")

            # Iniciar transacción
            mariadb_conexion.start_transaction()

            # Obtener los datos del libro
            cursor.execute("SELECT autor, editorial, titulo FROM libro_new WHERE ID_Libro = %s", (ID_Libro,))
            libro_data = cursor.fetchone()
            autor = libro_data[0]
            editorial = libro_data[1]
            titulo = libro_data[2]

            # Verificar la cantidad de ejemplares disponibles basándose en ID_Libro
            cursor.execute("""
                SELECT SUM(n_ejemplares) 
                FROM ejemplares 
                WHERE ID_Libro = %s
            """, (ID_Libro,))
            ejemplares_disponibles = cursor.fetchone()[0]
            print(f"Ejemplares disponibles para el libro {titulo} de {autor}: {ejemplares_disponibles}")

            if ejemplares_disponibles <= 1:
                print("No hay ejemplares disponibles para prestar.")
                messagebox.showerror("Error", "No hay ejemplares disponibles para prestar.")
                return False

            # Restar 1 a la cantidad de ejemplares
            cursor.execute("""
                UPDATE ejemplares 
                SET n_ejemplares = n_ejemplares - 1 
                WHERE ID_Libro = %s
            """, (ID_Libro,))
            print(f"Ejemplar prestado. Nuevos ejemplares disponibles: {ejemplares_disponibles - 1}")

            # Insertar un nuevo préstamo
            cursor.execute("""
                INSERT INTO prestamo (ID_Prestamo, fecha_registro, fecha_limite)
                VALUES (%s, %s, %s)
            """, (ID_Prestamo, fecha_registrar, fecha_limite))
            print(f"Nuevo préstamo insertado: {ID_Prestamo}, {fecha_registrar}, {fecha_limite}")

            # Verificar e insertar en libros_prestamo
            cursor.execute("""
                INSERT INTO libros_prestamo (ID_Libro_Prestamo, ID_Prestamo, ID_Libro)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE ID_Prestamo = VALUES(ID_Prestamo), ID_Libro = VALUES(ID_Libro)
            """, (ID_Libro_Prestamo, ID_Prestamo, ID_Libro))
            print(f"Registro insertado/verificado en libros_prestamo: ID_Libro_Prestamo={ID_Libro_Prestamo}, ID_Prestamo={ID_Prestamo}, ID_Libro={ID_Libro}")

            # Verificar si ya existe una entrada en cliente_prestamo
            cursor.execute("""
                SELECT COUNT(*) FROM cliente_prestamo WHERE ID_Cliente = %s AND ID_Prestamo = %s
            """, (ID_Cliente, ID_Prestamo))
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"El préstamo ya está asociado con el cliente: {ID_Cliente}, {ID_Prestamo}")
            else:
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


# def update_all_tables(ID_Cliente, ID_Libro, ID_Libro_Prestamo, ID_Prestamo, ID_Usuario):
#     try:
#         # Establecer conexión a la base de datos
#         mariadb_conexion = establecer_conexion()
#         if mariadb_conexion:
#             cursor = mariadb_conexion.cursor(buffered=True)
#             print("Conexión a la base de datos establecida.")

#             # Iniciar transacción
#             mariadb_conexion.start_transaction()

#             # Obtener los datos del libro
#             cursor.execute("SELECT autor, editorial, titulo FROM libro_new WHERE ID_Libro = %s", (ID_Libro,))
#             libro_data = cursor.fetchone()
#             autor = libro_data[0]
#             editorial = libro_data[1]
#             titulo = libro_data[2]

#             # Verificar la cantidad de ejemplares disponibles basándose en ID_Libro
#             cursor.execute("""
#                 SELECT SUM(n_ejemplares) 
#                 FROM ejemplares 
#                 WHERE ID_Libro = %s
#             """, (ID_Libro,))
#             ejemplares_disponibles = cursor.fetchone()[0]
#             print(f"Ejemplares disponibles para el libro {titulo} de {autor}: {ejemplares_disponibles}")

#             if ejemplares_disponibles <= 1:
#                 print("No hay ejemplares disponibles para prestar.")
#                 messagebox.showerror("Error", "No hay ejemplares disponibles para prestar.")
#                 return False

#             # Restar 1 a la cantidad de ejemplares
#             cursor.execute("""
#                 UPDATE ejemplares 
#                 SET n_ejemplares = n_ejemplares - 1 
#                 WHERE ID_Libro = %s
#             """, (ID_Libro,))
#             print(f"Ejemplar prestado. Nuevos ejemplares disponibles: {ejemplares_disponibles - 1}")

#             # Verificar e insertar en libros_prestamo
#             cursor.execute("""
#                 INSERT INTO libros_prestamo (ID_Libro_Prestamo, ID_Prestamo, ID_Libro)
#                 VALUES (%s, %s, %s)
#                 ON DUPLICATE KEY UPDATE ID_Prestamo = VALUES(ID_Prestamo), ID_Libro = VALUES(ID_Libro)
#             """, (ID_Libro_Prestamo, ID_Prestamo, ID_Libro))
#             print(f"Registro insertado/verificado en libros_prestamo: ID_Libro_Prestamo={ID_Libro_Prestamo}, ID_Prestamo={ID_Prestamo}, ID_Libro={ID_Libro}")

#             # Insertar en cliente_prestamo
#             cursor.execute("""
#                 INSERT INTO cliente_prestamo (ID_Cliente, ID_Prestamo, ID_Usuario, ID_Libro, ID_Libro_Prestamo)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, (ID_Cliente, ID_Prestamo, ID_Usuario, ID_Libro, ID_Libro_Prestamo))
#             print(f"Registro insertado en cliente_prestamo: ID_Cliente={ID_Cliente}, ID_Prestamo={ID_Prestamo}, ID_Usuario={ID_Usuario}, ID_Libro={ID_Libro}, ID_Libro_Prestamo={ID_Libro_Prestamo}")

#             # Obtener el ID_CP generado
#             cursor.execute("SELECT LAST_INSERT_ID()")
#             ID_CP = cursor.fetchone()[0]
#             print(f"ID_CP obtenido: {ID_CP}")

#             # Actualizar la tabla cliente con el ID_CP
#             cursor.execute("""
#                 UPDATE cliente
#                 SET ID_CP = %s
#                 WHERE ID_Cliente = %s
#             """, (ID_CP, ID_Cliente))
#             print(f"Tabla cliente actualizada con ID_CP={ID_CP} para ID_Cliente={ID_Cliente}")

#             # Actualizar la tabla prestamo con el ID_CP
#             cursor.execute("""
#                 UPDATE prestamo
#                 SET ID_CP = %s
#                 WHERE ID_Prestamo = %s
#             """, (ID_CP, ID_Prestamo))
#             print(f"Tabla prestamo actualizada con ID_CP={ID_CP} para ID_Prestamo={ID_Prestamo}")

#             # Confirmar transacción
#             mariadb_conexion.commit()
#             print("Transacción confirmada.")

#             return True
#     except mariadb.Error as e:
#         print(f"Error al conectar a la base de datos: {e}")
#         if mariadb_conexion:
#             mariadb_conexion.rollback()
#             print("Transacción revertida.")
#         return False
#     finally:
#         if mariadb_conexion:
#             cursor.close()
#             mariadb_conexion.close()
#             print("Conexión a la base de datos cerrada.")


#Función para seleccionar el préstamo que se le renovará su tiempo de préstamo
def renew_loan_due_date(id_prestamo):
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        try:
            # Obtener la fecha límite actual del préstamo
            cursor.execute("SELECT Fecha_Limite FROM prestamo WHERE ID_Prestamo = %s", (id_prestamo,))
            busqueda = cursor.fetchone()
            if busqueda is None:
                print(f"No se encontró el préstamo con el ID proporcionado: {id_prestamo}")
                return False
            else:
                fecha_limite_actual = busqueda[0]
                # Convertir fecha_limite_actual a un objeto datetime
                fecha_limite_actual = datetime.strptime(fecha_limite_actual, '%d-%m-%Y').date()
                hoy = datetime.now().date()

                # Verificar si el préstamo ya ha sido renovado hoy
                if fecha_limite_actual > hoy:
                    print("El préstamo ya ha sido renovado hoy.")
                    return False

                # Obtener el número de registro del libro asociado al préstamo
                cursor.execute("SELECT n_registro FROM libro WHERE ID_Libro = (SELECT ID_Libro FROM cliente_prestamo WHERE ID_Prestamo = %s)", (id_prestamo,))
                busqueda_libro = cursor.fetchone()
                if busqueda_libro is None:
                    print("No se pudo obtener el número de registro del libro.")
                    return False
                n_registro = busqueda_libro[0]

                # Obtener el ID del libro utilizando el número de registro
                id_libro = get_libro_id_by_registro(n_registro)
                if id_libro is None:
                    print("No se pudo obtener el ID del libro.")
                    return False

                # Verificar si el libro es una novela
                if es_novela(id_libro):
                    nueva_fecha_limite = fecha_limite_actual + timedelta(days=8)
                else:
                    nueva_fecha_limite = fecha_limite_actual + timedelta(days=3)

                # Convertir nueva_fecha_limite a cadena de texto en formato 'día-mes-año'
                nueva_fecha_limite = nueva_fecha_limite.strftime('%d-%m-%Y')

                # Actualizar la fecha límite del préstamo
                cursor.execute('''
                    UPDATE prestamo
                    SET Fecha_Limite = %s
                    WHERE ID_Prestamo = %s
                ''', (nueva_fecha_limite, id_prestamo))

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
            cursor = mariadb_conexion.cursor(buffered=True)
            cliente_prestamo_table_deleted = False
            for item in selected_items:
                item_values = self.cliente_prestamo_table.item(item, 'values')
                item_id = item_values[7]  # ID_Prestamo está en la posición 7
                nro_registro = item_values[3]  # Asegúrate de que este índice coincida con el número de registro en tu Treeview

                # Depuración: Verificar el ID_Prestamo
                print(f"ID_Prestamo seleccionado: {item_id}")

                # Obtener los datos del libro por número de registro
                cursor.execute("SELECT ln.autor, ln.editorial, ln.titulo FROM libro_new ln JOIN ejemplares e ON ln.ID_Libro = e.ID_Libro WHERE e.n_registro = %s", (nro_registro,))
                libro_data = cursor.fetchone()
                if not libro_data:
                    print(f"No se encontró el libro con número de registro {nro_registro}.")
                    continue
                autor, editorial, titulo = libro_data

                # Verificar si el préstamo ya está marcado como eliminado
                cursor.execute('SELECT estado_cliente_prestamo FROM cliente_prestamo WHERE ID_Prestamo = %s', (item_id,))
                estado_prestamo = cursor.fetchone()
                if estado_prestamo and estado_prestamo[0] == "eliminado":
                    print(f"El préstamo con ID_Prestamo={item_id} ya está marcado como eliminado.")
                    continue

                # Marcar el registro como eliminado en lugar de eliminarlo
                cursor.execute('UPDATE cliente_prestamo SET estado_cliente_prestamo = "eliminado" WHERE ID_Prestamo = %s', (item_id,))
                
                # Verificar si la actualización fue exitosa
                if cursor.rowcount == 0:
                    print(f"No se encontró el préstamo con ID_Prestamo={item_id} o ya estaba eliminado.")
                    continue

                # Sumar 1 a la cantidad de ejemplares disponibles basándose en ID_Libro
                cursor.execute("""
                    UPDATE ejemplares 
                    SET n_ejemplares = n_ejemplares + 1 
                    WHERE ID_Libro = (SELECT ID_Libro FROM libro_new WHERE autor = %s AND editorial = %s AND titulo = %s)
                """, (autor, editorial, titulo))
                print(f"Ejemplar devuelto. Autor={autor}, Editorial={editorial}, Título={titulo}")

                # Eliminar la fila del Treeview
                self.cliente_prestamo_table.delete(item)
                cliente_prestamo_table_deleted = True

            if cliente_prestamo_table_deleted:
                mariadb_conexion.commit()
                messagebox.showinfo("Éxito", "El préstamo ha sido marcado como eliminado y los ejemplares han sido actualizados.")
            else:
                messagebox.showwarning("Advertencia", "No se pudo eliminar ningún préstamo.")
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        messagebox.showerror("Error", f"Error durante la conexión: {ex}")
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()


# def delete_selected_prestamo(self):
#     selected_items = self.cliente_prestamo_table.selection()
#     if not selected_items:
#         messagebox.showwarning("Selección vacía", "Por favor, seleccione un préstamo de la tabla.")
#         return
    
#     respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar los préstamos seleccionados?")
#     if not respuesta:
#         messagebox.showinfo("Cancelado", "Eliminación cancelada.")
#         return

#     try:
#         mariadb_conexion = establecer_conexion()
#         if mariadb_conexion:
#             cursor = mariadb_conexion.cursor()
#             cliente_prestamo_table_deleted = False
#             for item in selected_items:
#                 item_values = self.cliente_prestamo_table.item(item, 'values')
#                 item_id = item_values[7]  # ID_Prestamo está en la posición 7
#                 nro_registro = item_values[3]  # Asegúrate de que este índice coincida con el número de registro en tu Treeview

#                 # Depuración: Verificar el ID_Prestamo
#                 print(f"ID_Prestamo seleccionado: {item_id}")

#                 # Obtener los datos del libro por número de registro
#                 cursor.execute("SELECT autor, editorial, titulo FROM libro WHERE n_registro = %s", (nro_registro,))
#                 libro_data = cursor.fetchone()
#                 if not libro_data:
#                     print(f"No se encontró el libro con número de registro {nro_registro}.")
#                     continue
#                 autor, editorial, titulo = libro_data

#                 # Verificar si el préstamo ya está marcado como eliminado
#                 cursor.execute('SELECT estado_cliente_prestamo FROM cliente_prestamo WHERE ID_Prestamo = %s', (item_id,))
#                 estado_prestamo = cursor.fetchone()
#                 if estado_prestamo and estado_prestamo[0] == "eliminado":
#                     print(f"El préstamo con ID_Prestamo={item_id} ya está marcado como eliminado.")
#                     continue

#                 # Marcar el registro como eliminado en lugar de eliminarlo
#                 cursor.execute('UPDATE cliente_prestamo SET estado_cliente_prestamo = "eliminado" WHERE ID_Prestamo = %s', (item_id,))
                
#                 # Verificar si la actualización fue exitosa
#                 if cursor.rowcount == 0:
#                     print(f"No se encontró el préstamo con ID_Prestamo={item_id} o ya estaba eliminado.")
#                     continue

#                 # Sumar 1 a la cantidad de ejemplares disponibles basándose en autor, editorial y título
#                 cursor.execute("""
#                     UPDATE libro 
#                     SET n_ejemplares = n_ejemplares + 1 
#                     WHERE autor = %s AND editorial = %s AND titulo = %s
#                 """, (autor, editorial, titulo))
#                 print(f"Ejemplar devuelto. Autor={autor}, Editorial={editorial}, Título={titulo}")

#                 # Eliminar la fila del Treeview
#                 self.cliente_prestamo_table.delete(item)
#                 cliente_prestamo_table_deleted = True

#             if cliente_prestamo_table_deleted:
#                 mariadb_conexion.commit()
#                 messagebox.showinfo("Éxito", "El préstamo ha sido marcado como eliminado y los ejemplares han sido actualizados.")
#             else:
#                 messagebox.showwarning("Advertencia", "No se pudo eliminar ningún préstamo.")
#     except mariadb.Error as ex:
#         print("Error durante la conexión:", ex)
#         messagebox.showerror("Error", f"Error durante la conexión: {ex}")
#     finally:
#         if mariadb_conexion:
#             mariadb_conexion.close()

def es_novela(id_libro):
    try:
        mariadb_conexion = establecer_conexion()
        if not mariadb_conexion:
            print("Failed to establish connection.")
            return False

        cursor = mariadb_conexion.cursor()

        query = '''
        SELECT 
            ID_Asignatura
        FROM 
            libro 
        WHERE 
            ID_Libro = %s
        '''

        cursor.execute(query, (id_libro,))
        resultado = cursor.fetchone()

        if resultado and 'Novela' in resultado[0]:
            return True
        else:
            return False

    except mariadb.Error as ex:
        print(f"Error durante la ejecución de la consulta: {ex}")
        return False
    finally:
        if mariadb_conexion is not None:
            cursor.close()
            mariadb_conexion.close()
            print("Connection closed.")


#Funciones de obtencion de datos para el reporte de prestamo
def get_cliente_id_by_cedula(cedula):
    try:
        mariadb_conexion = establecer_conexion()
        if not mariadb_conexion:
            print("Failed to establish connection.")
            return None

        cursor = mariadb_conexion.cursor()
        query = "SELECT ID_Cliente FROM cliente WHERE Cedula = %s"
        cursor.execute(query, (cedula,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None
    except mariadb.Error as ex:
        print(f"Error during query execution: {ex}")
        return None
    finally:
        if mariadb_conexion is not None:
            cursor.close()
            mariadb_conexion.close()
            print("Connection closed.")
            
def get_libro_id_by_registro(n_registro):
    try:
        mariadb_conexion = establecer_conexion()
        if not mariadb_conexion:
            print("Failed to establish connection.")
            return None
        cursor = mariadb_conexion.cursor()
        query = """
            SELECT e.ID_Libro 
            FROM ejemplares e
            JOIN libro_new ln ON e.ID_Libro = ln.ID_Libro
            WHERE e.n_registro = %s
        """
        cursor.execute(query, (n_registro,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except mariadb.Error as ex:
        print(f"Error during query execution: {ex}")
        return None
    finally:
        if mariadb_conexion is not None:
            cursor.close()
            mariadb_conexion.close()
            print("Connection closed.")

def ajustar_texto(texto, tipo):
    if tipo == "categoria":
        longitud_maxima = 53
    elif tipo == "titulo":
        longitud_maxima = 57
    else:
        return texto  # Si el tipo no es ni "categoria" ni "titulo", no se ajusta el texto

    if len(texto) > longitud_maxima:
        texto_ajustado = texto[:longitud_maxima-3] + "..."
        print(f"Original: {texto} (Longitud: {len(texto)})")
        print(f"Ajustado: {texto_ajustado} (Longitud: {len(texto_ajustado)})")
        return texto_ajustado
    print(f"Texto sin ajustar: {texto} (Longitud: {len(texto)})")
    return texto


#OBTENCION DE DATOS PARA REPORTE DE PDF
# OBTENCION DE DATOS PARA REPORTE DE PDF
def obtener_datos_libro(libro_id):
    try:
        conn = establecer_conexion()
        if conn:
            cursor = conn.cursor()
            query = '''
                SELECT e.ID_Sala, e.ID_Categoria, e.ID_Asignatura, e.Cota, e.n_registro, e.edicion, e.n_volumenes, ln.titulo, ln.autor, ln.editorial, e.año, SUM(e.n_ejemplares) as total_ejemplares
                FROM ejemplares e
                JOIN libro_new ln ON e.ID_Libro = ln.ID_Libro
                WHERE e.ID_Libro = %s
                GROUP BY e.ID_Sala, e.ID_Categoria, e.ID_Asignatura, e.Cota, e.n_registro, e.edicion, e.n_volumenes, ln.titulo, ln.autor, ln.editorial, e.año
            '''
            cursor.execute(query, (libro_id,))
            resultado_libro = cursor.fetchone()
            if resultado_libro:
                autor = resultado_libro[8]
                titulo = resultado_libro[7]
                editorial = resultado_libro[9]
                
                total_ejemplares = obtener_total_ejemplares(autor, titulo, editorial)
                ejemplares_prestados_por_cliente = obtener_ejemplares_prestados_por_cliente(autor, titulo, editorial)
                ejemplares_disponibles = obtener_ejemplares_disponibles(autor, titulo, editorial)
                
                book_data = {
                    "ID_Sala": resultado_libro[0],
                    "ID_Categoria": ajustar_texto(resultado_libro[1], "categoria"),
                    "ID_Asignatura": resultado_libro[2],
                    "Cota": resultado_libro[3],
                    "n_registro": resultado_libro[4],
                    "edicion": resultado_libro[5],
                    "n_volumenes": resultado_libro[6],
                    "titulo": ajustar_texto(resultado_libro[7], "titulo"),
                    "autor": resultado_libro[8],
                    "editorial": resultado_libro[9],
                    "año": resultado_libro[10],
                    "n_ejemplares": resultado_libro[11],
                    "total_ejemplares": total_ejemplares,
                    "ejemplares_prestados_por_cliente": ejemplares_prestados_por_cliente,
                    "ejemplares_disponibles": ejemplares_disponibles
                }
                #print("Book Data:", book_data)
                return book_data
            else:
                print("No se encontró información del libro.")
            conn.close()
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
    return None


# Función para obtener la cantidad total de ejemplares de un libro específico
def obtener_total_ejemplares(autor, titulo, editorial):
    try:
        conn = establecer_conexion()
        if conn:
            cursor = conn.cursor()
            query = '''
                SELECT SUM(n_ejemplares)
                FROM ejemplares e
                JOIN libro_new ln ON e.ID_Libro = ln.ID_Libro
                WHERE ln.autor = %s AND ln.titulo = %s AND ln.editorial = %s
            '''
            cursor.execute(query, (autor, titulo, editorial))
            total_ejemplares = cursor.fetchone()[0]
            conn.close()
            print(f"Total ejemplares para {titulo} de {autor}: {total_ejemplares}")
            return total_ejemplares
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
    return None


def obtener_ejemplares_prestados_por_cliente(autor, titulo, editorial):
    try:
        conn = establecer_conexion()
        if conn:
            cursor = conn.cursor()
            query = '''
                SELECT c.Cedula, COUNT(*)
                FROM cliente_prestamo cp
                JOIN ejemplares e ON cp.ID_Libro = e.ID_Libro
                JOIN cliente c ON cp.ID_Cliente = c.ID_Cliente
                JOIN libro_new ln ON e.ID_Libro = ln.ID_Libro
                WHERE ln.autor = %s AND ln.titulo = %s AND ln.editorial = %s AND cp.estado_cliente_prestamo = 'activo'
                GROUP BY c.Cedula
            '''
            cursor.execute(query, (autor, titulo, editorial))
            ejemplares_prestados_por_cliente = cursor.fetchall()
            conn.close()
            if ejemplares_prestados_por_cliente:
                # Extraer solo la cantidad de ejemplares prestados
                ejemplares_prestados = [cantidad for _, cantidad in ejemplares_prestados_por_cliente]
                print(f"Ejemplares prestados por cliente para {titulo} de {autor}: {ejemplares_prestados}")
                return ejemplares_prestados_por_cliente
            else:
                print("No se encontraron ejemplares prestados por cliente.")
                return []
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
    return []


def obtener_ejemplares_disponibles(autor, titulo, editorial):
    total_ejemplares = obtener_total_ejemplares(autor, titulo, editorial)
    ejemplares_prestados = sum([cantidad for _, cantidad in obtener_ejemplares_prestados_por_cliente(autor, titulo, editorial)])
    if total_ejemplares is not None and ejemplares_prestados is not None:
        ejemplares_disponibles = total_ejemplares - ejemplares_prestados
        print(f"Ejemplares disponibles para {titulo} de {autor}: {ejemplares_disponibles}")
        return ejemplares_disponibles
    return None

def obtener_datos_cliente(cliente_id):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            cursor.execute('''
                SELECT Cedula, Nombre, Apellido, Telefono, Direccion
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
                #print("User Data:", user_data)  # Depuración
                return user_data
            else:
                print("No se encontró información del cliente.")
            mariadb_conexion.close()
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
    return None

def obtener_datos_usuario(usuario_id):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            cursor.execute('''
                SELECT Cedula, Nombre, Apellido, ID_Cargo
                FROM usuarios
                WHERE ID_Usuario = %s
            ''', (usuario_id,))
            resultado_usuario = cursor.fetchone()
            #print(f"Resultado Usuario: {resultado_usuario}")  # Depuración
            if resultado_usuario:
                cargos = {
                    1: "Encargado de Servicio",
                    2: "Asistente Bibliotecario"
                }
                user_data = {
                    "Cedula": resultado_usuario[0],
                    "Nombre": resultado_usuario[1],
                    "Apellido": resultado_usuario[2],
                    "Cargo": cargos.get(resultado_usuario[3], "Desconocido")
                }
                print("User Data:", user_data)  # Depuración
                return user_data
            else:
                print("No se encontró información del usuario.")
            mariadb_conexion.close()
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
    return None

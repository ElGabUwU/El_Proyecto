import mysql.connector as mariadb
#import mariadb
from colorama import init, Fore, Back, Style
from db.conexion import establecer_conexion
import subprocess
from tkinter import messagebox
init(autoreset=True)

def obtener_datos_libros():
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            cursor.execute("SELECT titulo, n_registro FROM libros")
            datos = cursor.fetchall()
            mariadb_conexion.close()
            return datos
        else:
            return []
    except mariadb.Error as ex:
        print(f"Error durante la conexión: {ex}")
        return []

#FUNCIONES QUE SE USAN PARA LISTAR TODOS LOS LIBROS 
def get_book_data(book_status='activo'):
    try:
        mariadb_connection = establecer_conexion()
        if mariadb_connection:
            cursor = mariadb_connection.cursor()
            query = """
                SELECT 
                e.ID_Libro, 
                e.ID_Sala, 
                e.ID_Categoria, 
                e.ID_Asignatura, 
                e.Cota, 
                e.n_registro, 
                ln.titulo, 
                ln.autor, 
                ln.editorial, 
                e.año, 
                e.edicion, 
                e.n_volumenes, 
                SUM(e.n_ejemplares) as total_ejemplares,
                e.ID_Ejemplar
                FROM 
                    ejemplares e
                JOIN 
                    libro_new ln ON e.ID_Libro = ln.ID_Libro
                WHERE 
                    e.estado_ejemplar = %s AND ln.estado_new_libro = %s
                GROUP BY 
                    e.ID_Libro, e.ID_Sala, e.ID_Categoria, e.ID_Asignatura, e.Cota, e.n_registro, ln.titulo, ln.autor, ln.editorial, e.año, e.edicion, e.n_volumenes
            """
            cursor.execute(query, (book_status, book_status))
            data = cursor.fetchall()
            mariadb_connection.close()
            return data
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
    return []


def search_books(field, term, book_status='activo'):
    try:
        mariadb_connection = establecer_conexion()
        if mariadb_connection:
            cursor = mariadb_connection.cursor()
            query = f"""
                SELECT 
                e.ID_Libro, 
                e.ID_Sala, 
                e.ID_Categoria, 
                e.ID_Asignatura, 
                e.Cota, 
                e.n_registro, 
                ln.titulo, 
                ln.autor, 
                ln.editorial, 
                e.año, 
                e.edicion, 
                e.n_volumenes, 
                SUM(e.n_ejemplares) as total_ejemplares,
                e.ID_Ejemplar
                FROM 
                    ejemplares e
                JOIN 
                    libro_new ln ON e.ID_Libro = ln.ID_Libro
                WHERE 
                    LOWER({field}) LIKE %s
                    AND e.estado_ejemplar = %s 
                    AND ln.estado_new_libro = %s
                GROUP BY 
                    e.ID_Libro, e.ID_Sala, e.ID_Categoria, e.ID_Asignatura, e.Cota, e.n_registro, ln.titulo, ln.autor, ln.editorial, e.año, e.edicion, e.n_volumenes
            """
            cursor.execute(query, (f'%{term}%', book_status, book_status))
            data = cursor.fetchall()
            mariadb_connection.close()
            return data
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
    return []

# def search_books(field, term):
#     try:
#         mariadb_connection = establecer_conexion()
#         if mariadb_connection:
#             cursor = mariadb_connection.cursor()
#             query = f"""
#                 SELECT ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, titulo, autor, editorial, año, edicion, n_volumenes, n_ejemplares 
#                 FROM libro 
#                 WHERE LOWER({field}) LIKE %s
#             """
#             cursor.execute(query, (f'%{term}%',))
#             data = cursor.fetchall()
#             mariadb_connection.close()
#             return data
#     except mariadb.Error as ex:
#         print("Error durante la conexión:", ex)
#     return []


# Actualizar un libro
def check_asignatura_exists(cursor, ID_Asignatura):
    cursor.execute("SELECT COUNT(*) FROM asignatura WHERE ID_Asignatura = %s", (ID_Asignatura,))
    result = cursor.fetchone()
    return result[0] > 0
def obtener_longitudes_min_max():
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()

            # Consultas para obtener las longitudes mínimas y máximas
            consultas = {
                "titulo": "SELECT MIN(LENGTH(titulo)), MAX(LENGTH(titulo)) FROM libro",
                "autor": "SELECT MIN(LENGTH(autor)), MAX(LENGTH(autor)) FROM libro",
                "editorial": "SELECT MIN(LENGTH(editorial)), MAX(LENGTH(editorial)) FROM libro",
                "n_registro": "SELECT MIN(LENGTH(n_registro)), MAX(LENGTH(n_registro)) FROM libro",
                "n_volumenes": "SELECT MIN(LENGTH(n_volumenes)), MAX(LENGTH(n_volumenes)) FROM libro",
                "edicion": "SELECT MIN(LENGTH(edicion)), MAX(LENGTH(edicion)) FROM libro"
            }

            longitudes = {}
            for campo, consulta in consultas.items():
                cursor.execute(consulta)
                resultado = cursor.fetchone()
                longitudes[campo] = {"min": resultado[0], "max": resultado[1]}

            mariadb_conexion.close()
            return longitudes
    except mariadb.Error as ex:
        print(f"Error durante la consulta: {ex}")
        return None

def create_books(ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año):
    print("Valores recibidos para insertar el libro:")
    print("ID_Sala:", ID_Sala)
    print("ID_Categoria:", ID_Categoria)
    print("ID_Asignatura:", ID_Asignatura)
    print("Cota:", Cota)
    print("n_registro:", n_registro)
    print("Edicion:", edicion)
    print("n_volumenes:", n_volumenes)
    print("Titulo:", titulo)
    print("Autor:", autor)
    print("Editorial:", editorial)
    print("Año:", año)

    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            
            # Verificar si el libro ya existe en libro_new
            cursor.execute('''
                SELECT ID_Libro, estado_new_libro
                FROM libro_new
                WHERE titulo = %s AND autor = %s AND editorial = %s
            ''', (titulo, autor, editorial))
            resultado = cursor.fetchall()

            libro_eliminado = None
            ID_Libro = None

            for row in resultado:
                if row[1] == 'eliminado':
                    libro_eliminado = row[0]
                else:
                    ID_Libro = row[0]

            if libro_eliminado:
                # Reactivar el libro eliminado en libro_new
                cursor.execute('''
                    UPDATE libro_new
                    SET estado_new_libro = 'activo'
                    WHERE ID_Libro = %s
                ''', (libro_eliminado,))
                ID_Libro = libro_eliminado
            elif not ID_Libro:
                # Insertar el nuevo libro en libro_new
                cursor.execute('''
                    INSERT INTO libro_new (titulo, autor, editorial, estado_new_libro)
                    VALUES (%s, %s, %s, 'activo')
                ''', (titulo, autor, editorial))
                ID_Libro = cursor.lastrowid

            if ID_Libro:
                # Verificar si el ejemplar ya existe en ejemplares
                cursor.execute('''
                    SELECT ID_Ejemplar
                    FROM ejemplares
                    WHERE ID_Libro = %s AND ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND Cota = %s AND n_registro = %s AND edicion = %s AND año = %s AND n_volumenes = %s
                ''', (ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, año, n_volumenes))
                ejemplar_resultado = cursor.fetchall()

                if ejemplar_resultado:
                    # Actualizar el ejemplar existente
                    cursor.execute('''
                        UPDATE ejemplares
                        SET n_ejemplares = n_ejemplares + 1, estado_ejemplar = 'activo'
                        WHERE ID_Ejemplar = %s
                    ''', (ejemplar_resultado[0][0],))
                else:
                    # Insertar el nuevo ejemplar en la tabla ejemplares
                    cursor.execute('''
                        INSERT INTO ejemplares (ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, año, n_volumenes, n_ejemplares, estado_ejemplar)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1, 'activo')
                    ''', (ID_Libro, ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, año, n_volumenes))
            
            mariadb_conexion.commit()
            mariadb_conexion.close()
            return True
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        return False
    
# def create_books(ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año):
#     print("Valores recibidos para insertar el libro:")
#     print("ID_Sala:", ID_Sala)
#     print("ID_Categoria:", ID_Categoria)
#     print("ID_Asignatura:", ID_Asignatura)
#     print("Cota:", Cota)
#     print("n_registro:", n_registro)
#     print("Edicion:", edicion)
#     print("n_volumenes:", n_volumenes)
#     print("Titulo:", titulo)
#     print("Autor:", autor)
#     print("Editorial:", editorial)
#     print("Año:", año)

#     try:
#         mariadb_conexion = establecer_conexion()
#         if mariadb_conexion:
#             cursor = mariadb_conexion.cursor()
            
#             # Verificar si ya existen registros con la misma sala, categoría, asignatura, autor, editorial, título y año
#             cursor.execute('''
#                 SELECT ID_Libro, n_ejemplares, estado_libro
#                 FROM libro
#                 WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND autor = %s AND editorial = %s AND titulo = %s AND año = %s
#             ''', (ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año))
#             resultado = cursor.fetchall()

#             libro_eliminado = None
#             n_ejemplares_actual = 0

#             for row in resultado:
#                 if row[2] == 'eliminado':
#                     libro_eliminado = row[0]
#                 else:
#                     n_ejemplares_actual = max(n_ejemplares_actual, row[1])

#             if libro_eliminado:
#                 # Reactivar el libro eliminado
#                 cursor.execute('''
#                     UPDATE libro
#                     SET estado_libro = 'activo', n_ejemplares = n_ejemplares + 1
#                     WHERE ID_Libro = %s
#                 ''', (libro_eliminado,))
#             else:
#                 n_ejemplares_nuevo = n_ejemplares_actual + 1
                
#                 # Insertar el nuevo libro con el número de ejemplares incrementado
#                 cursor.execute('''
#                     INSERT INTO libro (ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares, estado_libro)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'activo')
#                 ''', (ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares_nuevo))
            
#             mariadb_conexion.commit()
#             mariadb_conexion.close()
#             return True
#     except mariadb.Error as ex:
#         print("Error durante la conexión:", ex)
#         return False


#import mariadb

def update_books(book_data, nuevos_valores):
    try:
        # Establecer conexión con la base de datos
        mariadb_conexion = establecer_conexion()
        if not mariadb_conexion:
            print("No se pudo establecer la conexión con la base de datos.")
            return False
        
        cursor = mariadb_conexion.cursor()
        cambios_realizados = False

        # Imprimir datos para depuración
        print("Datos para actualizar:", book_data, nuevos_valores)
        
        # Asegúrate de que book_data contiene el ID del libro
        if 'ID' not in book_data:
            print("ID del libro no proporcionado")
            return False
        
        # Validar los nuevos valores
        required_fields = ['ID_Sala', 'ID_Categoria', 'ID_Asignatura', 'Cota', 'n_registro', 'Titulo', 'Autor', 'Editorial', 'Año', 'Edicion', 'n_volumenes']
        for field in required_fields:
            if field not in nuevos_valores:
                print(f"Falta el campo requerido: {field}")
                return False

        # Ejecutar la consulta para verificar si el libro existe en libro_new
        cursor.execute("SELECT * FROM libro_new WHERE ID_Libro = %s", (book_data['ID'],))
        libro_actual = cursor.fetchone()
        print("Datos actuales del libro:", libro_actual)
        
        if libro_actual is None:
            print(f"Libro con ID {book_data['ID']} no encontrado.")
            return False
        
        # Verificar si hay cambios en los datos críticos
        campos_criticos = ['Titulo', 'Autor', 'Editorial']
        cambios = any(libro_actual[i + 1] != nuevos_valores[field] for i, field in enumerate(campos_criticos))
        
        if cambios:
            # Si hay cambios, actualizar todos los registros coincidentes en libro_new
            cursor.execute('''
                UPDATE libro_new
                SET titulo=%s, autor=%s, editorial=%s
                WHERE ID_Libro = %s
            ''', (
                nuevos_valores['Titulo'], nuevos_valores['Autor'], nuevos_valores['Editorial'], book_data['ID']
            ))
        
        # Ejecutar la actualización en la base de datos para el ejemplar específico
        cursor.execute('''
            UPDATE ejemplares
            SET ID_Sala=%s, ID_Categoria=%s, ID_Asignatura=%s, Cota=%s, n_registro=%s, año=%s, edicion=%s, n_volumenes=%s
            WHERE ID_Libro=%s
        ''', (
            nuevos_valores['ID_Sala'], nuevos_valores['ID_Categoria'], nuevos_valores['ID_Asignatura'],
            nuevos_valores['Cota'], nuevos_valores['n_registro'], nuevos_valores['Año'],
            nuevos_valores['Edicion'], nuevos_valores['n_volumenes'], book_data['ID']
        ))

        cambios_realizados = True

        # Confirmar los cambios
        mariadb_conexion.commit()
        mariadb_conexion.close()
        print("Libro actualizado exitosamente")
        return cambios_realizados
    
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        return False


def delete_selected(self):
    selected_items = self.book_table_list.selection()
    if not selected_items:
        messagebox.showwarning("Advertencia", "No se ha seleccionado ningún libro.")
        return

    respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar el libro seleccionado?")
    if not respuesta:
        return

    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            for item in selected_items:
                item_id = self.book_table_list.item(item, 'values')[13]

                # Obtener los detalles del ejemplar
                cursor.execute('''
                    SELECT e.ID_Sala, e.ID_Categoria, e.ID_Asignatura, ln.autor, ln.editorial, ln.titulo, e.año, e.n_ejemplares, e.estado_ejemplar, ln.ID_Libro
                    FROM ejemplares e
                    JOIN libro_new ln ON e.ID_Libro = ln.ID_Libro
                    WHERE e.ID_Ejemplar = %s
                ''', (item_id,))
                ejemplar_detalles = cursor.fetchone()

                if ejemplar_detalles:
                    ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año, n_ejemplares_actual, estado_ejemplar, ID_Libro = ejemplar_detalles

                    # Verificar si ya existen registros con la misma sala, categoría, asignatura, autor, editorial, título y año
                    cursor.execute('''
                        SELECT e.n_ejemplares
                        FROM ejemplares e
                        JOIN libro_new ln ON e.ID_Libro = ln.ID_Libro
                        WHERE e.ID_Sala = %s AND e.ID_Categoria = %s AND e.ID_Asignatura = %s AND ln.autor = %s AND ln.editorial = %s AND ln.titulo = %s AND e.año = %s AND e.estado_ejemplar = 'activo'
                    ''', (ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año))
                    resultado = cursor.fetchall()

                    if resultado:
                        n_ejemplares_actual = max([row[0] for row in resultado])
                        n_ejemplares_nuevo = n_ejemplares_actual - 1

                        if n_ejemplares_nuevo > 0:
                            cursor.execute('''
                                UPDATE ejemplares
                                SET n_ejemplares = %s
                                WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND ID_Libro = %s AND año = %s AND estado_ejemplar = 'activo'
                            ''', (n_ejemplares_nuevo, ID_Sala, ID_Categoria, ID_Asignatura, ID_Libro, año))
                        else:
                            cursor.execute('''
                                UPDATE ejemplares
                                SET estado_ejemplar = 'eliminado'
                                WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND ID_Libro = %s AND año = %s AND estado_ejemplar = 'activo'
                            ''', (ID_Sala, ID_Categoria, ID_Asignatura, ID_Libro, año))

                    # Actualizar el estado del libro en libro_new
                    cursor.execute('''
                        UPDATE libro_new
                        SET estado_new_libro = 'eliminado'
                        WHERE ID_Libro = %s
                    ''', (ID_Libro,))

                    self.book_table_list.delete(item)

            mariadb_conexion.commit()
            messagebox.showinfo("Éxito", "El libro ha sido eliminado correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo establecer la conexión a la base de datos.")
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        messagebox.showerror("Error", f"Error durante la conexión: {ex}")
    finally:
        if mariadb_conexion:
            mariadb_conexion.close()

# def delete_selected(self):
#     selected_items = self.book_table_list.selection()
#     if not selected_items:
#         messagebox.showwarning("Advertencia", "No se ha seleccionado ningún libro.")
#         return

#     respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar el libro seleccionado?")
#     if not respuesta:
#         return

#     try:
#         mariadb_conexion = establecer_conexion()
#         if mariadb_conexion:
#             cursor = mariadb_conexion.cursor()
#             for item in selected_items:
#                 item_id = self.book_table_list.item(item, 'values')[0]

#                 # Obtener los detalles del libro
#                 cursor.execute('''
#                     SELECT ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año, n_ejemplares, estado_libro
#                     FROM ejemplares
#                     WHERE ID_Libro = %s
#                 ''', (item_id,))
#                 libro_detalles = cursor.fetchone()

#                 if libro_detalles:
#                     ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año, n_ejemplares_actual, estado_libro = libro_detalles

#                     # Verificar si ya existen registros con la misma sala, categoría, asignatura, autor, editorial, título y año
#                     cursor.execute('''
#                         SELECT n_ejemplares
#                         FROM ejemplares
#                         WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND autor = %s AND editorial = %s AND titulo = %s AND año = %s AND estado_libro = 'activo'
#                     ''', (ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año))
#                     resultado = cursor.fetchall()

#                     if resultado:
#                         n_ejemplares_actual = max([row[0] for row in resultado])
#                         n_ejemplares_nuevo = n_ejemplares_actual - 1

#                         if n_ejemplares_nuevo > 0:
#                             cursor.execute('''
#                                 UPDATE libro_new
#                                 SET n_ejemplares = %s
#                                 WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND autor = %s AND editorial = %s AND titulo = %s AND año = %s AND estado_libro = 'activo'
#                             ''', (n_ejemplares_nuevo, ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año))
#                         else:
#                             cursor.execute('''
#                                 UPDATE libro
#                                 SET estado_libro = 'eliminado'
#                                 WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND autor = %s AND editorial = %s AND titulo = %s AND año = %s AND estado_libro = 'activo'
#                             ''', (ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año))

#                     self.book_table_list.delete(item)

#             mariadb_conexion.commit()
#             messagebox.showinfo("Éxito", "El libro ha sido eliminado correctamente.")
#         else:
#             messagebox.showerror("Error", "No se pudo establecer la conexión a la base de datos.")
#     except mariadb.Error as ex:
#         print("Error durante la conexión:", ex)
#         messagebox.showerror("Error", f"Error durante la conexión: {ex}")
#     finally:
#         if mariadb_conexion:
#             mariadb_conexion.close()
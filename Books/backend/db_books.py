
import mysql.connector as mariadb
from colorama import init, Fore, Back, Style
from db.conexion import establecer_conexion
import subprocess
from tkinter import messagebox
init(autoreset=True)
# # Conectar a la base de datos
# def import_sql_file():
#     try:
#         subprocess.run(['mysql', '-u', 'root', '-p2525', 'basedatosbiblioteca', '<', 'backend/BD_BIBLIOTECA_V7.sql'], check=True)
#     except subprocess.CalledProcessError as e:
#         print("Error al importar el archivo SQL:", e)

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


# Leer todos los libros
def read_books(book_name):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor=mariadb_conexion.cursor()
            cursor.execute('''
                SELECT * FROM libro''')
            resultados=cursor.fetchall()
            print("\t\t\t\t\t===================LEYENDA========================")
            print("\n")
            print(f"\t\t\t\t\t\t ||{Fore.BLUE}IDLibro{Fore.LIGHTWHITE_EX}--{Fore.BLUE}Cota{Fore.LIGHTWHITE_EX}--{Fore.BLUE}IDPrestamo{Fore.LIGHTWHITE_EX}||")
            print("\n")
            print(f"\t\t\t\t\t    ||{Fore.GREEN}IDCategoria{Fore.LIGHTWHITE_EX}--{Fore.GREEN}IDSala{Fore.LIGHTWHITE_EX}--{Fore.GREEN}IDAsignatura{Fore.LIGHTWHITE_EX}||")
            print("\n")
            print(f"\t\t\t\t\t\t||{Fore.RED}N°Registro{Fore.LIGHTWHITE_EX}--{Fore.RED}Autor{Fore.LIGHTWHITE_EX}--{Fore.RED}Titulo{Fore.LIGHTWHITE_EX}||")
            print("\n")
            print(f"\t\t\t\t\t   ||{Fore.YELLOW}Asignatura{Fore.LIGHTWHITE_EX}--{Fore.YELLOW}N°Volumenes{Fore.LIGHTWHITE_EX}--{Fore.YELLOW}N°Ejemplares{Fore.LIGHTWHITE_EX}||")
            print("\n")
            print(f"\t\t\t\t\t\t  ||{Fore.CYAN}Edición{Fore.LIGHTWHITE_EX}--{Fore.CYAN}Año{Fore.LIGHTWHITE_EX}--{Fore.CYAN}Editorial{Fore.LIGHTWHITE_EX}||")
            print("\t\t\t\t\t===================================================")
            for fila in resultados:
                print(f"""
    ||===================================================================================||
    |||{Fore.BLUE}{fila[0]}--{fila[1]}--{fila[2]}{Fore.LIGHTWHITE_EX}
    |||{Fore.GREEN}{fila[3]}--{fila[4]}--{fila[5]}{Fore.LIGHTWHITE_EX}
    |||{Fore.RED}{fila[6]}--{fila[7]}--{fila[8]}{Fore.LIGHTWHITE_EX}
    |||{Fore.YELLOW}{fila[9]}-{fila[10]}--{fila[11]}{Fore.LIGHTWHITE_EX}
    |||{Fore.CYAN}{fila[12]}-{fila[13]}-
    ||===================================================================================||
                    """)
            mariadb_conexion.close()
            return resultados
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)

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
            
            # Verificar si ya existen registros con la misma sala, categoría, asignatura, autor, editorial, título y año
            cursor.execute('''
                SELECT n_ejemplares
                FROM libro
                WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND autor = %s AND editorial = %s AND titulo = %s AND año = %s
            ''', (ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año))
            resultado = cursor.fetchall()

            # Incrementar el número de ejemplares si existen registros coincidentes
            if resultado:
                n_ejemplares_actual = max([row[0] for row in resultado])
                n_ejemplares_nuevo = n_ejemplares_actual + 1
                
                cursor.execute('''
                    UPDATE libro
                    SET n_ejemplares = %s
                    WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND autor = %s AND editorial = %s AND titulo = %s AND año = %s
                ''', (n_ejemplares_nuevo, ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año))
                
            else:
                n_ejemplares_nuevo = 1
            
            # Insertar el nuevo libro con el número de ejemplares incrementado
            cursor.execute('''
                INSERT INTO libro (ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares_nuevo))
            
            mariadb_conexion.commit()
            mariadb_conexion.close()
            return True
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        return False


import mariadb

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

        # Ejecutar la consulta para verificar si el libro existe
        cursor.execute("SELECT * FROM libro WHERE ID_Libro = %s", (book_data['ID'],))
        libro_actual = cursor.fetchone()
        print("Datos actuales del libro:", libro_actual)
        
        if libro_actual is None:
            print(f"Libro con ID {book_data['ID']} no encontrado.")
            return False
        
        # Verificar si hay cambios en los datos críticos
        campos_criticos = ['Titulo', 'Autor', 'Editorial', 'Año']
        cambios = any(book_data[field] != nuevos_valores[field] for field in campos_criticos)
        
        if cambios:
            # Si hay cambios, actualizar todos los registros coincidentes
            cursor.execute('''
                UPDATE libro
                SET Titulo=%s, Autor=%s, Editorial=%s, Año=%s
                WHERE ID_Sala=%s AND ID_Categoria=%s AND ID_Asignatura=%s AND Cota=%s
            ''', (
                nuevos_valores['Titulo'], nuevos_valores['Autor'], nuevos_valores['Editorial'], nuevos_valores['Año'],
                book_data['ID_Sala'], book_data['ID_Categoria'], book_data['ID_Asignatura'], book_data['Cota']
            ))
        
        # Ejecutar la actualización en la base de datos para el libro específico
        cursor.execute('''
            UPDATE libro
            SET ID_Sala=%s, ID_Categoria=%s, ID_Asignatura=%s, Cota=%s, n_registro=%s, Titulo=%s, Autor=%s, Editorial=%s, Año=%s, Edicion=%s, n_volumenes=%s
            WHERE ID_Libro=%s
        ''', (
            nuevos_valores['ID_Sala'], nuevos_valores['ID_Categoria'], nuevos_valores['ID_Asignatura'],
            nuevos_valores['Cota'], nuevos_valores['n_registro'], nuevos_valores['Titulo'],
            nuevos_valores['Autor'], nuevos_valores['Editorial'], nuevos_valores['Año'],
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
                    item_id = self.book_table_list.item(item, 'values')[0]

                    # Obtener los detalles del libro
                    cursor.execute('''
                        SELECT ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año, n_ejemplares
                        FROM libro
                        WHERE ID_Libro = %s
                    ''', (item_id,))
                    libro_detalles = cursor.fetchone()

                    if libro_detalles:
                        ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año, n_ejemplares_actual = libro_detalles

                        # Verificar si ya existen registros con la misma sala, categoría, asignatura, autor, editorial, título y año
                        cursor.execute('''
                            SELECT n_ejemplares
                            FROM libro
                            WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND autor = %s AND editorial = %s AND titulo = %s AND año = %s
                        ''', (ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año))
                        resultado = cursor.fetchall()

                        if resultado:
                            n_ejemplares_actual = max([row[0] for row in resultado])
                            n_ejemplares_nuevo = n_ejemplares_actual - 1

                            if n_ejemplares_nuevo > 0:
                                cursor.execute('''
                                    UPDATE libro
                                    SET n_ejemplares = %s
                                    WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND autor = %s AND editorial = %s AND titulo = %s AND año = %s
                                ''', (n_ejemplares_nuevo, ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año))
                            else:
                                cursor.execute('''
                                    DELETE FROM libro
                                    WHERE ID_Sala = %s AND ID_Categoria = %s AND ID_Asignatura = %s AND autor = %s AND editorial = %s AND titulo = %s AND año = %s
                                ''', (ID_Sala, ID_Categoria, ID_Asignatura, autor, editorial, titulo, año))

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

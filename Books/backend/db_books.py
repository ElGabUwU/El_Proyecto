
import mysql.connector as mariadb
from colorama import init, Fore, Back, Style
from db.conexion import establecer_conexion
import subprocess

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

from collections import Counter

def analizar_titulos_y_registros(datos):
    caracteres_especiales = {}
    numeros_en_titulos = False
    patrones_punto = {}

    for titulo, n_registro in datos:
        # Analizar caracteres especiales en títulos
        for char in titulo:
            if not char.isalnum() and not char.isspace():
                if char in caracteres_especiales:
                    caracteres_especiales[char] += 1
                else:
                    caracteres_especiales[char] = 1
            if char.isdigit():
                numeros_en_titulos = True

        # Analizar patrones en números de registro
        if '.' in n_registro:
            posiciones = [pos for pos, char in enumerate(n_registro) if char == '.']
            for posicion in posiciones:
                if posicion in patrones_punto:
                    patrones_punto[posicion] += 1
                else:
                    patrones_punto[posicion] = 1

    return caracteres_especiales, numeros_en_titulos, patrones_punto
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



# Crear un nuevo Pokémon
def create_books(ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares):
    print("ID SALA", {ID_Sala}, "ID CATEGORIA", {ID_Categoria}, "ID ASIGNATURA", {ID_Asignatura}, "COTA", {Cota}, "REGISTRO", {n_registro})
    print("Edicion", {edicion}, "VOLUMEN", {n_volumenes}, "TITULO", {titulo}, "AUTOR", {autor}, "EDITORIAL", {editorial}, "AÑO", {año}, "EJEMPLARES", {n_ejemplares})
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor=mariadb_conexion.cursor()
            cursor.execute('''
                INSERT INTO libro (ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares))
            mariadb_conexion.commit()
            mariadb_conexion.close()
            return True
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)

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

        # Verificar si hay cambios en los datos
        cambios = any(
            libro_actual[i] != nuevos_valores[field] for i, field in enumerate(required_fields, start=1)
        )

        if not cambios:
            print(f"No hay cambios en los datos del libro con ID {book_data['ID']}.")
            return False

        # Verificar que ID_Asignatura existe en la tabla asignatura
        if not check_asignatura_exists(cursor, nuevos_valores['ID_Asignatura']):
            print(f"ID_Asignatura {nuevos_valores['ID_Asignatura']} no existe en la tabla asignatura.")
            return False

        # Ejecutar la actualización en la base de datos
        cursor.execute('''
            UPDATE libro
            SET ID_Sala=%s, ID_Categoria=%s, ID_Asignatura=%s, Cota=%s, n_registro=%s, Titulo=%s, Autor=%s, Editorial=%s, Año=%s, Edicion=%s, n_volumenes=%s
            WHERE ID_Libro=%s
        ''', (
            nuevos_valores['ID_Sala'], nuevos_valores['ID_Categoria'], nuevos_valores['ID_Asignatura'],
            nuevos_valores['Cota'], nuevos_valores['n_registro'], nuevos_valores['Titulo'],
            nuevos_valores['Autor'], nuevos_valores['Editorial'], nuevos_valores['Año'],
            nuevos_valores['Edicion'], nuevos_valores['n_volumenes'],
            book_data['ID']
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


        

# Eliminar un libro
def delete_books(ID_Libro):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            with mariadb_conexion.cursor() as cursor:
                # Executing the delete statement
                cursor.execute('DELETE FROM libro WHERE ID_Libro=%s', (ID_Libro,))
                if cursor.rowcount == 0:
                    print("No se encontró el libro con el ID proporcionado.")
                    return False
                # Committing the transaction
                mariadb_conexion.commit()
        return True
    except mariadb.Error as err:
        # Handling any database errors
        print(f"Error: {err}")
        return False
    
def delete_selected(self):
        selected_items = self.book_table_list.selection()
        try:
            mariadb_conexion = establecer_conexion()
            if mariadb_conexion:
                cursor = mariadb_conexion.cursor()
                for item in selected_items:
                    item_id = self.book_table_list.item(item, 'values')[0]
                    cursor.execute('DELETE FROM libro WHERE ID_Libro = %s', (item_id,))
                    self.book_table_list.delete(item)
                mariadb_conexion.commit()
                mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)

#import sqlite3
import mysql.connector as mariadb
from colorama import init, Fore, Back, Style
import subprocess

init(autoreset=True)
# # Conectar a la base de datos
# def import_sql_file():
#     try:
#         subprocess.run(['mysql', '-u', 'root', '-p2525', 'basedatosbiblioteca', '<', 'backend/BD_BIBLIOTECA_V7.sql'], check=True)
#     except subprocess.CalledProcessError as e:
#         print("Error al importar el archivo SQL:", e)

def connect():
    #mariadb_conexion = mariadb.connect('backend/BD_BIBLIOTECA_V7.sql')
    mariadb_conexion= mariadb.connect(host='localhost',
                                        port='3306',
                                        password='2525',
                                        database='basedatosbiblioteca')
    return mariadb_conexion

# Crear un nuevo Pokémon
def create_books(ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares):
    print("ID SALA", {ID_Sala}, "ID CATEGORIA", {ID_Categoria}, "ID ASIGNATURA", {ID_Asignatura}, "COTA", {Cota}, "REGISTRO", {n_registro})
    print("Edicion", {edicion}, "VOLUMEN", {n_volumenes}, "TITULO", {titulo}, "AUTOR", {autor}, "EDITORIAL", {editorial}, "AÑO", {año}, "EJEMPLARES", {n_ejemplares})
    try:
        mariadb_conexion=connect()
        if mariadb_conexion.is_connected():
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
        mariadb_conexion=connect()
        if mariadb_conexion.is_connected():
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
def update_books(ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares, ID_Libro,):
    mariadb_conexion=connect()
    cursor = mariadb_conexion.cursor()
    cursor.execute("SELECT ID_Libro FROM libro WHERE ID_Libro = %s", (ID_Libro,))
    busqueda=()
    busqueda=cursor.fetchone()
    print(busqueda)
    if busqueda is None:
        mariadb_conexion.close()
        return False
    else:
        cursor.execute('''
            UPDATE libro
            SET ID_Sala=%s, ID_Categoria=%s, ID_Asignatura=%s, Cota=%s, n_registro=%s, edicion=%s, n_volumenes=%s, 
            titulo=%s, autor=%s, editorial=%s, año=%s, n_ejemplares=%s WHERE ID_Libro=%s
        ''', (ID_Sala, ID_Categoria, ID_Asignatura, Cota, n_registro, edicion, n_volumenes, titulo, autor, editorial, año, n_ejemplares, ID_Libro))
        mariadb_conexion.commit()
        mariadb_conexion.close()
        return True

# Eliminar un libro
def delete_books(ID_Libro):
    try:
        # Establishing the connection using a context manager
        with connect() as mariadb_conexion:
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
            mariadb_conexion=connect()
            cursor = mariadb_conexion.cursor()
            for item in selected_items:
                item_id = self.book_table_list.item(item, 'values')[0]
                cursor.execute('DELETE FROM libro WHERE ID_Libro = %s', (item_id,))
                self.book_table_list.delete(item)
            mariadb_conexion.commit()
            mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)
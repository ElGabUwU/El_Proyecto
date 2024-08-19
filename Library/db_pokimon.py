#import sqlite3
import mysql.connector as mariadb
from colorama import init, Fore, Back, Style

init(autoreset=True)
# Conectar a la base de datos
def connect():
    #conn = mariadb.connect('Library/pokimons.db')
    mariadb_conexion=mariadb.connect(host='localhost',
                                        port='3306',
                                        password='2525',
                                        database='basedatosbiblioteca')
    return mariadb_conexion

# Crear un nuevo Pokémon
def create_pokemon(Cota, n_registro, autor, titulo, asignatura, n_volumenes, n_ejemplares, edicion, año, editorial):
    try:
        mariadb_conexion=connect()
        if mariadb_conexion.is_connected():
            cursor=mariadb_conexion.cursor()
            cursor.execute('''
                INSERT INTO pokemons (Cota, n_registro, autor, titulo, asignatura, n_volumenes, n_ejemplares, edicion, año, editorial)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (Cota, n_registro, autor, titulo, asignatura, n_volumenes, n_ejemplares, edicion, año, editorial))
            mariadb_conexion.commit()
            mariadb_conexion.close()
            return True
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)

# Leer todos los Pokémon
def read_pokemons():
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
    |||{Fore.CYAN}{fila[12]}-{fila[13]}-{fila[14]}{Fore.LIGHTWHITE_EX}
    ||===================================================================================||
                    """)
            mariadb_conexion.close()
            return resultados
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)

# Actualizar un Pokémon
def update_pokemon(Cota, n_registro, autor, titulo, asignatura, n_volumenes, n_ejemplares, edicion, año, editorial):
    mariadb_conexion=connect()
    cursor = mariadb_conexion.cursor()
    cursor.execute("SELECT autor FROM libro WHERE autor = ?", (autor))
    busqueda=()
    busqueda=cursor.fetchone()
    print(busqueda)
    if busqueda is None:
        mariadb_conexion.close()
        return False
    else:
        cursor.execute('''
            UPDATE libro
            SET autor=?, Cota=?, n_registro=?, titulo=?, asignatura=?, n_volumenes=?, n_ejemplares=?,
            edicion=?, año=?, editorial=?
            WHERE autor=?
        ''', (autor, Cota, n_registro, titulo, asignatura, n_volumenes, n_ejemplares, edicion, año, editorial))
        mariadb_conexion.commit()
        mariadb_conexion.close()
        return True

# Eliminar un Pokémon
def delete_pokemon(ID_Libro):
    mariadb_conexion=connect()
    cursor = mariadb_conexion.cursor()
    cursor.execute('DELETE FROM libro WHERE ID_Libro=?', (ID_Libro))
    mariadb_conexion.commit()
    mariadb_conexion.close()
    return True
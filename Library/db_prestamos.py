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

# Crear un nuevo cliente-prestamo
def create_client_loans(ID_Cedula,nombre, apellido, telefono, direccion):
    try:
        mariadb_conexion=connect()
        if mariadb_conexion.is_connected():
            cursor=mariadb_conexion.cursor()
            cursor.execute('''
                INSERT INTO cliente (Cedula_Cliente, Nombre, Apellido, Telefono, Direccion)
                VALUES (%s, %s, %s, %s, %s)
            ''', (ID_Cedula, nombre, apellido, telefono, direccion))
            mariadb_conexion.commit()
            mariadb_conexion.close()
            return True
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)

# Leer todos los prestamos
def read_client_loans():
    try:
        mariadb_conexion=connect()
        if mariadb_conexion.is_connected():
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
    mariadb_conexion=connect()
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
        with connect() as mariadb_conexion:
            with mariadb_conexion.cursor() as cursor:
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
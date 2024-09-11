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
def create_user(ID_Cargo, ID_Rol, Nombre,Apellido,Cedula,Nombre_Usuario,Clave):
    print("CARGO:", ID_Cargo,"ID_Rol:", ID_Rol, "Nombre:", Nombre, "APELLIDO:", Apellido, "CEDULA:", Cedula)
    print("NOMBRE DE USUARIO:", Nombre_Usuario, "CLAVE:", Clave)
    try:
        mariadb_conexion=connect()
        if mariadb_conexion.is_connected():
            cursor=mariadb_conexion.cursor()
            cursor.execute('''
                INSERT INTO usuarios (ID_Cargo, ID_Rol, Nombre, Apellido, Cedula, Nombre_Usuario, Clave)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (ID_Cargo, ID_Rol, Nombre,Apellido, Cedula, Nombre_Usuario, Clave))
            # Confirmar la transacción
            mariadb_conexion.commit()
            # Cerrar la conexión
            mariadb_conexion.close()
            return True
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        return False
        
        
 #revisar el orden de los datos enviados
def update_user(ID_Cargo, Nombre, Apellido, Cedula, Nombre_Usuario, Clave, ID_Usuario):
    ID_Rol=1
    mariadb_conexion = connect()
    cursor = mariadb_conexion.cursor()
    cursor.execute("SELECT ID_Usuario FROM usuarios WHERE ID_Usuario = %s", (ID_Usuario,))
    busqueda = cursor.fetchone()
    print(busqueda)
    if busqueda is None:
        mariadb_conexion.close()
        return False
    else:
        cursor.execute('''
            UPDATE usuarios
            SET ID_Cargo=%s, ID_Rol=%s, Nombre=%s, Apellido=%s, Cedula=%s, Nombre_Usuario=%s, Clave=%s
            WHERE ID_Usuario=%s
        ''', (ID_Cargo, ID_Rol, Nombre, Apellido, Cedula, Nombre_Usuario, Clave, ID_Usuario))
        mariadb_conexion.commit()
        mariadb_conexion.close()
        return True


def delete_user_db(ID_Usuario):
    try:
        # Estableciendo la conexión usando un administrador de contexto
        with connect() as mariadb_conexion:
            with mariadb_conexion.cursor() as cursor:
                # Ejecutando la sentencia de eliminación
                cursor.execute('DELETE FROM usuarios WHERE ID_Usuario=%s', (ID_Usuario,))
                if cursor.rowcount == 0:
                    print("No se encontró el usuario con el ID proporcionado.")
                    return False
                # Confirmando la transacción
                mariadb_conexion.commit()
        return True
    except mariadb.Error as err:
        # Manejando cualquier error de la base de datos
        print(f"Error: {err}")
        return False

def list_users_db(user_table_list):
        try:
            mariadb_conexion = mariadb.connect(
            host='localhost',
            port='3306',
            password='2525',
            database='basedatosbiblioteca'
            )
            if mariadb_conexion.is_connected():
                cursor = mariadb_conexion.cursor()
                cursor.execute("""SELECT ID_Usuario, ID_Cargo, ID_Rol, Nombre, Apellido, 
                           Cedula, Nombre_Usuario FROM usuarios""")
                resultados = cursor.fetchall() 
            for row in user_table_list.get_children():
                user_table_list.delete(row)
            # Insertar los datos en el Treeview
            for fila in resultados:
                user_table_list.insert("", "end", values=tuple(fila))
            mariadb_conexion.close()
        except mariadb.Error as ex:
            print("Error durante la conexión:", ex)

# Actualizar un prestamo
def update_user_list(id_cedula, name_user, nombre, apellido, id):
    mariadb_conexion=connect()
    cursor = mariadb_conexion.cursor()
    cursor.execute("SELECT ID_Usuario FROM usuarios WHERE ID_Usuario=%s", (id,))
    busqueda=()
    busqueda=cursor.fetchone()
    print(busqueda)
    if busqueda is None:
        mariadb_conexion.close()
        print("No se encontró al usuario.")
        return False
    else:
        # Actualizar la fecha límite del préstamo
        cursor.execute('''
            UPDATE usuarios
            SET Cedula = %s,
            Nombre_Usuario = %s,
            Nombre = %s,
            Apellido = %s
            WHERE ID_Usuario = %s
        ''', (id_cedula, name_user, nombre, apellido, id))
        print("Actualización éxitosa.")
        mariadb_conexion.commit()
        mariadb_conexion.close()
        return True



"""
import mariadb

def create_user(ID_Cargo, ID_Rol, Nombre_Apellido, Cedula, Nombre_Usuario, Clave):
    print("ID CARGO:", ID_Cargo, "ID ROL:", ID_Rol, "NOMBRE Y APELLIDO:", Nombre_Apellido, "CEDULA:", Cedula)
    print("NOMBRE DE USUARIO:", Nombre_Usuario, "CLAVE:", Clave)
    try:
        # Conectar a la base de datos
        mariadb_conexion = mariadb.connect(
            user="tu_usuario",
            password="tu_contraseña",
            host="localhost",
            database="tu_base_de_datos"
        )
        cursor = mariadb_conexion.cursor()
        
        # Ejecutar la consulta SQL
        cursor.execute('''
            INSERT INTO usuarios (ID_Cargo, ID_Rol, Nombre_Apellido, Cedula, Nombre_Usuario, Clave)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (ID_Cargo, ID_Rol, Nombre_Apellido, Cedula, Nombre_Usuario, Clave))
        
        # Confirmar la transacción
        mariadb_conexion.commit()
        
        # Cerrar la conexión
        mariadb_conexion.close()
        return True
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        return False

# Ejemplo de uso
create_user(1, 2, "Juan Pérez", 12345678, "jperez", "mi_clave_segura")




"""
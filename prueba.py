import mysql.connector
from mysql.connector import Error
from tkinter import ttk,messagebox

def establecer_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='2525',
            database='basedatosbiblioteca',
            charset='utf8mb4',
            collation='utf8mb4_general_ci',
        )
        if conexion.is_connected():
            print("Conexión exitosa")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def get_user_id_by_username(username):
    conexion = establecer_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            consulta = """SELECT ID_Usuario FROM usuarios WHERE Nombre_Usuario = %s"""
            cursor.execute(consulta, (username,))
            user_id = cursor.fetchone()
            return user_id[0] if user_id else None

        except Error as e:
            print(f"Error al realizar la consulta: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
def get_user_data_by_id(user_id):
    conexion = establecer_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            consulta = """SELECT ID_Cargo, ID_Rol, Nombre, Apellido, Cedula, Nombre_Usuario, Clave 
                          FROM usuarios 
                          WHERE ID_Usuario = %s"""
            cursor.execute(consulta, (user_id,))
            user_data = cursor.fetchone()
            return user_data

        except Error as e:
            print(f"Error al realizar la consulta: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
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

def get_user_by_username(username):
    conexion = establecer_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            consulta = """SELECT * FROM usuarios WHERE Nombre_Usuario = %s"""
            cursor.execute(consulta, (username,))
            user = cursor.fetchone()
            return user

        except Error as e:
            print(f"Error al realizar la consulta: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()

def is_user(user):
    if user is None:
        return False
    return True

def is_password(password, user):
    if password == user[7]:  # Asumiendo que la contraseña está en la octava columna
        return True
    else:
        return False
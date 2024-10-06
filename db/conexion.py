import mysql.connector
from mysql.connector import Error
from tkinter import ttk,messagebox
#Modulo dedicado a la conexion con la base de datos en caso de tener problemas ajustan sus credenciales en base a sus usuario del gestor de base de datos
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

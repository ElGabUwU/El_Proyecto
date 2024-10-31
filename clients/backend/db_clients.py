from db.conexion import establecer_conexion
import mysql.connector as mariadb
from tkinter import messagebox


def update_client(client_data, nuevos_valores):
    cedula = client_data["cedula"]
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        
        # Verificar si el cliente existe
        cursor.execute("SELECT ID_Cliente FROM cliente WHERE Cedula = %s", (cedula,))
        busqueda = cursor.fetchone()
        
        if busqueda is None:
            mariadb_conexion.close()
            return False
        
        else:
            # Ejecutar la actualización
            cursor.execute('''
                UPDATE cliente
                SET Cedula=%s, Nombre=%s, Apellido=%s, Telefono=%s, Direccion=%s
                WHERE Cedula=%s
            ''', (
                nuevos_valores["Cedula"], nuevos_valores["Nombre"], nuevos_valores["Apellido"],
                nuevos_valores["Telefono"], nuevos_valores["Direccion"], cedula
            ))
            
            mariadb_conexion.commit()
            mariadb_conexion.close()
            return True
    else:
        return False

# Crear un nuevo cliente
def register_client_in_db(cedula, nombre, apellido, telefono, direccion):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            sql_insert_query = """INSERT INTO cliente (Cedula, Nombre, Apellido, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql_insert_query, (cedula, nombre, apellido, telefono, direccion))
            mariadb_conexion.commit()
            ID_Cliente = cursor.lastrowid
            return ID_Cliente
    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()


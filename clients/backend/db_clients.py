from db.conexion import establecer_conexion
import mysql.connector as mariadb
from tkinter import messagebox


def update_client(client_data, nuevos_valores):
    ID_Cliente = client_data["id"]
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        
        # Verificar si el cliente existe
        cursor.execute("SELECT ID_Cliente FROM cliente WHERE ID_Cliente = %s", (ID_Cliente,))
        busqueda = cursor.fetchone()
        
        if busqueda is None:
            mariadb_conexion.close()
            return False
        
        else:
            # Ejecutar la actualización
            cursor.execute('''
                UPDATE cliente
                SET Cedula_Cliente=%s, Nombre=%s, Apellido=%s, Telefono=%s, Direccion=%s
                WHERE ID_Cliente=%s
            ''', (
                nuevos_valores["Cedula"], nuevos_valores["Nombre"], nuevos_valores["Apellido"],
                nuevos_valores["Telefono"], nuevos_valores["Direccion"], ID_Cliente
            ))
            
            mariadb_conexion.commit()
            mariadb_conexion.close()
            return True
    else:
        return False

# Crear un nuevo cliente-prestamo
def register_client_in_db(cedula, nombre, apellido, telefono, direccion):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            sql_insert_query = """INSERT INTO cliente (Cedula_Cliente, Nombre, Apellido, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql_insert_query, (cedula, nombre, apellido, telefono, direccion))
            mariadb_conexion.commit()
            ID_Cliente = cursor.lastrowid
            return ID_Cliente
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()


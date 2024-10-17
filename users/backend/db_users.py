from db.conexion import establecer_conexion
import mysql.connector as mariadb
from colorama import init, Fore, Back, Style
from tkinter import messagebox
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

#Esta clase obtiene los valores del usuario, implmentar a futuro en mi perfil
class Usuario:
    def __init__(self, user_data):
        self.id_usuario = user_data[0]
        self.id_cargo = user_data[1]
        self.id_rol = user_data[2]
        self.nombre = user_data[3]
        self.apellido = user_data[4]
        self.cedula = user_data[5]
        self.nombre_usuario = user_data[6]
        self.clave = user_data[7]

    def mostrar_informacion(self):
        print(f"ID Usuario: {self.id_usuario}")
        print(f"ID Cargo: {self.id_cargo}")
        print(f"ID Rol: {self.id_rol}")
        print(f"Nombre: {self.nombre}")
        print(f"Apellido: {self.apellido}")
        print(f"Cédula: {self.cedula}")
        print(f"Nombre de Usuario: {self.nombre_usuario}")


usuario_actual = None

def iniciar_sesion(username, password):
    global usuario_actual
    user_data = get_user_by_username(username)
    if user_data and is_password(password, user_data):
        usuario_actual = Usuario(user_data)
        print("Inicio de sesión exitoso")
        usuario_actual.mostrar_informacion()
        return usuario_actual
    else:
        print("Nombre de usuario o contraseña incorrectos")
        return None



def is_user(user):#Validacion de usuario
    if user is None:
        return False
    return True

def is_password(password, user):
    if password == user[7]:  # Asumiendo que la contraseña está en la octava columna
        return True
    else:
        return False


#FUCNIONES ASOCIADAS A LOS BOTONES 
init(autoreset=True)
# Conectar a la base de datos

import mariadb

def create_user(ID_Cargo, ID_Rol, Nombre, Apellido, Cedula, Nombre_Usuario, Clave):
    print("CARGO:", ID_Cargo, "ID_Rol:", ID_Rol, "Nombre:", Nombre, "APELLIDO:", Apellido, "CEDULA:", Cedula)
    print("NOMBRE DE USUARIO:", Nombre_Usuario, "CLAVE:", Clave)
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            cursor.execute('''
                INSERT INTO usuarios (ID_Cargo, ID_Rol, Nombre, Apellido, Cedula, Nombre_Usuario, Clave)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (ID_Cargo, ID_Rol, Nombre, Apellido, Cedula, Nombre_Usuario, Clave))
            mariadb_conexion.commit()
            return True
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        return False
    finally:
        if cursor:
            cursor.close()
        if mariadb_conexion:
            mariadb_conexion.close()

        
 #revisar el orden de los datos enviados
def update_user(ID_Cargo, Nombre, Apellido, Cedula, Nombre_Usuario, Clave, ID_Usuario):
    ID_Rol=1
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
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
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
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
    
def delete_selected_user(self):
    selected_items = self.user_table_list.selection()
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            #cursor = mariadb_conexion.cursor()
            for item in selected_items:
                item_id = self.user_table_list.item(item, 'values')[0]
                
                # Marcar el registro como eliminado en lugar de eliminarlo
                cursor.execute('UPDATE usuarios SET estado_usuario = "eliminado" WHERE ID_Usuario = %s', (item_id,))
                
                # Eliminar la fila del Treeview
                self.user_table_list.delete(item)
            
            mariadb_conexion.commit()
            messagebox.showinfo("Éxito", "El usuario ha sido marcado como eliminado.")
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        messagebox.showerror("Error", f"Error durante la conexión: {ex}")
    finally:
        if mariadb_conexion:
            mariadb_conexion.close()
def list_users_db(user_table_list):
    mariadb_conexion = establecer_conexion()
    try:
        
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            cursor.execute("""SELECT ID_Usuario, ID_Cargo, ID_Rol, Nombre, Apellido, 
                        Cedula, Nombre_Usuario FROM usuarios WHERE estado_usuario != 'eliminado'""")
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
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
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
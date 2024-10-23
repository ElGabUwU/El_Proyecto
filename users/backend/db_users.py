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

def update_user(user_data, nuevos_valores):
    ID_Usuario = user_data["id"]
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        
        # Verificar si el usuario existe
        cursor.execute("SELECT ID_Usuario FROM usuarios WHERE ID_Usuario = %s", (ID_Usuario,))
        busqueda = cursor.fetchone()
        
        if busqueda is None:
            mariadb_conexion.close()
            return False
        
        else:
            # Ejecutar la actualización
            cursor.execute('''
                UPDATE usuarios
                SET ID_Cargo=%s, Nombre=%s, Apellido=%s, Cedula=%s, Nombre_Usuario=%s, Clave=%s
                WHERE ID_Usuario=%s
            ''', (
                nuevos_valores["Cargo"], nuevos_valores["Nombre"], nuevos_valores["Apellido"],
                nuevos_valores["Cedula"], nuevos_valores["Username"], nuevos_valores["Password"], ID_Usuario
            ))
            
            mariadb_conexion.commit()
            mariadb_conexion.close()
            return True
    else:
        return False

def delete_selected_user(self):
    from users.backend.db_users import usuario_actual

    selected_items = self.user_table_list.selection()

    if not selected_items:
        messagebox.showinfo("Error", "Por favor, selecciona al menos un usuario para eliminar.")
        return

    respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que deseas eliminar los usuarios seleccionados?")
    if not respuesta:
        messagebox.showinfo("Cancelado", "Eliminación cancelada.")
        return

    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            users_deleted = False
            for item in selected_items:
                item_id = self.user_table_list.item(item, 'values')[0]

                # Verificar si el usuario seleccionado es el usuario actual
                if str(item_id) == str(usuario_actual.id_usuario):
                    messagebox.showwarning("Advertencia", "No puedes eliminar el usuario que está actualmente logueado.")
                    continue

                # Actualizar el estado del usuario a 'eliminado'
                cursor.execute('UPDATE usuarios SET estado_usuario = %s WHERE ID_Usuario = %s', ('eliminado', item_id))

                # Eliminar la fila del Treeview
                self.user_table_list.delete(item)
                users_deleted = True

            if users_deleted:
                mariadb_conexion.commit()
                messagebox.showinfo("Éxito", "El usuario ha sido marcado como eliminado.")
    except mariadb.Error as ex:
        print("Error durante la conexión:", ex)
        messagebox.showerror("Error", f"Error durante la conexión: {ex}")
    finally:
        if mariadb_conexion:
            mariadb_conexion.close()

def list_users_db(treeview, cargos):
    # Conexión a la base de datos y obtención de datos
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        query = "SELECT * FROM usuarios WHERE estado_usuario = 'activo'"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        mariadb_conexion.close()
        
        # Limpiar el Treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Insertar datos en el Treeview
        for row in rows:
            # Reemplazar el ID de cargo con su nombre correspondiente
            row = list(row)
            row[1] = cargos.get(row[1], "Desconocido")  # Supongamos que la columna 1 es la del cargo
            treeview.insert('', 'end', values=tuple(row))

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
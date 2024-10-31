from db.conexion import establecer_conexion
from loans.backend.db_loans import *
from tkinter import messagebox
import tkinter as tk
from datetime import datetime, timedelta
import random
import string

#Función que limpia los entrys una vez cumplido el proceso de registro de prestamo
def clear_entries_list_register(self):
    try:
        self.cedula.delete(0, tk.END)
    except AttributeError as e:
        print(f"Error al limpiar los campos: {e}")

def clear_entries_list(self):
    try:
        self.cedula_entry.delete(0, tk.END)
        self.fecha_limite_entry.delete(0, tk.END)
        # Si tienes otros campos que necesitas limpiar, asegúrate de que existan y estén correctamente referenciados
        # self.input_cantidad.delete(0, tk.END)
    except AttributeError as e:
        print(f"Error al limpiar los campos: {e}")

#Función que valida si los campos han sido rellanados    
def validate_entries(instance, event=None):
        # Comprobar si todos los campos están llenos
        if (instance.id_cliente.get()):
            instance.boton_R.place(x=40.0, y=450.0, width=130.0, height=40.0)  # Mostrar el botón
        else:
            instance.boton_R.place_forget()  # Ocultar el botón si algún campo está vacío

#Función que genera una cadena alfanumérica de 6 digitos aleatorios para el ID_Prestamo
def generate_alphanumeric_id(length=6):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))

# Función que formatea la fecha según el formato DD-MM-YYYY
def format_date(date_str):
    try:
        # Convertir la fecha del formato DD/MM/YYYY al formato DD-MM-YYYY
        formatted_date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%d-%m-%Y")
        return formatted_date
    except ValueError as e:
        print(f"Error al formatear la fecha: {e}")
        return None
        
#Función que genera una ID_Libro_Prestamo aleatoria
def generate_id_libro_prestamo(self):
        while True:
            new_id = random.randint(1000, 9999)
            if not libro_prestamo_exists(new_id):
                return new_id

#Función que verifica si el usuario posee o no credenciales para eliminar
def verificar_eliminar(self):
        if self.parent.id_rol == 1:
            print("Sin permisos suficientes para eliminar!")
            messagebox.showinfo("AVISO", "Sin permisos suficientes para eliminar!")
        
        else:
            delete_selected_prestamo(self)

#Función que verifica si el libro existe o no dentro de la tabla prestamo
def libro_prestamo_exists(new_id):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            # Verificar si el ID_Libro_Prestamo existe en la tabla libros_prestamo
            cursor.execute("SELECT 1 FROM libros_prestamo WHERE ID_Libro_Prestamo = %s", (new_id,))
            result = cursor.fetchone()
            return result is not None
    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()

#Función que consigue la ID del cliente basado en la cédula
# def get_cliente_id_by_cp(cp):
#     try:
#         mariadb_conexion = establecer_conexion()
#         if not mariadb_conexion:
#             print("Failed to establish connection.")
#             return None

#         cursor = mariadb_conexion.cursor()
#         query = "SELECT ID_CP FROM cliente_prestamo WHERE ID_CP = %s"
#         cursor.execute(query, (cp,))
#         result = cursor.fetchone()

#         if result:
#             return result[0]
#         else:
#             return None
#     except mariadb.Error as ex:
#         print(f"Error during query execution: {ex}")
#         return None
#     finally:
#         if mariadb_conexion is not None:
#             cursor.close()
#             mariadb_conexion.close()
#             print("Connection closed.")

def get_cliente_id_by_cedula(cedula):
    try:
        mariadb_conexion = establecer_conexion()
        if not mariadb_conexion:
            print("Failed to establish connection.")
            return None

        cursor = mariadb_conexion.cursor()
        query = "SELECT ID_Cliente FROM cliente WHERE Cedula = %s"
        cursor.execute(query, (cedula,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None
    except mariadb.Error as ex:
        print(f"Error during query execution: {ex}")
        return None
    finally:
        if mariadb_conexion is not None:
            cursor.close()
            mariadb_conexion.close()
            print("Connection closed.")

#Función que valida el numero de cedula
def validate_cedula(cedula):
    if not cedula:
        return False, "El campo de la cédula es obligatorio."
    if len(cedula) < 7 or len(cedula) > 10:
        return False, "La cédula debe tener entre 7 y 10 caracteres."
    return True, ""

# Función que valida si la cédula ha sido registrada o no dentro del sistema
def is_cedula_registered(cedula):
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        try:
            query = "SELECT COUNT(*) FROM cliente WHERE Cedula = %s"
            cursor.execute(query, (cedula,))
            result = cursor.fetchone()
            if result[0] > 0:
                return True, ""
            else:
                return False, "La cédula no está registrada."
        finally:
            cursor.close()
            mariadb_conexion.close()
    else:
        return False, "No se pudo establecer conexión con la base de datos."
    
#Función que verifica la fecha_limite
def validate_fecha_limite(fecha_limite):
    if not fecha_limite:
        return False, "El campo de la fecha límite es obligatorio."
    try:
        # Intentar convertir la fecha al formato DD-MM-YYYY
        fecha = datetime.strptime(fecha_limite, '%d-%m-%Y')
    except ValueError:
        return False, "La fecha límite debe estar en el formato DD-MM-YYYY."
    
    hoy = datetime.now()
    
    # Verificar que la fecha no sea anterior a hoy
    if fecha.date() < hoy.date():
        return False, "La fecha límite no puede ser anterior a la fecha actual."
    
    # Verificar que la fecha esté dentro del año actual
    if fecha.year != hoy.year:
        return False, "La fecha límite debe estar dentro del año actual."
    
    return True, ""

#Función que valida los campos insertado en la ventana de modificar
def validar_campos(tipo_validacion="registro", cedula=None, fecha_limite=None, client_id=None):
    error_messages = []

    def add_error(is_valid, message):
        if not is_valid:
            error_messages.append(message)

    try:
        if tipo_validacion == "modificar":
            is_valid, message = validate_cedula(cedula)
            add_error(is_valid, message)
            
            if is_valid:
                cedula_ok, message = is_cedula_registered(cedula)
                add_error(cedula_ok, message)
            
            # Validar fecha límite
            is_valid, message = validate_fecha_limite(fecha_limite)
            add_error(is_valid, message)

    except Exception as e:
        error_messages.append(f"Error inesperado: {str(e)}")

    return error_messages

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
        if (instance.cedula.get()):
            instance.boton_R.place(x=35.0, y=495.0, width=130.0, height=40.0)  # Mostrar el botón
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






#Función que valida el numero de cedula
def validate_cedula(cedula):
    if not cedula:
        return False, "El campo de la cédula es obligatorio."
    if len(cedula) < 7 or len(cedula) > 10:
        return False, "La cédula debe tener entre 7 y 10 caracteres."
    return True, ""

#Función que verifica el estado del libro, si está 'activo' o 'eliminado'
def libro_active_or_delete(libro_id):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            # Verificar si el ID_Libro existe en la tabla libro y su estado
            cursor.execute("SELECT estado_libro FROM libro WHERE ID_Libro = %s", (libro_id,))
            result = cursor.fetchone()
            if result:
                estado_libro = result[0]
                return estado_libro == 'activo'
            return False
    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()


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

#Función que verifica si el libro está en prestamo o no
def validar_libro_no_prestado(n_registro):
    conn = establecer_conexion()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT l.ID_Libro
            FROM libro l
            JOIN cliente_prestamo cp ON l.ID_Libro = cp.ID_Libro
            WHERE l.n_registro = %s AND cp.estado_cliente_prestamo = 'activo'
        """
        cursor.execute(query, (n_registro,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return f"El libro con número de registro {n_registro} ya está prestado."
    return None
#ojo sentencia abajo
# def validar_libro_no_prestado(n_registro, cedula_cliente_actual):
#     conn = establecer_conexion()
#     if conn:
#         cursor = conn.cursor()
#         query = """
#             SELECT l.ID_Libro, c.Nombre, c.Apellido, p.Fecha_Registro, p.Fecha_Limite, c.Cedula, l.titulo
#             FROM libro l
#             JOIN cliente_prestamo cp ON l.ID_Libro = cp.ID_Libro
#             JOIN cliente c ON cp.ID_Cliente = c.ID_Cliente
#             JOIN prestamo p ON cp.ID_Prestamo = p.ID_Prestamo
#             WHERE l.n_registro = %s AND cp.estado_cliente_prestamo = 'activo'
#         """
#         cursor.execute(query, (n_registro,))
#         resultado = cursor.fetchone()
#         conn.close()
#         if resultado:
#             id_libro, nombre_cliente, apellido_cliente, fecha_registro, fecha_limite, cedula_cliente, titulo_libro = resultado
#             hoy = datetime.now().date()
#             try:
#                 fecha_limite = datetime.strptime(fecha_limite, '%d-%m-%Y').date()
#             except ValueError:
#                 fecha_limite = datetime.strptime(fecha_limite, '%Y-%m-%d').date()

#             estado_prestamo = 'vencido' if fecha_limite <= hoy else 'activo'
#             fecha_limite_formateada = fecha_limite.strftime('%d-%m-%Y')

#             if cedula_cliente == cedula_cliente_actual:
#                 if estado_prestamo == 'activo':
#                     return f"""El libro con número de registro {n_registro} está registrado a este cliente.

# Por favor, asegúrese de que el cliente devuelva el libro antes de la fecha límite.
# Consulte el apartado de préstamos para obtener más información sobre los libros prestados.
# """
#                 else:
#                     return f"""El libro con número de registro {n_registro} está registrado a este cliente.

# Por favor, contacte al cliente para renovar el préstamo vencido o devolver el libro. Consulte el apartado de clientes para obtener más información sobre los datos del cliente.
# """
#             else:
#                 mensaje_error = f"""El libro con número de registro {n_registro} ya está prestado.

# Detalles del Préstamo:
# - Título del Libro: {titulo_libro}
# - Fecha de Registro: {fecha_registro}
# - Fecha Límite: {fecha_limite_formateada}
# - Nombre del Cliente: {nombre_cliente} {apellido_cliente}
# - Cédula del Cliente: {cedula_cliente}
# - Estado del Préstamo: {estado_prestamo.capitalize()}

# """
#                 if estado_prestamo == 'vencido':
#                     mensaje_error += """
# Por favor, contacte al cliente para renovar el préstamo vencido o devolver el libro. Consulte el apartado de clientes para obtener más información sobre los datos del cliente.
# """
#                 else:
#                     mensaje_error += "El préstamo está registrado a este cliente."
#                 return mensaje_error
#     return None
#Función que valida los campos insertado en la ventana de modificar
def validar_campos_loans(tipo_validacion="registro", cedula=None, libro_id=None, n_registro=None):
    error_messages = []

    def add_error(is_valid, message):
        if not is_valid:
            error_messages.append(message)

    try:
        if tipo_validacion == "registro":
            is_valid, message = validate_cedula(cedula)
            add_error(is_valid, message)
            
            if is_valid:
                cedula_ok, message = is_cedula_registered(cedula)
                add_error(cedula_ok, message)
            
            # Validar si el libro está activo
            if not libro_active_or_delete(libro_id):
                add_error(False, "El libro seleccionado está marcado como eliminado y no puede ser prestado.")
            
                

    except Exception as e:
        error_messages.append(f"Error inesperado: {str(e)}")

    return error_messages

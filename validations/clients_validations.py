from db.conexion import establecer_conexion
from loans.backend.db_loans import *
import tkinter as tk
from tkinter import messagebox
import random
import string
import re
from clients.backend.db_clients import *


        
#Generador de ID Préstamo Alfanumérica       
def generate_alphanumeric_id(self, length=8):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))

# # clients_validations.py
# def validate_entries(instance, event=None):
#     # Comprobar si todos los campos están llenos
#     if (instance.input_cedula.get() and instance.input_nombre.get() and instance.input_apellido.get() and
#             instance.input_telefono.get() and instance.input_direccion.get()):
#         instance.boton_R.place(x=553.0, y=300.0, width=130.0, height=40.0)  # Mostrar el botón
#     else:
#         instance.boton_R.place_forget()  # Ocultar el botón si algún campo está vacío

# #Verificación de Rango Usuario
def verificar_eliminar(self):
        if self.parent.id_rol == 1:
            print("Sin permisos suficientes para eliminar!")
            messagebox.showinfo("AVISO", "Sin permisos suficientes para eliminar!")
        
        else:
            delete_client_loans(self)

# VALIDACIONES DE FORMATEO DE VALORES INGRESADOS
def limit_length(text, max_length):
    return text[:max_length]

def allow_permitted_characters(char):
    # Check if the character is permitted
    return re.match(r'[a-zA-Z0-9\s,.\-#]', char)


def capitalize_first_letter(text):
    return text.title()

# VALIDACION DE DATOS CAMPOS INGRESADOS DE FORMA INCORRECTA
def validate_name(name):
    if not name:
        return False, "El campo del nombre es obligatorio."
    if len(name) < 3 or len(name) > 30:
        return False, "El nombre debe tener como mínimo 3 caracteres."
    if re.search(r'^\s', name):
        return False, "El nombre no puede comenzar con un espacio."
    if re.search(r'\s{2,}', name):
        return False, "El nombre no puede contener más de un espacio consecutivo."
    if name[-1] == " ":
        return False, "El nombre no puede terminar en un espacio."
    return True, ""

def validate_apellido(apellido):
    if not apellido:
        return False, "El campo del apellido es obligatorio."
    if len(apellido) < 4 or len(apellido) > 30:
        return False, "El apellido debe tener entre 4 y 30 caracteres."
    if re.search(r'^\s', apellido):
        return False, "El apellido no puede comenzar con un espacio."
    if re.search(r'\s{2,}', apellido):
        return False, "El apellido no puede contener más de un espacio consecutivo."
    if apellido[-1] == " ":
        return False, "El apellido no puede terminar en un espacio."
    return True, ""



def validate_cedula(cedula):
    if not cedula:
        return False, "El campo de la cédula es obligatorio."
    if len(cedula) < 7 or len(cedula) > 10:
        return False, "La cédula debe tener entre 7 y 10 caracteres."
    return True, ""

def is_cedula_registered(cedula):
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        try:
            query = "SELECT COUNT(*) FROM cliente WHERE Cedula = %s"
            cursor.execute(query, (cedula,))
            result = cursor.fetchone()
            if result[0] > 0:
                return False, "La cédula ya está registrada."
            else:
                return True, ""
        finally:
            cursor.close()
            mariadb_conexion.close()
    else:
        return False, "No se pudo establecer conexión con la base de datos."

def is_cedula_unique_for_client(cedula, client_id):
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        try:
            # Verificar si la cédula ingresada es diferente a la del cliente original
            query = "SELECT Cedula FROM cliente WHERE ID_Cliente = %s"
            cursor.execute(query, (client_id,))
            cedula_original = cursor.fetchone()

            if cedula_original and cedula != cedula_original[0]:
                # Verificar si la nueva cédula ya está registrada por otro cliente
                query = "SELECT ID_Cliente FROM cliente WHERE Cedula = %s AND ID_Cliente != %s"
                cursor.execute(query, (cedula, client_id))
                result = cursor.fetchone()
                if result:
                    return False, f"La cédula {cedula} ya está en uso por otro cliente."
            return True, ""
        finally:
            cursor.close()
            mariadb_conexion.close()
    else:
        return False, "No se pudo establecer conexión con la base de datos."

def validate_direccion(direccion):
    if not direccion:
        return False, "El campo de la dirección es obligatorio."
    if len(direccion) < 10:
        return False, "La dirección debe tener al menos 10 caracteres."
    if len(direccion) > 100:
        return False, "La dirección no debe exceder los 100 caracteres."
    if re.search(r'\s{2,}', direccion):
        return False, "La dirección no puede contener más de un espacio consecutivo."
    if direccion[-1] == " ":
        return False, "La dirección no puede terminar en un espacio."
    if re.search(r'[,.#-]{2,}', direccion):
        return False, "La dirección no puede contener signos repetidos consecutivos como comas, puntos, guiones o signos de número."
    
    # Permitir solo caracteres válidos en una dirección
    #direccion = re.sub(r'[^a-zA-Z0-9\s,.-#]', '', direccion)
    
    return True, ""

def validate_phone_number(phone_number):
    if not phone_number:
        return False, "El campo del número de teléfono es obligatorio."
    
    # Permitir solo dígitos
    phone_number = re.sub(r'[^0-9]', '', phone_number)
    
    # Verificar longitud
    if len(phone_number) != 11:
        return False, "El número de teléfono debe tener 11 dígitos, incluyendo el código de área."
    
    # Verificar códigos de área válidos
    valid_area_codes = ['0412', '0414', '0424', '0416', '0426', '0212', '0261', '0241']
    if phone_number[:4] not in valid_area_codes:
        return False, "El código de área no es válido."
    
    return True, ""

def validar_campos(tipo_validacion="registro", nombre=None, apellido=None, cedula=None, telefono=None, direccion=None, client_id=None):
    error_messages = []

    def add_error(is_valid, message):
        if not is_valid:
            error_messages.append(message)

    try:
        if tipo_validacion == "registro":
            is_valid, message = validate_name(nombre)
            add_error(is_valid, message)
            
            is_valid, message = validate_apellido(apellido)
            add_error(is_valid, message)
            
            is_valid, message = validate_cedula(cedula)
            add_error(is_valid, message)
            if is_valid:
                cedula_ok, message = is_cedula_registered(cedula)
                add_error(cedula_ok, message)
            
            is_valid, message = validate_phone_number(telefono)
            add_error(is_valid, message)
            
            is_valid, message = validate_direccion(direccion)
            add_error(is_valid, message)

        if tipo_validacion == "modificar":
            is_valid, message = validate_name(nombre)
            add_error(is_valid, message)
            
            is_valid, message = validate_apellido(apellido)
            add_error(is_valid, message)
            
            is_valid, message = validate_cedula(cedula)
            add_error(is_valid, message)
            if is_valid:
                if client_id:
                    cedula_ok, message = is_cedula_unique_for_client(cedula, client_id)
                else:
                    cedula_ok, message = is_cedula_registered(cedula)
                add_error(cedula_ok, message)
            
            is_valid, message = validate_phone_number(telefono)
            add_error(is_valid, message)
            
            is_valid, message = validate_direccion(direccion)
            add_error(is_valid, message)

    except Exception as e:
        error_messages.append(f"Error inesperado: {str(e)}")

    return error_messages

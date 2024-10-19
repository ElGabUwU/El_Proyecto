import re
from users.backend.db_users import *

# VALIDACIONES DE FORMATEO DE VALORES INGRESADOS
def limit_length(text, max_length):
    return text[:max_length]

def allow_permitted_characters(text):
    # Permitir solo letras, números y guiones bajos
    return re.sub(r'[^a-zA-Z0-9_$]', '', text)

def capitalize_first_letter(text):
    return text.title()

# VALIDACION DE DATOS CAMPOS INGRESADOS DE FORMA INCORRECTA
def validate_username(username):
    if not username:
        return False, "El campo de nombre de usuario es obligatorio."
    if len(username) < 6 or len(username) > 12:
        return False, "El nombre de usuario debe tener entre 6 y 11 caracteres. Asegúrate de que tu nombre de usuario tenga la longitud adecuada."
    if not re.match(r'^[A-Z][a-zA-Z0-9_]*$', username):
        return False, "El nombre de usuario debe comenzar con una letra mayúscula y solo puede contener letras, números, signo de dolar y guiones bajos. Asegúrate de que tu nombre de usuario cumpla con este formato."
    if re.search(r'[_$]{2}', username):
        return False, "El nombre de usuario no puede contener dos caracteres permitidos de forma consecutiva. Asegúrate de que tu nombre de usuario no tenga '__' o '$$'."
    return True, ""

def validate_password(password):
    if not password:
        return False, "El campo de la contraseña es obligatorio."
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres. Asegúrate de que tu contraseña sea lo suficientemente larga."
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula. Incluye al menos una letra mayúscula en tu contraseña."
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula. Incluye al menos una letra minúscula en tu contraseña."
    if not re.search(r'[0-9]', password):
        return False, "La contraseña debe contener al menos un número. Incluye al menos un número en tu contraseña."
    if not re.search(r'[\W_]', password):
        return False, "La contraseña debe contener al menos un carácter especial. Incluye al menos un carácter especial en tu contraseña."
    return True, ""

def validate_name(name):
    if not name:
        return False, "El campo del nombre es obligatorio."
    if len(name) < 4 or len(name) > 30:
        return False, "El nombre debe tener entre 4 y 30 caracteres."
    if re.search(r'\s{2,}', name):
        return False, "El nombre no puede contener más de un espacios consecutivos."
    if name[-1] == " ":
        return False, "El nombre no puede terminar en un espacio."
    return True, ""

def validate_apellido(apellido):
    if not apellido:
        return False, "El campo del apellido es obligatorio."
    if len(apellido) < 4 or len(apellido) > 30:
        return False, "El apellido debe tener entre 4 y 30 caracteres."
    if re.search(r'\s{2,}', apellido):
        return False, "El apellido no puede contener más de dos espacios consecutivos."
    if apellido[-1] == " ":
        return False, "El apellido no puede terminar en un espacio."
    return True, ""

def cedula_existe(cedula):
    mariadb_conexion = establecer_conexion()
    if mariadb_conexion:
        cursor = mariadb_conexion.cursor()
        try:
            query = "SELECT COUNT(*) FROM usuarios WHERE Cedula = %s"
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

def validate_cedula(cedula):
    if not cedula:
        return False, "El campo de la cédula es obligatorio."
    if len(cedula) < 7 or len(cedula) > 10:
        return False, "La cédula debe tener entre 7 y 10 caracteres."
    return True, ""


def validar_campos(user_name, password, tipo_validacion="login", nombre=None, apellido=None, cedula=None, cargo=None, verify_password=None):
    error_messages = []
    
    # Validar nombre de usuario
    is_valid, message = validate_username(user_name)
    if not is_valid:
        error_messages.append(message)
    
    # Obtener usuario de la base de datos solo si los datos anteriores son válidos (para login)
    if tipo_validacion == "login" and not error_messages:
        user_db = get_user_by_username(user_name)
        if not is_user(user_db):
            error_messages.append("Usuario no encontrado. Por favor, verifica tu nombre de usuario.")
        else:
            # Validar contraseña solo si el usuario es válido
            is_valid, message = validate_password(password)
            if not is_valid:
                error_messages.append(message)
            elif not is_password(password, user_db):
                error_messages.append("Contraseña incorrecta.")
    
    # Validaciones adicionales para registro
    if tipo_validacion == "registro":
        # Validar nombre
        is_valid, message = validate_name(nombre)
        if not is_valid:
            error_messages.append(message)
        
        # Validar apellido
        is_valid, message = validate_apellido(apellido)
        if not is_valid:
            error_messages.append(message)
        
        # Validar cédula
        is_valid, message = validate_cedula(cedula)
        if not is_valid:
            error_messages.append(message)
        else:
            cedula_ok, message = cedula_existe(cedula)
            if not cedula_ok:
                error_messages.append(message)
        
        # Validar cargo
        if not cargo or len(cargo.strip()) == 0:
            error_messages.append("El campo de cargo es obligatorio.")
        
        # Validar contraseña (también necesaria para registro)
        is_valid, message = validate_password(password)
        if not is_valid:
            error_messages.append(message)
        
        # Validar que las contraseñas coinciden
        if password != verify_password:
            error_messages.append("Las contraseñas no coinciden.")
    
    return error_messages

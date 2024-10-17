import re
from users.backend.db_users import *
#VALIDACIONES DE FORMATEO DE VALORES INGRESADOS
def limit_length(text, max_length):
    return text[:max_length]

def allow_permitted_characters(text):
    # Permitir solo letras, números y guiones bajos
    return re.sub(r'[^a-zA-Z0-9_$]', '', text)


#VALIDACION DE DATOS CAMPOS INGRESADOS DE FORMA INCORRECTA
def validate_username(username):
    if len(username) < 6 or len(username) > 12:
        return False, "El nombre de usuario debe tener entre 6 y 11 caracteres. Asegúrate de que tu nombre de usuario tenga la longitud adecuada."
    if not re.match(r'^[A-Z][a-zA-Z0-9_]*$', username):
        return False, "El nombre de usuario debe comenzar con una letra mayúscula y solo puede contener letras, números, signo de dolar y guiones bajos. Asegúrate de que tu nombre de usuario cumpla con este formato."
    if re.search(r'[_$]{2}', username):
        return False, "El nombre de usuario no puede contener dos caracteres permitidos de forma consecutiva. Asegúrate de que tu nombre de usuario no tenga '__' o '$$'."
    return True, ""

def validate_password(password):
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

def validar_campos(user_name, password, tipo_validacion="login", nombre=None, apellido=None, cedula=None, cargo=None):
    error_messages = []

    # Validar nombre de usuario
    is_valid, message = validate_username(user_name)
    if not is_valid:
        error_messages.append(f"{message}")

    # Obtener usuario de la base de datos solo si los datos anteriores son válidos (para login)
    if tipo_validacion == "login" and not error_messages:
        user_db = get_user_by_username(user_name)
        if not is_user(user_db):
            error_messages.append(f"Usuario no encontrado. Por favor, verifica tu nombre de usuario.")
        else:
            # Validar contraseña solo si el usuario es válido
            is_valid, message = validate_password(password)
            if not is_valid:
                error_messages.append(f"{message}")
            elif not is_password(password, user_db):
                error_messages.append(f"Contraseña incorrecta.")

    # Validaciones adicionales para registro
    if tipo_validacion == "registro":
        # Validar nombre
        if not nombre or len(nombre.strip()) == 0:
            error_messages.append("El campo de nombre es obligatorio.")
        
        # Validar apellido
        if not apellido or len(apellido.strip()) == 0:
            error_messages.append("El campo de apellido es obligatorio.")
        
        # Validar cédula
        if not cedula or len(cedula.strip()) == 0:
            error_messages.append("El campo de cédula es obligatorio.")
        
        # Validar cargo
        if not cargo or len(cargo.strip()) == 0:
            error_messages.append("El campo de cargo es obligatorio.")
        
        # Validar contraseña (también necesaria para registro)
        is_valid, message = validate_password(password)
        if not is_valid:
            error_messages.append(f"{message}")

    return error_messages

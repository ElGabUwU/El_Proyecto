import re

def validate_username(username):
    if len(username) < 6 or len(username) > 30:
        return False, "El nombre de usuario debe tener entre 6 y 30 caracteres. Asegúrate de que tu nombre de usuario tenga la longitud adecuada."
    if not re.match(r'^[A-Z][a-zA-Z0-9_]*$', username):
        return False, "El nombre de usuario debe comenzar con una letra mayúscula y solo puede contener letras, números y guiones bajos. Asegúrate de que tu nombre de usuario cumpla con este formato."
    if re.search(r'[&=\'\-+,<>]', username):
        return False, "El nombre de usuario no puede contener los caracteres especiales: & = ' - + , < >. Elimina cualquier carácter especial de tu nombre de usuario."
    if '..' in username:
        return False, "El nombre de usuario no puede contener dos puntos consecutivos. Asegúrate de que tu nombre de usuario no tenga '..'."
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

import re

def validar_cota(cota):
    if not (3 <= len(cota) <= 14):
        return "La longitud de la cota debe estar entre 3 y 14 caracteres."
    if len(cota) == 3 and not cota.isalpha():
        return "Las cotas de longitud 3 solo debe contener letras."
    if ".." in cota:
        return "La cota no puede contener dos puntos consecutivos."
    if not re.match(r'^[a-zA-Z0-9.]+$', cota):
        return "La cota solo puede contener letras, números y puntos."
    return None

def validar_titulo(titulo):
    if not (4 <= len(titulo) <= 166):
        return "La longitud del título debe estar entre 4 y 166 caracteres."
    if not re.match(r'^[a-zA-Z0-9\s]+$', titulo):
        return "El título solo puede contener letras, números y espacios."
    return None

def validar_y_formatear_texto(texto):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áéíóúÁÉÍÓÚñÑ"
    filtered_text = ''.join([char for char in texto if char in allowed_chars])
    
    # Capitalizar el texto
    return filtered_text.title()

def validar_campos(cota, titulo):
    errores = []

    error_cota = validar_cota(cota)
    if error_cota:
        errores.append(error_cota)

    error_titulo = validar_titulo(titulo)
    if error_titulo:
        errores.append(error_titulo)

    # Agrega más validaciones según sea necesario

    return errores

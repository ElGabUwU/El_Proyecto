import re
from datetime import datetime
from db.conexion import establecer_conexion
#VALIDACION Y FORMATEO DE LO QUE INGRESA EL USUARIO
import re

# Validaciones para Título
def longitud_titulo(texto, max_length=166):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto

def format_title(texto):
    if texto:
        return texto[0].upper() + texto[1:]
    return texto

def validate_and_format_title(titulo):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áéíóúÁÉÍÓÚñÑ.,;:!?-"
    
    # Filtrar caracteres no permitidos
    filtered_text = ''.join([char for char in titulo if char in allowed_chars])
    
    # Evitar dos signos de puntuación consecutivos y permitir solo uno
    filtered_text = re.sub(r'([.,;:!?-]){2,}', r'\1', filtered_text)
    
    # Evitar dos signos de puntuación diferentes consecutivos
    filtered_text = re.sub(r'([.,;:!?-])([.,;:!?-])', r'\1', filtered_text)
    
    # Formatear el texto para capitalizar solo la primera letra
    formatted_text = format_title(filtered_text)
    
    return formatted_text

# Validaciones para Cota
def limitar_longitud_cota(texto, max_length=14):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto

def convert_to_uppercase(texto):
    return texto.upper()

def allow_only_letters_numbers_dots(char):
    if re.match(r'^[a-zA-Z0-9.]$', char):
        return char
    return ''

# Validaciones para Autor y Editorial
def validar_y_formatear_texto(texto):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áéíóúÁÉÍÓÚñÑ"
    
    # Filtrar caracteres no permitidos
    filtered_text = ''.join([char for char in texto if char in allowed_chars])
    
    # Formatear el texto para capitalizar solo la primera letra de cada palabra
    formatted_text = filtered_text.title()
    
    return formatted_text

def longitud_autor(texto, max_length=53):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto

def longitud_editorial(texto, max_length=49):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto

# Validaciones para Nro de Registro, Año, Nro de Edición y Volumen
def longitud_nro_registro(texto, max_length=10):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto

def longitud_anio(texto, max_length=4):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto

def longitud_nro_edicion(texto, max_length=2):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto

def longitud_volumen(texto, max_length=2):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto


#VALIDACION DE DATOS INGRESADOS
def validar_cota(cota):
    if len(cota) < 3:
        return "La longitud de la cota debe ser al menos de 3 caracteres."
    if len(cota) == 3 and not cota.isalpha():
        return "Las cotas de longitud 3 solo deben contener letras."
    if ".." in cota:
        return "La cota no puede contener dos puntos consecutivos."
    if not re.match(r'^[a-zA-Z0-9.]+$', cota):
        return "La cota solo puede contener letras, números y puntos."
    return None

def validar_titulo(titulo):
    if len(titulo) < 4:
        return "La longitud del título debe ser al menos de 4 caracteres."
    if not re.match(r'^[a-zA-Z0-9\s]+$', titulo):
        return "El título solo puede contener letras, números y espacios."
    return None

def validar_autor(autor):
    if len(autor) < 5:
        return "La longitud del nombre del autor debe ser al menos de 5 caracteres."
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', autor):
        return "El nombre del autor solo puede contener letras y espacios."
    return None

def validar_editorial(editorial):
    if len(editorial) < 3:
        return "La longitud del nombre de la editorial debe ser al menos de 3 caracteres."
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', editorial):
        return "El nombre de la editorial solo puede contener letras y espacios."
    return None

def validar_n_registro(n_registro):
    if len(n_registro) < 1:
        return "La longitud del número de registro debe ser al menos de 1 carácter."

def validar_n_volumenes(n_volumenes):
    if len(n_volumenes) < 1:
        return "La longitud del número de volúmenes debe ser al menos de 1 carácter."
    if not n_volumenes.isdigit():
        return "El número de volúmenes solo puede contener números."
    return None

def validar_edicion(edicion):
    if len(edicion) < 1:
        return "La longitud del número de edición debe ser al menos de 1 carácter."
    if not edicion.isdigit():
        return "El número de edición solo puede contener números."
    return None

def validate_year(new_value):
    if new_value.isdigit() and len(new_value) == 4:
        year = int(new_value)
        current_year = datetime.now().year
        if 1500 <= year <= current_year:
            return True
    return False

# Validación de Nro de Registro Único
def validar_nro_registro_unico(n_registro):
    conn = establecer_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Libro FROM libro WHERE n_registro = %s", (n_registro,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            id_libro_existente = resultado[0]
            return f"El libro con ID {id_libro_existente} ya tiene el número de registro {n_registro}."
    return None

def validar_campos(cota, titulo, autor, editorial, n_registro, n_volumenes, edicion, year):
    errores = []

    error_cota = validar_cota(cota)
    if error_cota:
        errores.append(error_cota)

    error_titulo = validar_titulo(titulo)
    if error_titulo:
        errores.append(error_titulo)

    error_autor = validar_autor(autor)
    if error_autor:
        errores.append(error_autor)

    error_editorial = validar_editorial(editorial)
    if error_editorial:
        errores.append(error_editorial)

    error_n_registro = validar_n_registro(n_registro)
    if error_n_registro:
        errores.append(error_n_registro)
    else:
        error_n_registro_repetido = validar_nro_registro_unico(n_registro)
        if error_n_registro_repetido:
            errores.append(error_n_registro_repetido)

    error_n_volumenes = validar_n_volumenes(n_volumenes)
    if error_n_volumenes:
        errores.append(error_n_volumenes)

    error_edicion = validar_edicion(edicion)
    if error_edicion:
        errores.append(error_edicion)

    if not validate_year(year):
        errores.append("El año debe ser un número de 4 dígitos entre 1500 y el año actual.")

    return errores

# Ejemplo de uso
# errores = validar_campos("C123", "Un Título", "Nombre Autor", "Editorial", "12345", "2", "1", "2023")
# if errores:
#     for error in errores:
#         print(error)
# else:
#     print("Todos los campos son válidos.")

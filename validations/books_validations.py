import re
from datetime import datetime
from db.conexion import establecer_conexion


#VALIDACION Y FORMATEO DE LO QUE INGRESA EL USUARIO
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
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áéíóúÁÉÍÓÚñÑ.,;:!?¡¿-"
    
    # Filtrar caracteres no permitidos
    filtered_text = ''.join([char for char in titulo if char in allowed_chars])

    # Evitar signos de puntuación entre letras
    filtered_text = re.sub(r'([a-zA-Z])([.,;:!?¡¿-]+)([a-zA-Z])', r'\1 \3', filtered_text)

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
def format_autor_editorial(texto):
    if texto:
        return texto[0].upper() + texto[1:]
    return texto
def validar_y_formatear_texto(texto):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ áéíóúÁÉÍÓÚñÑ.,&()/-'\"äëïöü"
    
    # Filtrar caracteres no permitidos
    filtered_text = ''.join([char for char in texto if char in allowed_chars])
    
    # Formatear el texto para capitalizar solo la primera letra de cada palabra
    formatted_text = format_autor_editorial(filtered_text)
    
    return formatted_text


def longitud_autor(texto, max_length=53):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto

def longitud_editorial(texto, max_length=49):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto
#Longitud de nro de edicion y volumen
def validar_digitos(event, longitud_func, max_digitos=3):
    if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'):
        # Obtener el texto actual antes de borrar
        current_text = event.widget.get()
        if event.keysym == 'Delete':
            current_text = current_text[:-1]  # Eliminar solo un carácter
        if len(current_text) > max_digitos:
            return "break"
        return longitud_func(current_text)
    if not event.char.isdigit():
        return "break"
    current_text = event.widget.get()
    if len(current_text) >= max_digitos:
        return "break"
    return longitud_func(current_text)
# Validaciones para Nro de Registro, Año, Nro de Edición y Volumen
def longitud_nro_registro(texto, max_length=10):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto
def allow_only_numbers_and_dot_at_thousands(text):
    # Permitir solo números y puntos en el formato correcto
    if re.match(r'^\d{1,3}(\.\d{0,3})*$', text):
        return True
    return False

def longitud_ano(texto, max_length=4):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto

def longitud_nro_edicion(texto, max_length=3):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto

def longitud_volumen(texto, max_length=3):
    if len(texto) >= max_length:
        return texto[:max_length]
    return texto
#VALIDACION DE SALAS 
def mostrar_opciones(self, categoria_values, asignatura_values):

        self.categoria_cb['values'] = categoria_values
        self.asignatura_cb['values'] = asignatura_values
        self.check_changes()
        
   

#VALIDACION DE DATOS INGRESADOS
# Diccionario de asignaturas permitidas por sala
asignaturas_permitidas_por_sala = {
    "1I": [
        "Cuentos de Aventuras",
        "Poesías y Canciones Venezolanas",
        "Cuentos Realistas",
        "Cuentos de Hadas y Fantasía",
        "Novelas de Aventuras",
        "Cuentos de Animales",
        "Sección de los más pequeños",
        "Novelas Históricas",
        "Fábulas",
        "Cuentos Venezolanos"
    ]
}

def validar_cota(cota, sala, asignatura):
    if not cota:
        return "El campo cota es obligatorio."
    if len(cota) < 3:
        return "La longitud de la cota debe ser al menos de 3 caracteres."
    if len(cota) == 3 and not cota.isalpha() and sala in asignaturas_permitidas_por_sala:
        return f"Las cotas de longitud 3 solo deben contener letras en la sala {sala}."
    if len(cota) > 3 and not cota.isalpha() and sala in asignaturas_permitidas_por_sala and asignatura in asignaturas_permitidas_por_sala[sala]:
        return f"Las cotas de más de 3 caracteres solo deben contener letras en la asignatura '{asignatura}' en la sala {sala}."
    if len(cota) == 3 and asignatura not in asignaturas_permitidas_por_sala.get(sala, []):
        return f"En la sala {sala}, las cotas de longitud 3 solo están permitidas en las asignaturas: {', '.join(asignaturas_permitidas_por_sala[sala])}."
    if ".." in cota:
        return "La cota no puede contener puntos consecutivos."
    if not re.match(r'^[a-zA-Z0-9.]+$', cota):
        return "La cota solo puede contener letras, números y puntos."
    return None

def validar_cota_unica(cota):
    conn = establecer_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Libro FROM libro WHERE cota = %s", (cota,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            id_libro_existente = resultado[0]
            return f"La cota '{cota}' ya está asignada al libro con ID {id_libro_existente}."
    return None

def validar_cota_unica_modificar(cota, id_libro_original):
    conn = establecer_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Libro FROM libro WHERE cota = %s AND ID_Libro != %s", (cota, id_libro_original))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            id_libro_existente = resultado[0]
            return f"La cota '{cota}' ya está asignada al libro con ID {id_libro_existente}."
    return None

def validar_titulo(titulo):
    if not titulo:
        return "El campo título es obligatorio."
    if titulo[0] == " ":
        return "El título no puede comenzar con un espacio."
    if len(titulo) < 4:
        return "La longitud del título debe ser al menos de 4 caracteres."
    if ".." in titulo:
        return "El título no puede contener más de un punto consecutivo."
    if "!!" in titulo or "¡¡" in titulo:
        return "El título no puede contener más de un signo de exclamación consecutivo."
    if "??" in titulo or "¿¿" in titulo:
        return "El título no puede contener más de un signo de interrogación consecutivo."
    if "--" in titulo:
        return "El título no puede contener más de un guion consecutivo."
    if ",," in titulo:
        return "El título no puede contener más de una coma consecutiva."
    if ";;" in titulo:
        return "El título no puede contener más de un punto y coma consecutivo."
    if "::" in titulo:
        return "El título no puede contener más de un signo de dos puntos consecutivo."
    if titulo.count("¿") != titulo.count("?"):
        return "El título debe tener un número igual de signos de apertura y cierre de interrogación."
    if titulo.count("¡") != titulo.count("!"):
        return "El título debe tener un número igual de signos de apertura y cierre de exclamación."
    if re.search(r'[^¿?!¡][?!¡¿]', titulo):
        return "El título tiene signos de puntuación en el orden incorrecto."
    if re.search(r'¿[^?]*$', titulo) or re.search(r'¡[^!]*$', titulo):
        return "El título tiene un signo de apertura sin su correspondiente cierre."
    if re.search(r'\s{2,}', titulo):
        return "El título no puede contener más de un espacio consecutivo."
    if titulo[-1] == " ":
        return "El título no puede terminar en un espacio."
    return None  # Título válido

def validar_autor(autor):
    if not autor:
        return "El campo autor es obligatorio."
    if autor[0] == " ":
        return "El nombre del autor no puede comenzar con un espacio."
    if len(autor) < 3:
        return "La longitud del nombre del autor debe ser al menos de 3 caracteres."
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s.,&()/-\'"äëïöü]+$', autor):
        return "El nombre del autor solo puede contener letras, espacios y los caracteres ., & ( ) / - ' \" ä ë ï ö ü."
    if re.search(r'\s{2,}', autor):
        return "El nombre del autor no puede contener más de un espacio consecutivo."
    if re.search(r'\.{2,}', autor):
        return "El nombre del autor no puede contener más de un punto consecutivo."
    if re.search(r'&{2,}', autor):
        return "El nombre del autor no puede contener más de un ampersand consecutivo."
    if re.search(r'\({2,}', autor) or re.search(r'\){2,}', autor):
        return "El nombre del autor no puede contener más de un paréntesis consecutivo."
    if re.search(r'/{2,}', autor):
        return "El nombre del autor no puede contener más de una barra consecutiva."
    if re.search(r'-{2,}', autor):
        return "El nombre del autor no puede contener más de un guion consecutivo."
    if re.search(r'\'{2,}', autor):
        return "El nombre del autor no puede contener más de un apóstrofo consecutivo."
    if re.search(r'\"{2,}', autor):
        return "El nombre del autor no puede contener más de una comilla consecutiva."
    if autor[-1] == " ":
        return "El nombre del autor no puede terminar en un espacio."
    return None
def validar_editorial(editorial):
    if not editorial:
        return "El campo editorial es obligatorio."
    if editorial[0] == " ":
        return "El nombre de la editorial no puede comenzar con un espacio."
    if len(editorial) < 3:
        return "La longitud del nombre de la editorial debe ser al menos de 3 caracteres."
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s.,&()/-\'"äëïöü]+$', editorial):
        return "El nombre de la editorial solo puede contener letras, espacios y los caracteres ., & ( ) / - ' \" ä ë ï ö ü."
    if re.search(r'\s{2,}', editorial):
        return "El nombre de la editorial no puede contener más de un espacio consecutivo."
    if re.search(r'\.{2,}', editorial):
        return "El nombre de la editorial no puede contener más de un punto consecutivo."
    if re.search(r'&{2,}', editorial):
        return "El nombre de la editorial no puede contener más de un ampersand consecutivo."
    if re.search(r'\({2,}', editorial) or re.search(r'\){2,}', editorial):
        return "El nombre de la editorial no puede contener más de un paréntesis consecutivo."
    if re.search(r'/{2,}', editorial):
        return "El nombre de la editorial no puede contener más de una barra consecutiva."
    if re.search(r'-{2,}', editorial):
        return "El nombre de la editorial no puede contener más de un guion consecutivo."
    if re.search(r'\'{2,}', editorial):
        return "El nombre de la editorial no puede contener más de un apóstrofo consecutivo."
    if re.search(r'\"{2,}', editorial):
        return "El nombre de la editorial no puede contener más de una comilla consecutiva."
    if editorial[-1] == " ":
        return "El nombre de la editorial no puede terminar en un espacio."
    return None

def validar_n_registro(n_registro):
    if not n_registro:
        return "El campo número de registro es obligatorio."
    if len(n_registro) < 5:
        return "La longitud del número de registro debe ser al menos de  4 numeros."

def validar_n_volumenes(n_volumenes):
    if not n_volumenes:
        return "El campo número de volumenes es obligatorio."
    if len(n_volumenes) < 1:
        return "La longitud del número de volúmenes debe ser al menos de 1 carácter."
    if not n_volumenes.isdigit():
        return "El número de volúmenes solo puede contener números."
    return None

def validar_edicion(edicion):
    if not edicion:
        return "El campo edición es obligatorio."
    if len(edicion) < 1:
        return "La longitud del número de edición debe ser al menos de 1 carácter."
    if not edicion.isdigit():
        return "El número de edición solo puede contener números."
    return None

def validate_year(new_value):
    if not new_value:
        return "El campo año es obligatorio."
    if new_value.isdigit() and len(new_value) == 4:
        year = int(new_value)
        current_year = datetime.now().year
        if 1500 <= year <= current_year:
            return True
    return False

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

def validar_nro_registro_unico_modificar(n_registro, id_libro_original):
    conn = establecer_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Libro FROM libro WHERE n_registro = %s AND ID_Libro != %s", (n_registro, id_libro_original))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            id_libro_existente = resultado[0]
            return f"El libro con ID {id_libro_existente} ya tiene el número de registro {n_registro}."
    return None

def validar_campos(categoria, asignatura, cota, titulo, autor, editorial, n_registro, n_volumenes, edicion, year, sala, id_libro=None):
    errores = []

    # Validación de Categoría y Asignatura
    if (categoria == "No se ha seleccionado una categoría" or not categoria) and \
       (asignatura == "No se ha seleccionado una asignatura" or not asignatura):
        errores.append("Debe seleccionar una categoría y una asignatura.")
    elif categoria == "No se ha seleccionado una categoría" or not categoria:
        errores.append("Debe seleccionar una categoría.")
    elif asignatura == "No se ha seleccionado una asignatura" or not asignatura:
        errores.append("Debe seleccionar una asignatura.")

    # Validar Cota
    error_cota = validar_cota(cota, sala, asignatura)
    if error_cota:
        errores.append(error_cota)
    else:
        if sala != "1I" or asignatura not in asignaturas_permitidas_por_sala:
            if id_libro:
                print(f"Validar cota para modificación con ID libro: {id_libro}")  # Depuración
                error_cota_unica = validar_cota_unica_modificar(cota, id_libro)
            else:
                print(f"Validar cota para creación: {cota}")  # Depuración
                error_cota_unica = validar_cota_unica(cota)

            if error_cota_unica:
                errores.append(error_cota_unica)

    # Validar Título
    error_titulo = validar_titulo(titulo)
    if error_titulo:
        errores.append(error_titulo)

    # Validar Autor
    error_autor = validar_autor(autor)
    if error_autor:
        errores.append(error_autor)

    # Validar Editorial
    error_editorial = validar_editorial(editorial)
    if error_editorial:
        errores.append(error_editorial)

    # Validar Número de Registro
    error_n_registro = validar_n_registro(n_registro)
    if error_n_registro:
        errores.append(error_n_registro)
    else:
        if id_libro:
            print(f"Validar número de registro para modificación con ID libro: {id_libro}")  # Depuración
            error_n_registro_repetido = validar_nro_registro_unico_modificar(n_registro, id_libro)
        else:
            print(f"Validar número de registro para creación: {n_registro}")  # Depuración
            error_n_registro_repetido = validar_nro_registro_unico(n_registro)

        if error_n_registro_repetido:
            errores.append(error_n_registro_repetido)

    # Validar Número de Volúmenes
    error_n_volumenes = validar_n_volumenes(n_volumenes)
    if error_n_volumenes:
        errores.append(error_n_volumenes)

    # Validar Edición
    error_edicion = validar_edicion(edicion)
    if error_edicion:
        errores.append(error_edicion)

    # Validar Año
    if not validate_year(year):
        errores.append("El año debe ser un número de 4 dígitos entre 1500 y el año actual.")

    return errores
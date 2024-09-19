from fpdf import FPDF   #SI NO LES FUNCIONA DEBEN INSTALAR la libreria fpdf
from datetime import datetime, timedelta
import os
import filecmp#Libreria para comparar archivos

def obtener_nombre_archivo_unico(nombre_archivo_base):#Este funcion evita lo sobreescritura de un mismo archivo con el uso de un contador
    contador = 1
    nombre_archivo = nombre_archivo_base
    while os.path.exists(nombre_archivo):#Comprueba la existencia del reporte
        nombre_archivo = f"{nombre_archivo_base}({contador}).pdf"
        contador += 1
    return nombre_archivo

# Función para verificar y renombrar el archivo si es necesario
def verificar_y_guardar_pdf(pdf, nombre_archivo_base):
    nombre_archivo_temporal = "temp_reporte.pdf"
    pdf.output(nombre_archivo_temporal, 'F')
    
    nombre_archivo_final = obtener_nombre_archivo_unico(nombre_archivo_base)
    if os.path.exists(nombre_archivo_final):
        if filecmp.cmp(nombre_archivo_temporal, nombre_archivo_final, shallow=False):#Si los archivos son idénticos, se elimina el archivo temporal y se imprime un mensaje indicando que el archivo ya existe y su contenido es idéntico.
            os.remove(nombre_archivo_temporal)
            print("El archivo ya existe y su contenido es idéntico.")
        else:
            os.rename(nombre_archivo_temporal, nombre_archivo_final)#renombra el archivo
            print(f"Archivo guardado como {nombre_archivo_final}")
    else:
        os.rename(nombre_archivo_temporal, nombre_archivo_final)
        print(f"Archivo guardado como {nombre_archivo_final}")


class Cliente:
    def __init__(self, nombre, telefono, cedula, direccion):
        self.nombre = nombre
        self.telefono = telefono
        self.cedula = cedula
        self.direccion = direccion

class Libro:
    def __init__(self, cota, categoria, sala, asignatura, numero_registro, autor, titulo, num_volumenes, num_ejemplares, edicion, año, editorial):
        self.cota = cota
        self.categoria = categoria
        self.sala = sala
        self.asignatura = asignatura
        self.numero_registro = numero_registro
        self.autor = autor
        self.titulo = titulo
        self.num_volumenes = num_volumenes
        self.num_ejemplares = num_ejemplares
        self.edicion = edicion
        self.año = año
        self.editorial = editorial

class PDF(FPDF):
    def header(self):
        self.image('assets_2/logo-biblioteca-red-2.png', x=10, y=10, w=35, h=15)
        self.set_font('Arial', 'B', 20)
        self.cell(w=0, h=15, txt='Reporte de Préstamo de Libros', border=0, ln=1, align='C', fill=0)
        self.ln(5)

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 12)
        self.cell(w=0, h=10, txt='Pagina ' + str(self.page_no()) + '/{nb}', border=1, align='C', fill=0)

    def agregar_datos_cliente(self, cliente):
        self.set_font("Arial", "", 9)
        self.cell(w=0, h=10, txt="DATOS DEL CLIENTE", border=1, ln=1, align="C", fill=0)
        self.cell(w=150, h=10, txt=f"Apellidos y Nombres: {cliente.nombre}", border=1, align="L", fill=0)
        self.cell(w=0, h=10, txt=f"C.I.: {cliente.cedula}", border=1, align="L",ln=1, fill=0)
        self.cell(w=150, h=10, txt=f"Dirección: {cliente.direccion}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Teléfono: {cliente.telefono}", border=1, align="L", fill=0)

    def agregar_datos_libro(self, libro, fecha_registro, fecha_limite):
        
        self.set_font("Arial", "", 9)
        self.cell(w=0, h=10, txt="DATOS DEL LIBRO", border=1, ln=1, align="C", fill=0)
        self.cell(w=48, h=10, txt=f"Sala: {libro.sala}", border=1, align="L", fill=0)
        self.cell(w=48, h=10, txt=f"Cota: {libro.cota}", border=1, align="L", fill=0)
        self.cell(w=30, h=10, txt=f"Nro Ejemplares: {libro.num_ejemplares}", border=1, align="L", fill=0)
        self.cell(w=34, h=10, txt=f"Nro Registro: {libro.numero_registro}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Nro Volúmenes: {libro.num_volumenes}", border=1, align="L", fill=0)
        self.cell(w=96, h=10, txt=f"Categoría: {libro.categoria}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Asignatura: {libro.asignatura}", border=1, align="L", fill=0)
        self.cell(w=96, h=10, txt=f"Título: {libro.titulo}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Autor: {libro.autor}", border=1, align="L", fill=0)
        self.cell(w=96, h=10, txt=f"Editorial: {libro.editorial}", border=1, align="L", fill=0)
        self.cell(w=48, h=10, txt=f"Año: {libro.año}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Edición: {libro.edicion}", border=1, align="L", fill=0)
        self.cell(w=96, h=10, txt=f"Fecha de Registro: {fecha_registro}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Fecha Límite: {fecha_limite}", border=1, align="L", fill=0)

    def agregar_firmas(self):
        self.set_font("Arial", "", 9)
        self.cell(w=96, h=10, txt="FIRMA DEL SOLICITANTE", border=1, ln=0, align="C", fill=0)
        self.cell(w=0, h=10, txt="FIRMA DEL ENCARGADO", border=1, ln=1, align="C", fill=0)
        self.cell(w=48, h=10, txt="Prestamo", border=1, align="C", fill=0)
        self.cell(w=48, h=10, txt="Devolucion", border=1, align="C", fill=0)
        self.cell(w=48, h=10, txt="Prestamo", border=1, align="C", fill=0)
        self.cell(w=0, h=10, txt="Devolucion", border=1, ln=1, align="C", fill=0)
        self.cell(w=48, h=20, txt="", border=1, align="C", fill=0)
        self.cell(w=48, h=20, txt="", border=1, align="C", fill=0)
        self.cell(w=48, h=20, txt="", border=1, align="C", fill=0)
        self.cell(w=0, h=20, txt="", border=1, ln=1, align="C", fill=0)
        self.cell(w=48, h=10, txt="Fecha Préstamo", border=1, align="C", fill=0)
        self.cell(w=48, h=10, txt="Fecha Devolución", border=1, align="C", fill=0)
        self.cell(w=48, h=10, txt="Fecha Préstamo", border=1, align="C", fill=0)
        self.cell(w=0, h=10, txt="Fecha Devolución", border=1, ln=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=16, h=10, txt="", border=1, align="C", fill=0)
        self.cell(w=0, h=10, txt="", border=1, align="C", fill=0)


# Instanciación de la clase PDF
pdf = PDF()
pdf.alias_nb_pages()
pdf.set_font('Arial', '', 12)

# Crear instancia del cliente
cliente = Cliente("Keyner Ivan Lizarazo Diaz", "04263757236", "30905297", "Las Margaritas Via Delicias")

# Crear instancias de libros ficticios
libro1 = Libro("12345", "Ficción", "Sala A", "Literatura", "001", "Gabriel García Márquez", "Cien Años de Soledad", "1", "3", "Primera", "1967", "Editorial Sudamericana")
libro2 = Libro("D221", "Fantasia", "General","Literatura", 123.323, "Brayan Diaz", "Historias Medievales",2, 2, 12, 1998, "Libertadores" )
libros_prestamos1 = [libro1,libro2]
libros_prestamos2 = [libro2,libro1]
# Fecha de registro y fecha límite
fecha_registro = datetime.now().strftime("%d/%m/%Y")
fecha_limite = (datetime.now() + timedelta(days=20)).strftime("%d/%m/%Y")

# Añadir pagina, se llaman a los metodos para lograr el formato deseado
pdf.add_page()
pdf.agregar_datos_cliente(cliente)
pdf.agregar_datos_libro(libro1, fecha_registro, fecha_limite)
pdf.agregar_firmas() 

for indice,libro in enumerate(libros_prestamos2): # De esta forma se desempaqueta el contenido de la lista y genera las hojas necesarias
     if indice > 0:#De esta forma se crea la pagina antes de entrar al bucle y no crear una pagina adicional
         pdf.add_page()
     pdf.agregar_datos_cliente(cliente)
     pdf.agregar_datos_libro(libro, fecha_registro, fecha_limite)
     pdf.agregar_firmas() 



fecha_actual = datetime.now().strftime("%d_%m_%Y")#Aqui se usa un guion bajo para evitar errores con caracteres espéciales en el nombre del documento
nombre_corregido = cliente.nombre.replace(" ","_")#De esta forma se remplazan los espacios en blanco para evitar errores al crear el archivo
nombre_archivo_base= f"Reporte_de_prestamo_{nombre_corregido}_{fecha_actual}"

#Establecer metadatos del documento
pdf.set_title("Reporte de Libro")
pdf.set_author(cliente.nombre)#Esto debe ser modificado a futuro en base al usuario que haga el reporte
pdf.set_creator("Aplicación de la Biblioteca Pública de Rubio")
pdf.set_subject("Reporte de préstamo de libros")
pdf.set_keywords("Reporte,Libro,Préstamo,Biblioteca")#Estas palabras clave pueden ser usadas por los motores de búsqueda y los lectores de PDF para indexar y encontrar el documento más fácilmente.

nombre_archivo = obtener_nombre_archivo_unico(nombre_archivo_base)
verificar_y_guardar_pdf(pdf,nombre_archivo_base)

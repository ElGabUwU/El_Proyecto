from fpdf import FPDF   #SI NO LES FUNCIONA DEBEN INSTALAR la libreria fpdf
from datetime import datetime, timedelta
import os
import filecmp#Libreria para comparar archivos
from tkinter.filedialog import asksaveasfilename
import tkinter as tk
from tkinter import messagebox

def formatear_fecha(fecha):
    try:
        return datetime.strptime(fecha, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        try:
            return datetime.strptime(fecha, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            print(f"Error: El formato de la fecha '{fecha}' no es válido.")
            return fecha

def formatear_fecha_titulo(fecha):
    return datetime.strptime(fecha, "%Y-%m-%d").strftime("%d_%m_%Y")
def obtener_nombre_archivo_unico(nombre_archivo_base):
    contador = 1
    nombre_archivo = f"{nombre_archivo_base}.pdf"
    while os.path.exists(nombre_archivo):
        nombre_archivo = f"{nombre_archivo_base}({contador}).pdf"
        contador += 1
    return nombre_archivo

def verificar_y_guardar_pdf(pdf, nombre_archivo_base):
    nombre_archivo_temporal = "temp_reporte.pdf"
    pdf.output(nombre_archivo_temporal, 'F')
    
    nombre_archivo_final = f"{nombre_archivo_base}.pdf"
    if os.path.exists(nombre_archivo_final):
        if filecmp.cmp(nombre_archivo_temporal, nombre_archivo_final, shallow=False):
            os.remove(nombre_archivo_temporal)
            print("El archivo ya existe y su contenido es idéntico.")
            # Aplicar el contador para generar un nombre único
            nombre_archivo_final = obtener_nombre_archivo_unico(nombre_archivo_base)
            os.rename(nombre_archivo_temporal, nombre_archivo_final)
            print(f"Archivo guardado como: {nombre_archivo_final}")
        else:
            os.remove(nombre_archivo_final)  # Elimina el archivo existente
            os.rename(nombre_archivo_temporal, nombre_archivo_final)  # Renombra el archivo temporal
            print(f"Archivo sobrescrito como: {nombre_archivo_final}")
    else:
        os.rename(nombre_archivo_temporal, nombre_archivo_final)
        print(f"Archivo guardado como {nombre_archivo_final}")

from loans.backend.models import Cliente, Libro
class PDF(FPDF):
    def header(self):
        self.image('assets_2/logo-biblioteca-red-2.png', x=10, y=10, w=35, h=15)
        self.set_font('Arial', 'B', 20)
        self.cell(w=0, h=15, txt='Reporte de Préstamo de Libros', border=0, ln=1, align='C', fill=0)
        self.ln(5)

    def agregar_rif(self):
        self.set_y(-30) 
        self.set_font('Arial', '', 10)
        self.cell(w=0, h=10, txt="RIF G-20000160-7", border=0, align='C', fill=0)

    def footer(self):
        self.agregar_rif()
        self.set_y(-20)
        self.set_font('Arial', 'I', 12)
        self.cell(w=0, h=10, txt='Pagina ' + str(self.page_no()) + '/{nb}', border=1, align='C', fill=0)

    def agregar_datos_cliente(self, cliente):
        self.set_font("Arial", "", 9)
        self.cell(w=0, h=10, txt="DATOS DEL CLIENTE", border=1, ln=1, align="C", fill=0)
        self.cell(w=150, h=10, txt=f"Apellidos y Nombres: {cliente.apellido} {cliente.nombre}", border=1, align="L", fill=0)
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
        self.cell(w=96, h=10, txt=f"Fecha de Registro: {formatear_fecha(fecha_registro)}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Fecha Límite: {formatear_fecha(fecha_limite)}", border=1, align="L", fill=0)


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
    
    def agregar_datos_al_pdf(self,cliente, libro, fecha_registro, fecha_limite):
        self.agregar_datos_cliente(cliente)
        self.agregar_datos_libro(libro, fecha_registro, fecha_limite)
        self.agregar_firmas()

def generar_pdf(cliente, books_data, prestamos_data, nombre_archivo_base):
    pdf = PDF()
    pdf.alias_nb_pages()

    for index, book_data in enumerate(books_data):
        pdf.add_page()
        prestamo = prestamos_data[index]
        libro = Libro(
            cota=book_data["Cota"],
            categoria=book_data["ID_Categoria"],
            sala=book_data["ID_Sala"],
            asignatura=book_data["ID_Asignatura"],
            numero_registro=book_data["n_registro"],
            autor=book_data["autor"],
            titulo=book_data["titulo"],
            num_volumenes=book_data["n_volumenes"],
            num_ejemplares=book_data["n_ejemplares"],
            edicion=book_data["edicion"],
            año=book_data["año"],
            editorial=book_data["editorial"]
        )
        # Añadir datos al PDF
        pdf.agregar_datos_al_pdf(cliente, libro, formatear_fecha(prestamo["fecha_r"]), formatear_fecha(prestamo["fecha_en"]))

    # Establecer metadatos del documento
    pdf.set_title("Reporte de Libro")
    pdf.set_author(f"{cliente.nombre} {cliente.apellido}")
    pdf.set_creator("Aplicación de la Biblioteca Pública de Rubio")
    pdf.set_subject("Reporte de préstamo de libros")
    pdf.set_keywords("Reporte,Libro,Préstamo,Biblioteca")

    # Crear ventana de diálogo para guardar el archivo
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter
    carpeta_documentos = os.path.expanduser("~/Documents")

    nombre_archivo_final = asksaveasfilename(
        defaultextension=".pdf",
        initialfile=f"{nombre_archivo_base}.pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialdir=carpeta_documentos
    )

    if nombre_archivo_final:
        verificar_y_guardar_pdf(pdf, nombre_archivo_final)
        messagebox.showinfo("Éxito", "El reporte ha sido creado de forma exitosa.")
    else:
        print("Guardado cancelado.")
        root.destroy()


# def generar_pdf(cliente, libro, fecha_registro, fecha_limite, nombre_archivo_base):
#     pdf = PDF()
#     pdf.alias_nb_pages()
#     pdf.add_page()

#     # Añadir datos al PDF
#     pdf.agregar_datos_al_pdf(cliente, libro, fecha_registro, fecha_limite)

#     # Establecer metadatos del documento
#     pdf.set_title("Reporte de Libro")
#     pdf.set_author(f"{cliente.nombre} {cliente.apellido}")
#     pdf.set_creator("Aplicación de la Biblioteca Pública de Rubio")
#     pdf.set_subject("Reporte de préstamo de libros")
#     pdf.set_keywords("Reporte,Libro,Préstamo,Biblioteca")

#     # Crear ventana de diálogo para guardar el archivo
#     root = tk.Tk()
#     root.withdraw()  # Oculta la ventana principal de tkinter
#     nombre_archivo_base = f"Reporte_Prestamo_{cliente.nombre}_{cliente.apellido}_{formatear_fecha_titulo(fecha_registro)}"
    
#     # Obtener la ruta de la carpeta Documentos del usuario
#     carpeta_documentos = os.path.expanduser("~/Documents")
    
#     nombre_archivo_final = asksaveasfilename(
#         defaultextension=".pdf",
#         initialfile=f"{nombre_archivo_base}.pdf",
#         filetypes=[("PDF files", "*.pdf")],
#         initialdir=carpeta_documentos  # Establecer la carpeta Documentos como directorio inicial
#     )
    
#     if nombre_archivo_final:
#         # Guardar el PDF
#         verificar_y_guardar_pdf(pdf, nombre_archivo_final)
#         # Mostrar mensaje de éxito
#         messagebox.showinfo("Éxito", "El reporte ha sido creado de forma exitosa.")
#     else:
#         print("Guardado cancelado.")
    
#     root.destroy()





















# Instanciación de la clase PDF
# pdf = PDF()
# pdf.alias_nb_pages()
# pdf.set_font('Arial', '', 12)
# pdf.add_page()

# Crear instancia del cliente
#cliente = Cliente("Keyner Ivan Lizarazo Diaz", "04263757236", "30905297", "Las Margaritas Via Delicias")

# Crear instancias de libros ficticios
#libro1 = Libro("12345", "Ficción", "Sala A", "Literatura", "001", "Gabriel García Márquez", "Cien Años de Soledad", "1", "3", "Primera", "1967", "Editorial Sudamericana")
#libro2 = Libro("D221", "Fantasia", "General","Literatura", 123.323, "Brayan Diaz", "Historias Medievales",2, 2, 12, 1998, "Libertadores" )
#libros_prestamos1 = [libro1,libro2]
#libros_prestamos2 = [libro2,libro1]
# Fecha de registro y fecha límite
#fecha_registro = datetime.now().strftime("%d/%m/%Y")
# fecha_limite = (datetime.now() + timedelta(days=20)).strftime("%d/%m/%Y")

# # Añadir páginas y datos para los libros en la lista
# for indice, libro in enumerate(libros_prestamos2):
#     if indice > 0:  # Añadir una nueva página solo después de la primera iteración
#         pdf.add_page()
#     pdf.agregar_datos_al_pdf(cliente, libro, fecha_registro, fecha_limite)


# fecha_actual = datetime.now().strftime("%d_%m_%Y")#Aqui se usa un guion bajo para evitar errores con caracteres espéciales en el nombre del documento
# nombre_corregido = cliente.nombre.replace(" ","_")#De esta forma se remplazan los espacios en blanco para evitar errores al crear el archivo
# nombre_archivo_base= f"Reporte_de_prestamo_{nombre_corregido}_{fecha_actual}"

# #Establecer metadatos del documento
# pdf.set_title("Reporte de Libro")
# pdf.set_author(self.cliente["Nombre"])#Esto debe ser modificado a futuro en base al usuario que haga el reporte
# pdf.set_creator("Aplicación de la Biblioteca Pública de Rubio")
# pdf.set_subject("Reporte de préstamo de libros")
# pdf.set_keywords("Reporte,Libro,Préstamo,Biblioteca")#Estas palabras clave pueden ser usadas por los motores de búsqueda y los lectores de PDF para indexar y encontrar el documento más fácilmente.

# nombre_archivo = obtener_nombre_archivo_unico(nombre_archivo_base)
# verificar_y_guardar_pdf(pdf,nombre_archivo_base)

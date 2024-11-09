from fpdf import FPDF   #SI NO LES FUNCIONA DEBEN INSTALAR la libreria fpdf
from datetime import datetime, timedelta
import os
import filecmp#Libreria para comparar archivos
from tkinter.filedialog import asksaveasfilename
import tkinter as tk
from tkinter import messagebox, Tk
from util.utilidades import resource_path

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
import os
import filecmp
from tkinter import messagebox

def obtener_nombre_archivo_unico(nombre_archivo_base):
    contador = 1
    nombre_archivo = f"{nombre_archivo_base}.pdf"
    while os.path.exists(nombre_archivo):
        nombre_archivo = f"{nombre_archivo_base}({contador}).pdf"
        contador += 1
    return nombre_archivo

import os
import filecmp
from tkinter import messagebox

def obtener_nombre_archivo_unico(nombre_archivo_base):
    contador = 1
    nombre_archivo = f"{nombre_archivo_base}.pdf"
    while os.path.exists(nombre_archivo):
        nombre_archivo = f"{nombre_archivo_base}({contador}).pdf"
        contador += 1
    return nombre_archivo

def verificar_y_guardar_pdf(pdf, nombre_archivo_final, parent):
    nombre_archivo_temporal = "temp_reporte.pdf"
    pdf.output(nombre_archivo_temporal, 'F')
    
    print(f"Depuración: nombre_archivo_final inicial = {nombre_archivo_final}")
    try:
        if os.path.exists(nombre_archivo_final):
            if filecmp.cmp(nombre_archivo_temporal, nombre_archivo_final, shallow=False):
                os.remove(nombre_archivo_temporal)
                print("El archivo ya existe y su contenido es idéntico.")
                os.rename(nombre_archivo_temporal, nombre_archivo_final)
                print(f"Archivo guardado como: {nombre_archivo_final}")
            else:
                os.remove(nombre_archivo_final)  # Elimina el archivo existente
                os.rename(nombre_archivo_temporal, nombre_archivo_final)  # Renombra el archivo temporal
                print(f"Archivo sobrescrito como: {nombre_archivo_final}")
        else:
            os.rename(nombre_archivo_temporal, nombre_archivo_final)
            print(f"Archivo guardado como {nombre_archivo_final}")
        return True
    except PermissionError:
        os.remove(nombre_archivo_temporal)
        archivo_nombre = os.path.basename(nombre_archivo_final)
        messagebox.showerror("Error", f"El archivo {archivo_nombre} está abierto. Por favor, ciérralo e inténtalo de nuevo.", parent=parent)
        return False

from loans.backend.models import Cliente, Libro
class PDF(FPDF):
    def header(self):
        self.image(resource_path('assets_2/logo-biblioteca-red-2.png'), x=10, y=10, w=35, h=15)
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
        self.cell(w=0, h=10, txt=f"C.I.: {cliente.cedula}", border=1, align="L", ln=1, fill=0)
        self.cell(w=150, h=10, txt=f"Dirección: {cliente.direccion}", border=1, align="L", fill=0)
        self.cell(w=0, h=10, txt=f"Teléfono: {cliente.telefono}", border=1, ln=1, align="L", fill=0)

    def agregar_datos_usuario(self, usuario):
        self.set_font("Arial", "", 9)
        self.cell(w=0, h=10, txt="DATOS DEL ENCARGADO", border=1, ln=1, align="C", fill=0)
        self.cell(w=150, h=10, txt=f"Apellidos y Nombres: {usuario.apellido} {usuario.nombre}", border=1, align="L", fill=0)
        self.cell(w=0, h=10, txt=f"C.I.: {usuario.cedula}", border=1, align="L", ln=1, fill=0)
        self.cell(w=0, h=10, txt=f"Cargo: {usuario.cargo}", border=1, align="L", ln=1, fill=0)

    def agregar_datos_libro(self, libro, fecha_registro, fecha_limite):
        self.set_font("Arial", "", 9)
        self.cell(w=0, h=10, txt="DATOS DEL LIBRO", border=1, ln=1, align="C", fill=0)
        # Primera fila
        self.cell(w=24, h=10, txt=f"Sala: {libro.sala}", border=1, align="L", fill=0)
        self.cell(w=24, h=10, txt=f"Año: {libro.año}", border=1, align="L", fill=0)
        self.cell(w=48, h=10, txt=f"Cota: {libro.cota}", border=1, align="L", fill=0)
        self.cell(w=28, h=10, txt=f"Nro Volúmen: {libro.num_volumenes}", border=1, align="L", fill=0)
        self.cell(w=32, h=10, txt=f"Nro Edición: {libro.edicion}", border=1, align="L", fill=0)
        self.cell(w=0, h=10, txt=f"Nro Registro: {libro.numero_registro}", border=1, ln=1, align="L", fill=0)
        # Segunda fila
        self.cell(w=96, h=10, txt=f"Categoría: {libro.categoria}", border=1, align="L", fill=0)
        self.cell(w=0, h=10, txt=f"Asignatura: {libro.asignatura}", border=1, ln=1, align="L", fill=0)
        # Tercera Fila
        self.cell(w=96, h=10, txt=f"Título: {libro.titulo}", border=1, align="L", fill=0)
        self.cell(w=0, h=10, txt=f"Autor: {libro.autor}", border=1, ln=1, align="L", fill=0)
        # Cuarta Fila
        self.cell(w=96, h=10, txt=f"Editorial: {libro.editorial}", border=1, align="L", fill=0)
        self.cell(w=28, h=10, txt=f"Ejem. Total: {libro.total_ejemplares}", border=1, align="L", fill=0)
        self.cell(w=32, h=10, txt=f"Ejem. Prestados: {libro.ejemplares_prestados}", border=1, align="L", fill=0)
        self.cell(w=0, h=10, txt=f"Ejem. Disponibles: {libro.ejemplares_disponibles}", border=1, ln=1, align="L", fill=0)
        self.cell(w=96, h=10, txt=f"Fecha de Registro: {fecha_registro}", border=1, align="L", fill=0)
        self.cell(w=0, h=10, txt=f"Fecha Límite: {fecha_limite}", border=1, ln=1, align="L", fill=0)


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
    
    def agregar_datos_al_pdf(self, cliente, libro, fecha_registro, fecha_limite, usuario):
        self.agregar_datos_cliente(cliente)
        self.agregar_datos_libro(libro, fecha_registro, fecha_limite)
        self.agregar_datos_usuario(usuario)
        self.agregar_firmas()
    
def generate_pdf(clientes, books_data, prestamos_data, user_data, nombre_archivo_base, parent):
    pdf = PDF()
    pdf.alias_nb_pages()
    for index, libro in enumerate(books_data):
        pdf.add_page()
        prestamo = prestamos_data[index]
        cliente = clientes.get(prestamo["Cedula"])
        usuario = user_data[index]
        if cliente:
            # Añadir datos al PDF
            pdf.agregar_datos_al_pdf(cliente, libro, prestamo["fecha_r"], prestamo["fecha_en"], usuario)
    # Establecer metadatos del documento
    pdf.set_title("Reporte de Libro")
    pdf.set_author("Aplicación de la Biblioteca Pública de Rubio")
    pdf.set_creator("Aplicación de la Biblioteca Pública de Rubio")
    pdf.set_subject("Reporte de préstamo de libros")
    pdf.set_keywords("Reporte,Libro,Préstamo,Biblioteca")
    # Crear ventana de diálogo para guardar el archivo
    root = Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter
    carpeta_documentos = os.path.expanduser("~/Documents")
    nombre_archivo_final = asksaveasfilename(
        defaultextension=".pdf",
        initialfile=f"{nombre_archivo_base}.pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialdir=carpeta_documentos,
        parent=parent  # Pasar la ventana de generar reporte como parent
    )
    if nombre_archivo_final:
        # Asegurarse de que la extensión .pdf no se repita
        print(f"Nombre archivo final antes de ajuste: {nombre_archivo_final}")
        if not nombre_archivo_final.endswith(".pdf"):
            nombre_archivo_final += ".pdf"
        print(f"Nombre archivo final después de ajuste: {nombre_archivo_final}")
        success = verificar_y_guardar_pdf(pdf, nombre_archivo_final, parent)
        root.destroy()
        return success
    else:
        print("Guardado cancelado.")
        root.destroy()
        return False

def generate_report_by_day(clientes, books_data, prestamos_data, user_data, parent):
    fecha_actual = datetime.now().strftime("%d-%m-%Y")
    nombre_archivo_base = f"Reporte_Prestamos_{fecha_actual}"
    return generate_pdf(clientes, books_data, prestamos_data, user_data, nombre_archivo_base, parent)

def generate_report_by_month(clientes, books_data, prestamos_data, user_data, parent):
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    fecha_actual = datetime.now()
    mes_actual = meses[fecha_actual.month]
    año_actual = fecha_actual.year
    nombre_archivo_base = f"Reporte_Prestamos_{mes_actual}_{año_actual}"
    return generate_pdf(clientes, books_data, prestamos_data, user_data, nombre_archivo_base, parent)
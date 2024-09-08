from fpdf import FPDF
from datetime import datetime, timedelta

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
        self.image('logo-biblioteca-red-2.png', x=10, y=10, w=35, h=15)
        self.set_font('Arial', 'B', 20)
        self.cell(w=0, h=15, txt='Reporte de Préstamo de Libros', border=0, ln=1, align='C', fill=0)
        self.ln(5)

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 12)
        self.cell(w=0, h=10, txt='Pagina ' + str(self.page_no()) + '/{nb}', border=1, align='C', fill=0)

    def agregar_datos_cliente(self, cliente):
        self.set_font("Arial", "", 10)
        self.cell(w=0, h=15, txt="DATOS DEL CLIENTE", border=1, ln=1, align="C", fill=0)
        self.cell(w=45, h=15, txt="Nombre y Apellido", border=1, align="C", fill=0)
        self.cell(w=30, h=15, txt="Telefono", border=1, align="C", fill=0)
        self.cell(w=30, h=15, txt="Cedula", border=1, align="C", fill=0)
        self.multi_cell(w=0, h=15, txt="Dirección", border=1, align="C", fill=0)
        self.cell(w=45, h=15, txt=cliente.nombre, border=1, align="C", fill=0)
        self.cell(w=30, h=15, txt=cliente.telefono, border=1, align="C", fill=0)
        self.cell(w=30, h=15, txt=cliente.cedula, border=1, align="C", fill=0)
        self.multi_cell(w=0, h=15, txt=cliente.direccion, border=1, align="C", fill=0)

    def agregar_datos_libro(self, libro, fecha_registro, fecha_limite):
        self.ln(10)
        self.cell(w=0, h=15, txt="DATOS DEL LIBRO", border=1, ln=1, align="C", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Cota: {libro.cota}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Categoría: {libro.categoria}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Sala: {libro.sala}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Asignatura: {libro.asignatura}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Número de Registro: {libro.numero_registro}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Autor: {libro.autor}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Título: {libro.titulo}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Número de Volúmenes: {libro.num_volumenes}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Número de Ejemplares: {libro.num_ejemplares}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Edición: {libro.edicion}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Año: {libro.año}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Editorial: {libro.editorial}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Fecha de Registro: {fecha_registro}", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt=f"Fecha Límite: {fecha_limite}", border=1, align="L", fill=0)

# Instanciación de la clase PDF
pdf = PDF()
pdf.alias_nb_pages()
pdf.set_font('Arial', '', 12)

# Solicitar la cantidad de libros
cantidad_libros = int(input("Ingrese la cantidad de libros: "))

# Crear instancia del cliente
cliente = Cliente("Keyner Ivan Lizarazo Diaz", "04263757236", "30905297", "Las Margaritas Via Delicias")

# Crear instancias de libros ficticios
libros = [Libro("12345", "Ficción", "Sala A", "Literatura", "001", "Gabriel García Márquez", "Cien Años de Soledad", "1", "3", "Primera", "1967", "Editorial Sudamericana")]

# Fecha de registro y fecha límite
fecha_registro = datetime.now().strftime("%d/%m/%Y")
fecha_limite = (datetime.now() + timedelta(days=20)).strftime("%d/%m/%Y")

# Añadir página y datos del cliente
pdf.add_page()


# Añadir datos de los libros
for i in range(cantidad_libros):
    for libro in libros:
        pdf.agregar_datos_cliente(cliente)
        pdf.agregar_datos_libro(libro, fecha_registro, fecha_limite)
        if i < cantidad_libros - 1:
            pdf.add_page()

pdf.output('Prueba_3.pdf', 'F')

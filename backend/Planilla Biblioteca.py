from fpdf import FPDF
from datetime import datetime, timedelta



class PDF(FPDF):
    def header(self):
        self.image('logo-biblioteca-red-2.png', x=10, y=10, w=35, h=15)
        self.set_font('Arial', 'B', 20)
        self.cell(w=0, h=15, txt='Préstamo de Libro', border=0, ln=1, align='C', fill=0)
        self.ln(5)


    def agregar_datos_cliente(self):
        self.set_font("Arial", "", 9)
        self.cell(w=0, h=10, txt="DATOS DEL CLIENTE", border=1, ln=1, align="C", fill=0)
        self.cell(w=150, h=10, txt="Apellidos y Nombres:", border=1, align="L", fill=0)
        self.cell(w=0, h=10, txt="C.I.:", border=1, align="L",ln=1, fill=0)
        self.cell(w=150, h=10, txt="Dirección:", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt="Teléfono:", border=1, align="L", fill=0)
      
    def agregar_datos_libro(self):
        self.set_font("Arial", "", 9)
        self.cell(w=0, h=10, txt="DATOS DEL LIBRO", border=1, ln=1, align="C", fill=0)
        
        
        self.cell(w=48, h=10, txt="Sala:", border=1, align="L", fill=0)
        self.cell(w=48, h=10, txt="Cota:", border=1, align="L", fill=0)
        
        
        self.cell(w=30, h=10, txt="Nro Ejemplares:", border=1, align="L", fill=0)
        self.cell(w=34, h=10, txt="Nro Registro:", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt="Nro Volúmenes:", border=1, align="L", fill=0)
        self.cell(w=96, h=10, txt="Categoría:", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt="Asignatura:", border=1, align="L", fill=0)
        self.cell(w=96, h=10, txt="Título:", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt="Autor:", border=1, align="L", fill=0)
        
        
        self.cell(w=96, h=10, txt="Editorial:", border=1, align="L", fill=0)
        self.cell(w=48, h=10, txt="Año:", border=1, align="L", fill=0)
        
        self.multi_cell(w=0, h=10, txt="Edición:", border=1, align="L", fill=0)
        
        
        
        self.cell(w=96, h=10, txt="Fecha de Registro:", border=1, align="L", fill=0)
        self.multi_cell(w=0, h=10, txt="Fecha Límite:", border=1, align="L", fill=0)
        
        
        

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
        self.multi_cell(w=0, h=10, txt="", border=1, align="C", fill=0)
        

# Instanciación de la clase PDF
pdf = PDF()
pdf.alias_nb_pages()
pdf.set_font('Arial', '', 10)


# Agregar datos del cliente al PDF
pdf.add_page()
pdf.agregar_datos_cliente()
pdf.agregar_datos_libro()
pdf.agregar_firmas()

# Guardar el PDF
pdf.output('prestamo_libros.pdf')

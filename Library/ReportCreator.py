from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from Library.librerias import recoger_sesion,search_favorite_pk,search_pk_fav,search_all_pk

def main():
    def cadena_a_lista(cadena):
        # Utiliza el método split() para dividir la cadena en una lista
        if cadena:
            return cadena.split(',')
        else:
            pass
    
    username= recoger_sesion()
    pkfav = search_favorite_pk(username)
    value = cadena_a_lista(pkfav[0])
    search = search_pk_fav(value)
    all = search_all_pk()
    # Crear un archivo PDF
    doc = SimpleDocTemplate("Personal_Pokedex.pdf", pagesize=letter)

    # Estilos de texto
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle("Titulo", parent=styles["Title"])
    titulo_style.alignment = 1  # Centrado

    # Contenido del PDF
    contenido = []
    contenido.append(Paragraph("Personal Pokédex System 1", titulo_style))
    contenido.append(Spacer(1, 20))  # Dos saltos de línea
    contenido.append(Paragraph(f"Pokémon favoritos de {username}", styles["Heading1"]))

    # Crear tabla con los campos ID, Nombre, Tipo y Descripción
    tabla_datos = [["ID", "Nombre", "Tipo", "Descripción"]]
    for pokemon in all:
        tabla_datos.append((pokemon[1], pokemon[2], pokemon[2], pokemon[6]))

    tabla = Table(tabla_datos[0], colWidths=[40, 100, 80, 200])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), "#CCCCCC"),  # Fila de encabezado
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Centrar contenido
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Centrar verticalmente
        ("INNERGRID", (0, 0), (-1, -1), 0.25, "#000000"),  # Líneas internas
        ("BOX", (0, 0), (-1, -1), 0.5, "#000000"),  # Borde exterior
    ]))

    contenido.append(tabla)

    # Construir el PDF
    doc.build(contenido)
    print("PDF generado correctamente.")

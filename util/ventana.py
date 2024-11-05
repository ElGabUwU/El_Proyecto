from PIL import ImageTk, Image

def leer_imagen(path, size):
    try:
        
        imagen = Image.open(path)
        imagen = imagen.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagen)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta {path}")
        return None

def centrar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_largo = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (aplicacion_ancho / 2))
    y = int((pantalla_largo / 2) - (aplicacion_largo / 2))
    ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")

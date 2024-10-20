from db.conexion import establecer_conexion
from loans.backend.db_loans import *
from tkinter import messagebox
import tkinter as tk
from datetime import datetime, timedelta
import random
import string


def clear_entries_list(self):
        self.id_cliente.delete(0, tk.END)
        #self.input_cantidad.delete(0, tk.END)
        # self.fecha_limite_entry.delete(0, tk.END)
    
def validate_entries(instance, event=None):
        # Comprobar si todos los campos están llenos
        if (instance.id_cliente.get()):
            instance.boton_R.place(x=40.0, y=450.0, width=130.0, height=40.0)  # Mostrar el botón
        else:
            instance.boton_R.place_forget()  # Ocultar el botón si algún campo está vacío

def generate_alphanumeric_id(length=6):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))
    
def format_date(date_str):
        try:
            # Convertir la fecha del formato DD/MM/YYYY al formato YYYY-MM-DD
            formatted_date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            return formatted_date
        except ValueError as e:
            print(f"Error al formatear la fecha: {e}")
            return None

def generate_id_libro_prestamo(self):
        while True:
            new_id = random.randint(1000, 9999)
            if not libro_prestamo_exists(new_id):
                return new_id

def verificar_eliminar(self):
        if self.parent.id_rol == 1:
            print("Sin permisos suficientes para eliminar!")
            messagebox.showinfo("AVISO", "Sin permisos suficientes para eliminar!")
        
        else:
            delete_selected_prestamo(self)

def libro_prestamo_exists(new_id):
    try:
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:
            cursor = mariadb_conexion.cursor()
            # Verificar si el ID_Libro_Prestamo existe en la tabla libros_prestamo
            cursor.execute("SELECT 1 FROM libros_prestamo WHERE ID_Libro_Prestamo = %s", (new_id,))
            result = cursor.fetchone()
            return result is not None
    except mariadb.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return False
    finally:
        if mariadb_conexion:
            cursor.close()
            mariadb_conexion.close()
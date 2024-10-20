from db.conexion import establecer_conexion
from loans.backend.db_loans import *
import tkinter as tk
from tkinter import messagebox
import random
import string

#Validación de cédula en Tabla Clientes
def cedula_existe(self,cedula):
        mariadb_conexion = establecer_conexion()
        if mariadb_conexion:#.is_connected():
            cursor = mariadb_conexion.cursor()
            query = "SELECT COUNT(*) FROM cliente WHERE Cedula_Cliente = %s"
            cursor.execute(query, (cedula,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] > 0
        
#Generador de ID Préstamo Alfanumérica       
def generate_alphanumeric_id(self, length=8):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=length))

# clients_validations.py
def validate_entries(instance, event=None):
    # Comprobar si todos los campos están llenos
    if (instance.input_cedula.get() and instance.input_nombre.get() and instance.input_apellido.get() and
            instance.input_telefono.get() and instance.input_direccion.get()):
        instance.boton_R.place(x=553.0, y=300.0, width=130.0, height=40.0)  # Mostrar el botón
    else:
        instance.boton_R.place_forget()  # Ocultar el botón si algún campo está vacío

#Verificación de Rango Usuario
def verificar_eliminar(self):
        if self.parent.id_rol == 1:
            print("Sin permisos suficientes para eliminar!")
            messagebox.showinfo("AVISO", "Sin permisos suficientes para eliminar!")
        
        else:
            delete_client_loans(self)
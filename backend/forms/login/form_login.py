import tkinter as tk
from tkinter import ttk,messagebox
from tkinter.font import BOLD
from util import ventana
from forms.login.from_login_designer import FormLoginDesigner
from forms.master.form_master import MasterPanel
from db.conexion import get_user_by_username, is_user, is_password 
from util.validations import validate_password,validate_username


class FormLogin(FormLoginDesigner):
    
    def verificar(self, event=None):
        user_name = self.user.get()
        password = self.password.get()

        # Validar nombre de usuario
        is_valid_username, username_message = validate_username(user_name)
        if not is_valid_username:
            messagebox.showerror(message=username_message, title="Error")
            self.user.delete(0, tk.END)
            return

        # Obtener usuario de la base de datos
        user_db = get_user_by_username(user_name)
        if not is_user(user_db):
            messagebox.showerror(message="Usuario no encontrado.", title="Error")
            self.user.delete(0, tk.END)
            return  # Detener la ejecución si el usuario no es encontrado

        # Si el nombre de usuario es válido y existe, mover el foco al campo de contraseña
        self.password.focus()

        # Validar contraseña solo si se ha ingresado
        if password:
            is_valid_password, password_message = validate_password(password)
            if not is_valid_password:
                messagebox.showerror(message=password_message, title="Error")
                self.password.delete(0, tk.END)
                return

            # Verificar la contraseña
            if not is_password(password, user_db):
                messagebox.showerror(message="Contraseña incorrecta.", title="Error")
                self.password.delete(0, tk.END)
            else:
                self.ventana.destroy()
                MasterPanel()

    def on_enter(self, event, next_widget):
        next_widget.focus()

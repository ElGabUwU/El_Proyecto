import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.utilidades as utl
from users.frontend.from_login_designer import FormLoginDesigner
from users.frontend.form_master import MasterPanel
from users.backend.db_users import get_user_by_username, is_user, is_password , iniciar_sesion, Usuario
from validations.user_validations import validate_password, validate_username, validar_campos, limit_length, allow_permitted_characters
from MainAppConector import start_starter 

class FormLogin(FormLoginDesigner):
    def show(self):
        self.ventana.mainloop()
    
    def verificar(self, event=None):
        user_name = self.user.get()
        password = self.password.get()
        
        # Validar campos y obtener mensajes de error
        error_messages = validar_campos(user_name, password, tipo_validacion="login")
        
        # Verificar si el nombre de usuario es válido y si el usuario existe
        if not error_messages:
                    user_db = get_user_by_username(user_name)
                    is_valid_username = user_db
                    if not is_valid_username:
                        error_messages.append("Usuario no encontrado. Por favor, verifica tu nombre de usuario.")
        
        # Mostrar todos los mensajes de error acumulados en viñetas
        if error_messages:
            messagebox.showerror(
                message="Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"- {msg}" for msg in error_messages),
                title="Error"
            )
            # Vaciar ambos campos si hay errores relacionados con el nombre de usuario o si el usuario no existe
            for message in error_messages:
                if "nombre de usuario" in message or "Usuario no encontrado" in message:
                    self.user.delete(0, tk.END)
                    self.password.delete(0, tk.END)
                elif "contraseña" in message or "Contraseña incorrecta." in message:
                    self.password.delete(0, tk.END)
        else:
            # Validar la contraseña solo si el nombre de usuario es válido
            if not is_user(user_db):
                error_messages.append("Usuario no encontrado. Por favor, verifica tu nombre de usuario.")
            else:
                is_valid, message = validate_password(password)
                if not is_valid:
                    error_messages.append(message)
                elif not is_password(password, user_db):
                    error_messages.append("Contraseña incorrecta.")
            
            # Mostrar mensajes de error relacionados con la contraseña, si los hay
            if error_messages:
                messagebox.showerror(
                    message="Por favor, corrija los siguientes errores:\n\n" + "\n".join(f"- {msg}" for msg in error_messages),
                    title="Error"
                )
                self.password.delete(0, tk.END)
            else:
                # Si todas las validaciones pasan, destruir la ventana y mostrar el panel principal
                usuario = iniciar_sesion(user_name, password)
                self.ventana.destroy()
                self.mostrar_master_panel()

    def mostrar_master_panel(self):
        # Crear una instancia de MasterPanel y pasar el callback iniciar_starter
        master_panel = MasterPanel(on_close_callback=self.iniciar_starter)
        
        self.ventana.after(1500, master_panel.on_close)  # Esperar 1500 milisegundos antes de iniciar Starter
        master_panel.show()

    def iniciar_starter(self):
        start_starter()

    def on_enter(self, event, next_widget):
        next_widget.focus()
    
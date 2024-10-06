import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.ventana as utl
from forms.login.from_login_designer import FormLoginDesigner
from forms.master.form_master import MasterPanel
from db.conexion import get_user_by_username, is_user, is_password 
from util.validations import validate_password, validate_username
from MainAppConector import start_starter 

class FormLogin(FormLoginDesigner):
    def show(self):
        self.ventana.mainloop()
    
    def verificar(self, event=None):
        user_name = self.user.get()
        password = self.password.get()

        # Lista para acumular mensajes de error
        error_messages = []
        error_counter = 1  # Contador para numerar los errores

        # Validar que ambos campos no estén vacíos
        if not user_name and not password:
            error_messages.append(f"{error_counter}. El campo de nombre de usuario es obligatorio.")
            error_counter += 1
            error_messages.append(f"{error_counter}. El campo de contraseña es obligatorio.")
            error_counter += 1
        else:
            # Validar que el campo de nombre de usuario no esté vacío
            if not user_name:
                error_messages.append(f"{error_counter}. El campo de nombre de usuario es obligatorio.")
                error_counter += 1
                self.user.delete(0, tk.END)
                self.password.delete(0, tk.END)
                
            else:
                # Validar nombre de usuario solo si no está vacío
                is_valid_username, username_message = validate_username(user_name)
                if not is_valid_username:
                    error_messages.append(f"{error_counter}. {username_message}")
                    error_counter += 1
                    self.user.delete(0, tk.END)
                    self.password.delete(0, tk.END)
                else:
                    # Obtener usuario de la base de datos solo si el nombre de usuario es válido
                    user_db = get_user_by_username(user_name)
                    if not is_user(user_db):
                        error_messages.append(f"{error_counter}. Usuario no encontrado. Por favor, verifica tu nombre de usuario.")
                        error_counter += 1
                        self.user.delete(0, tk.END)
                        self.password.delete(0, tk.END)
                    else:
                        # Validar que el campo de contraseña no esté vacío solo si el nombre de usuario es válido y existe
                        if not password:
                            error_messages.append(f"{error_counter}. El campo de contraseña es obligatorio.")
                            error_counter += 1
                        else:
                            # Validar contraseña solo si no está vacía y el usuario existe
                            is_valid_password, password_message = validate_password(password)
                            if not is_valid_password:
                                error_messages.append(f"{error_counter}. {password_message}")
                                error_counter += 1
                                self.password.delete(0, tk.END)
                            elif not is_password(password, user_db):
                                error_messages.append(f"{error_counter}. Contraseña incorrecta.")
                                error_counter += 1
                                self.password.delete(0, tk.END)

        # Mostrar todos los mensajes de error acumulados en viñetas
        if error_messages:
            messagebox.showerror(message="Por favor, corrija los siguientes errores:\n" + "\n".join(f"- {msg}" for msg in error_messages), title="Error")
            return
        # Si todas las validaciones pasan, destruir la ventana y mostrar el panel principal
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

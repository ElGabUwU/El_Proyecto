from db.conexion import establecer_conexion
from MainAppConector import app_state,Usuario,AppState

def get_user_by_username(username):
    conexion = establecer_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            consulta = """SELECT * FROM usuarios WHERE Nombre_Usuario = %s"""
            cursor.execute(consulta, (username,))
            user = cursor.fetchone()
            return user

        except Error as e:
            print(f"Error al realizar la consulta: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()

# #Esta clase obtiene los valores del usuario, implmentar a futuro en mi perfil
# class Usuario:
#     def __init__(self, user_data):
#         self.id_usuario = user_data[0]
#         self.id_cargo = user_data[1]
#         self.id_rol = user_data[2]
#         self.nombre = user_data[3]
#         self.apellido = user_data[4]
#         self.cedula = user_data[5]
#         self.nombre_usuario = user_data[6]
#         self.clave = user_data[7]

#     def mostrar_informacion(self):
#         print(f"ID Usuario: {self.id_usuario}")
#         print(f"ID Cargo: {self.id_cargo}")
#         print(f"ID Rol: {self.id_rol}")
#         print(f"Nombre: {self.nombre}")
#         print(f"Apellido: {self.apellido}")
#         print(f"Cédula: {self.cedula}")
#         print(f"Nombre de Usuario: {self.nombre_usuario}")

# def iniciar_sesion(username, password):
#     # Obtener los datos del usuario desde la base de datos
#     user_data = get_user_by_username(username)
    
#     # Verificar si los datos del usuario existen y si la contraseña es correcta
#     if user_data and is_password(password, user_data):
#         # Crear una instancia de Usuario con los datos obtenidos
#         usuario = Usuario(user_data)
#         print("Inicio de sesión exitoso")
        
#         # Mostrar la información del usuario (opcional)
#         usuario.mostrar_informacion()
        
#         # Guardar el usuario en el estado de la aplicación
#         app_state.usuario = usuario
#         return usuario
#     else:
#         # Mensaje de error si las credenciales son incorrectas
#         print("Nombre de usuario o contraseña incorrectos")
#         return None


def is_user(user):#Validacion de usuario
    if user is None:
        return False
    return True

def is_password(password, user):
    if password == user[7]:  # Asumiendo que la contraseña está en la octava columna
        return True
    else:
        return False
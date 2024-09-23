#Si no lo tienen instalar: pip install mysql-connector-python
import mysql.connector 


def tabla_representantes(cursor):

    cursor.execute("USE escuela_danza")

    tabla_sql = '''
                CREATE TABLE IF NOT EXISTS representantes (
                cedula INT PRIMARY KEY,
                nombres VARCHAR(30),
                apellidos VARCHAR(30),
                telefono VARCHAR(10),
                direccion VARCHAR (30)
                        )
                    '''
    cursor.execute(tabla_sql)

def tabla_estudiante(cursor):

    cursor.execute("USE escuela_danza")

    tabla_sql = '''
                CREATE TABLE IF NOT EXISTS estudiante (
                id INT PRIMARY KEY AUTO_INCREMENT,
                1er_nombre VARCHAR(30),
                2do_nombre VARCHAR(30),
                1er_apellido VARCHAR(30),
                2do_apellido VARCHAR(30),
                edad INT,
                cedula VARCHAR (9),
                cedula_representante INT,
				FOREIGN KEY (cedula_representante) REFERENCES representantes (cedula));
                    '''
    
    cursor.execute(tabla_sql)

def Conexionbd():

    # Credenciales de la conexion, lo unico que tienen que cambiar es el host, el user y la password a las credenciales que tengan
    # en mariadb u otros gestores, recordar que esta bd es de mysql
    #Las tablas se crean automaticamente a la hora de ingresar la informacion en ambos casos tanto de estudiantes 
    #como representantes, mirar los archivos agregar en la carpeta funciones

    host = "localhost"
    user = "root"
    password = "mortadela"
    database = "escuela_danza"
    charset='utf8mb4'
    collation='utf8mb4_general_ci'

    try:
        # Estableciendo conexion
        Conexion = mysql.connector.connect(
            host="localhost",
            user="Root",
            password="2525",
            database="basedatosbiblioteca",
            charset=charset,
            collation=collation,
            port= "3306"
            
        )

        #este print pueden borrarlo si les apetece
        

        return Conexion

        
    # Aqui recoge el error y lo retorna como err y detecta si no se puede establecer una conexion
    # con la bd puesta en la credencial si no existe la crea

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            aux = mysql.connector.connect(
                host="localhost",
                user="Root",
                password="2525",
                database="basedatosbiblioteca",
                charset=charset,
                collation=collation,
                port= "3306"
            )

            cur = aux.cursor()
            cur.execute(f"CREATE DATABASE {database}")
            print(f"Base de datos '{database}' creada correctamente.")

            

            Conexion = mysql.connector.connect(
            host="localhost",
            user="Root",
            password="2525",
            database="basedatosbiblioteca",
            charset=charset,
            collation=collation,
            port= "3306"
        )
            tabla_representantes(cur)
            tabla_estudiante(cur)

            return Conexion

        else:
            print("Error al conectar a la base de datos:", err)

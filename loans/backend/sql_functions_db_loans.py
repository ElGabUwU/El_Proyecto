import mariadb

#FUNCIONES MODULARIZADA PARA UPDATED_ALL_TABLES
def iniciar_transaccion(conexion):
    conexion.start_transaction()
    print("1) Transacción iniciada.")

def verificar_e_insertar_libro_prestamo(cursor, ID_Libro_Prestamo, ID_Prestamo, ID_Libro):
    if not check_libro_prestamo_exists(cursor, ID_Libro_Prestamo):
        insert_libro_prestamo(cursor, ID_Libro_Prestamo, ID_Prestamo, ID_Libro)
        print(f"2) ID_Libro_Prestamo {ID_Libro_Prestamo} no existía y fue insertado.")


#Función relacionada con verificar_e_insertar_libro_prestamo
def check_libro_prestamo_exists(cursor, ID_Libro_Prestamo):
    try:
        cursor.execute("SELECT 1 FROM libros_prestamo WHERE ID_Libro_Prestamo = %s", (ID_Libro_Prestamo,))
        result = cursor.fetchone() is not None
        print(f"1.2) check_libro_prestamo_exists: {result}")
        return result
    except mariadb.Error as e:
        print(f"Error en check_libro_prestamo_exists: {e}")
        return False
    
def insert_libro_prestamo(cursor, ID_Libro_Prestamo, ID_Prestamo, ID_Libro):
    try:
        query = """
        INSERT INTO libros_prestamo (ID_Libro_Prestamo, ID_Prestamo, ID_Libro)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (ID_Libro_Prestamo, ID_Prestamo, ID_Libro))
        print(f"1.3) insert_libro_prestamo ejecutado (t. libros prestamo): {ID_Libro_Prestamo}, {ID_Prestamo}, {ID_Libro}")
    except mariadb.Error as e:
        print(f"Error en insert_libro_prestamo: {e}")


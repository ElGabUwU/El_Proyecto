# def register_client(self):
#     fecha_registrar = self.format_date(self.fecha_registrar.get())
#     fecha_limite = self.format_date(self.fecha_limite.get())
#     Cantidad = int(self.input_cantidad.get())
#     ID_Prestamo = self.generate_alphanumeric_id()
#     if fecha_registrar and fecha_limite:
#         if create_loan(ID_Prestamo, fecha_registrar, fecha_limite):
            # if ID_Cliente:
#             selected_items = self.clients_table_list_loans.selection()
#             if len(selected_items) > 5:
#                 messagebox.showinfo("Error", "Solo puedes seleccionar un máximo de 5 libros.")
#                 return
#             selected_books = []
#             for item in selected_items:
#                 book_info = self.clients_table_list_loans.item(item, "values")
#                 ID_Libro = book_info[0]
#                 selected_books.append(ID_Libro)
#                 ID_Libro_Prestamo = self.generate_id_libro_prestamo()  # Generar ID_Libro_Prestamo
#                 save_books_to_db(self, selected_books, ID_Prestamo, Cantidad)

#                 if not self.libro_prestamo_exists(ID_Libro_Prestamo):
#                     if update_prestamo_and_libro(ID_Prestamo, ID_Cliente, ID_Libro, ID_Libro_Prestamo, Cantidad):
#                                 messagebox.showinfo("Éxito", f"""
# Registro éxitoso del cliente y del libro. 
# ID Préstamo: {ID_Prestamo}
# Libros seleccionados: {selected_books}
#                     """)
#                                 self.clear_entries_register_loans()
                        #     else:
                        #         messagebox.showinfo("Error", "No se pudo registrar el libro en el préstamo.")
                        # else:
                        #     messagebox.showinfo("Error", "No se pudo actualizar el préstamo con el cliente.")
                    # else:
                    #     messagebox.showinfo("Registro fallido", "Cliente no pudo ser registrado.")
            # else:
            #     messagebox.showinfo("Error", "No se pudo crear el préstamo.")
        # else:
        #     messagebox.showinfo("Error", "Formato de fecha incorrecto.")

        
    # def format_date(self, date_str):
    #     try:
    #         # Convertir la fecha del formato DD/MM/YYYY al formato YYYY-MM-DD
    #         formatted_date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    #         return formatted_date
    #     except ValueError as e:
    #         print(f"Error al formatear la fecha: {e}")
    #         return None

    # def generate_id_libro_prestamo(self):
    #     while True:
    #         new_id = random.randint(1000, 9999)
    #         if not self.libro_prestamo_exists(new_id):
    #             return new_id

    # def libro_prestamo_exists(self, ID_Libro_Prestamo):
    #     try:
    #         mariadb_conexion = establecer_conexion()
    #         if mariadb_conexion:#.is_connected():
    #             cursor = mariadb_conexion.cursor()
    #             sql_check_query = "SELECT 1 FROM libros_prestamo WHERE ID_Libro_Prestamo = %s"
    #             cursor.execute(sql_check_query, (ID_Libro_Prestamo,))
    #             result = cursor.fetchone()
    #             return result is not None

        # except Error as e:
        #     print(f"Error al conectar a la base de datos: {e}")
        #     return False

        # finally:
        #     if mariadb_conexion:#.is_connected():
        #         cursor.close()
        #         mariadb_conexion.close()
from tkinter import messagebox

def filter_books(self):
    id_prestamo = self.id_prestamos_entry.get().strip()
    id_cliente = self.id_cliente_entry.get().strip()
    id_libro_cliente = self.id_libro_cliente_entry.get().strip()

    # Validar que los campos no estén vacíos
    if not id_prestamo:
        messagebox.showerror("Error", "Ingrese un código de préstamo válido.")
        return False
    if not id_cliente:
        messagebox.showerror("Error", "Ingrese una ID de cliente válida.")
        return False
    if not id_libro_cliente:
        messagebox.showerror("Error", "Ingrese una ID de libro válida.")
        return False

    # Validar que los campos contengan valores válidos (por ejemplo, solo números)
    if not id_prestamo.isdigit():
        messagebox.showerror("Error", "El código de préstamo debe ser un número.")
        return False
    if not id_cliente.isdigit():
        messagebox.showerror("Error", "La ID de cliente debe ser un número.")
        return False
    if not id_libro_cliente.isdigit():
        messagebox.showerror("Error", "La ID de libro debe ser un número.")
        return False

    found_match = False

    for row in self.prestamo_table.get_children():
        values = self.prestamo_table.item(row, "values")
        # Convertir los valores a enteros si es posible, de lo contrario mantenerlos como cadenas
        converted_values = []
        for value in values:
            try:
                converted_values.append(int(value))
            except ValueError as e:
                converted_values.append(value)
                messagebox.showinfo("Error", f"Se ha producido el siguiente error: {e}.")
        values = [str(value) for value in values]
        if (id_prestamo in values[0].lower() and values[0].upper() and
            id_cliente in values[2].lower() and values[1].upper() and
            id_libro_cliente in values[4].lower() and values[3].upper()):
            self.prestamo_table.item(row, tags='match')
            messagebox.showinfo("Éxito", "Se encontraron los siguientes resultados en pantalla")
            found_match = True
        else:
            self.prestamo_table.item(row, tags='nomatch')
            messagebox.showinfo("Fallido", "No se encontraron resultados en pantalla")

    self.prestamo_table.tag_configure('match', background='green')
    self.prestamo_table.tag_configure('nomatch', background='gray')

    return found_match
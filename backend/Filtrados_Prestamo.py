from tkinter import messagebox

def filter_books_one(self):
    id_cliente = self.id_cliente_entry.get().lower() or self.id_cliente_entry.get().upper()
    match_count = 0

    for row in self.prestamo_table.get_children():
        values = self.prestamo_table.item(row, "values")
        # Convertir los valores a enteros si es posible, de lo contrario mantenerlos como cadenas
        converted_values = []
        for value in values:
            try:
                converted_values.append(int(value))
            except ValueError:
                converted_values.append(value)
        values = [str(value) for value in values]
        if id_cliente in values[1].lower() or id_cliente in values[1].upper():
            self.prestamo_table.item(row, tags='match')
            match_count += 1
        else:
            self.prestamo_table.item(row, tags='nomatch')

    self.prestamo_table.tag_configure('match', background='green')
    self.prestamo_table.tag_configure('nomatch', background='gray')

    if match_count == 0:
        messagebox.showerror("Error", "No se encontraron resultados.")
    else:
        messagebox.showinfo("Resultados", f"Se encontraron {match_count} resultados.")

def filter_books_two(self):
    id_prestamo = self.id_prestamo_entry.get().lower() or self.id_prestamo_entry.get().upper()
    match_count = 0

    for row in self.prestamo_table.get_children():
        values = self.prestamo_table.item(row, "values")
        # Convertir los valores a enteros si es posible, de lo contrario mantenerlos como cadenas
        converted_values = []
        for value in values:
            try:
                converted_values.append(int(value))
            except ValueError:
                converted_values.append(value)
        values = [str(value) for value in values]
        if id_prestamo in values[3].lower() or id_prestamo in values[3].upper():
            self.prestamo_table.item(row, tags='match')
            match_count += 1
        else:
            self.prestamo_table.item(row, tags='nomatch')

    self.prestamo_table.tag_configure('match', background='green')
    self.prestamo_table.tag_configure('nomatch', background='gray')

    if match_count == 0:
        messagebox.showerror("Error", "No se encontraron resultados.")
    else:
        messagebox.showinfo("Resultados", f"Se encontraron {match_count} resultados.")

def filter_books_three(self):
    id_prestamo = self.id_prestamo_entry.get().lower() or self.id_prestamo_entry.get().upper()
    id_cliente = self.id_cliente_entry.get().lower() or self.id_cliente_entry.get().upper()
    id_libro_cliente = self.id_libro_cliente_entry.get().lower() or self.id_libro_cliente_entry.get().upper()
    match_count = 0

    for row in self.prestamo_table.get_children():
        values = self.prestamo_table.item(row, "values")
        # Convertir los valores a enteros si es posible, de lo contrario mantenerlos como cadenas
        converted_values = []
        for value in values:
            try:
                converted_values.append(int(value))
            except ValueError:
                converted_values.append(value)
        values = [str(value) for value in values]
        if (id_prestamo in values[0].lower() or id_prestamo in values[0].upper()) and \
           (id_cliente in values[1].lower() or id_cliente in values[1].upper()) and \
           (id_libro_cliente in values[3].lower() or id_libro_cliente in values[3].upper()):
            self.prestamo_table.item(row, tags='match')
            match_count += 1
        else:
            self.prestamo_table.item(row, tags='nomatch')

    self.prestamo_table.tag_configure('match', background='green')
    self.prestamo_table.tag_configure('nomatch', background='gray')

    if match_count == 0:
        messagebox.showerror("Error", "No se encontraron resultados.")
    else:
        messagebox.showinfo("Resultados", f"Se encontraron {match_count} resultados.")
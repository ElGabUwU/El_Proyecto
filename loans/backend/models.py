# models.py

class Cliente:
    def __init__(self, nombre,apellido, telefono, cedula, direccion):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.cedula = cedula
        self.direccion = direccion

class Encargado:
    def __init__(self, nombre,apellido, cargo, cedula):
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo
        self.cedula = cedula

class Libro:
    def __init__(self, cota, categoria, sala, asignatura, numero_registro, autor, titulo, num_volumen, total_ejemplares, ejemplares_disponibles, ejemplares_prestados, edicion, año, editorial):
        self.cota = cota
        self.categoria = categoria
        self.sala = sala
        self.asignatura = asignatura
        self.autor = autor
        self.titulo = titulo
        self.numero_registro = numero_registro
        self.num_volumenes = num_volumen 
        self.edicion = edicion
        self.total_ejemplares = total_ejemplares
        self.ejemplares_prestados = ejemplares_prestados
        self.ejemplares_disponibles = ejemplares_disponibles
        self.año = año
        self.editorial = editorial

    def __str__(self):
        return f"Libro(titulo={self.titulo}, autor={self.autor}, numero_registro={self.numero_registro}, cota={self.cota}, categoria={self.categoria}, sala={self.sala}, asignatura={self.asignatura}, num_volumenes={self.num_volumenes}, num_ejemplares={self.num_ejemplares}, edicion={self.edicion}, año={self.año}, editorial={self.editorial})"

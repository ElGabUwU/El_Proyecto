# models.py

class Cliente:
    def __init__(self, nombre,apellido, telefono, cedula, direccion):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.cedula = cedula
        self.direccion = direccion

class Libro:
    def __init__(self, cota, categoria, sala, asignatura, numero_registro, autor, titulo, num_volumenes, num_ejemplares, edicion, año, editorial):
        self.cota = cota
        self.categoria = categoria
        self.sala = sala
        self.asignatura = asignatura
        self.numero_registro = numero_registro
        self.autor = autor
        self.titulo = titulo
        self.num_volumenes = num_volumenes
        self.num_ejemplares = num_ejemplares
        self.edicion = edicion
        self.año = año
        self.editorial = editorial

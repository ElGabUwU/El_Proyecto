import sqlite3

# Conectar a la base de datos
def connect():
    conn = sqlite3.connect('Library/pokimons.db')
    return conn

# Crear un nuevo Pokémon
def create_pokemon(pkNombre, pkTipo, pkPeso, pkAltura, pkSexo, pkDesc):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pokemons (pkNombre, pkTipo, pkPeso, pkAltura, pkSexo, pkDesc)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (pkNombre, pkTipo, pkPeso, pkAltura, pkSexo, pkDesc))
    conn.commit()
    conn.close()
    return True

# Leer todos los Pokémon
def read_pokemons():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT usuarioNombre, usuarioPsw FROM usuarios WHERE usuarioNombre == ? and usuarioPsw == ?
        ''')
    pokemons = cursor.fetchall()
    conn.close()
    return pokemons

# Actualizar un Pokémon
def update_pokemon(pkNombre, pkTipo, pkPeso, pkAltura, pkSexo, pkDesc):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT pkNombre FROM pokemons WHERE pknombre = ?", (pkNombre,))
    busqueda=()
    busqueda=cursor.fetchone()
    print(busqueda)
    if busqueda is None:
        conn.close()
        return False
    else:
        cursor.execute('''
            UPDATE pokemons
            SET pkNombre = ?, pkTipo = ?, pkPeso = ?, pkAltura = ?, pkSexo = ?, pkDesc = ?
            WHERE pkNombre = ?
        ''', (pkNombre, pkTipo, pkPeso, pkAltura, pkSexo, pkDesc, pkNombre))
        conn.commit()
        conn.close()
        return True

# Eliminar un Pokémon
def delete_pokemon(pkId):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pokemons WHERE pkNombre = ?', (pkId,))
    conn.commit()
    conn.close()
    return True
import sqlite3

class CrearTablasDB:
    def __init__(self, ruta_db):
        super().__init__
        self.ruta_db = ruta_db
        
        self.CrearTablaJugador()
        self.CrearTablaPuntaje()

    def CrearTablaJugador(self):
        conexion = sqlite3.connect(self.ruta_db)
        cursor = conexion.cursor()
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS jugadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    ''')
        
        conexion.commit()
        conexion.close()

    def CrearTablaPuntaje(self):
        conexion = sqlite3.connect(self.ruta_db)
        cursor = conexion.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS puntaje(id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        dificultad TEXT,
        duracion_total INTEGER,
        puntaje INTEGER,
        fecha_partida DATE,
        FOREIGN KEY (nombre) REFERENCES jugadores(NamePlayer)
    )
    """)
        
        conexion.commit()
        conexion.close()
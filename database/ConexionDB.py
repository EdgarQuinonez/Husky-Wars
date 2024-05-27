import sqlite3

class ConexionBD:
    def __init__(self):
        self.create_tables(self)
        

    @staticmethod
    def connect_db():
        return sqlite3.connect("database/sqlite.db")
    
    @staticmethod
    def create_tables(self):
        conexion = self.connect_db()
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                puntaje INTEGER,
                duracion_total INTEGER
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS puntaje (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                dificultad TEXT,
                duracion_total INTEGER,
                puntaje INTEGER,
                fecha_partida DATE,
                FOREIGN KEY (nombre) REFERENCES jugadores(nombre)
            );
        """)

        conexion.commit()
        conexion.close()

    @staticmethod
    def add_game_record(self, nombre, puntaje, duracion_total):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO jugadores (nombre, puntaje, duracion_total)
        VALUES (?, ?, ?)
        ''', (nombre, puntaje, duracion_total))
        conn.commit()
        conn.close()

    @staticmethod
    def get_top_50_scores_with_duration_60(self):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT nombre, puntaje, duracion_total
        FROM jugadores
        WHERE duracion_total = 60
        ORDER BY puntaje DESC
        LIMIT 50
        ''')
        results = cursor.fetchall()
        connection.close()
        
        return results

    @staticmethod
    def get_top_50_scores(self):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT nombre, puntaje, duracion_total
        FROM jugadores
        ORDER BY puntaje DESC
        LIMIT 50
        ''')
        results = cursor.fetchall()
        connection.close()
        
        return results
    

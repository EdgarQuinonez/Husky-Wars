import sqlite3

class ConexionBD:
    def __init__(self):
        self.create_tables()
        
    @staticmethod
    def connect_db():
        return sqlite3.connect("database/sqlite.db")
    
    
    def create_tables(self):
        conexion = self.connect_db()
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS puntaje (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                dificultad INTEGER,
                duracion_total INTEGER,
                puntaje INTEGER,
                fecha_partida DATE                
            );
        ''')

        conexion.commit()
        conexion.close()
       
    def get_player_by_name(self, nombre):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT id, nombre
        FROM jugadores
        WHERE nombre = ?
        ''', (nombre,))
        player = cursor.fetchone()
        conn.close()
        return player
    
    def insert_player(self, nombre):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO jugadores (nombre)
        VALUES (?)
        ''', (nombre,))
        conn.commit()
        conn.close()
        
    def add_match_score(self, nombre, dificultad, duracion_total, puntaje, fecha_partida):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO puntaje (nombre, dificultad, duracion_total, puntaje, fecha_partida)
        VALUES (?, ?, ?, ?, ?)
        ''', (nombre, dificultad, duracion_total, puntaje, fecha_partida))
        conn.commit()
        conn.close()

    
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

    
    def get_top_10_scores(self):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT nombre, puntaje, duracion_total
        FROM puntaje
        ORDER BY puntaje DESC
        LIMIT 10
        ''')
        results = cursor.fetchall()
        connection.close()
        
        return results    
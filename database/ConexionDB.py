import sqlite3

class ConexionDB():
    def __init__(self, ruta_db):        
        self.ruta_db = ruta_db        
        
    def connect_db(self):
        return sqlite3.connect(self.ruta_db)
    
    def add_nombre(player_name):
        connection = ConexionJugadoresBD.connect_db()
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO jugadores (NamePlayer)
        VALUES (?)
        """, (player_name,))
        connection.commit()
        connection.close()
        
    def add_game_record(nombre, dificultad, duracion_total, puntaje, fecha_partida):
        conn = ConexionPuntajeBD.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO puntaje (nombre, dificultad, duracion_total, puntaje, fecha_partida)
        VALUES (?, ?, ?, ?, ?)
        ''', (nombre, dificultad, duracion_total, puntaje, fecha_partida))
        conn.commit()
        conn.close()

    #@staticmethod
    def get_high_score(nombre):
        connection = ConexionPuntajeBD.connect_db()
        cursor = connection.cursor()
        cursor.execute('''
        SELECT nombre, MAX(puntaje)
        FROM puntaje
        WHERE nombre = ?
        GROUP BY nombre
        ''', (nombre,))
        result = cursor.fetchone()
        connection.close()
        return result
        
    

class ConexionJugadoresBD(ConexionDB):
    def __init__(self):
        super().__init__()

    #@staticmethod
    

    #@staticmethod
    

class ConexionPuntajeBD:
    def __init__(self):
        super().__init__()

    #@staticmethod
    def connect_db():
        return sqlite3.connect("puntaje.db")

    #@staticmethod
    



# Agregar un nuevo jugador
ConexionJugadoresBD.add_nombre("Jugador1")

# Agregar un nuevo registro de juego
ConexionPuntajeBD.add_game_record("Jugador1", "Difícil", 120, 5000, "2024-05-24")

# Obtener la mayor puntuación del jugador
result = ConexionPuntajeBD.get_high_score("Jugador1")
if result:
    nombre, max_puntaje = result
    print(f"Jugador: {nombre}, Mayor Puntuación: {max_puntaje}")
else:
    print(f"No se encontraron registros para el jugador Jugador1.")
    
                   

    #Tambien tendria que meter como consulta cual es el jugador con mayor puntuacion 
    #Para que gema lo pueda meter en su tabla de high score, ya esta 
    #Lo que esta faltando ahora es si tenemos que hacer un puntaje para cada jugador que son dos 
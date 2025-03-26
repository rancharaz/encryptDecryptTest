import sqlite3
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DB_PATH = os.getenv("DATABASE_PATH", "Database/data.db")  # Utilisation de .env

def get_db_connection():
    """Ouvre une connexion à la base de données SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par nom
        return conn
    except sqlite3.Error as e:
        raise Exception(f"Erreur de connexion à la base de données: {e}") from e

def init_db():
    """Crée la table dans la base de données si elle n'existe pas."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS encrypted_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("✅ Base de données initialisée avec succès.")
    except sqlite3.Error as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")

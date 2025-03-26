# controller.py
from cryptography.fernet import Fernet
import json
import os
from Db_connection.db_connect import get_db_connection  # Import the DB connection function

# Générer et sauvegarder la clé si elle n'existe pas
def get_key():
    try:
        if os.path.exists("key.json"):
            with open("key.json", "r") as file:
                return json.load(file)["key"].encode()
        else:
            key = Fernet.generate_key()
            with open("key.json", "w") as file:
                json.dump({"key": key.decode()}, file)
            return key
    except Exception as e:
        print(f"Erreur lors de la gestion de la clé: {e}")
        return None

# Chiffrer et stocker la donnée
def encrypt_data(data):
    key = get_key()
    if key is None:
        return None, "Erreur de clé"
    
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())

    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO encrypted_data (data) VALUES (?)", (encrypted_data.decode(),))
            conn.commit()
            data_id = cursor.lastrowid
            conn.close()
            return data_id, None  # Return ID and no error
        else:
            return None, "Erreur de connexion à la base de données"
    except Exception as e:
        return None, f"Erreur de base de données: {e}"

# Déchiffrer une donnée spécifique
def decrypt_data(data_id):
    key = get_key()
    if key is None:
        return None, "Erreur de clé"

    cipher = Fernet(key)

    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM encrypted_data WHERE id = ?", (data_id,))
            row = cursor.fetchone()
            conn.close()

            if row:
                decrypted_data = cipher.decrypt(row["data"].encode()).decode()
                return decrypted_data, None  # Return decrypted data and no error
            else:
                return None, "Donnée non trouvée"
        else:
            return None, "Erreur de connexion à la base de données"
    except Exception as e:
        return None, f"Erreur de base de données: {e}"

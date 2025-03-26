from flask import Flask, request, jsonify
import sqlite3
from cryptography.fernet import Fernet
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialiser la base de données
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS encrypted_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Générer et sauvegarder la clé si elle n'existe pas
def get_key():
    try:
        with open("key.json", "r") as file:
            return json.load(file)["key"].encode()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("key.json", "w") as file:
            json.dump({"key": key.decode()}, file)
        return key

# Route pour chiffrer et stocker la donnée
@app.route("/encrypt", methods=["POST"])
def encrypt_data():
    data = request.json.get("data")
    if not data:
        return jsonify({"error": "Aucune donnée fournie"}), 400

    key = get_key()
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO encrypted_data (data) VALUES (?)", (encrypted_data.decode(),))
    conn.commit()
    data_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": f"Donnée chiffrée avec succès, ID: {data_id}"}), 201

# Route pour déchiffrer une donnée spécifique
@app.route("/decrypt/<int:data_id>", methods=["GET"])
def decrypt_data(data_id):
    key = get_key()
    cipher = Fernet(key)

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM encrypted_data WHERE id = ?", (data_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        decrypted_data = cipher.decrypt(row[0].encode()).decode()
        return jsonify({"decrypted_data": decrypted_data})
    else:
        return jsonify({"error": "Donnée non trouvée"}), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

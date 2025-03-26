# routes.py
from flask import Blueprint, request, jsonify
from Controller.App_Controller import encrypt_data, decrypt_data  # Import controller functions

# Create a Blueprint instance
routes = Blueprint("routes", __name__)

# Route pour chiffrer et stocker la donnée
@routes.route("/encrypt", methods=["POST"])
def encrypt_data_route():
    data = request.json.get("data")
    if not data:
        return jsonify({"error": "Aucune donnée fournie"}), 400

    data_id, error = encrypt_data(data)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"message": f"Donnée chiffrée avec succès, ID: {data_id}"}), 201

# Route pour déchiffrer une donnée spécifique
@routes.route("/decrypt/<int:data_id>", methods=["GET"])
def decrypt_data_route(data_id):
    decrypted_data, error = decrypt_data(data_id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"decrypted_data": decrypted_data})

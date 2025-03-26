from flask import Flask
from flask_cors import CORS
from Routes.App_Routes import routes  # Vérifiez bien le nom du fichier

from Db_connection.db_connect import init_db  # Vérifiez ce chemin aussi

app = Flask(__name__)
CORS(app)

# Enregistrer le Blueprint des routes
app.register_blueprint(routes)

if __name__ == "__main__":
    print("🔧 Initialisation de la base de données...")
    init_db()
    print("Serveur Flask démarré sur http://localhost:5000")
    app.run(debug=True)

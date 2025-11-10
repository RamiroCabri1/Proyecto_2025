from api import app
from flask import jsonify

# mensaje de ok inicial
@app.route('/')
def index():
    return jsonify({"message": "API corriendo"}), 200

if __name__ == "__main__":
	app.run(debug=True, port=5000)
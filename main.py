import pymysql
pymysql.install_as_MySQLdb()

from api import app
from flask import jsonify


@app.route('/')
def index():
    return jsonify({"message": "API corriendo"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
import logging
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import psycopg2
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="medy_supply",
        user="medy_supply_app",
        password="postgres",
        port="5433"
    )
    return conn

#Servicio de health check
@app.route("/health")
def health_check():

    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

#Servicio para almacenar un pedido en la base de datos
@app.route('/insertar_pedido', methods=['POST'])
def save_order():
    data = request.get_json()
    nombre = data['nombre']
    cantidad = data['cantidad']
    precio = data['precio']
    fecha_pedido = datetime.now().isoformat()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pedidos (nombre, cantidad, precio, fecha_pedido) VALUES (%s, %s, %s, %s)",
        (nombre, cantidad, precio, fecha_pedido)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Pedido insertado"}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, threaded=False)

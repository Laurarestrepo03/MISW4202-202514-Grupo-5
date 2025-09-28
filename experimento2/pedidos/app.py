import logging
import os
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
        host=os.environ.get('POSTGRES_HOST'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        port=os.environ.get('POSTGRES_PORT')
    )
    return conn


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

#Servicio de health check
@app.route("/audit_result")
def audit_result():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM pedidos;')
    total_pedidos = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM audit_log;')
    total_audit = cur.fetchone()[0]
    cur.close()
    conn.close()
    return jsonify({'total_pedidos': total_pedidos,'total_audit':total_audit})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, threaded=False)

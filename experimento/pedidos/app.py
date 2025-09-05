import logging
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import random, time
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
metrics = PrometheusMetrics(app)

dummy_orders = [
    {"order_id": 1, "customer": "John Doe", "items": [{"product": "Laptop", "quantity": 1}], "total": 999.99, "status": "pending"},
    {"order_id": 2, "customer": "Jane Smith", "items": [{"product": "Smartphone", "quantity": 1}], "total": 699.99, "status": "completed"},
    {"order_id": 3, "customer": "Bob Johnson", "items": [{"product": "Headphones", "quantity": 1}], "total": 149.99, "status": "shipped"}
]

@app.route("/health")
def health_check():

    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route("/orders")
def orders():

    if random.random() >= 0.3:
    
        delay = random.uniform(30, 45)
        logger.warning(f"Simulating Failure: Delay for {delay:.2f} seconds")
        time.sleep(delay)
        return jsonify({"error": "Internal Server Error"}), 500

    return jsonify({"orders": dummy_orders, "total_count": len(dummy_orders), "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, threaded=False)

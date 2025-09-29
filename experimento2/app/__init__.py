import os, logging
import threading
import time

from flask import Flask

from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_restful import Api
from prometheus_client import Gauge
from prometheus_flask_exporter import PrometheusMetrics
from sqlalchemy.sql.expression import text

from .db import db
from .schemas import ma
from .models import Usuario, Cliente, Producto, Pedido, PedidoItem


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


audit_logs_count = Gauge('audit_metrics', 'Numero de Registros en la tabla de auditoria')

def create_app(test_config=None):

    logger.info("Start application instance")
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    metrics = PrometheusMetrics(app)


    logger.info("Initialize database")

    db.init_app(app)
    ma.init_app(app)

    logger.info("Migrate database")
    migrate = Migrate(app, db)

    api = Api(app)

    with app.app_context():

        from .endpoints import PedidosEndpoint
        api.add_resource(PedidosEndpoint, '/pedidos')

        db.drop_all()
        db.create_all()

        try:

            logger.info("Initializing Triggers and Audit Table..")
            # db.session.execute(text("DROP TABLE audit_log CASCADE"))
            db.session.execute(
                text("CREATE TABLE IF NOT EXISTS audit_log (id SERIAL PRIMARY KEY, pedido_id INT, accion VARCHAR(10), usuario VARCHAR(60), message TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP); "))
            db.session.execute(text("""CREATE OR REPLACE FUNCTION audit_log_pedidos_fn()
                RETURNS TRIGGER AS
            $$
            BEGIN
                IF (tg_op = 'INSERT') THEN
                    INSERT INTO audit_log(pedido_id, accion, usuario, message) 
                    VALUES (NEW.id, TG_OP, CURRENT_USER,
                            'Se ha creado un nuevo pedido con id ' 
                                || NEW.id || ' en la tabla ' || TG_TABLE_NAME || ' por el usuario ' || CURRENT_USER || 
                            ' con valor total: ' || NEW.total_pedido || ' y comision: ' || NEW.comision || ' y vendedor: ' || NEW.usuario_creacion);
                    RETURN NEW;
                        
                ELSIF (tg_op = 'UPDATE') THEN
                    
                    INSERT INTO audit_log(pedido_id, accion, usuario, message) 
                    VALUES (NEW.id, TG_OP, CURRENT_USER,
                            'Se ha actualizado un nuevo pedido con id '|| NEW.id || ' en la tabla ' || TG_TABLE_NAME || ' por el usuario ' || CURRENT_USER || 
                            'Valor Total Pedido anterior: ' || OLD.total_pedido || ' comision anterior: ' || OLD.comision || ' y Valor Total Pedido nuevo: ' || NEW.total_pedido || ' y comision nueva: ' || NEW.comision ||' y vendedor anterior: ' || OLD.usuario_creacion || ' y vendedor nuevo: ' || NEW.usuario_creacion);
                    RETURN NEW;
                        
                ELSIF (tg_op = 'DELETE') THEN
                    
                    INSERT INTO audit_log(pedido_id, accion, usuario, message) 
                    VALUES (NEW.id, TG_OP, CURRENT_USER,
                            'Se ha eliminado pedido con id '|| old.id || ' en la tabla ' || TG_TABLE_NAME || ' por el usuario ' || CURRENT_USER || 
                            'Total Pedido anterior: ' || OLD.total_pedido || ' comision anterior: ' || OLD.comision);
                    RETURN OLD;
                END IF;
            END;
            $$ LANGUAGE plpgsql;"""))

            db.session.execute(text("DROP TRIGGER IF EXISTS pedidos_audit_trigger ON pedidos;"))
            db.session.execute(text("""
                    CREATE TRIGGER pedidos_audit_trigger
                        AFTER INSERT OR UPDATE OR DELETE ON pedidos
                        FOR EACH ROW
                        EXECUTE FUNCTION audit_log_pedidos_fn();
                    """))
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")


        db.session.begin_nested()

        usuario = Usuario(username="system")
        usuario2 = Usuario(username="vendedor2")
        usuario3 = Usuario(username="vendedor3")

        db.session.add_all([usuario, usuario2, usuario3])

        cliente1 = Cliente(nombre="Cliente 1")
        cliente2 = Cliente(nombre="Cliente 2")

        db.session.add_all([cliente1, cliente2])

        producto1 = Producto(nombre="Jeringas x 100",precio=100.0)
        producto2 = Producto(nombre="Guantes x 100",precio=80.0)
        producto3 = Producto(nombre="Tapabocas x 50",precio=50.0)

        db.session.add_all([producto1, producto2, producto3])

        pedido = Pedido()
        pedido.cliente = cliente1
        pedido.usuario_creacion = usuario.username

        item1 = PedidoItem(cantidad=10)
        item1.producto = producto1
        item2 = PedidoItem(cantidad=20)
        item2.producto = producto2
        pedido.pedido_items = [item1, item2]

        pedido.total_pedido = sum([item.cantidad * item.producto.precio for item in pedido.pedido_items])
        pedido.comision = sum([item.cantidad * item.producto.precio for item in pedido.pedido_items]) * 0.1

        db.session.add(pedido)
        db.session.commit()

        threading.Thread(target=refresh_audit_logs_count, args=(app,), daemon=True).start()

    return app


def refresh_audit_logs_count(app_instance):

    logger.info(f"Refreshing audit logs count for {app_instance.name}")
    with app_instance.app_context():
        while True:
            result = db.session.execute(text("SELECT COUNT(*) FROM audit_log"))
            count = result.scalar()
            audit_logs_count.set(count)
            time.sleep(5)



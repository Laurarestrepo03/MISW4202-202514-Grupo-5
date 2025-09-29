import logging
import time

from prometheus_client import Gauge
from flask_restful import Resource
from sqlalchemy.sql.expression import text

from .db import db
from .models import Usuario, Pedido, Cliente, Producto, PedidoItem
from .schemas import PedidoSchema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PedidosEndpoint(Resource):

    def get(self):
        data = Pedido.query.all()
        schema = PedidoSchema(many=True)
        return schema.dump(data), 200
    
    def post(self):
        
        usuario = Usuario.query.get(2)
        cliente = Cliente.query.get(1)

        producto_nuevo = Producto.query.get(3)

        nuevo_pedido = Pedido()
        nuevo_pedido.cliente = cliente
        nuevo_pedido.usuario_creacion = usuario.username

        item1 = PedidoItem(cantidad=40)
        item1.producto = producto_nuevo
        nuevo_pedido.pedido_items = [item1]

        nuevo_pedido.total_pedido = sum([item.cantidad * item.producto.precio for item in nuevo_pedido.pedido_items])
        nuevo_pedido.comision = sum([item.cantidad * item.producto.precio for item in nuevo_pedido.pedido_items]) * 0.1

        db.session.add(nuevo_pedido)
        db.session.commit()

        return {'message': 'Pedido creado correctamente', 'pedido_id': nuevo_pedido.id}, 201